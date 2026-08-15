// Ajunta les dues auditories i en treu un informe llegible.
//
//   node tests/report.mjs            → resum per consola
//   node tests/report.mjs --md fitxer.md
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const OUT = path.join(ROOT, 'tests/out');
const args = process.argv.slice(2);
const mdPath = args.includes('--md') ? args[args.indexOf('--md') + 1] : null;

const read = (f) => {
  const p = path.join(OUT, f);
  if (!fs.existsSync(p)) { console.error(`Falta ${f}. Executa primer les auditories.`); process.exit(1); }
  return JSON.parse(fs.readFileSync(p, 'utf8'));
};
const seo = read('seo-geo.json');
const br = read('browser.json');

// El microlloc del Premi Dona i Esport té sistema visual propi i les eines
// internes no són públiques: es compten a part per no barrejar diagnòstics.
const zoneOf = (url) => {
  if (url.startsWith('/premidonaesport')) return 'premidonaesport';
  if (url.includes('admin') || url.startsWith('/briefing') || url.startsWith('/opina/print')) return 'intern';
  return 'públic';
};

const lines = [];
const say = (s = '') => { lines.push(s); console.log(s); };
const table = (head, rows) => {
  say('| ' + head.join(' | ') + ' |');
  say('|' + head.map(() => '---').join('|') + '|');
  for (const r of rows) say('| ' + r.join(' | ') + ' |');
  say();
};

const vps = [...new Set(br.results.map((r) => r.viewport))];
const byVp = (v) => br.results.filter((r) => r.viewport === v);

say(`# Bateria de proves · cbgrupbarna.info`);
say();
say(`${seo.pages} pàgines · ${vps.length} amplades de pantalla · ${br.results.length} càrregues verificades`);
say(`Generat el ${new Date(br.generated).toLocaleString('ca-ES')}`);
say();

// ---------- 1. Renderitzat per amplada ----------
say('## 1 · Com es comporta a cada amplada');
say();
const rows = [];
for (const v of vps) {
  const set = byVp(v);
  const w = set[0]?.width;
  rows.push([
    `${v} (${w}px)`,
    set.length,
    set.filter((r) => r.overflow).length,
    set.reduce((n, r) => n + (r.tapTargetsTotal || 0), 0),
    set.reduce((n, r) => n + (r.counts?.smallText || 0), 0),
    set.reduce((n, r) => n + (r.counts?.contrast || 0), 0),
    set.reduce((n, r) => n + (r.images?.upscaled || []).length, 0),
  ]);
}
table(['Amplada', 'Pàgines', 'Desbordament', 'Zones < 44 px', 'Text < 12 px', 'Contrast insuficient', 'Fotos ampliades'], rows);

const overflowing = br.results.filter((r) => r.overflow);
if (!overflowing.length) {
  say('**Cap pàgina desborda horitzontalment en cap amplada.** És el resultat més important d\'aquest bloc: la maqueta aguanta de 360 a 1440 px.');
} else {
  say(`**${overflowing.length} càrregues amb desbordament horitzontal:**`);
  for (const r of overflowing.slice(0, 15)) {
    say(`- \`${r.page}\` a ${r.viewport}: sobren ${r.overflow.excess} px — ${r.overflow.elements.slice(0, 2).map((e) => e.el).join(', ')}`);
  }
}
say();

// ---------- 2. Errors durs ----------
say('## 2 · Errors tècnics');
say();
const brokenLinks = new Map();
for (const p of seo.perPage) {
  for (const i of p.issues.filter((x) => x.code === 'enllaç-trencat')) {
    for (const t of i.targets) {
      if (!brokenLinks.has(t.href)) brokenLinks.set(t.href, new Set());
      brokenLinks.get(t.href).add(p.url);
    }
  }
}
if (brokenLinks.size) {
  say(`### Destins interns que no existeixen (${brokenLinks.size})`);
  say();
  table(['Destí', 'Pàgines que hi enllacen'],
    [...brokenLinks.entries()].sort((a, b) => b[1].size - a[1].size)
      .map(([h, s]) => [`\`${h}\``, s.size]));
}

const http404 = new Map();
for (const r of br.results) for (const f of r.failed || []) {
  if (f.reason === 'net::ERR_ABORTED') continue;
  const k = f.url + (f.status ? ` (${f.status})` : ' (no carrega)');
  if (!http404.has(k)) http404.set(k, new Set());
  http404.get(k).add(r.page);
}
if (http404.size) {
  say('### Recursos que el navegador no arriba a carregar');
  say();
  table(['Recurs', 'Des de'], [...http404.entries()].map(([k, s]) => [`\`${k}\``, [...s].join(', ')]));
}

const dupIds = br.results.filter((r) => (r.duplicateIds || []).length);
say(dupIds.length ? `### IDs duplicats\n\n${dupIds.length} càrregues afectades.` : '**Cap ID duplicat** en tot el lloc.');
say();

// ---------- 3. Accessibilitat i UX ----------
say('## 3 · Accessibilitat i ús real');
say();
const mob = byVp(vps.find((v) => v.startsWith('mòbil')) || vps[0]);
const zones = { 'públic': [], 'premidonaesport': [], 'intern': [] };
for (const r of mob) zones[zoneOf(r.page)].push(r);

table(['Zona', 'Pàgines', 'Text < 12 px', 'Contrast < AA', 'Zones < 44 px', 'Focus invisible'],
  Object.entries(zones).map(([z, set]) => [
    z, set.length,
    set.reduce((n, r) => n + (r.counts?.smallText || 0), 0),
    set.reduce((n, r) => n + (r.counts?.contrast || 0), 0),
    set.reduce((n, r) => n + (r.tapTargetsTotal || 0), 0),
    set.reduce((n, r) => n + (r.keyboardFocus?.invisible || []).length, 0),
  ]));

// Mides de lletra
const sizeTally = {};
for (const r of mob) for (const s of r.smallText || []) sizeTally[s.size] = (sizeTally[s.size] || 0) + 1;
const under10 = Object.entries(sizeTally).filter(([s]) => +s < 10).reduce((n, [, v]) => n + v, 0);
say(`### Mida de lletra a 360 px`);
say();
say(`${under10} mostres de text per sota de 10 px. Les més petites:`);
say();
table(['Mida', 'Mostres'], Object.entries(sizeTally).sort((a, b) => a[0] - b[0]).slice(0, 8).map(([s, n]) => [`${s} px`, n]));

// Contrast agrupat
const cg = new Map();
for (const r of br.results) for (const c of r.contrast || []) {
  const k = `${c.fg} sobre ${c.bg} · ${c.size} px`;
  if (!cg.has(k) || cg.get(k).ratio > c.ratio) cg.set(k, { ratio: c.ratio, need: c.need, el: c.el, pages: new Set() });
  cg.get(k).pages.add(r.page);
}
say('### Combinacions de color per sota del mínim AA');
say();
table(['Ràtio', 'Cal', 'Combinació', 'Pàgines', 'Exemple'],
  [...cg.entries()].sort((a, b) => a[1].ratio - b[1].ratio).slice(0, 15)
    .map(([k, v]) => [`${v.ratio}:1`, `${v.need}:1`, k, v.pages.size, `\`${v.el.slice(0, 44)}\``]));

// Zones tocables
const tapWorst = mob.slice().sort((a, b) => (b.tapTargetsTotal || 0) - (a.tapTargetsTotal || 0)).slice(0, 8);
say('### Zones tocables per sota de 44 px (mòbil)');
say();
table(['Pàgina', 'Quantes', 'La més petita'],
  tapWorst.map((r) => [`\`${r.page}\``, r.tapTargetsTotal, r.tapTargets?.[0] ? `${r.tapTargets[0].w}×${r.tapTargets[0].h} — ${r.tapTargets[0].el.slice(0, 40)}` : '—']));

// Focus
const fg = new Map();
for (const r of br.results) for (const f of r.keyboardFocus?.invisible || []) {
  const k = f.split('«')[0].trim();
  if (!fg.has(k)) fg.set(k, new Set());
  fg.get(k).add(r.page);
}
if (fg.size) {
  say('### Elements sense indicador de focus en tabular');
  say();
  table(['Element', 'Pàgines'], [...fg.entries()].sort((a, b) => b[1].size - a[1].size).slice(0, 12).map(([k, s]) => [`\`${k}\``, s.size]));
} else {
  say('**Tots els elements enfocats amb el teclat mostren un indicador visible.**');
  say();
}

// Elements tapats
const occ = new Map();
for (const r of br.results) for (const o of r.occluded || []) {
  const k = `${o.el.split('«')[0].trim()} ← ${o.tapat_per.split('«')[0].trim()}`;
  if (!occ.has(k)) occ.set(k, { pages: new Set(), max: 0, ex: o });
  occ.get(k).pages.add(`${r.page} (${r.viewport})`);
  occ.get(k).max = Math.max(occ.get(k).max, o.cobreix);
}
if (occ.size) {
  say('### Controls tapats per un altre element');
  say();
  say('Botons i enllaços que existeixen però que en aquell punt de la pantalla en respon un altre: qui hi toqui, no els prem.');
  say();
  table(['Control tapat', 'Cobert', 'On'],
    [...occ.entries()].sort((a, b) => b[1].max - a[1].max).slice(0, 12)
      .map(([k, v]) => [`\`${k}\``, `${v.max} %`, [...v.pages].slice(0, 3).join(', ') + (v.pages.size > 3 ? ` +${v.pages.size - 3}` : '')]));
} else {
  say('**Cap control queda tapat per un altre element** en cap amplada.');
  say();
}

// Estructura
say('### Estructura de les pàgines');
say();
table(['Comprovació', 'Pàgines que fallen', 'De'], [
  ['sense `<main>`', mob.filter((r) => r.landmarks && !r.landmarks.main).length, mob.length],
  ['sense `<nav>`', mob.filter((r) => r.landmarks && !r.landmarks.nav).length, mob.length],
  ['sense `<footer>`', mob.filter((r) => r.landmarks && !r.landmarks.footer).length, mob.length],
  ['sense atribut `lang`', mob.filter((r) => r.landmarks && !r.landmarks.lang).length, mob.length],
  ['salts de nivell d\'encapçalament', mob.filter((r) => (r.headings?.skips || []).length).length, mob.length],
  ['controls sense nom accessible', mob.reduce((n, r) => n + (r.unnamed || []).length, 0), '—'],
  ['taules que desborden', mob.reduce((n, r) => n + (r.tables || []).length, 0), '—'],
]);

// ---------- 4. Mode fosc ----------
const dm = br.results.filter((r) => r.darkMode);
const reacts = dm.filter((r) => r.darkMode.reacts);
say('## 4 · Modes clar i fosc');
say();
say(`De ${dm.length} pàgines provades amb \`prefers-color-scheme: dark\`, **${reacts.length} canvien d'aspecte**.`);
say();
if (!reacts.length) {
  say('Cap pàgina té definit el mode fosc, i tampoc no hi ha enlloc un commutador de tema. Qui tingui el mòbil en fosc rebrà el lloc en blanc.');
  say();
}

// ---------- 5. Fotografia ----------
say('## 5 · Fotografia');
say();
const up = new Map();
for (const r of mob) for (const i of r.images?.upscaled || []) {
  if (!up.has(i.src) || up.get(i.src).shortfall < i.shortfall) up.set(i.src, { ...i, pages: new Set() });
  up.get(i.src).pages.add(r.page);
}
say(`${up.size} imatges es pinten més grans del que fa el fitxer (a 3× de densitat, com un mòbil actual).`);
say();
table(['Fitxer', 'Píxels reals', 'Amplada CSS', 'Li falta', 'Pàgines'],
  [...up.values()].sort((a, b) => b.shortfall - a.shortfall).slice(0, 14)
    .map((i) => [`\`${i.src}\``, `${i.natural} px`, `${i.css} px`, `${i.shortfall}×`, i.pages.size]));

const noAlt = mob.reduce((n, r) => n + (r.images?.noAlt || []).length, 0);
say(`Imatges sense atribut \`alt\`: **${noAlt}**.`);
say();

// ---------- 6. SEO ----------
say('## 6 · SEO');
say();
const tally = {};
for (const p of seo.perPage) for (const i of p.issues) {
  const k = `${i.level} · ${i.code}`;
  tally[k] = (tally[k] || 0) + 1;
}
table(['Nivell i codi', 'Pàgines'], Object.entries(tally).sort((a, b) => b[1] - a[1]).map(([k, v]) => [k, v]));

const list = (code, label) => {
  const hits = seo.perPage.filter((p) => p.issues.some((i) => i.code === code));
  if (!hits.length) return;
  say(`**${label}** (${hits.length}): ${hits.slice(0, 12).map((p) => `\`${p.url}\``).join(', ')}${hits.length > 12 ? ' …' : ''}`);
  say();
};
list('idioma-divergent', 'Pàgines on el text no és de l\'idioma declarat');
list('h1', 'Pàgines sense `<h1>`');
list('description', 'Pàgines sense meta description');
list('canonical', 'Pàgines sense canonical');
list('canonical-divergent', 'Canonical que apunta a una altra URL');
list('viewport', 'Pàgines sense meta viewport');

say('### Sitemap');
say();
say(`${seo.sitemap.count} URLs declarades.`);
for (const i of seo.sitemap.issues) say(`- **${i.level}** · ${i.msg}${i.sample ? `\n  - ${i.sample.slice(0, 8).map((s) => `\`${s}\``).join('\n  - ')}` : ''}`);
say();

say('### hreflang');
say();
if (!seo.hreflang.issues.length) say('Sense incidències.');
for (const i of seo.hreflang.issues.filter((x) => x.level === 'error')) say(`- **${i.level}** · ${i.msg}`);
say();

if (seo.duplicates.issues.length) {
  say('### Títols i descripcions repetits');
  say();
  for (const i of seo.duplicates.issues) say(`- ${i.msg}: ${i.urls.map((u) => `\`${u}\``).join(', ')} — «${i.value}»`);
  say();
}

// ---------- 7. GEO ----------
say('## 7 · GEO');
say();
say('### Geogràfic: som localitzables com a club del Clot?');
say();
table(['Senyal', 'Estat'], [
  ...Object.entries(seo.geo.geoMeta).map(([k, v]) => [`\`${k}\``, v ? `\`${v}\`` : '**absent**']),
  ['coordenades dins de Barcelona', seo.geo.coords ? 'sí' : 'no comprovable'],
  ['entitats `SportsClub` / `LocalBusiness`', seo.geo.localEntities],
  ['pàgines que mencionen Clot, Sant Martí o Barcelona', `${seo.geo.placeCoverage.withPlace} de ${seo.geo.placeCoverage.total} (${seo.geo.placeCoverage.pct} %)`],
]);
say('Camps de l\'entitat de la portada:');
say();
table(['Camp', 'Hi és'], Object.entries(seo.geo.entityFields).map(([k, v]) => [`\`${k}\``, v ? 'sí' : '**no**']));
say('Coherència del NAP a les dades estructurades del club:');
say();
table(['Dada', 'Valors trobats'], Object.entries(seo.geo.napVariants).map(([k, v]) => [k, v.map((x) => `\`${x}\``).join(' · ')]));
for (const i of seo.geo.issues) say(`- **${i.level}** · ${i.msg}${i.values ? ` → ${i.values.map((v) => `\`${v}\``).join(', ')}` : ''}`);
say();

say('### Generatiu: ens poden citar les IA?');
say();
table(['Senyal', 'Valor'], [
  ['`llms.txt`', `${seo.llms.bytes} bytes, ${seo.llms.urls} URLs, ${seo.llms.issues.filter((i) => i.level === 'error').length} enllaços trencats`],
  ['rastrejadors d\'IA amb permís explícit', Object.values(seo.robots.aiBots).filter(Boolean).length + ' de ' + Object.keys(seo.robots.aiBots).length],
  ['encapçalaments en forma de pregunta', seo.generative.signals.questionHeadings],
  ['pàgines amb preguntes', seo.generative.signals.pagesWithQuestions],
  ['pàgines amb data a les dades estructurades', seo.generative.signals.datedPages],
  ['pàgines amb autor o editor', seo.generative.signals.pagesWithAuthor],
]);
say('Tipus de dades estructurades presents al lloc:');
say();
table(['Tipus', 'Pàgines'], Object.entries(seo.generative.schemaTally).sort((a, b) => b[1] - a[1]).map(([k, v]) => [`\`${k}\``, v]));
for (const i of seo.generative.issues) say(`- **${i.level}** · ${i.msg}`);
say();
const noBots = Object.entries(seo.robots.aiBots).filter(([, v]) => !v).map(([k]) => k);
if (noBots.length) say(`Rastrejadors sense regla pròpia (els cobreix el comodí \`User-agent: *\`): ${noBots.map((b) => `\`${b}\``).join(', ')}.`);
say();

// ---------- 8. Tercers ----------
say('## 8 · Dependències externes');
say();
const tp = new Map();
for (const r of mob) for (const h of r.thirdParty || []) {
  if (!tp.has(h)) tp.set(h, new Set());
  tp.get(h).add(r.page);
}
table(['Domini', 'Pàgines que hi depenen'], [...tp.entries()].sort((a, b) => b[1].size - a[1].size).map(([h, s]) => [`\`${h}\``, s.size]));
say('Les proves s\'han fet amb tot el trànsit extern tallat: el lloc es carrega i es maqueta igualment, cosa que vol dir que cap peça de contingut depèn d\'un tercer per aparèixer.');
say();

if (mdPath) {
  fs.writeFileSync(path.resolve(ROOT, mdPath), lines.join('\n'));
  console.error(`\nInforme desat a ${mdPath}`);
}
