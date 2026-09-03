// Auditoria de preparació per publicar.
//
//   node tests/audit-llancament.mjs [--out tests/out]
//
// Les altres dues auditories miren si el lloc està ben fet: aquesta mira si
// està LLEST PER SORTIR. Són preguntes diferents. Una pàgina pot tenir un SEO
// impecable i, alhora, apuntar a una foto que no s'ha pujat, demanar dades
// personals sense casella de consentiment o portar un «pendent de confirmar»
// escrit al mig. Res d'això surt a `audit-seo-geo.mjs` ni a `audit-browser.mjs`,
// i tot això es veu el dia que la web és pública.
//
// No obre cap navegador i no surt a la xarxa: llegeix el disc, que és el que
// GitHub Pages publicarà.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const SITE = 'https://cbgrupbarna.info';
const DOMINI = 'cbgrupbarna.info';
const args = process.argv.slice(2);
const argVal = (n, d) => { const i = args.indexOf(`--${n}`); return i >= 0 ? args[i + 1] : d; };
const OUT = path.resolve(ROOT, argVal('out', 'tests/out'));
// A GitHub Actions el repositori es baixa sense les imatges ni els vídeos (són
// 515 MB dels 636 del directori de treball, i cap comprovació d'aquí els obre).
// Amb aquest interruptor no es demana que existeixin: si es demanés, la
// comprovació d'actius diria que falten centenars de fotos que sí que hi són al
// repositori, i el veredicte seria sempre vermell per un motiu fals.
const SENSE_BINARIS = args.includes('--sense-binaris');
const ES_BINARI = /\.(jpe?g|png|webp|gif|avif|mp4|mov|pdf|ico|woff2?|ttf|otf|mp3|m4a)$/i;

// Zones que no són web pública i que per tant no s'han de jutjar amb la
// mateixa vara: el panell d'administració, les pàgines d'impressió, el mirall
// del Premi Dona i Esport (té la seva pròpia web oficial externa) i el residu
// exportat de `patrocinis/`, que ja és una redirecció.
const NO_PUBLIC = [
  /(^|\/)admin(\/|\.html$)/, /\/print\//, /(^|\/)token\.html$/,
  /^premidonaesport\//, /^patrocinis\//, /^galeria\/node_modules\//,
];
const esPublica = (rel) => !NO_PUBLIC.some((r) => r.test(rel));

// ---------- recollida de fitxers ----------
const IGNORA_DIR = new Set(['.git', 'node_modules', '.github', 'tests', 'scripts', 'i18n', 'docs', '.claude']);
function walk(dir, acc = []) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    if (e.isDirectory()) {
      if (IGNORA_DIR.has(e.name)) continue;
      walk(path.join(dir, e.name), acc);
    } else acc.push(path.relative(ROOT, path.join(dir, e.name)));
  }
  return acc;
}
const tots = walk(ROOT);
const pagines = tots.filter((f) => f.endsWith('.html'));
const fullsCss = tots.filter((f) => f.endsWith('.css'));

// ---------- utilitats ----------
const attr = (tag, name) => {
  const m = tag.match(new RegExp(`\\b${name}\\s*=\\s*("([^"]*)"|'([^']*)'|([^\\s>]+))`, 'i'));
  return m ? (m[2] ?? m[3] ?? m[4]) : undefined;
};
const urlOf = (rel) => {
  const u = '/' + rel.replace(/\\/g, '/');
  return u.endsWith('/index.html') ? u.slice(0, -'index.html'.length) : u;
};
// El text que veu una persona, sense codi ni marques.
const textVisible = (html) => html
  .replace(/<script[\s\S]*?<\/script>/gi, ' ')
  .replace(/<style[\s\S]*?<\/style>/gi, ' ')
  .replace(/<!--[\s\S]*?-->/g, ' ')
  .replace(/<[^>]+>/g, ' ')
  .replace(/&nbsp;/g, ' ')
  .replace(/\s+/g, ' ');

// Resol una ruta local tal com ho faria GitHub Pages.
let binarisOmesos = 0;
function existeixLocal(href, desDe) {
  if (!href) return null;
  const h = href.trim();
  if (!h || h.startsWith('#')) return null;
  // El filtre viu aquí i no a cada comprovació: així no se'n pot escapar cap.
  // Va costar una passada de CI en vermell descobrir-ho — l'interruptor tapava
  // el bloc d'actius i deixava fora el JSON-LD i les icones del manifest, que
  // miren l'existència dels mateixos fitxers per un altre camí.
  if (SENSE_BINARIS && ES_BINARI.test(h.split('#')[0].split('?')[0])) { binarisOmesos++; return null; }
  if (/^[a-z][a-z0-9+.-]*:/i.test(h) || h.startsWith('//')) return null;  // extern o amb esquema
  if (/\$\{|<%|\{\{|['"]\s*\+/.test(h)) return null;                      // el munta un script
  const net = h.split('#')[0].split('?')[0];
  if (!net) return null;
  const base = h.startsWith('/') ? ROOT : path.dirname(path.join(ROOT, desDe));
  const dest = path.resolve(base, net.replace(/^\//, ''));
  if (!dest.startsWith(ROOT)) return { href: h, exists: false };
  if (fs.existsSync(dest)) {
    if (fs.statSync(dest).isDirectory()) return { href: h, exists: fs.existsSync(path.join(dest, 'index.html')) };
    return { href: h, exists: true };
  }
  return { href: h, exists: fs.existsSync(dest + '.html') };
}

const troballes = [];
const afegeix = (nivell, bloc, codi, msg, extra = {}) =>
  troballes.push({ nivell, bloc, codi, msg, ...extra });

// =====================================================================
// 1 · Cada fitxer que la pàgina demana existeix de debò
// =====================================================================
// `audit-seo-geo.mjs` ja mira els <a href>, els <img src> i els <script src>.
// El que es perd —i és justament el que sol faltar el dia del llançament— són
// les fotos responsives (`srcset`), els vídeos i les seves miniatures, les
// tipografies i els fons declarats des del CSS.
{
  const falten = new Map();  // ruta que falta -> qui la demana
  const anota = (res, on) => {
    if (res && !res.exists) {
      if (!falten.has(res.href)) falten.set(res.href, []);
      falten.get(res.href).push(on);
    }
  };
  for (const rel of pagines) {
    if (!esPublica(rel)) continue;
    const html = fs.readFileSync(path.join(ROOT, rel), 'utf8');
    // srcset: «ruta 400w, ruta 800w» → cal partir per comes i quedar-se la ruta
    for (const m of html.matchAll(/\bsrcset\s*=\s*("([^"]*)"|'([^']*)')/gi)) {
      for (const cand of (m[2] ?? m[3]).split(',')) anota(existeixLocal(cand.trim().split(/\s+/)[0], rel), rel);
    }
    for (const re of [
      /<source\b[^>]*\bsrc\s*=\s*("([^"]*)"|'([^']*)')/gi,
      /<video\b[^>]*\bsrc\s*=\s*("([^"]*)"|'([^']*)')/gi,
      /<audio\b[^>]*\bsrc\s*=\s*("([^"]*)"|'([^']*)')/gi,
      /<iframe\b[^>]*\bsrc\s*=\s*("([^"]*)"|'([^']*)')/gi,
      /\bposter\s*=\s*("([^"]*)"|'([^']*)')/gi,
      /<link\b[^>]*\bhref\s*=\s*("([^"]*)"|'([^']*)')/gi,
    ]) for (const m of html.matchAll(re)) anota(existeixLocal(m[2] ?? m[3], rel), rel);
    // fons i tipografies declarats a un <style> de la mateixa pàgina
    for (const s of html.matchAll(/<style[^>]*>([\s\S]*?)<\/style>/gi)) {
      for (const u of s[1].matchAll(/url\(\s*['"]?([^'")]+)['"]?\s*\)/gi)) {
        if (!u[1].startsWith('data:')) anota(existeixLocal(u[1], rel), rel);
      }
    }
  }
  // i els que demana el CSS compartit
  for (const css of fullsCss) {
    const txt = fs.readFileSync(path.join(ROOT, css), 'utf8');
    for (const u of txt.matchAll(/url\(\s*['"]?([^'")]+)['"]?\s*\)/gi)) {
      if (!u[1].startsWith('data:')) anota(existeixLocal(u[1], css), css);
    }
  }
  for (const [href, on] of falten) {
    afegeix('error', 'actius', 'actiu-inexistent', `no existeix al repositori: ${href}`,
      { demanat_per: [...new Set(on)].slice(0, 5), pagines: new Set(on).size });
  }
}

// =====================================================================
// 2 · Res del que es veu depèn d'un tercer
// =====================================================================
// La regla del club: tipografies servides des del mateix domini i Leaflet
// vendoritzat. Un CDN caigut, un canvi de política de galetes o una connexió
// dolenta no poden fer que la web es vegi malament. A més, un `http://` dins
// d'una pàgina servida per `https://` el navegador el bloqueja directament.
{
  const externs = new Map();
  for (const rel of [...pagines, ...fullsCss]) {
    if (rel.endsWith('.html') && !esPublica(rel)) continue;
    const txt = fs.readFileSync(path.join(ROOT, rel), 'utf8');
    // Cal distingir dos casos que sovint es confonen. Un recurs que la pàgina
    // necessita per pintar-se (script, full d'estils, imatge, iframe) demanat
    // per http:// el navegador el BLOQUEJA: la pàgina es veu trencada. Un
    // <a href="http://…"> no es bloqueja; només porta a un lloc sense xifrar,
    // que és cosa del tercer i sovint no es pot arreglar des d'aquí.
    for (const m of txt.matchAll(/<(script|link|img|iframe|source|video)\b[^>]*\b(?:src|href)\s*=\s*"(http:\/\/[^"]+)"/gi)) {
      if (!/^http:\/\/(www\.)?(w3\.org|schema\.org|purl\.org|ogp\.me)/i.test(m[2])) {
        afegeix('error', 'externs', 'contingut-mixt', `<${m[1].toLowerCase()}> demanat per http://: el navegador el bloquejarà i la pàgina es veurà trencada`, { pagina: urlOf(rel), url: m[2] });
      }
    }
    for (const m of txt.matchAll(/<a\b[^>]*\bhref\s*=\s*"(http:\/\/[^"]+)"/gi)) {
      const host = (m[1].match(/^http:\/\/([^/]+)/) || [])[1];
      afegeix('avís', 'externs', 'enllac-sense-xifrar', `enllaça a ${host} per http://: el navegador avisarà que el destí no és segur`, { pagina: urlOf(rel), url: m[1] });
    }
    // recursos que la pàgina necessita per pintar-se, no simples enllaços
    for (const m of txt.matchAll(/<(script|link|iframe)\b[^>]*\b(?:src|href)\s*=\s*"(https?:\/\/[^"]+)"/gi)) {
      const tag = m[1].toLowerCase(); const u = m[2];
      if (u.includes(DOMINI)) continue;
      if (tag === 'link' && !/rel\s*=\s*["'](stylesheet|preload|preconnect)/i.test(m[0])) continue;
      const host = (u.match(/^https?:\/\/([^/]+)/) || [])[1];
      const k = `${tag}|${host}`;
      if (!externs.has(k)) externs.set(k, { tag, host, exemple: u, pagines: new Set() });
      externs.get(k).pagines.add(urlOf(rel));
    }
  }
  for (const e of externs.values()) {
    // GA4 va darrere del consentiment i és una decisió presa; la resta, avís.
    const analitica = /googletagmanager|google-analytics/.test(e.host);
    afegeix(analitica ? 'informatiu' : 'avís', 'externs', 'dependencia-externa',
      `<${e.tag}> servit per ${e.host}`, { exemple: e.exemple, pagines: e.pagines.size });
  }
}

// =====================================================================
// 3 · Les dades estructurades es poden llegir
// =====================================================================
// Un JSON-LD amb una coma de més no dona cap error visible: simplement Google
// no en fa cas i el club es queda sense fitxa, sense estrelles i sense
// esdeveniments al buscador. Només es veu si algú el prova de llegir.
{
  for (const rel of pagines) {
    if (!esPublica(rel)) continue;
    const html = fs.readFileSync(path.join(ROOT, rel), 'utf8');
    for (const b of html.matchAll(/<script[^>]*type\s*=\s*["']application\/ld\+json["'][^>]*>([\s\S]*?)<\/script>/gi)) {
      let dades;
      try { dades = JSON.parse(b[1]); }
      catch (e) {
        afegeix('error', 'dades', 'jsonld-invalid', `JSON-LD que no es pot llegir: ${e.message}`, { pagina: urlOf(rel) });
        continue;
      }
      for (const node of (Array.isArray(dades) ? dades : [dades])) {
        if (!node || typeof node !== 'object') continue;
        if (!node['@context']) afegeix('avís', 'dades', 'jsonld-sense-context', 'JSON-LD sense @context', { pagina: urlOf(rel) });
        if (!node['@type'] && !node['@graph']) afegeix('avís', 'dades', 'jsonld-sense-tipus', 'JSON-LD sense @type', { pagina: urlOf(rel) });
        // rutes internes dins del JSON-LD: han d'existir igual que les altres
        const brut = JSON.stringify(node);
        for (const u of brut.matchAll(new RegExp(`"(${SITE}[^"]*)"`, 'g'))) {
          const ruta = u[1].slice(SITE.length) || '/';
          if (/\.(pdf|jpg|jpeg|png|webp|svg|ics)$/i.test(ruta) || ruta.endsWith('/') || /\.html$/.test(ruta)) {
            const res = existeixLocal(ruta, rel);
            if (res && !res.exists) {
              afegeix('error', 'dades', 'jsonld-ruta-morta', `les dades estructurades citen una adreça que no existeix: ${ruta}`, { pagina: urlOf(rel) });
            }
          }
        }
      }
    }
  }
}

// =====================================================================
// 4 · Els formularis recullen dades com toca
// =====================================================================
// Els formularis del lloc demanen dades personals. Cadascun ha de tenir un
// destí on enviar-ho, la política de privacitat a l'abast i, quan la base
// legal és el consentiment, una casella. Si falla res d'això el problema no és
// de disseny: el dia que es publica ja s'estan recollint dades de famílies.
{
  const CAMPS_PERSONALS = /\btype\s*=\s*["'](email|tel)["']|\bname\s*=\s*["'][^"']*(nom|name|correu|email|mail|telefon|telefono|phone|mobil)[^"']*["']/i;
  const RE_PRIVACITAT = /politica-de-privacitat|privacy-policy|politica-de-privacidad/i;
  const cacheJs = new Map();
  const jsDe = (rutaJs) => {
    if (!cacheJs.has(rutaJs)) {
      try { cacheJs.set(rutaJs, fs.readFileSync(rutaJs, 'utf8')); } catch { cacheJs.set(rutaJs, ''); }
    }
    return cacheJs.get(rutaJs);
  };

  for (const rel of pagines) {
    if (!esPublica(rel)) continue;
    const html = fs.readFileSync(path.join(ROOT, rel), 'utf8');
    const on = urlOf(rel);

    // Tot el codi que la pàgina executa: el que porta a dins i el dels fitxers
    // .js propis que carrega. Sense això, un formulari perfectament funcional
    // amb el gestor a /js/bustia.js semblaria que no envia les dades enlloc.
    let codi = [...html.matchAll(/<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)<\/script>/gi)].map((m) => m[1]).join('\n');
    for (const m of html.matchAll(/<script\b[^>]*\bsrc\s*=\s*["']([^"']+)["']/gi)) {
      const res = existeixLocal(m[1], rel);
      if (!res || !res.exists) continue;
      const base = m[1].startsWith('/') ? ROOT : path.dirname(path.join(ROOT, rel));
      codi += '\n' + jsDe(path.resolve(base, m[1].split('?')[0].replace(/^\//, '')));
    }

    for (const f of html.matchAll(/<form\b([^>]*)>([\s\S]*?)<\/form>/gi)) {
      const obertura = '<form' + f[1] + '>';
      const cos = f[2];
      const id = attr(obertura, 'id') || attr(obertura, 'name');
      const nom = id || 'sense id';
      const action = attr(obertura, 'action');

      // --- va a algun lloc? ---
      const gestor = /addEventListener\s*\(\s*['"]submit|\.onsubmit\s*=|\bonsubmit\s*=/i.test(codi + obertura)
        && (!id || codi.includes(id) || /querySelector\(\s*['"]form/i.test(codi));
      if (!action && !gestor) {
        afegeix('error', 'formularis', 'form-sense-desti',
          `el formulari «${nom}» no té ni action ni cap gestor de submit: les dades no van enlloc`, { pagina: on });
      }
      if (action && !/^(https?:|mailto:)/i.test(action)) {
        const res = existeixLocal(action, rel);
        if (res && !res.exists) afegeix('error', 'formularis', 'form-action-morta', `el formulari «${nom}» envia a ${action}, que no existeix`, { pagina: on });
      }
      if (!/<(button|input)[^>]*type\s*=\s*["']submit["']|<button(?![^>]*\btype=)/i.test(cos)) {
        afegeix('avís', 'formularis', 'form-sense-boto', `el formulari «${nom}» no té botó d'enviar`, { pagina: on });
      }

      // --- RGPD ---
      if (CAMPS_PERSONALS.test(cos)) {
        // El requisit dur és que qui deixa les seves dades pugui saber què se'n
        // farà: si la política de privacitat no és enlloc de la pàgina, és un
        // error. Que l'enllaç estigui al peu i no dins del formulari és pitjor
        // que tenir-lo al costat de la casella, però no és el mateix forat.
        if (!RE_PRIVACITAT.test(html)) {
          afegeix('error', 'formularis', 'form-sense-privacitat',
            `el formulari «${nom}» demana dades personals i la pàgina no enllaça enlloc la política de privacitat`, { pagina: on });
        } else if (!RE_PRIVACITAT.test(cos)) {
          afegeix('avís', 'formularis', 'privacitat-lluny',
            `el formulari «${nom}» només enllaça la política de privacitat des del peu, no al costat del camp`, { pagina: on });
        }
        const caselles = cos.match(/<input[^>]*type\s*=\s*["']checkbox["'][^>]*>/gi) || [];
        // Una casella de consentiment es reconeix perquè el text que l'acompanya
        // parla de dades o de privacitat; les altres caselles del formulari
        // (quins dies vens, quines edicions t'interessen) no compten.
        const teConsentiment = RE_PRIVACITAT.test(cos)
          || /accepto|acepto|i accept|consent|autoritzo|autorizo/i.test(textVisible(cos));
        if (!teConsentiment) {
          afegeix('avís', 'formularis', 'form-sense-consentiment',
            `el formulari «${nom}» demana dades personals i no hi ha cap casella ni text de consentiment`, { pagina: on });
        } else if (caselles.length && !caselles.some((c) => /required/i.test(c))) {
          afegeix('avís', 'formularis', 'consentiment-opcional',
            `cap casella de «${nom}» és obligatòria: es pot enviar sense acceptar res`, { pagina: on });
        }
      }

      // --- cada camp ha de tenir nom accessible ---
      // Compta tant <label for="x"> com el camp embolcallat dins d'un <label>,
      // que és el patró que fa servir tot aquest lloc per a les caselles.
      for (const inp of cos.matchAll(/<(input|select|textarea)\b[^>]*>/gi)) {
        const tag = inp[0];
        const tipus = (attr(tag, 'type') || 'text').toLowerCase();
        if (['hidden', 'submit', 'button', 'image', 'reset'].includes(tipus)) continue;
        if (attr(tag, 'aria-label') || attr(tag, 'aria-labelledby') || attr(tag, 'title')) continue;
        const idCamp = attr(tag, 'id');
        if (idCamp && new RegExp(`<label[^>]*\\bfor\\s*=\\s*["']${idCamp}["']`, 'i').test(cos)) continue;
        // embolcallat: l'últim <label> obert abans del camp encara no s'ha tancat
        const abans = cos.slice(0, inp.index);
        const obre = (abans.match(/<label\b/gi) || []).length;
        const tanca = (abans.match(/<\/label>/gi) || []).length;
        if (obre > tanca) continue;
        afegeix('avís', 'formularis', 'camp-sense-nom', `un camp de «${nom}» no té etiqueta`,
          { pagina: on, camp: attr(tag, 'name') || idCamp || tipus });
      }
    }
  }
}

// =====================================================================
// 5 · Publicació: els fitxers que fan que GitHub Pages funcioni
// =====================================================================
{
  const llegeix = (f) => fs.existsSync(path.join(ROOT, f)) ? fs.readFileSync(path.join(ROOT, f), 'utf8') : null;

  const cname = llegeix('CNAME');
  if (!cname) afegeix('error', 'publicacio', 'sense-cname', 'falta CNAME: el domini propi no s\'aplicarà');
  else if (cname.trim() !== DOMINI) afegeix('error', 'publicacio', 'cname-divergent', `CNAME diu «${cname.trim()}» i el lloc es publica a ${DOMINI}`);

  if (!fs.existsSync(path.join(ROOT, '.nojekyll'))) {
    afegeix('error', 'publicacio', 'sense-nojekyll', 'falta .nojekyll: Jekyll s\'empassarà les carpetes que comencen per guió baix');
  }

  const robots = llegeix('robots.txt');
  if (!robots) afegeix('error', 'publicacio', 'sense-robots', 'falta robots.txt');
  else {
    if (/^\s*Disallow:\s*\/\s*$/mi.test(robots)) afegeix('error', 'publicacio', 'robots-bloqueja-tot', 'robots.txt bloqueja tot el lloc');
    if (!/^\s*Sitemap:/mi.test(robots)) afegeix('avís', 'publicacio', 'robots-sense-sitemap', 'robots.txt no declara el sitemap');
    for (const m of robots.matchAll(/^\s*Sitemap:\s*(\S+)/gmi)) {
      const res = existeixLocal(m[1].replace(SITE, ''), 'robots.txt');
      if (res && !res.exists) afegeix('error', 'publicacio', 'sitemap-declarat-inexistent', `robots.txt declara ${m[1]}, que no existeix`);
    }
  }

  const p404 = llegeix('404.html');
  if (!p404) afegeix('error', 'publicacio', 'sense-404', 'falta 404.html: GitHub Pages ensenyarà la seva pàgina genèrica');
  else {
    if (!/noindex/i.test(p404)) afegeix('avís', 'publicacio', '404-indexable', 'la pàgina 404 no porta noindex');
    if (!/href\s*=\s*["']\/["']/i.test(p404)) afegeix('avís', 'publicacio', '404-sense-sortida', 'la pàgina 404 no ofereix tornar a la portada');
  }

  const sm = llegeix('sitemap.xml');
  if (!sm) afegeix('error', 'publicacio', 'sense-sitemap', 'falta sitemap.xml');
  else {
    const locs = [...sm.matchAll(/<loc>([^<]+)<\/loc>/g)].map((m) => m[1]);
    if (locs.length > 50000) afegeix('error', 'publicacio', 'sitemap-massa-gran', `${locs.length} URLs: el límit és 50.000`);
    if (Buffer.byteLength(sm) > 50 * 1024 * 1024) afegeix('error', 'publicacio', 'sitemap-massa-pesat', 'el sitemap passa de 50 MB');
    const fora = locs.filter((u) => !u.startsWith(SITE));
    if (fora.length) afegeix('error', 'publicacio', 'sitemap-fora-de-domini', `${fora.length} URLs del sitemap no són de ${DOMINI}`, { mostra: fora.slice(0, 3) });
  }

  // manifest i icones: el que decideix si la web es pot afegir a la pantalla d'inici
  const manRaw = llegeix('manifest.json');
  if (!manRaw) afegeix('avís', 'publicacio', 'sense-manifest', 'falta manifest.json');
  else {
    let man; try { man = JSON.parse(manRaw); } catch (e) { afegeix('error', 'publicacio', 'manifest-invalid', `manifest.json no es pot llegir: ${e.message}`); }
    if (man) {
      for (const camp of ['name', 'short_name', 'start_url', 'icons', 'display']) {
        if (!man[camp]) afegeix('avís', 'publicacio', 'manifest-incomplet', `manifest.json sense «${camp}»`);
      }
      if (man.start_url) {
        const res = existeixLocal(man.start_url, 'manifest.json');
        if (res && !res.exists) afegeix('error', 'publicacio', 'manifest-start-morta', `start_url del manifest apunta a ${man.start_url}, que no existeix`);
      }
      for (const ic of man.icons || []) {
        const res = existeixLocal(ic.src, 'manifest.json');
        if (res && !res.exists) afegeix('error', 'publicacio', 'manifest-icona-morta', `icona del manifest que no existeix: ${ic.src}`);
      }
      if (!(man.icons || []).some((i) => /maskable/.test(i.purpose || ''))) {
        afegeix('informatiu', 'publicacio', 'manifest-sense-maskable', 'cap icona «maskable»: a Android la icona sortirà dins d\'un quadre blanc');
      }
    }
  }

  // la imatge que es veu quan algú comparteix el lloc
  for (const f of ['og-image.jpg', 'favicon.svg']) {
    if (!fs.existsSync(path.join(ROOT, f))) afegeix('avís', 'publicacio', 'falta-imatge-social', `falta ${f}`);
  }
}

// =====================================================================
// 6 · Res a mig fer que es vegi publicat
// =====================================================================
// Un «lorem ipsum», un «TODO» o un enllaç que no porta enlloc és el defecte
// més barat d'arreglar i el més car de deixar-se: qui el veu conclou que la
// web no està acabada, i té raó.
{
  const PROVISIONAL = [
    [/lorem ipsum/i, 'text de farciment «lorem ipsum»'],
    [/\bTODO\b|\bFIXME\b|\bXXX\b(?!\/)/, 'una nota de feina pendent (TODO/FIXME)'],
    [/\bplaceholder\b(?![-\w])/i, 'la paraula «placeholder»'],
    [/\bpendent de (confirmar|definir|decidir)\b/i, 'un «pendent de confirmar»'],
    [/\b(pr[òo]ximamente|coming soon|properament)\b/i, 'un «properament» sense data'],
    [/\bXX\/XX|\bDD\/MM|\b00\/00\b/, 'una data sense omplir'],
  ];
  for (const rel of pagines) {
    if (!esPublica(rel)) continue;
    const html = fs.readFileSync(path.join(ROOT, rel), 'utf8');
    const text = textVisible(html);
    for (const [re, que] of PROVISIONAL) {
      const m = text.match(re);
      if (m) afegeix('avís', 'provisional', 'text-provisional', `es veu ${que}`, { pagina: urlOf(rel), fragment: text.slice(Math.max(0, text.indexOf(m[0]) - 40), text.indexOf(m[0]) + 60).trim() });
    }
    // enllaços que no porten enlloc dins del contingut (les pestanyes i els
    // desplegables sí que fan servir href="#" de forma legítima)
    for (const a of html.matchAll(/<a\b([^>]*)>([\s\S]{0,120}?)<\/a>/gi)) {
      const href = attr('<a' + a[1] + '>', 'href');
      if (href !== undefined && href.trim() === '') {
        afegeix('avís', 'provisional', 'enllac-buit', 'un enllaç amb href buit', { pagina: urlOf(rel), text: textVisible(a[2]).trim().slice(0, 40) });
      }
    }
  }
}

// =====================================================================
// 7 · Cap clau ni cap secret publicat sense voler
// =====================================================================
// Tot el que hi ha en aquest repositori es publica tal qual. Una clau d'API
// dins d'un HTML és pública des del primer minut.
{
  const PATRONS = [
    [/\bghp_[A-Za-z0-9]{20,}/, 'token personal de GitHub'],
    [/\bgithub_pat_[A-Za-z0-9_]{20,}/, 'token de GitHub (pat)'],
    [/\bsk-[A-Za-z0-9]{20,}/, 'clau d\'API tipus OpenAI'],
    [/\bAIza[0-9A-Za-z_-]{30,}/, 'clau de Google API'],
    [/\bxox[baprs]-[A-Za-z0-9-]{10,}/, 'token de Slack'],
    [/-----BEGIN [A-Z ]*PRIVATE KEY-----/, 'clau privada'],
    [/\bservice_role\b[^\n]{0,40}\beyJ[A-Za-z0-9_-]{20,}/, 'clau de servei de Supabase'],
    [/\b(password|contrasenya|passwd)\s*[:=]\s*["'][^"'\s]{6,}["']/i, 'una contrasenya escrita al codi'],
  ];
  const candidats = tots.filter((f) => /\.(html|js|json|css|txt|md|yml|yaml)$/i.test(f) && !f.startsWith('tests/out'));
  for (const rel of candidats) {
    let txt;
    try { txt = fs.readFileSync(path.join(ROOT, rel), 'utf8'); } catch { continue; }
    for (const [re, que] of PATRONS) {
      const m = txt.match(re);
      if (!m) continue;
      // Un exemple escrit expressament perquè algú sàpiga què ha d'enganxar
      // (`placeholder="ghp_xxxxxxxx"`) no és cap fuita. Es descarta el que és
      // òbviament una plantilla, no el que té pinta de clau de debò.
      if (/x{6,}|X{6,}|\.{3}|…|AQUI|AQUÍ|EXEMPLE|EJEMPLO|EXAMPLE|TU_|YOUR_|<[a-z]/i.test(m[0])) continue;
      const linia = txt.slice(0, m.index).split('\n').length;
      afegeix('error', 'secrets', 'secret-publicat', `sembla ${que} dins d'un fitxer que es publica`, { fitxer: rel, linia, fragment: m[0].slice(0, 12) + '…' });
    }
  }
}

// =====================================================================
// 8 · Pes: el que trigarà a carregar-se amb la xarxa del pavelló
// =====================================================================
// Es compta el pes del HTML més el dels fitxers propis que la pàgina necessita
// per pintar-se la primera vegada. No és el temps real de càrrega (GitHub
// Pages comprimeix i cacheja), però una pàgina de 6 MB és de 6 MB a tot arreu.
{
  const mida = (rel) => { try { return fs.statSync(path.join(ROOT, rel)).size; } catch { return 0; } };
  const pesos = [];
  for (const rel of pagines) {
    if (!esPublica(rel)) continue;
    const html = fs.readFileSync(path.join(ROOT, rel), 'utf8');
    let total = Buffer.byteLength(html);
    const vistos = new Set();
    const sumaRuta = (href) => {
      const res = existeixLocal(href, rel);
      if (!res || !res.exists) return;
      const abs = path.resolve(href.startsWith('/') ? ROOT : path.dirname(path.join(ROOT, rel)), href.split('#')[0].split('?')[0].replace(/^\//, ''));
      const r = path.relative(ROOT, abs);
      if (vistos.has(r)) return;
      vistos.add(r); total += mida(r);
    };
    for (const m of html.matchAll(/<(?:img|script)\b[^>]*\bsrc\s*=\s*"([^"]+)"/gi)) sumaRuta(m[1]);
    for (const m of html.matchAll(/<link\b[^>]*rel\s*=\s*"(?:stylesheet|preload)"[^>]*\bhref\s*=\s*"([^"]+)"/gi)) sumaRuta(m[1]);
    pesos.push({ url: urlOf(rel), kb: Math.round(total / 1024) });
  }
  pesos.sort((a, b) => b.kb - a.kb);
  const LIMIT = 3000;   // 3 MB: per damunt d'això es nota amb dades mòbils
  for (const p of pesos.filter((p) => p.kb > LIMIT)) {
    afegeix('avís', 'pes', 'pagina-pesada', `${p.kb} kB de contingut propi en una sola pàgina`, { pagina: p.url });
  }
  afegeix('informatiu', 'pes', 'pes-mitja', `pes mitjà ${Math.round(pesos.reduce((n, p) => n + p.kb, 0) / (pesos.length || 1))} kB · la més pesada ${pesos[0]?.kb} kB`, { top: pesos.slice(0, 5) });
}

// =====================================================================
// 9 · El codi de cada pàgina es pot llegir
// =====================================================================
// Un error de sintaxi en un <script> no dona cap avís: el navegador
// simplement no executa res d'aquell bloc, i el que en depenia deixa de
// funcionar en silenci. Va passar amb `/partits/cartell.html`, on una cometa
// de més dins de `x.font='170px Anton, 'Anton', sans-serif'` va deixar mort
// tot el generador de cartells en els tres idiomes durant setmanes.
{
  const { execFileSync } = await import('node:child_process');
  const os = await import('node:os');
  const tmp = path.join(os.tmpdir(), `cbgb-sintaxi-${process.pid}.mjs`);
  const provaSintaxi = (codi) => {
    fs.writeFileSync(tmp, codi);
    try { execFileSync(process.execPath, ['--check', tmp], { stdio: 'pipe' }); return null; }
    catch (e) { return (e.stderr?.toString() || e.message).split('\n').find((l) => /SyntaxError/.test(l)) || 'error de sintaxi'; }
  };
  for (const rel of [...pagines.filter(esPublica), ...tots.filter((f) => f.endsWith('.js') && !f.startsWith('galeria/'))]) {
    const txt = fs.readFileSync(path.join(ROOT, rel), 'utf8');
    if (rel.endsWith('.js')) {
      const err = provaSintaxi(txt);
      if (err) afegeix('error', 'codi', 'js-no-compila', `${rel} no es pot llegir com a JavaScript: ${err}`, { fitxer: rel });
      continue;
    }
    const blocs = [...txt.matchAll(/<script(?![^>]*\bsrc=)([^>]*)>([\s\S]*?)<\/script>/gi)]
      .filter((m) => !/type\s*=\s*["'](?!text\/javascript|module|application\/javascript)/i.test(m[1]));
    if (!blocs.length) continue;
    // Es proven junts, com els executa el navegador; si peten, es busca quin.
    if (!provaSintaxi(blocs.map((b) => b[2]).join('\n;\n'))) continue;
    for (const b of blocs) {
      const err = provaSintaxi(b[2]);
      if (err) {
        const linia = txt.slice(0, b.index).split('\n').length;
        afegeix('error', 'codi', 'js-no-compila', `un <script> de la pàgina no es pot llegir: ${err}`, { pagina: urlOf(rel), linia });
      }
    }
  }
  try { fs.unlinkSync(tmp); } catch {}
}

// =====================================================================
// 10 · Els tres idiomes van junts
// =====================================================================
// Cada pàgina en català ha de tenir bessona a /es/ i /en/, i cap dels tres
// menús d'idioma pot portar a una adreça morta: és la manera més ràpida de
// fer que algú es perdi el dia que la web s'anuncia.
{
  const canonics = new Map();
  for (const rel of pagines) {
    if (!esPublica(rel)) continue;
    const html = fs.readFileSync(path.join(ROOT, rel), 'utf8');
    for (const m of html.matchAll(/<link\b[^>]*rel\s*=\s*["']alternate["'][^>]*>/gi)) {
      const href = attr(m[0], 'href'); const lang = attr(m[0], 'hreflang');
      if (!href || !href.startsWith(SITE)) continue;
      const res = existeixLocal(href.slice(SITE.length) || '/', rel);
      if (res && !res.exists) {
        afegeix('error', 'idiomes', 'hreflang-mort', `el canvi d'idioma «${lang}» porta a ${href.slice(SITE.length)}, que no existeix`, { pagina: urlOf(rel) });
      }
    }
    const canon = html.match(/<link\b[^>]*rel\s*=\s*["']canonical["'][^>]*>/i);
    if (canon) {
      const href = attr(canon[0], 'href');
      if (href) canonics.set(urlOf(rel), href);
    }
  }
  // pàgines en català sense traducció declarada
  let sense = 0; const mostra = [];
  for (const rel of pagines) {
    if (!esPublica(rel) || rel.startsWith('es/') || rel.startsWith('en/')) continue;
    const html = fs.readFileSync(path.join(ROOT, rel), 'utf8');
    if (/noindex/i.test(html) || /http-equiv=["']refresh["']/i.test(html)) continue;
    if (!/hreflang\s*=\s*["']es["']/i.test(html) || !/hreflang\s*=\s*["']en["']/i.test(html)) {
      sense++; if (mostra.length < 8) mostra.push(urlOf(rel));
    }
  }
  if (sense) afegeix('avís', 'idiomes', 'sense-traduccio', `${sense} pàgines en català no declaren versió en castellà o anglès`, { mostra });
}

// ---------- sortida ----------
fs.mkdirSync(OUT, { recursive: true });
const resum = { errors: 0, avisos: 0, informatius: 0 };
for (const t of troballes) {
  if (t.nivell === 'error') resum.errors++;
  else if (t.nivell === 'avís') resum.avisos++;
  else resum.informatius++;
}
if (binarisOmesos) {
  afegeix('informatiu', 'actius', 'binaris-omesos',
    `${binarisOmesos} rutes d'imatge, vídeo, PDF o tipografia no s'han comprovat: el repositori s'ha baixat sense binaris (--sense-binaris)`);
}

const sortida = {
  generated: new Date().toISOString(),
  pages: pagines.filter(esPublica).length,
  resum,
  troballes,
};
fs.writeFileSync(path.join(OUT, 'llancament.json'), JSON.stringify(sortida, null, 2));

const perBloc = {};
for (const t of troballes) {
  perBloc[t.bloc] ||= { error: 0, 'avís': 0, informatiu: 0 };
  perBloc[t.bloc][t.nivell]++;
}
console.log(`${sortida.pages} pàgines públiques analitzades`);
for (const [bloc, n] of Object.entries(perBloc)) {
  console.log(`  ${bloc.padEnd(14)} errors: ${n.error} · avisos: ${n['avís']}`);
}
console.log(`errors: ${resum.errors} · avisos: ${resum.avisos} · informatius: ${resum.informatius}`);
console.log(`Desat a ${path.relative(ROOT, path.join(OUT, 'llancament.json'))}`);
