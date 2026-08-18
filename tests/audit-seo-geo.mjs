// Auditoria d'SEO clàssic i de GEO, entès en els dos sentits que hi toquen:
// geogràfic (som un club del Clot i això s'ha de notar a les dades) i
// generatiu (que ChatGPT, Perplexity o Claude sàpiguen citar-nos bé).
//
//   node tests/audit-seo-geo.mjs [--out tests/out]
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const args = process.argv.slice(2);
const OUT = path.resolve(ROOT, (args[args.indexOf('--out') + 1] && args.includes('--out')) ? args[args.indexOf('--out') + 1] : 'tests/out');
const SITE = 'https://cbgrupbarna.info';

const SKIP = [/^\.git\//, /^node_modules\//, /^tests\//, /^\.github\//];
const NOINDEX_OK = ['/admin/', '/fotos/admin.html', '/jugadors/admin.html', '/partits/admin.html', '/briefing/'];

// ---------- utilitats de lectura d'HTML ----------
// Prou per a metadades: el marcatge d'aquest lloc és regular i no cal un DOM.
const attr = (tag, name) => {
  const m = tag.match(new RegExp(`${name}\\s*=\\s*("([^"]*)"|'([^']*)')`, 'i'));
  return m ? (m[2] ?? m[3]) : null;
};
const metas = (html, kind) => {
  const found = {};
  for (const tag of html.match(/<meta\b[^>]*>/gi) || []) {
    const key = attr(tag, kind);
    if (key) found[key.toLowerCase()] = attr(tag, 'content');
  }
  return found;
};
const links = (html) => (html.match(/<link\b[^>]*>/gi) || []).map((t) => ({
  rel: (attr(t, 'rel') || '').toLowerCase(), href: attr(t, 'href'), hreflang: attr(t, 'hreflang'), type: attr(t, 'type'),
}));
const textOf = (html) => html
  .replace(/<script[\s\S]*?<\/script>/gi, ' ')
  .replace(/<style[\s\S]*?<\/style>/gi, ' ')
  .replace(/<[^>]+>/g, ' ')
  .replace(/&[a-z]+;|&#\d+;/gi, ' ')
  .replace(/\s+/g, ' ')
  .trim();

function findPages() {
  const pages = [];
  const walk = (dir) => {
    for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
      const abs = path.join(dir, e.name);
      const rel = path.relative(ROOT, abs);
      if (SKIP.some((re) => re.test(rel + (e.isDirectory() ? '/' : '')))) continue;
      if (e.isDirectory()) walk(abs);
      else if (e.name.endsWith('.html')) pages.push(rel);
    }
  };
  walk(ROOT);
  return pages.sort();
}

const urlOf = (rel) => '/' + rel.replace(/index\.html$/, '');

// ---------- enllaços interns ----------
function resolveLocal(href, fromRel) {
  if (!href) return null;
  if (/^[a-z][a-z0-9+.-]*:/i.test(href)) return null;   // qualsevol esquema: http, mailto, webcal, tel…
  if (href.startsWith('//')) return null;               // relatiu al protocol, però extern
  if (/^#/.test(href)) return null;
  // Enllaços que un script munta en temps d'execució: aquí no es poden resoldre.
  if (/\$\{|['"]\s*\+|\+\s*['"]|<%|\{\{/.test(href)) return null;
  const clean = href.split('#')[0].split('?')[0];
  if (!clean) return null;
  const base = href.startsWith('/') ? ROOT : path.dirname(path.join(ROOT, fromRel));
  let target = path.resolve(base, clean.replace(/^\//, ''));
  if (!target.startsWith(ROOT)) return { href, exists: false, reason: 'fora de l\'arrel' };
  if (fs.existsSync(target)) {
    if (fs.statSync(target).isDirectory()) {
      return { href, exists: fs.existsSync(path.join(target, 'index.html')), reason: 'carpeta sense index.html' };
    }
    return { href, exists: true };
  }
  // GitHub Pages també serveix /x com a /x.html
  if (fs.existsSync(target + '.html')) return { href, exists: true };
  return { href, exists: false, reason: 'no existeix' };
}

// ---------- anàlisi per pàgina ----------
function auditPage(rel) {
  const html = fs.readFileSync(path.join(ROOT, rel), 'utf8');
  const url = urlOf(rel);
  const r = { file: rel, url, issues: [], info: {} };
  const add = (level, code, msg, extra) => r.issues.push({ level, code, msg, ...extra });

  const name = metas(html, 'name');
  const prop = metas(html, 'property');
  const ls = links(html);
  const noindex = /noindex/i.test(name.robots || '');
  // Una pàgina que demana no ser indexada no necessita Open Graph, ni
  // descripció, ni dades estructurades: exigir-li-ho és soroll. Val tant per
  // a les eines internes com per a les redireccions amb canonical.
  const isAdmin = noindex || NOINDEX_OK.some((p) => url.startsWith(p) || url === p);
  r.info.noindex = noindex;
  r.info.admin = isAdmin;

  // --- bàsics ---
  if (!/^<!doctype html>/i.test(html.trim())) add('error', 'doctype', 'sense <!DOCTYPE html>');
  const lang = (html.match(/<html[^>]*>/i) || [''])[0];
  const langVal = attr(lang, 'lang');
  r.info.lang = langVal;
  if (!langVal) add('error', 'lang', '<html> sense atribut lang');
  if (!/charset\s*=\s*["']?utf-8/i.test(html)) add('error', 'charset', 'sense <meta charset="UTF-8">');
  if (!name.viewport) add('error', 'viewport', 'sense meta viewport');
  else if (/user-scalable\s*=\s*no|maximum-scale\s*=\s*1(\b|[^.])/i.test(name.viewport)) {
    add('error', 'zoom', 'el viewport bloqueja el zoom', { value: name.viewport });
  }

  // --- mojibake ---
  const bad = html.match(/Ã[-¿]|â€[]|Â[ -¿]/g);
  if (bad) add('error', 'encoding', `${bad.length} seqüències d'accents trencats`, { sample: [...new Set(bad)].slice(0, 5) });

  // --- títol i descripció ---
  const title = (html.match(/<title[^>]*>([\s\S]*?)<\/title>/i) || [])[1]?.trim();
  r.info.title = title;
  if (!title) add('error', 'title', 'sense <title>');
  else {
    if (title.length < 15 && !isAdmin) add('avís', 'title-curt', `títol de ${title.length} caràcters`, { title });
    if (title.length > 65 && !isAdmin) add('avís', 'title-llarg', `títol de ${title.length} caràcters, Google el retallarà`, { title });
  }
  const desc = name.description;
  r.info.description = desc;
  if (!desc) { if (!isAdmin) add('error', 'description', 'sense meta description'); }
  else {
    if (desc.length < 70 && !isAdmin) add('avís', 'desc-curta', `descripció de ${desc.length} caràcters`);
    if (desc.length > 165 && !isAdmin) add('avís', 'desc-llarga', `descripció de ${desc.length} caràcters, es retallarà`);
  }

  // --- canonical ---
  const canon = ls.find((l) => l.rel === 'canonical');
  r.info.canonical = canon?.href;
  if (!canon) { if (!isAdmin && !noindex) add('error', 'canonical', 'sense rel=canonical'); }
  else {
    if (!canon.href?.startsWith('http')) add('error', 'canonical-relatiu', 'canonical relatiu', { href: canon.href });
    else {
      const expect = SITE + (url === '/' ? '/' : url);
      const got = canon.href.replace(/\/$/, '') || canon.href;
      // Una redirecció amb noindex ha d'apuntar al seu destí: és el que la fa
      // correcta, no un error.
      if (!noindex && got.replace(/\/$/, '') !== expect.replace(/\/$/, '')) {
        add('avís', 'canonical-divergent', 'la canonical no apunta a la pròpia URL', { href: canon.href, expect });
      }
    }
  }

  // --- Open Graph i Twitter ---
  if (!isAdmin) {
    for (const k of ['og:title', 'og:description', 'og:image', 'og:url', 'og:type']) {
      if (!prop[k]) add('avís', 'og', `falta ${k}`);
    }
    if (prop['og:image'] && !prop['og:image'].startsWith('http')) {
      add('error', 'og-image-relativa', 'og:image ha de ser absoluta', { href: prop['og:image'] });
    }
    if (!name['twitter:card']) add('avís', 'twitter', 'sense twitter:card');
  }

  // --- encapçalaments al codi font ---
  const h1s = (html.match(/<h1\b[^>]*>([\s\S]*?)<\/h1>/gi) || []).map((h) => textOf(h));
  r.info.h1 = h1s;
  // Una pàgina que no s'indexa pot no tenir <h1>: no és un problema de cerca.
  if (h1s.length === 0 && !isAdmin) add('error', 'h1', 'cap <h1>');
  else if (h1s.length > 1) add('avís', 'h1-multiple', `${h1s.length} <h1>`, { h1s: h1s.slice(0, 4) });

  // --- imatges sense alt ---
  const imgs = html.match(/<img\b[^>]*>/gi) || [];
  const noAlt = imgs.filter((t) => attr(t, 'alt') === null);
  if (noAlt.length) add('error', 'img-alt', `${noAlt.length} imatges sense alt`, { sample: noAlt.slice(0, 3).map((t) => attr(t, 'src')) });
  const emptyAltLink = (html.match(/<a\b[^>]*>\s*<img\b[^>]*alt\s*=\s*""[^>]*>\s*<\/a>/gi) || []).length;
  if (emptyAltLink) add('avís', 'enllaç-img-sense-nom', `${emptyAltLink} enllaços que només contenen una imatge amb alt buit`);

  // --- enllaços interns ---
  const hrefs = [...html.matchAll(/<a\b[^>]*href\s*=\s*("([^"]*)"|'([^']*)')/gi)].map((m) => m[2] ?? m[3]);
  const broken = [];
  for (const h of hrefs) {
    const res = resolveLocal(h, rel);
    if (res && !res.exists) broken.push(res);
  }
  // i els recursos
  const assets = [
    ...[...html.matchAll(/<img\b[^>]*src\s*=\s*("([^"]*)"|'([^']*)')/gi)].map((m) => m[2] ?? m[3]),
    ...[...html.matchAll(/<script\b[^>]*src\s*=\s*("([^"]*)"|'([^']*)')/gi)].map((m) => m[2] ?? m[3]),
    ...ls.filter((l) => l.href).map((l) => l.href),
  ];
  for (const a of assets) {
    const res = resolveLocal(a, rel);
    if (res && !res.exists) broken.push({ ...res, asset: true });
  }
  if (broken.length) {
    const uniq = [...new Map(broken.map((b) => [b.href, b])).values()];
    add('error', 'enllaç-trencat', `${uniq.length} destins interns que no existeixen`, { targets: uniq.slice(0, 8) });
  }
  r.info.outLinks = hrefs.length;

  // --- enllaços externs sense rel ---
  const extAnchors = [...html.matchAll(/<a\b[^>]*>/gi)].map((m) => m[0])
    .filter((t) => /href\s*=\s*["']https?:/i.test(t) && !/cbgrupbarna\.info/i.test(t));
  const unsafe = extAnchors.filter((t) => /target\s*=\s*["']_blank/i.test(t) && !/rel\s*=\s*["'][^"']*noopener/i.test(t));
  if (unsafe.length) add('avís', 'noopener', `${unsafe.length} enllaços target=_blank sense rel="noopener"`);

  // --- dades estructurades ---
  const blocks = [...html.matchAll(/<script[^>]*type\s*=\s*["']application\/ld\+json["'][^>]*>([\s\S]*?)<\/script>/gi)];
  const types = [];
  r.info.jsonld = [];
  for (const [, raw] of blocks) {
    try {
      const parsed = JSON.parse(raw.trim());
      const nodes = Array.isArray(parsed) ? parsed : (parsed['@graph'] || [parsed]);
      // Els tipus també compten quan van niats: un ImageObject dins d'una
      // galeria o un HowTo dins de mainEntity valen igual per a qui ens llegeix.
      const walk = (n) => {
        if (Array.isArray(n)) { n.forEach(walk); return; }
        if (!n || typeof n !== 'object') return;
        const t = Array.isArray(n['@type']) ? n['@type'].join('+') : n['@type'];
        if (t) types.push(t);
        for (const [k, v] of Object.entries(n)) if (k !== '@type' && k !== '@context') walk(v);
      };
      for (const n of nodes) {
        walk(n);
        r.info.jsonld.push(n);
      }
    } catch (e) {
      add('error', 'jsonld-invàlid', 'un bloc JSON-LD no és JSON vàlid', { error: String(e).slice(0, 120) });
    }
  }
  r.info.schemaTypes = types;
  if (!isAdmin && !types.length) add('avís', 'sense-schema', 'cap dada estructurada JSON-LD');

  // --- l'idioma declarat és el que s'hi llegeix? ---
  // Paraules funcionals que separen bé català, castellà i anglès. No cal
  // encertar el 100 %: només detectar una pàgina que diu una cosa i n'és una altra.
  const MARKERS = {
    ca: ['amb', 'això', 'aquest', 'aquesta', 'aquests', 'nosaltres', 'també', 'però', 'molt', 'anys', 'nens', 'què', 'són', 'més', 'dels', 'les', 'seva', 'fins', 'tots', 'nostre'],
    es: ['con', 'esto', 'este', 'esta', 'estos', 'nosotros', 'también', 'pero', 'muy', 'años', 'niños', 'qué', 'son', 'más', 'del', 'las', 'sus', 'hasta', 'todos', 'nuestro'],
    en: ['with', 'this', 'these', 'we', 'also', 'but', 'very', 'years', 'children', 'what', 'are', 'more', 'of', 'the', 'their', 'until', 'all', 'our', 'and', 'for'],
  };
  // Les citacions bibliogràfiques van en l'idioma de l'original i falsejarien
  // el recompte: una pàgina de bibliografia en català plena de títols anglesos
  // no és una pàgina en anglès.
  const bodyText = textOf(
    (html.match(/<body[\s\S]*<\/body>/i) || [html])[0]
      .replace(/<li\b[\s\S]*?<\/li>/gi, ' ')
      .replace(/<cite\b[\s\S]*?<\/cite>/gi, ' ')
      .replace(/<blockquote\b[\s\S]*?<\/blockquote>/gi, ' ')
  ).toLowerCase();
  const score = {};
  for (const [code, words] of Object.entries(MARKERS)) {
    score[code] = words.reduce((n, w) => n + (bodyText.match(new RegExp(`(^|[^\\p{L}])${w}([^\\p{L}]|$)`, 'giu')) || []).length, 0);
  }
  r.info.langScore = score;
  const declared = (langVal || '').slice(0, 2);
  const [winner, top] = Object.entries(score).sort((a, b) => b[1] - a[1])[0];
  // Només ho diem si la diferència és clara i hi ha text de sobres.
  if (declared && MARKERS[declared] && top >= 25 && winner !== declared && top > score[declared] * 1.6) {
    add('error', 'idioma-divergent', `declara \`lang="${langVal}"\` però el text sembla ${winner}`, { score });
  }

  // --- text útil ---
  const body = textOf((html.match(/<body[\s\S]*<\/body>/i) || [html])[0]);
  r.info.words = body.split(/\s+/).filter((w) => w.length > 1).length;
  if (!isAdmin && r.info.words < 120) add('avís', 'text-prim', `només ${r.info.words} paraules de text visible`);

  r.info.hreflang = ls.filter((l) => l.rel === 'alternate' && l.hreflang).map((l) => ({ lang: l.hreflang, href: l.href }));
  return r;
}

// ---------- sitemap ----------
function auditSitemap(pages, pageResults) {
  const out = { issues: [], urls: [] };
  const p = path.join(ROOT, 'sitemap.xml');
  if (!fs.existsSync(p)) { out.issues.push({ level: 'error', code: 'sitemap', msg: 'no hi ha sitemap.xml' }); return out; }
  const xml = fs.readFileSync(p, 'utf8');
  const locs = [...xml.matchAll(/<loc>\s*([^<]+?)\s*<\/loc>/gi)].map((m) => m[1]);
  const lastmods = [...xml.matchAll(/<lastmod>\s*([^<]+?)\s*<\/lastmod>/gi)].map((m) => m[1]);
  out.urls = locs;
  out.count = locs.length;

  const dupes = locs.filter((u, i) => locs.indexOf(u) !== i);
  if (dupes.length) out.issues.push({ level: 'avís', code: 'sitemap-duplicat', msg: `${new Set(dupes).size} URLs repetides`, sample: [...new Set(dupes)].slice(0, 5) });

  const today = new Date();
  const future = lastmods.filter((d) => new Date(d) > today);
  if (future.length) out.issues.push({ level: 'avís', code: 'lastmod-futur', msg: `${future.length} lastmod amb data futura`, sample: future.slice(0, 3) });

  const siteFiles = new Set(pages.map(urlOf));
  const missing = [];
  for (const loc of locs) {
    const u = loc.replace(SITE, '') || '/';
    const clean = u.split('#')[0];
    const asFile = clean.endsWith('/') ? clean + 'index.html' : clean;
    if (!fs.existsSync(path.join(ROOT, asFile.replace(/^\//, ''))) &&
        !fs.existsSync(path.join(ROOT, asFile.replace(/^\//, '') + '.html'))) {
      missing.push(loc);
    }
  }
  if (missing.length) out.issues.push({ level: 'error', code: 'sitemap-404', msg: `${missing.length} URLs del sitemap no existeixen al repositori`, sample: missing.slice(0, 8) });

  const inSitemap = new Set(locs.map((l) => (l.replace(SITE, '') || '/')));
  const noindexed = new Set(pageResults.filter((p) => p.info.admin).map((p) => p.url));
  const absent = [...siteFiles].filter((u) => !inSitemap.has(u) && !noindexed.has(u));
  if (absent.length) out.issues.push({ level: 'avís', code: 'fora-del-sitemap', msg: `${absent.length} pàgines publicades que no són al sitemap`, sample: absent.slice(0, 12) });

  if (!/xmlns\s*=\s*["']http:\/\/www\.sitemaps\.org/i.test(xml)) {
    out.issues.push({ level: 'error', code: 'sitemap-ns', msg: 'falta l\'espai de noms de sitemaps.org' });
  }
  return out;
}

// ---------- robots i llms.txt ----------
function auditRobots() {
  const out = { issues: [] };
  const p = path.join(ROOT, 'robots.txt');
  if (!fs.existsSync(p)) { out.issues.push({ level: 'error', code: 'robots', msg: 'no hi ha robots.txt' }); return out; }
  const txt = fs.readFileSync(p, 'utf8');
  out.text = txt;
  if (!/^sitemap:/im.test(txt)) out.issues.push({ level: 'error', code: 'robots-sitemap', msg: 'robots.txt no declara el sitemap' });

  // Rastrejadors d'IA: els que citen respostes i els que entrenen.
  const wanted = ['GPTBot', 'OAI-SearchBot', 'ChatGPT-User', 'PerplexityBot', 'ClaudeBot', 'Claude-SearchBot', 'Google-Extended', 'Applebot-Extended', 'Bingbot', 'CCBot', 'Amazonbot', 'meta-externalagent', 'Bytespider', 'cohere-ai', 'DuckAssistBot', 'MistralAI-User', 'Diffbot', 'Timpibot', 'Omgilibot', 'YouBot'];
  out.aiBots = {};
  for (const b of wanted) out.aiBots[b] = new RegExp(`^user-agent:\\s*${b}\\s*$`, 'im').test(txt);
  const absent = wanted.filter((b) => !out.aiBots[b]);
  if (absent.length) {
    out.issues.push({ level: 'info', code: 'ia-no-declarats', msg: `${absent.length} rastrejadors d'IA no declarats (queden coberts pel comodí)`, bots: absent });
  }
  return out;
}

function auditLlms() {
  const out = { issues: [] };
  const p = path.join(ROOT, 'llms.txt');
  if (!fs.existsSync(p)) { out.issues.push({ level: 'avís', code: 'llms', msg: 'no hi ha llms.txt' }); return out; }
  const txt = fs.readFileSync(p, 'utf8');
  out.bytes = Buffer.byteLength(txt);
  out.lines = txt.split('\n').length;
  if (!/^#\s+/m.test(txt)) out.issues.push({ level: 'avís', code: 'llms-titol', msg: 'llms.txt sense títol de primer nivell' });

  const urls = [...txt.matchAll(/https:\/\/cbgrupbarna\.info(\/[^\s)\]]*)?/g)].map((m) => m[1] || '/');
  const broken = [];
  for (const u of [...new Set(urls)]) {
    const clean = u.split('#')[0].split('?')[0];
    const asFile = clean.endsWith('/') ? clean + 'index.html' : clean;
    const abs = path.join(ROOT, asFile.replace(/^\//, ''));
    if (!fs.existsSync(abs) && !fs.existsSync(abs + '.html') && !fs.existsSync(path.join(abs, 'index.html'))) broken.push(u);
  }
  if (broken.length) out.issues.push({ level: 'error', code: 'llms-404', msg: `${broken.length} URLs del llms.txt no existeixen`, sample: broken.slice(0, 8) });
  out.urls = [...new Set(urls)].length;

  // Un llms.txt serveix per ser citat: cal que hi hagi les dades dures.
  const must = { 'adreça': /clot|sant mart|carrer|c\/|avinguda/i, 'any de fundació': /1965/, 'contacte': /@|whatsapp|tel|\+34/i, 'equips': /equip|categor/i };
  out.covers = {};
  for (const [k, re] of Object.entries(must)) {
    out.covers[k] = re.test(txt);
    if (!out.covers[k]) out.issues.push({ level: 'avís', code: 'llms-incomplet', msg: `el llms.txt no menciona ${k}` });
  }
  return out;
}

// ---------- GEO: senyals de lloc i coherència del NAP ----------
function auditGeo(pageResults) {
  const out = { issues: [], nap: {}, geoMeta: {} };
  const home = pageResults.find((p) => p.url === '/');
  const homeHtml = fs.readFileSync(path.join(ROOT, 'index.html'), 'utf8');
  const nm = metas(homeHtml, 'name');

  out.geoMeta = {
    'geo.region': nm['geo.region'] || null,
    'geo.placename': nm['geo.placename'] || null,
    'geo.position': nm['geo.position'] || null,
    ICBM: nm.icbm || null,
  };
  for (const [k, v] of Object.entries(out.geoMeta)) {
    if (!v) out.issues.push({ level: 'avís', code: 'geo-meta', msg: `la portada no declara ${k}` });
  }
  // Coordenades dins de Barcelona
  const pos = (out.geoMeta['geo.position'] || '').split(/[;,]/).map(Number);
  if (pos.length === 2 && !Number.isNaN(pos[0])) {
    const [lat, lon] = pos;
    if (lat < 41.3 || lat > 41.5 || lon < 2.0 || lon > 2.3) {
      out.issues.push({ level: 'error', code: 'geo-fora', msg: 'les coordenades no cauen a Barcelona', value: `${lat}, ${lon}` });
    }
    out.coords = { lat, lon };
  }

  // Entitat local a les dades estructurades: adreça, telèfon, horaris, mapa.
  const localTypes = ['SportsClub', 'SportsActivityLocation', 'LocalBusiness', 'Organization', 'SportsOrganization'];
  const entities = [];
  for (const p of pageResults) {
    for (const n of p.info.jsonld || []) {
      const t = Array.isArray(n['@type']) ? n['@type'] : [n['@type']];
      if (t.some((x) => localTypes.includes(x))) entities.push({ url: p.url, node: n });
    }
  }
  out.localEntities = entities.length;
  if (!entities.length) {
    out.issues.push({ level: 'error', code: 'sense-entitat-local', msg: 'cap pàgina declara SportsClub ni LocalBusiness amb schema.org' });
  }

  const firstHome = entities.find((e) => e.url === '/')?.node;
  const need = {
    address: 'adreça postal (PostalAddress)',
    geo: 'coordenades (GeoCoordinates)',
    telephone: 'telèfon',
    openingHoursSpecification: 'horaris d\'atenció',
    sameAs: 'perfils oficials (sameAs)',
    areaServed: 'àmbit territorial (areaServed)',
    foundingDate: 'any de fundació',
    logo: 'logotip',
  };
  out.entityFields = {};
  if (firstHome) {
    for (const [k, label] of Object.entries(need)) {
      const has = firstHome[k] !== undefined;
      out.entityFields[k] = has;
      if (!has) out.issues.push({ level: 'avís', code: 'entitat-incompleta', msg: `l'entitat de la portada no té ${label}` });
    }
    const a = firstHome.address || {};
    out.nap = {
      name: firstHome.name, street: a.streetAddress, locality: a.addressLocality,
      postal: a.postalCode, region: a.addressRegion, country: a.addressCountry,
      phone: firstHome.telephone, email: firstHome.email,
    };
    for (const [k, v] of Object.entries({ street: a.streetAddress, locality: a.addressLocality, postal: a.postalCode })) {
      if (!v) out.issues.push({ level: 'error', code: 'nap', msg: `l'adreça estructurada no té ${k}` });
    }
  }

  // El NAP ha de dir el mateix a totes les pàgines on aparegui. Només mirem
  // l'entitat del club: un ContactPoint d'una secció pot tenir el seu telèfon
  // i això no és cap incoherència.
  const phones = new Set(), postals = new Set(), streets = new Set();
  for (const p of pageResults) {
    for (const n of p.info.jsonld || []) {
      const t = Array.isArray(n['@type']) ? n['@type'] : [n['@type']];
      if (!t.some((x) => localTypes.includes(x))) continue;
      if (n.telephone) phones.add(String(n.telephone).replace(/[\s.-]/g, ''));
      if (n.address?.postalCode) postals.add(String(n.address.postalCode));
      if (n.address?.streetAddress) streets.add(String(n.address.streetAddress).trim());
    }
  }
  out.napVariants = { phones: [...phones], postals: [...postals], streets: [...streets] };
  for (const [k, set] of Object.entries({ 'telèfon': phones, 'codi postal': postals, 'carrer': streets })) {
    if (set.size > 1) out.issues.push({ level: 'error', code: 'nap-incoherent', msg: `el ${k} no és el mateix a tot el lloc`, values: [...set] });
  }

  // Senyals de lloc al text: barri, districte, ciutat.
  const terms = ['Clot', 'Sant Martí', 'Barcelona'];
  let withPlace = 0;
  for (const p of pageResults) {
    if (p.info.admin) continue;
    const html = fs.readFileSync(path.join(ROOT, p.file), 'utf8');
    const t = textOf(html);
    if (terms.some((x) => t.includes(x))) withPlace++;
  }
  const total = pageResults.filter((p) => !p.info.admin).length;
  out.placeCoverage = { withPlace, total, pct: Math.round((withPlace / total) * 100) };
  if (withPlace / total < 0.6) {
    out.issues.push({ level: 'avís', code: 'lloc-poc-present', msg: `només el ${out.placeCoverage.pct}% de les pàgines menciona el barri, el districte o la ciutat` });
  }

  return out;
}

// ---------- GEO generatiu: som citables? ----------
function auditGenerative(pageResults) {
  const out = { issues: [], signals: {} };
  const all = pageResults.filter((p) => !p.info.admin);

  const schemaTally = {};
  for (const p of all) for (const t of p.info.schemaTypes || []) schemaTally[t] = (schemaTally[t] || 0) + 1;
  out.schemaTally = schemaTally;

  // Els motors generatius citen el que poden extreure com a fet.
  const wanted = {
    FAQPage: 'preguntes freqüents (resposta directa citable)',
    BreadcrumbList: 'molles de pa (situa la pàgina dins del lloc)',
    SportsEvent: 'partits com a esdeveniments',
    Article: 'articles del blog',
    ImageObject: 'imatges descrites',
    Person: 'persones del club',
  };
  for (const [t, why] of Object.entries(wanted)) {
    if (!schemaTally[t]) out.issues.push({ level: 'avís', code: 'schema-absent', msg: `enlloc no hi ha ${t}: ${why}` });
  }

  // Preguntes com a encapçalament: el format que les IA reprodueixen.
  let qHeadings = 0, pagesWithQ = 0;
  for (const p of all) {
    const html = fs.readFileSync(path.join(ROOT, p.file), 'utf8');
    const hs = (html.match(/<h[23]\b[^>]*>([\s\S]*?)<\/h[23]>/gi) || []).map(textOf);
    const q = hs.filter((h) => /\?$/.test(h.trim()) || /^(qu[èé]|com|quan|on|per qu[èé]|quant|quin)/i.test(h.trim()));
    qHeadings += q.length;
    if (q.length) pagesWithQ++;
  }
  out.signals.questionHeadings = qHeadings;
  out.signals.pagesWithQuestions = pagesWithQ;
  if (pagesWithQ < 5) out.issues.push({ level: 'avís', code: 'poques-preguntes', msg: `només ${pagesWithQ} pàgines tenen encapçalaments en forma de pregunta` });

  // Dates: una resposta generativa prefereix el que sap datat.
  let dated = 0;
  for (const p of all) {
    const nodes = p.info.jsonld || [];
    if (nodes.some((n) => n.datePublished || n.dateModified || n.startDate)) dated++;
  }
  out.signals.datedPages = dated;

  // Autoria i entitat: "qui ho diu" pesa.
  const withAuthor = all.filter((p) => (p.info.jsonld || []).some((n) => n.author || n.publisher)).length;
  out.signals.pagesWithAuthor = withAuthor;
  if (withAuthor < 3) out.issues.push({ level: 'avís', code: 'sense-autoria', msg: 'poques pàgines declaren autor o editor a les dades estructurades' });

  // Google no dona resultat enriquit a un article sense imatge, i una peça
  // sense data de modificació sembla morta encara que no ho estigui.
  const ARTICLE = new Set(['Article', 'Report', 'ScholarlyArticle', 'BlogPosting', 'NewsArticle', 'TechArticle']);
  const noImage = [], noModified = [];
  for (const p of all) {
    for (const n of p.info.jsonld || []) {
      const walk = (x) => {
        if (Array.isArray(x)) return x.forEach(walk);
        if (!x || typeof x !== 'object') return;
        const t = Array.isArray(x['@type']) ? x['@type'] : [x['@type']];
        if (t.some((y) => ARTICLE.has(y))) {
          if (!x.image) noImage.push(p.url);
          if (!x.dateModified) noModified.push(p.url);
        }
        for (const [k, v] of Object.entries(x)) {
          if (k === '@type') continue;
          if (k === 'citation' || k === 'isBasedOn') continue;  // obra de tercers
          walk(v);
        }
      };
      walk(n);
    }
  }
  out.signals.articlesWithoutImage = noImage.length;
  out.signals.articlesWithoutDateModified = noModified.length;
  if (noImage.length) out.issues.push({ level: 'avís', code: 'article-sense-imatge', msg: `${noImage.length} articles sense \`image\`: Google no els donarà resultat enriquit`, sample: [...new Set(noImage)].slice(0, 6) });
  if (noModified.length) out.issues.push({ level: 'avís', code: 'article-sense-data', msg: `${noModified.length} articles sense \`dateModified\``, sample: [...new Set(noModified)].slice(0, 6) });

  // Consolidació d'entitat: quantes pàgines pengen del mateix @id del club.
  const clubId = 'https://cbgrupbarna.info/#club';
  const linked = all.filter((p) => JSON.stringify(p.info.jsonld || []).includes(clubId)).length;
  out.signals.pagesLinkedToClubEntity = `${linked} de ${all.length}`;
  if (linked / all.length < 0.6) {
    out.issues.push({ level: 'avís', code: 'entitat-dispersa', msg: `només ${linked} de ${all.length} pàgines es refereixen al mateix @id del club` });
  }

  // Caixa de cerca de Google: només surt si el lloc la declara.
  const hasSearch = all.some((p) => JSON.stringify(p.info.jsonld || []).includes('SearchAction'));
  out.signals.searchAction = hasSearch;
  if (!hasSearch) out.issues.push({ level: 'avís', code: 'sense-searchaction', msg: 'cap pàgina declara SearchAction al node WebSite' });

  // Un nom clar i constant: el que la IA usarà per referir-s'hi.
  const orgTypes = ['SportsClub', 'SportsOrganization', 'LocalBusiness', 'Organization'];
  const names = new Set();
  for (const p of all) {
    for (const n of p.info.jsonld || []) {
      const t = Array.isArray(n['@type']) ? n['@type'] : [n['@type']];
      if (n.name && t.some((x) => orgTypes.includes(x))) names.add(n.name);
    }
  }
  out.signals.clubNames = [...names];
  if (names.size > 3) out.issues.push({ level: 'avís', code: 'nom-inconstant', msg: 'el club s\'anomena de massa maneres a les dades estructurades', values: [...names].slice(0, 8) });

  return out;
}

// ---------- hreflang ----------
function auditHreflang(pageResults) {
  const out = { issues: [] };
  const byUrl = new Map(pageResults.map((p) => [p.url, p]));
  for (const p of pageResults) {
    const hl = p.info.hreflang || [];
    if (!hl.length) continue;
    const selfDeclared = hl.some((h) => h.href?.replace(SITE, '').replace(/\/$/, '') === p.url.replace(/\/$/, ''));
    if (!selfDeclared) out.issues.push({ level: 'avís', code: 'hreflang-sense-si-mateixa', msg: `${p.url} declara alternatives però no s'hi inclou`, page: p.url });
    if (!hl.some((h) => h.lang === 'x-default')) out.issues.push({ level: 'info', code: 'hreflang-xdefault', msg: `${p.url} sense x-default`, page: p.url });

    // Cada alternativa ha d'existir i ha de tornar l'enllaç.
    for (const h of hl) {
      const target = (h.href || '').replace(SITE, '') || '/';
      if (h.href?.startsWith(SITE)) {
        const other = byUrl.get(target);
        if (!other) {
          out.issues.push({ level: 'error', code: 'hreflang-404', msg: `${p.url} apunta a ${target}, que no existeix`, page: p.url });
        } else if (target !== p.url) {
          const back = (other.info.hreflang || []).some((x) => (x.href || '').replace(SITE, '') === p.url);
          if (!back) out.issues.push({ level: 'error', code: 'hreflang-no-recíproc', msg: `${p.url} → ${target} no torna l'enllaç`, page: p.url });
        }
        // L'idioma declarat ha de coincidir amb el de la pàgina de destí.
        if (other && other.info.lang && h.lang !== 'x-default' && !other.info.lang.startsWith(h.lang)) {
          out.issues.push({ level: 'error', code: 'hreflang-idioma', msg: `${p.url} diu que ${target} és «${h.lang}», però la pàgina és «${other.info.lang}»`, page: p.url });
        }
      }
    }
  }
  return out;
}

// ---------- títols i descripcions repetits ----------
function auditDupes(pageResults) {
  const out = { issues: [] };
  const group = (key) => {
    const m = new Map();
    for (const p of pageResults) {
      if (p.info.admin) continue;
      const v = p.info[key];
      if (!v) continue;
      if (!m.has(v)) m.set(v, []);
      m.get(v).push(p.url);
    }
    return [...m.entries()].filter(([, urls]) => urls.length > 1);
  };
  for (const [key, label] of [['title', 'títol'], ['description', 'descripció']]) {
    for (const [value, urls] of group(key)) {
      out.issues.push({ level: 'avís', code: `${key}-duplicat`, msg: `${urls.length} pàgines comparteixen ${label}`, value: value.slice(0, 80), urls: urls.slice(0, 6) });
    }
  }
  return out;
}

// ---------- execució ----------
const pages = findPages();
const pageResults = pages.map(auditPage);
const report = {
  generated: new Date().toISOString(),
  pages: pageResults.length,
  perPage: pageResults,
  sitemap: auditSitemap(pages, pageResults),
  robots: auditRobots(),
  llms: auditLlms(),
  geo: auditGeo(pageResults),
  generative: auditGenerative(pageResults),
  hreflang: auditHreflang(pageResults),
  duplicates: auditDupes(pageResults),
};

fs.mkdirSync(OUT, { recursive: true });
fs.writeFileSync(path.join(OUT, 'seo-geo.json'), JSON.stringify(report, null, 1));

const counts = { error: 0, 'avís': 0, info: 0 };
for (const p of pageResults) for (const i of p.issues) counts[i.level]++;
for (const sec of ['sitemap', 'robots', 'llms', 'geo', 'generative', 'hreflang', 'duplicates']) {
  for (const i of report[sec].issues) counts[i.level] = (counts[i.level] || 0) + 1;
}
console.log(`${pageResults.length} pàgines analitzades`);
console.log(`errors: ${counts.error} · avisos: ${counts['avís']} · informatius: ${counts.info}`);
console.log(`Desat a ${path.relative(ROOT, path.join(OUT, 'seo-geo.json'))}`);
