// Bateria de rendiment: carrega les pàgines amb el navegador de debò, amb
// xarxa i CPU frenades com un mòbil de gamma mitjana, i mesura el que sent
// una persona (Core Web Vitals) i el que li costa de dades.
//
//   node tests/audit-rendiment.mjs [--pages 12] [--out tests/out]
//
// Es queda deliberadament a mig camí de Lighthouse: no puntua de 0 a 100 ni
// necessita cap dependència nova. Mesura LCP, CLS, FCP, TTFB, feina del fil
// principal i el pes real per tipus de fitxer, i a més comprova les trampes
// que aquest lloc ja ha tingut i que no han de tornar:
//
//   - recursos precarregats que després ningú fa servir (el preload que
//     competeix amb la imatge LCP en comptes d'ajudar-la),
//   - tipografies servides des d'una còpia que no és /fonts/ (cada còpia és
//     una entrada de memòria cau diferent: la mateixa lletra baixada dos cops),
//   - <img> amb srcset el candidat més petit del qual ja és massa gran per a
//     la mida en què es pinta,
//   - imatges de dalt de tot amb loading="lazy" (endarrereix el propi LCP),
//   - <script> que bloquegen la pintada sense defer ni async.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';
import { startServer } from './lib/server.mjs';

const require = createRequire(import.meta.url);
// Playwright viu al node_modules global d'aquest entorn.
const { chromium } = (() => {
  try { return require('playwright'); }
  catch { return require('/opt/node22/lib/node_modules/playwright'); }
})();

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const args = process.argv.slice(2);
const argVal = (name, def) => {
  const i = args.indexOf(`--${name}`);
  return i >= 0 ? args[i + 1] : def;
};
const OUT = path.resolve(ROOT, argVal('out', 'tests/out'));

// Les pàgines que més gent visita i les que més pesen. La resta del lloc surt
// d'aquestes mateixes plantilles: si aquestes van bé, van bé les altres.
const PAGES = (argVal('urls', '') || [
  '/', '/es/', '/en/',
  '/partits/', '/campus/', '/femeni/', '/escoleta/',
  '/blog/', '/patrocinadors/', '/3x3/', '/fotos/', '/club/',
].join(',')).split(',').filter(Boolean);

// Mòbil de gamma mitjana amb 4G corrent: el visitant real del club, no el
// portàtil de qui fa la web.
const XARXA = { download: 1.6 * 1024 * 1024 / 8, upload: 750 * 1024 / 8, latency: 150 };
const CPU = 4;

// Llindars de Core Web Vitals de Google (el que compta com a «bo»).
const LLINDAR = { LCP: 2500, CLS: 0.1, INP: 200, FCP: 1800, TTFB: 800 };

const RECOLLIR = () => {
  window.__cwv = { lcp: 0, cls: 0, fcp: 0, shifts: [], lcpEl: '' };
  try {
    new PerformanceObserver((l) => {
      const e = l.getEntries().at(-1);
      window.__cwv.lcp = e.startTime;
      window.__cwv.lcpEl = e.element
        ? (e.element.tagName.toLowerCase()
           + (e.element.id ? '#' + e.element.id : '')
           + (e.element.currentSrc ? ' ' + e.element.currentSrc.split('/').pop() : ''))
        : (e.url || '').split('/').pop();
    }).observe({ type: 'largest-contentful-paint', buffered: true });

    new PerformanceObserver((l) => {
      for (const e of l.getEntries()) {
        if (e.hadRecentInput) continue;
        window.__cwv.cls += e.value;
        if (e.value > 0.01) {
          window.__cwv.shifts.push({
            valor: +e.value.toFixed(4),
            node: (e.sources || []).map((s) => s.node && s.node.tagName ? s.node.tagName.toLowerCase() : '?').join(','),
          });
        }
      }
    }).observe({ type: 'layout-shift', buffered: true });

    new PerformanceObserver((l) => {
      for (const e of l.getEntries()) if (e.name === 'first-contentful-paint') window.__cwv.fcp = e.startTime;
    }).observe({ type: 'paint', buffered: true });
  } catch (_) { /* navegador sense algun observador: la resta segueix */ }
};

// Comprovacions que es fan sobre el DOM ja pintat, no sobre el codi font:
// el que compta és el que el navegador ha decidit, no el que diu l'HTML.
const TRAMPES = () => {
  const out = { preloadsSenseUsar: [], lazyDaltDeTot: [], srcsetMassaGran: [], scriptsQueBloquegen: [] };
  const demanats = new Set(performance.getEntriesByType('resource').map((r) => r.name));

  for (const l of document.querySelectorAll('link[rel="preload"]')) {
    const href = l.href;
    if (!href || l.hasAttribute('imagesrcset')) continue;
    const usat = [...document.images].some((i) => i.currentSrc === href)
      || [...document.querySelectorAll('link[rel=stylesheet],script[src]')].some((e) => e.href === href || e.src === href)
      || (l.as === 'font' && [...document.fonts].some((f) => f.status === 'loaded'));
    if (!usat && demanats.has(href)) out.preloadsSenseUsar.push(href.replace(location.origin, ''));
  }

  const plec = window.innerHeight;
  for (const img of document.images) {
    const r = img.getBoundingClientRect();
    if (r.top < plec && r.width > 100 && img.loading === 'lazy') {
      out.lazyDaltDeTot.push((img.currentSrc || img.src).replace(location.origin, ''));
    }
    if (img.srcset && r.width > 0) {
      const cands = [...img.srcset.matchAll(/(\d+)w/g)].map((m) => +m[1]);
      const cal = r.width * (window.devicePixelRatio || 1);
      if (cands.length && Math.min(...cands) > cal * 1.6) {
        out.srcsetMassaGran.push({
          fitxer: (img.currentSrc || img.src).replace(location.origin, ''),
          esPinta: Math.round(r.width) + 'px', calen: Math.round(cal) + 'px',
          candidatMesPetit: Math.min(...cands) + 'w',
        });
      }
    }
  }

  for (const s of document.querySelectorAll('head script[src]')) {
    if (!s.defer && !s.async && s.type !== 'module') out.scriptsQueBloquegen.push(s.src.replace(location.origin, ''));
  }
  return out;
};

async function mesura(browser, origin, url) {
  const ctx = await browser.newContext({
    viewport: { width: 390, height: 844 },
    deviceScaleFactor: 2,
    isMobile: true,
    hasTouch: true,
    userAgent: 'Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Mobile Safari/537.36',
  });
  const p = await ctx.newPage();

  const recursos = [];
  const errors = [];
  const fallides = [];
  p.on('pageerror', (e) => errors.push(String(e.message).slice(0, 200)));
  p.on('requestfailed', (r) => fallides.push(r.url().replace(origin, '')));
  p.on('response', async (r) => {
    const req = r.request();
    let mida = 0;
    try { mida = (await r.body()).length; } catch (_) { /* redirecció o cos ja alliberat */ }
    recursos.push({ url: r.url().replace(origin, ''), tipus: req.resourceType(), estat: r.status(), bytes: mida });
  });

  await p.addInitScript(RECOLLIR);

  // Frena xarxa i CPU abans de navegar: si es fa després, la primera pintada
  // ja s'ha produït sense fre i el número no vol dir res.
  const cdp = await ctx.newCDPSession(p);
  await cdp.send('Network.enable');
  await cdp.send('Network.emulateNetworkConditions', { offline: false, latency: XARXA.latency, downloadThroughput: XARXA.download, uploadThroughput: XARXA.upload });
  await cdp.send('Emulation.setCPUThrottlingRate', { rate: CPU });

  const t0 = Date.now();
  const resp = await p.goto(origin + url, { waitUntil: 'load', timeout: 90000 });
  await p.waitForTimeout(3000);   // deixa tancar LCP i els desplaçaments tardans

  const cwv = await p.evaluate(() => window.__cwv);
  const nav = await p.evaluate(() => {
    const n = performance.getEntriesByType('navigation')[0] || {};
    return { ttfb: n.responseStart || 0, domContentLoaded: n.domContentLoadedEventEnd || 0, load: n.loadEventEnd || 0 };
  });
  const fil = await p.evaluate(() => {
    const t = performance.getEntriesByType('longtask') || [];
    return { tasquesLlargues: t.length, msBloquejats: Math.round(t.reduce((a, e) => a + Math.max(0, e.duration - 50), 0)) };
  });
  const trampes = await p.evaluate(TRAMPES);

  const perTipus = {};
  let total = 0;
  for (const r of recursos) {
    if (r.estat >= 400) continue;
    perTipus[r.tipus] = (perTipus[r.tipus] || 0) + r.bytes;
    total += r.bytes;
  }

  await ctx.close();

  const avisos = [];
  if (cwv.lcp > LLINDAR.LCP) avisos.push(`LCP ${Math.round(cwv.lcp)} ms (bo: <${LLINDAR.LCP})`);
  if (cwv.cls > LLINDAR.CLS) avisos.push(`CLS ${cwv.cls.toFixed(3)} (bo: <${LLINDAR.CLS})`);
  if (cwv.fcp > LLINDAR.FCP) avisos.push(`FCP ${Math.round(cwv.fcp)} ms (bo: <${LLINDAR.FCP})`);
  if (total > 1024 * 1024) avisos.push(`${Math.round(total / 1024)} KB per una sola pàgina`);
  for (const x of trampes.preloadsSenseUsar) avisos.push(`preload que ningú fa servir: ${x}`);
  for (const x of trampes.lazyDaltDeTot) avisos.push(`imatge de dalt de tot amb lazy: ${x}`);
  for (const x of trampes.srcsetMassaGran) avisos.push(`${x.fitxer}: es pinta a ${x.esPinta} i el candidat més petit és ${x.candidatMesPetit}`);
  for (const x of trampes.scriptsQueBloquegen) avisos.push(`script que bloqueja la pintada: ${x}`);
  const fontsFora = [...new Set(recursos.filter((r) => r.url.endsWith('.woff2') && !r.url.startsWith('/fonts/')).map((r) => r.url))];
  for (const x of fontsFora) avisos.push(`tipografia fora de /fonts/ (còpia amb memòria cau pròpia): ${x}`);
  for (const x of fallides) avisos.push(`petició fallida: ${x}`);
  for (const x of recursos.filter((r) => r.estat >= 400)) avisos.push(`${x.estat} a ${x.url}`);
  for (const x of errors) avisos.push(`error de JavaScript: ${x}`);

  return {
    url,
    estat: resp ? resp.status() : 0,
    msReals: Date.now() - t0,
    cwv: { LCP: Math.round(cwv.lcp), CLS: +cwv.cls.toFixed(3), FCP: Math.round(cwv.fcp), TTFB: Math.round(nav.ttfb) },
    lcpElement: cwv.lcpEl,
    fil,
    pes: { totalKB: Math.round(total / 1024), perTipusKB: Object.fromEntries(Object.entries(perTipus).map(([k, v]) => [k, Math.round(v / 1024)])) },
    mesPesats: recursos.filter((r) => r.estat < 400).sort((a, b) => b.bytes - a.bytes).slice(0, 5).map((r) => `${Math.round(r.bytes / 1024)} KB ${r.url}`),
    desplacaments: cwv.shifts,
    trampes,
    avisos,
  };
}

async function main() {
  fs.mkdirSync(OUT, { recursive: true });
  const { origin, close } = await startServer(ROOT);
  const browser = await chromium.launch({ args: ['--no-sandbox'] });

  const limit = +argVal('pages', 0) || PAGES.length;
  const llista = PAGES.slice(0, limit);
  console.log(`Rendiment a ${llista.length} pàgines · mòbil 390px, xarxa 4G, CPU ×${CPU}\n`);

  const resultats = [];
  // De una en una a propòsit: dues pestanyes competint pel mateix fre de CPU
  // es falsegen les mesures l'una a l'altra.
  for (const url of llista) {
    const r = await mesura(browser, origin, url);
    resultats.push(r);
    const cwv = r.cwv;
    const marca = r.avisos.length ? '!' : '·';
    console.log(`${marca} ${url.padEnd(18)} LCP ${String(cwv.LCP).padStart(5)} ms  CLS ${String(cwv.CLS).padStart(5)}  FCP ${String(cwv.FCP).padStart(5)} ms  ${String(r.pes.totalKB).padStart(4)} KB   ${r.lcpElement || ''}`);
    for (const a of r.avisos) console.log(`      ${a}`);
  }

  await browser.close();
  await close();

  const ambAvisos = resultats.filter((r) => r.avisos.length).length;
  const resum = {
    generat: new Date().toISOString(),
    condicions: { amplada: 390, dpr: 2, xarxa: '4G (1,6 Mbps, 150 ms)', cpu: `×${CPU}` },
    llindars: LLINDAR,
    pagines: resultats.length,
    ambAvisos,
    mitjanes: {
      LCP: Math.round(resultats.reduce((a, r) => a + r.cwv.LCP, 0) / resultats.length),
      CLS: +(resultats.reduce((a, r) => a + r.cwv.CLS, 0) / resultats.length).toFixed(3),
      FCP: Math.round(resultats.reduce((a, r) => a + r.cwv.FCP, 0) / resultats.length),
      pesKB: Math.round(resultats.reduce((a, r) => a + r.pes.totalKB, 0) / resultats.length),
    },
    resultats,
  };
  fs.writeFileSync(path.join(OUT, 'rendiment.json'), JSON.stringify(resum, null, 1));
  console.log(`\nMitjanes: LCP ${resum.mitjanes.LCP} ms · CLS ${resum.mitjanes.CLS} · FCP ${resum.mitjanes.FCP} ms · ${resum.mitjanes.pesKB} KB`);
  console.log(`${ambAvisos} de ${resultats.length} pàgines amb avisos`);
  console.log(`Desat a ${path.relative(ROOT, path.join(OUT, 'rendiment.json'))}`);
}

main().catch((e) => { console.error(e); process.exit(1); });
