// Captures de pantalla per mirar-s'ho amb els ulls, no només amb números.
//
//   node tests/screenshots.mjs [--pages /,/escoleta/,/partits/] [--out tests/out/captures]
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
const OUT = path.resolve(ROOT, argVal('out', 'tests/out/captures'));
const PAGES = argVal('pages', '/,/escoleta/,/partits/,/basquet-femeni/,/campus/,/patrocinadors/,/partners-mapa/,/premidonaesport/').split(',');
const FULL = args.includes('--full');

const VIEWPORTS = [
  { name: 'mobil-360', width: 360, height: 740, dpr: 2, mobile: true },
  { name: 'tauleta-820', width: 820, height: 1180, dpr: 2, mobile: true },
  { name: 'escriptori-1440', width: 1440, height: 900, dpr: 1, mobile: false },
];

const { origin, close } = await startServer(ROOT);
fs.mkdirSync(OUT, { recursive: true });
const browser = await chromium.launch();

for (const vp of VIEWPORTS) {
  const ctx = await browser.newContext({
    viewport: { width: vp.width, height: vp.height },
    deviceScaleFactor: vp.dpr, isMobile: vp.mobile, hasTouch: vp.mobile,
    locale: 'ca-ES', reducedMotion: 'reduce',
  });
  for (const url of PAGES) {
    const p = await ctx.newPage();
    await p.route('**', (r) => (r.request().url().startsWith(origin) ? r.continue() : r.abort()));
    try {
      // El lloc porta scroll-behavior: smooth, i amb això tornar a dalt és una
      // animació que la captura enxampa a mig camí. L'anul·lem.
      await p.addStyleTag({ content: 'html,body{scroll-behavior:auto !important}' });
      await p.goto(origin + url, { waitUntil: 'load', timeout: 30000 });
      await p.addStyleTag({ content: 'html,body{scroll-behavior:auto !important}' });
      await p.waitForTimeout(700);
      // Les entrades animades es disparen en fer scroll: les despertem totes.
      await p.evaluate(async () => {
        const h = document.body.scrollHeight;
        for (let y = 0; y < h; y += 400) { window.scrollTo(0, y); await new Promise((r) => setTimeout(r, 40)); }
      });
      await p.evaluate(() => window.scrollTo({ top: 0, behavior: 'instant' }));
      await p.waitForFunction(() => window.scrollY === 0, null, { timeout: 5000 }).catch(() => {});
      await p.waitForTimeout(500);
      const name = (url === '/' ? 'portada' : url.replace(/^\/|\/$/g, '').replace(/\//g, '-'));
      await p.screenshot({ path: path.join(OUT, `${name}__${vp.name}.png`), fullPage: FULL });
      console.log(`  ${name} · ${vp.name}`);
    } catch (e) {
      console.log(`  ERROR ${url} · ${vp.name}: ${String(e).slice(0, 100)}`);
    }
    await p.close();
  }
  await ctx.close();
}

await browser.close();
await close();
console.log(`\nCaptures a ${path.relative(ROOT, OUT)}`);
