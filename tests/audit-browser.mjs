// Bateria de proves de navegador: recorre totes les pàgines del lloc a
// diverses amplades i mira com es comporten de debò, no com diu el codi.
//
//   node tests/audit-browser.mjs [--pages 20] [--out tests/out]
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';
import { startServer } from './lib/server.mjs';
import { collect } from './lib/in-page.mjs';

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
const LIMIT = +argVal('pages', 0) || Infinity;
const SKIP_N = +argVal('skip', 0) || 0;
const CONCURRENCY = +argVal('workers', 5);
// Filtre d'amplades: `--viewports mobil,tauleta`. Serveix per repassar només
// mòbil i tauleta sense pagar les càrregues d'escriptori, i per trossejar la
// tanda sencera quan la memòria de l'entorn no dona per a 500 pàgines de cop.
const VP_FILTER = (argVal('viewports', '') || '')
  .split(',').map((s) => s.trim().toLowerCase()).filter(Boolean);

const VIEWPORTS = [
  { name: 'mòbil', width: 360, height: 740, dpr: 3, mobile: true },
  { name: 'mòbil-gran', width: 430, height: 932, dpr: 3, mobile: true },
  { name: 'tauleta', width: 820, height: 1180, dpr: 2, mobile: true },
  { name: 'tauleta-apaisada', width: 1024, height: 768, dpr: 2, mobile: true },
  { name: 'escriptori', width: 1440, height: 900, dpr: 2, mobile: false },
];

// Carpetes que no formen part del lloc públic.
const SKIP = [/^\.git\//, /^node_modules\//, /^tests\//, /^\.github\//];

function findPages() {
  const pages = [];
  const walk = (dir) => {
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      const abs = path.join(dir, entry.name);
      const rel = path.relative(ROOT, abs);
      if (SKIP.some((re) => re.test(rel + (entry.isDirectory() ? '/' : '')))) continue;
      if (entry.isDirectory()) walk(abs);
      else if (entry.name.endsWith('.html')) {
        const url = '/' + rel.replace(/index\.html$/, '').replace(/\\/g, '/');
        pages.push({ file: rel, url });
      }
    }
  };
  walk(ROOT);
  return pages.sort((a, b) => a.url.localeCompare(b.url));
}

const OPTS = { minTap: 44, minFont: 12, contrastText: 4.5, contrastLarge: 3 };

async function auditOne(context, origin, page, viewport) {
  const p = await context.newPage();
  const console_ = [];
  const failed = [];
  const thirdParty = new Set();
  const bytes = { total: 0, byType: {} };

  // Aquest entorn no té sortida a internet i les peticions externes es
  // quedarien penjades fins al temps d'espera. Les tallem i les anotem:
  // la llista de dominis de tercers és, ella mateixa, un resultat.
  await p.route('**', (route) => {
    const u = route.request().url();
    if (u.startsWith(origin) || u.startsWith('data:') || u.startsWith('blob:')) return route.continue();
    try { thirdParty.add(new URL(u).host); } catch { /* ignora */ }
    return route.abort();
  });

  p.on('console', (m) => {
    if (m.type() === 'error' || m.type() === 'warning') {
      console_.push({ type: m.type(), text: m.text().slice(0, 200) });
    }
  });
  p.on('pageerror', (e) => console_.push({ type: 'pageerror', text: String(e).slice(0, 200) }));
  p.on('requestfailed', (r) => {
    const u = r.url();
    if (!u.startsWith(origin)) return; // ja el tallem nosaltres a propòsit
    const reason = r.failure()?.errorText || '';
    // Un <video> avorta el seu propi flux quan tanquem la pestanya: no és
    // que el fitxer falti, i comptar-ho seria cridar el llop.
    if (reason === 'net::ERR_ABORTED') return;
    failed.push({ url: u.replace(origin, ''), reason });
  });
  p.on('response', async (r) => {
    if (!r.url().startsWith(origin)) return;
    if (r.status() >= 400) failed.push({ url: r.url().replace(origin, ''), status: r.status() });
    const len = +(r.headers()['content-length'] || 0);
    bytes.total += len;
    const type = (r.headers()['content-type'] || '').split('/')[0] || 'altre';
    bytes.byType[type] = (bytes.byType[type] || 0) + len;
  });

  const t0 = Date.now();
  let nav = null;
  try {
    nav = await p.goto(origin + page.url, { waitUntil: 'load', timeout: 30000 });
    // Deixem que arrenquin animacions, lazy-load i scripts diferits.
    await p.waitForTimeout(400);
    await p.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
    await p.waitForTimeout(300);
    await p.evaluate(() => window.scrollTo(0, 0));
    await p.waitForTimeout(150);
  } catch (e) {
    await p.close();
    return { page: page.url, viewport: viewport.name, error: String(e).slice(0, 200) };
  }
  const loadMs = Date.now() - t0;

  let data;
  try {
    data = await p.evaluate(collect, OPTS);
  } catch (e) {
    await p.close();
    return { page: page.url, viewport: viewport.name, error: 'collect: ' + String(e).slice(0, 200) };
  }

  // ---------- focus visible, tabulant de debò ----------
  // Chromium només aplica :focus-visible si el focus ve del teclat, així que
  // premem Tab en comptes de cridar focus() des de dins de la pàgina.
  const focus = { steps: 0, invisible: [], trapped: false };
  try {
    await p.evaluate(() => { document.body.focus(); window.scrollTo(0, 0); });
    const seen = new Set();
    for (let i = 0; i < 15; i++) {
      const before = await p.evaluate(() => {
        const el = document.activeElement;
        if (!el || el === document.body) return null;
        const cs = getComputedStyle(el);
        return { outline: cs.outlineWidth + cs.outlineStyle, shadow: cs.boxShadow, bd: cs.borderColor, bg: cs.backgroundColor, td: cs.textDecorationLine, color: cs.color };
      });
      await p.keyboard.press('Tab');
      const after = await p.evaluate(() => {
        const el = document.activeElement;
        if (!el || el === document.body) return null;
        const cs = getComputedStyle(el);
        const r = el.getBoundingClientRect();
        const id = el.id ? `#${el.id}` : '';
        const cls = typeof el.className === 'string' && el.className ? '.' + el.className.trim().split(/\s+/).slice(0, 2).join('.') : '';
        const txt = (el.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 30);
        return {
          key: el.tagName.toLowerCase() + id + cls,
          label: el.tagName.toLowerCase() + id + cls + (txt ? ` «${txt}»` : ''),
          offscreen: r.width === 0 && r.height === 0,
          style: { outline: cs.outlineWidth + cs.outlineStyle, shadow: cs.boxShadow, bd: cs.borderColor, bg: cs.backgroundColor, td: cs.textDecorationLine, color: cs.color },
          // Com es veu el mateix element quan NO té el focus.
          rest: null,
        };
      });
      if (!after) break;
      focus.steps++;
      if (seen.has(after.key + focus.steps)) continue;
      seen.add(after.key + focus.steps);

      // Comparem l'element enfocat amb ell mateix en repòs.
      const rest = await p.evaluate(() => {
        const el = document.activeElement;
        if (!el) return null;
        el.setAttribute('data-focus-probe', '1');
        el.blur();
        const cs = getComputedStyle(el);
        const s = { outline: cs.outlineWidth + cs.outlineStyle, shadow: cs.boxShadow, bd: cs.borderColor, bg: cs.backgroundColor, td: cs.textDecorationLine, color: cs.color };
        el.focus({ preventScroll: true });
        el.removeAttribute('data-focus-probe');
        return s;
      });
      if (rest && !after.offscreen) {
        const differs = Object.keys(rest).some((k) => rest[k] !== after.style[k]);
        const hasOutline = parseFloat(after.style.outline) > 0 && !/none/.test(after.style.outline);
        if (!differs && !hasOutline) focus.invisible.push(after.label);
      }
    }
  } catch { /* si la pàgina no deixa tabular, ho diu el nombre de passes */ }

  // El lloc respon al mode fosc del dispositiu?
  let darkMode = null;
  if (!viewport.mobile) {
    const light = await p.evaluate(() => getComputedStyle(document.body).backgroundColor + '|' + getComputedStyle(document.body).color);
    await p.emulateMedia({ colorScheme: 'dark' });
    await p.waitForTimeout(150);
    const dark = await p.evaluate(() => getComputedStyle(document.body).backgroundColor + '|' + getComputedStyle(document.body).color);
    await p.emulateMedia({ colorScheme: 'light' });
    darkMode = { reacts: light !== dark, light, dark };
  }

  await p.close();
  return {
    page: page.url, file: page.file, viewport: viewport.name, width: viewport.width,
    status: nav?.status() ?? 0, loadMs, bytes, console: console_.slice(0, 15),
    failed: failed.slice(0, 15), thirdParty: [...thirdParty], keyboardFocus: focus, darkMode, ...data,
  };
}

// «mòbil-gran» s'ha de poder demanar escrivint «mobil-gran».
const plain = (s) => s.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
const VIEWPORTS_ON = VP_FILTER.length
  ? VIEWPORTS.filter((v) => VP_FILTER.some((f) => plain(v.name) === plain(f)))
  : VIEWPORTS;

async function main() {
  if (!VIEWPORTS_ON.length) {
    console.error(`Cap amplada coincideix amb --viewports. N'hi ha: ${VIEWPORTS.map((v) => v.name).join(', ')}`);
    process.exit(2);
  }
  fs.mkdirSync(OUT, { recursive: true });
  const { origin, close } = await startServer(ROOT);
  const pages = findPages().slice(SKIP_N, SKIP_N + LIMIT);
  const browser = await chromium.launch();

  console.log(`Servint ${ROOT} a ${origin}`);
  console.log(`${pages.length} pàgines × ${VIEWPORTS_ON.length} amplades = ${pages.length * VIEWPORTS_ON.length} càrregues\n`);

  const jobs = [];
  for (const page of pages) for (const vp of VIEWPORTS_ON) jobs.push({ page, vp });

  const results = [];
  let done = 0;
  const contexts = await Promise.all(
    VIEWPORTS_ON.map((vp) => browser.newContext({
      viewport: { width: vp.width, height: vp.height },
      deviceScaleFactor: vp.dpr,
      isMobile: vp.mobile,
      hasTouch: vp.mobile,
      locale: 'ca-ES',
      colorScheme: 'light',
      reducedMotion: 'reduce',
    }))
  );
  const ctxFor = new Map(VIEWPORTS_ON.map((vp, i) => [vp.name, contexts[i]]));

  const queue = jobs.slice();
  const worker = async () => {
    while (queue.length) {
      const job = queue.shift();
      const r = await auditOne(ctxFor.get(job.vp.name), origin, job.page, job.vp);
      results.push(r);
      done++;
      if (done % 25 === 0 || done === jobs.length) {
        process.stdout.write(`\r  ${done}/${jobs.length}`);
      }
    }
  };
  await Promise.all(Array.from({ length: CONCURRENCY }, worker));
  process.stdout.write('\n');

  await browser.close();
  await close();

  fs.writeFileSync(path.join(OUT, 'browser.json'), JSON.stringify({ generated: new Date().toISOString(), viewports: VIEWPORTS_ON, results }, null, 1));
  console.log(`\nDesat a ${path.relative(ROOT, path.join(OUT, 'browser.json'))}`);
}

main().catch((e) => { console.error(e); process.exit(1); });
