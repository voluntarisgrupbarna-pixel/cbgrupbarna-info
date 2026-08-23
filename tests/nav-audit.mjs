// Auditoria de NAVEGACIÓ: per què una persona es perd pel web.
//
// Les altres bateries miren una pàgina de cada vegada. Aquesta mira el lloc
// SENCER com un mapa i respon a tres preguntes que es fa qualsevol visitant:
//
//   1. ON SÓC?       — la pàgina m'ho diu (títol, molla de pa, entrada activa)?
//   2. ON PUC ANAR?  — quantes sortides reals tinc des d'aquí, sense fer enrere?
//   3. HI PUC ARRIBAR? — des de la portada, en quants clics arribo a cada lloc?
//
// La clau: només compta el que es VEU DE DEBÒ al dispositiu. Un enllaç amagat
// per un media query no és una sortida. Per això es fa amb navegador i a dues
// amplades: el mòbil és on la navegació s'aprima i on la gent es perd.
//
//   node tests/nav-audit.mjs
//   node tests/nav-audit.mjs --amplades 360            # només mòbil
//   node tests/nav-audit.mjs --max 60                  # una mostra ràpida
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';
import { startServer } from './lib/server.mjs';

const require = createRequire(import.meta.url);
const { chromium } = (() => {
  try { return require('playwright'); }
  catch { return require('/opt/node22/lib/node_modules/playwright'); }
})();

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const args = process.argv.slice(2);
const argVal = (n, d) => (args.includes(`--${n}`) ? args[args.indexOf(`--${n}`) + 1] : d);
const OUT = path.resolve(ROOT, argVal('out', 'tests/out'));
const MAX = +argVal('max', 0) || Infinity;
const AMPLADES = argVal('amplades', '360,1440').split(',').map(Number);

const SKIP = [/^\.git\//, /^node_modules\//, /^tests\//, /^\.github\//, /^galeria\/node_modules\//];

function trobaPagines() {
  const out = [];
  const walk = (dir) => {
    for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
      const abs = path.join(dir, e.name);
      const rel = path.relative(ROOT, abs);
      if (SKIP.some((re) => re.test(rel + (e.isDirectory() ? '/' : '')))) continue;
      if (e.isDirectory()) walk(abs);
      else if (e.name.endsWith('.html')) {
        out.push({ file: rel, url: '/' + rel.replace(/index\.html$/, '').replace(/\\/g, '/') });
      }
    }
  };
  walk(ROOT);
  return out.sort((a, b) => a.url.localeCompare(b.url));
}

// ---------------------------------------------------------------------------
// Dins de la pàgina: separem el «xassís» (el que hi ha a totes les pàgines:
// capçalera, menú, peu) del cos. Les sortides que compten per no perdre's són
// les del xassís: hi són sempre, siguis on siguis. Les del cos depenen del
// contingut i no es poden donar per fetes.
// ---------------------------------------------------------------------------
const RECULL = `(function () {
  function visible(el) {
    var r = el.getBoundingClientRect();
    if (r.width < 1 || r.height < 1) return false;
    var cs = getComputedStyle(el);
    if (cs.visibility === 'hidden' || cs.display === 'none') return false;
    var op = 1, p = el;
    while (p && p.nodeType === 1) { op *= parseFloat(getComputedStyle(p).opacity || '1'); p = p.parentElement; }
    return op > 0.05;
  }
  function net(href) {
    if (!href) return null;
    try {
      var u = new URL(href, location.href);
      if (u.origin !== location.origin) return null;         // extern: no és navegació interna
      if (u.pathname === location.pathname && u.hash) return null;  // àncora a la mateixa pàgina
      var p = u.pathname;
      if (p.endsWith('/index.html')) p = p.slice(0, -10);
      return p;
    } catch (e) { return null; }
  }
  function recull(sel) {
    var vis = [], tot = [];
    document.querySelectorAll(sel).forEach(function (zona) {
      zona.querySelectorAll('a[href]').forEach(function (a) {
        // El commutador d'idioma no és una sortida cap a un altre lloc: porta
        // a la MATEIXA pàgina en una altra llengua. Comptar-lo com a destí
        // faria semblar que cada pàgina té una navegació diferent de totes
        // les altres, quan el que canvia és només l'adreça d'aquests dos
        // enllaços. Que hi sigui es mesura a part, al camp idiomes.
        // (Sense cometes invertides: aquest bloc és una plantilla de text.)
        if (a.closest('.lang-switch, .langs')) return;
        var d = net(a.getAttribute('href'));
        if (!d) return;
        tot.push(d);
        if (visible(a)) vis.push(d);
      });
    });
    return { vis: [].concat.apply([], [[...new Set(vis)]]), tot: [...new Set(tot)] };
  }

  var capcalera = recull('header, .head');
  var menu      = recull('#menu, .menu, [role=dialog] nav');
  var peu       = recull('footer, .foot');
  var cos       = recull('main, #main, body > section, body > div.wrap, article');

  // Molla de pa: la que sigui, marcada o no amb dades estructurades.
  // La classe .crumb és la que fa servir la major part del lloc; sense
  // mirar-la, aquesta auditoria acusaria 312 pàgines de no tenir molla de pa.
  // (Sense cometes invertides: aquest bloc és una plantilla de text.)
  var moll = document.querySelector('.crumb, .breadcrumb, .molla, [aria-label*="ruta" i], [aria-label*="breadcrumb" i], nav ol');
  var jsonMoll = false;
  document.querySelectorAll('script[type="application/ld+json"]').forEach(function (s) {
    if (/BreadcrumbList/.test(s.textContent || '')) jsonMoll = true;
  });

  // Entrada de navegació marcada com a actual.
  var actiu = document.querySelector('header [aria-current], .head [aria-current], header a.active, .head a.actiu, .head a.active');

  var h1 = document.querySelector('h1');
  var burger = document.querySelector('#burger, .head-burger, [aria-controls=menu]');

  return {
    titol: (document.title || '').trim(),
    h1: h1 ? (h1.textContent || '').trim().slice(0, 90) : null,
    quantsH1: document.querySelectorAll('h1').length,
    capcalera: capcalera, menu: menu, peu: peu, cos: cos,
    teBurger: !!burger,
    burgerVisible: !!(burger && visible(burger)),
    mollaVisible: !!(moll && visible(moll)),
    mollaDades: jsonMoll,
    actiu: actiu ? (actiu.textContent || '').trim().slice(0, 40) : null,
    idiomes: [].slice.call(document.querySelectorAll('.lang-switch a, [hreflang]')).filter(visible).length,
    tornarInici: !!([].slice.call(document.querySelectorAll('header a[href], .head a[href]'))
      .filter(visible).find(function (a) {
        var h = a.getAttribute('href') || '';
        return h === '/' || h === '/index.html' || /^https?:\\/\\/[^/]+\\/?$/.test(h);
      })),
  };
})()`;

// ---------------------------------------------------------------------------
const pagines = trobaPagines().slice(0, MAX);
const { origin, close } = await startServer(ROOT);
const browser = await chromium.launch();
const dades = {};   // dades[amplada][url]

console.log(`Mapejant ${pagines.length} pàgines a ${AMPLADES.join(' i ')} px\n`);

for (const amplada of AMPLADES) {
  const ctx = await browser.newContext({
    viewport: { width: amplada, height: amplada < 700 ? 740 : 900 },
    deviceScaleFactor: 2, isMobile: amplada < 700, hasTouch: amplada < 700, locale: 'ca-ES',
  });
  await ctx.route('**/*', (route) => (route.request().url().startsWith(origin) ? route.continue() : route.abort()));
  dades[amplada] = {};
  const page = await ctx.newPage();
  let n = 0;
  for (const p of pagines) {
    try {
      await page.goto(origin + p.url, { waitUntil: 'domcontentloaded', timeout: 20000 });
      await page.waitForTimeout(90);
      dades[amplada][p.url] = await page.evaluate(RECULL);
    } catch (e) {
      dades[amplada][p.url] = { error: String(e).slice(0, 100) };
    }
    if (++n % 40 === 0) process.stdout.write(`  ${amplada}px · ${n}/${pagines.length}\n`);
  }
  await ctx.close();
}
await browser.close();
await close();

// ---------------------------------------------------------------------------
// Anàlisi
// ---------------------------------------------------------------------------
const existeix = new Set(pagines.map((p) => p.url));
const problemes = [];
const resum = {};

for (const amplada of AMPLADES) {
  const d = dades[amplada];
  const mobil = amplada < 700;

  // --- Graf de navegació fent servir NOMÉS el xassís -----------------------
  // Si per anar d'una pàgina a una altra cal passar pel cos d'un article, la
  // navegació no és navegació: és sort.
  //
  // Un enllaç dins d'un menú tancat SÍ que compta, sempre que el botó que
  // l'obre es vegi: és un toc més, no un carreró. Comptar només el que ja és
  // a la pantalla diria que un lloc amb menú de gallet no té navegació, que
  // és fals. El que no compta mai és un enllaç que cap gest fa aparèixer.
  const sortides = {};
  for (const [url, v] of Object.entries(d)) {
    if (v.error) continue;
    const delMenu = v.burgerVisible ? v.menu.tot : v.menu.vis;
    sortides[url] = [...new Set([...v.capcalera.vis, ...delMenu, ...v.peu.vis])]
      .filter((x) => existeix.has(x) && x !== url);
  }

  // BFS des de la portada.
  const dist = { '/': 0 };
  let cua = ['/'];
  while (cua.length) {
    const seg = [];
    for (const u of cua) for (const v of (sortides[u] || [])) {
      if (dist[v] === undefined) { dist[v] = dist[u] + 1; seg.push(v); }
    }
    cua = seg;
  }

  const inabastables = pagines.map((p) => p.url).filter((u) => dist[u] === undefined);
  const lluny = Object.entries(dist).filter(([, k]) => k >= 4).map(([u, k]) => `${u} (${k} clics)`);

  // Formes diferents de navegació persistent: si n'hi ha moltes, el menú
  // «canvia» de pàgina en pàgina i és el que es percep com a incoherent.
  // Es mira el xassís sencer (capçalera + menú), no la capçalera sola: dues
  // pàgines amb el mateix menú ofereixen el mateix mapa encara que la barra
  // de dalt en mostri quatre entrades o set.
  const formes = new Map();
  for (const [url, v] of Object.entries(d)) {
    if (v.error) continue;
    const delMenu = v.burgerVisible ? v.menu.tot : v.menu.vis;
    const clau = [...new Set([...v.capcalera.vis, ...delMenu])].sort().join('|') || '(cap)';
    if (!formes.has(clau)) formes.set(clau, []);
    formes.get(clau).push(url);
  }

  const senseSortida = Object.entries(sortides).filter(([, s]) => s.length <= 1).map(([u]) => u);
  const senseMolla = Object.entries(d).filter(([u, v]) => !v.error && u !== '/' && !v.mollaVisible).map(([u]) => u);
  const senseActiu = Object.entries(d).filter(([u, v]) => !v.error && u !== '/' && !v.actiu).map(([u]) => u);
  const senseBurger = Object.entries(d).filter(([, v]) => !v.error && !v.burgerVisible).map(([u]) => u);
  const senseIdioma = Object.entries(d).filter(([, v]) => !v.error && !v.idiomes).map(([u]) => u);
  const senseH1 = Object.entries(d).filter(([, v]) => !v.error && !v.h1).map(([u]) => u);
  const multiH1 = Object.entries(d).filter(([, v]) => !v.error && v.quantsH1 > 1).map(([u]) => u);
  const senseInici = Object.entries(d).filter(([, v]) => !v.error && !v.tornarInici).map(([u]) => u);

  const nSort = Object.values(sortides).map((s) => s.length);
  const mitjana = nSort.length ? (nSort.reduce((a, b) => a + b, 0) / nSort.length) : 0;

  resum[amplada] = {
    pagines: pagines.length,
    sortidesMitjana: +mitjana.toFixed(1),
    sortidesMinim: Math.min(...nSort),
    sortidesMaxim: Math.max(...nSort),
    abastablesEnUnClic: Object.values(dist).filter((k) => k === 1).length,
    abastablesEnDosClics: Object.values(dist).filter((k) => k <= 2).length,
    inabastables: inabastables.length,
    formesDeNavegacio: formes.size,
  };

  const afegeix = (tipus, gravetat, llista, detall) => {
    if (!llista.length) return;
    problemes.push({ amplada, tipus, gravetat, quants: llista.length, detall,
      exemples: llista.slice(0, 8) });
  };

  afegeix('pagines-inabastables-des-de-la-navegacio', 'greu', inabastables,
    'no s\'hi arriba des de la portada seguint només capçalera, menú i peu: cal saber-ne l\'adreça');
  afegeix('sense-menu-complet', mobil ? 'greu' : 'mitja', senseBurger,
    'la pàgina no ofereix el menú complet del club: les sortides es redueixen a les de la capçalera');
  afegeix('carrero-sense-sortida', 'greu', senseSortida,
    'com a molt una sortida de navegació persistent: qui hi arriba, hi queda');
  afegeix('sense-molla-de-pa', 'mitja', senseMolla,
    'la pàgina no diu on és dins del club');
  afegeix('sense-entrada-activa', 'mitja', senseActiu,
    'cap entrada de la navegació marca la secció on ets (aria-current)');
  afegeix('sense-canvi-didioma', 'mitja', senseIdioma,
    'no s\'hi pot canviar de llengua: qui hi arriba en castellà o anglès hi queda atrapat');
  afegeix('sense-h1', 'mitja', senseH1, 'sense titular: no es pot saber de què va la pàgina');
  afegeix('h1-repetit', 'lleu', multiH1, 'més d\'un <h1>: la jerarquia deixa de ser llegible');
  afegeix('sense-tornar-a-inici', 'mitja', senseInici, 'no hi ha manera clara de tornar a la portada');
  if (lluny.length) afegeix('massa-lluny-de-la-portada', 'mitja', lluny, 'a 4 clics o més de la portada');
  if (formes.size > 3) {
    problemes.push({ amplada, tipus: 'navegacio-incoherent', gravetat: 'greu', quants: formes.size,
      detall: 'la navegació persistent no és la mateixa a tot el lloc: aquestes són les variants i quantes pàgines fa servir cadascuna',
      exemples: [...formes.entries()].sort((a, b) => b[1].length - a[1].length)
        .slice(0, 6).map(([k, v]) => `${v.length} pàgines · ${k.split('|').length} enllaços: ${k.slice(0, 90)}`) });
  }
}

fs.mkdirSync(OUT, { recursive: true });
fs.writeFileSync(path.join(OUT, 'nav-audit.json'),
  JSON.stringify({ data: new Date().toISOString(), amplades: AMPLADES, resum, problemes, dades }, null, 2));

// ---------------------------------------------------------------------------
console.log(`\n${'═'.repeat(74)}\nCOM ES NAVEGA EL LLOC\n${'═'.repeat(74)}`);
for (const a of AMPLADES) {
  const r = resum[a];
  console.log(`\n▸ A ${a}px ${a < 700 ? '(mòbil)' : '(escriptori)'}`);
  console.log(`    sortides de navegació per pàgina: ${r.sortidesMinim}–${r.sortidesMaxim} (mitjana ${r.sortidesMitjana})`);
  console.log(`    a un clic de la portada: ${r.abastablesEnUnClic} pàgines · a dos clics: ${r.abastablesEnDosClics} de ${r.pagines}`);
  console.log(`    no s'hi arriba navegant: ${r.inabastables} pàgines`);
  console.log(`    variants diferents de navegació: ${r.formesDeNavegacio}`);
}

const ordre = { greu: 0, mitja: 1, lleu: 2 };
console.log(`\n${'═'.repeat(74)}\nPROBLEMES\n${'═'.repeat(74)}`);
for (const p of problemes.sort((x, y) => ordre[x.gravetat] - ordre[y.gravetat] || y.quants - x.quants)) {
  console.log(`\n[${p.gravetat.toUpperCase()}] ${p.tipus} · ${p.quants} · a ${p.amplada}px`);
  console.log(`  ${p.detall}`);
  for (const e of p.exemples.slice(0, 5)) console.log(`    · ${e}`);
  if (p.quants > 5) console.log(`    …i ${p.quants - 5} més`);
}
console.log(`\nDades completes: ${path.relative(ROOT, path.join(OUT, 'nav-audit.json'))}`);
