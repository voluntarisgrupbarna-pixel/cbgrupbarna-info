// Passada axe-core (WCAG 2.x AA + bones pràctiques) sobre totes les pàgines
// del lloc, servit com a GitHub Pages i amb el trànsit extern tallat.
//
//   node tests/axe.mjs [--out tests/out]
//
// El motor és axe-core (Deque, MPL-2.0), vendoritzat a tests/lib/axe.min.js
// (v4.13.0) perquè la prova no necessiti instal·lar res. Es carrega cada
// pàgina amb `prefers-reduced-motion: reduce` i 400 ms de marge: sense això,
// les entrades amb `fadeIn` esglaonat es capturen a mig camí i el contrast
// surt barrejat amb el fons (fals positiu vist a /fotos/ el 26/08/2026).
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
const AXE_SRC = fs.readFileSync(path.join(ROOT, 'tests/lib/axe.min.js'), 'utf8');
const args = process.argv.slice(2);
const argVal = (name, def) => {
  const i = args.indexOf(`--${name}`);
  return i >= 0 ? args[i + 1] : def;
};
const OUT = path.resolve(ROOT, argVal('out', 'tests/out'));

const SKIP = [/^\.git\//, /^node_modules\//, /^tests\//, /^\.github\//, /^\.claude\//];

function findPages() {
  const pages = [];
  const walk = (dir) => {
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      const abs = path.join(dir, entry.name);
      const rel = path.relative(ROOT, abs);
      if (SKIP.some((re) => re.test(rel + (entry.isDirectory() ? '/' : '')))) continue;
      if (entry.isDirectory()) walk(abs);
      else if (entry.name.endsWith('.html')) {
        pages.push({ file: rel, url: '/' + rel.replace(/index\.html$/, '') });
      }
    }
  };
  walk(ROOT);
  return pages.sort((a, b) => a.url.localeCompare(b.url));
}

const { origin, close } = await startServer(ROOT);
const browser = await chromium.launch();
const context = await browser.newContext({ viewport: { width: 1280, height: 900 }, reducedMotion: 'reduce' });
await context.route(/^https?:\/\/(?!127\.0\.0\.1|localhost)/, (r) => r.abort());

const pages = findPages();
const results = [];
const CONCURRENCY = 5;
let i = 0;

async function worker() {
  const page = await context.newPage();
  while (i < pages.length) {
    const item = pages[i++];
    try {
      await page.goto(origin + item.url, { waitUntil: 'load', timeout: 15000 });
    } catch (e) {
      results.push({ ...item, error: String(e).slice(0, 120) });
      continue;
    }
    try {
      // Les redireccions noindex marxen soles: no s'auditen.
      const moved = await page.title().then((t) => /has moved|s'ha mogut|se ha movido/i.test(t)).catch(() => false);
      if (moved) continue;
      await page.waitForTimeout(400);
      await page.evaluate(AXE_SRC);
      const res = await page.evaluate(async () => {
        const r = await axe.run(document, {
          runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa', 'best-practice'] },
          resultTypes: ['violations'],
        });
        return r.violations.map((v) => ({
          id: v.id, impact: v.impact, help: v.help, tags: v.tags.filter((t) => t.startsWith('wcag')),
          nodes: v.nodes.slice(0, 5).map((n) => n.target.join(' ')),
          data: v.id === 'color-contrast' ? v.nodes.slice(0, 5).map((n) => n.any[0]?.data) : undefined,
          count: v.nodes.length,
        }));
      });
      if (res.length) results.push({ ...item, violations: res });
    } catch (e) {
      results.push({ ...item, error: String(e).slice(0, 120) });
    }
  }
  await page.close();
}

await Promise.all(Array.from({ length: CONCURRENCY }, worker));
await browser.close();
await close();

fs.mkdirSync(OUT, { recursive: true });
fs.writeFileSync(path.join(OUT, 'axe.json'),
  JSON.stringify({ generated: new Date().toISOString(), engine: 'axe-core', pagesTotal: pages.length, pagesWithIssues: results.length, results }, null, 1));
console.log(`${pages.length} pàgines · ${results.length} amb violacions o errors`);
console.log(`Desat a ${path.relative(ROOT, path.join(OUT, 'axe.json'))}`);
