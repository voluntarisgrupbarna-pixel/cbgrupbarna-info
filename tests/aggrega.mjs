// Ajunta els `browser.json` d'una tanda trossejada (--skip/--pages) en un de
// sol i en treu el resum per famílies de problema. La tanda sencera del lloc
// no cap en una sola execució: el navegador es queda sense memòria cap a la
// pàgina 250, i per això es parteix.
//
//   node tests/aggrega.mjs tests/out/chunks --out tests/out/browser.json
import fs from 'node:fs';
import path from 'node:path';

const args = process.argv.slice(2);
const dir = args[0] || 'tests/out/chunks';
const outI = args.indexOf('--out');
const out = outI >= 0 ? args[outI + 1] : null;

const results = [];
let viewports = [];
for (const sub of fs.readdirSync(dir).sort()) {
  const f = path.join(dir, sub, 'browser.json');
  if (!fs.existsSync(f)) continue;
  const d = JSON.parse(fs.readFileSync(f, 'utf8'));
  viewports = d.viewports;
  results.push(...d.results);
}
// Una pàgina pot sortir dues vegades si dos trossos se solapen.
const seen = new Set();
const uniq = results.filter((r) => {
  const k = r.page + '|' + r.viewport;
  if (seen.has(k)) return false;
  seen.add(k);
  return true;
});

if (out) {
  fs.mkdirSync(path.dirname(out), { recursive: true });
  fs.writeFileSync(out, JSON.stringify({ generated: new Date().toISOString(), viewports, results: uniq }, null, 1));
}

const pages = new Set(uniq.map((r) => r.page));
console.log(`${pages.size} pàgines · ${uniq.length} càrregues · amplades: ${viewports.map((v) => v.name).join(', ')}\n`);

// Agrupa per causa, no per pàgina: 300 avisos de la mateixa regla de CSS són
// una feina, no tres-centes.
const fam = new Map();
const add = (tipus, clau, r, extra) => {
  const k = tipus + ' :: ' + clau;
  if (!fam.has(k)) fam.set(k, { tipus, clau, pagines: new Set(), amplades: new Set(), mostra: extra });
  const e = fam.get(k);
  e.pagines.add(r.page);
  e.amplades.add(r.viewport);
};

for (const r of uniq) {
  if (r.error) { add('error', r.error.slice(0, 80), r); continue; }
  if (r.overflow) add('desbordament', `${r.overflow.elements[0]?.el?.slice(0, 50) || '?'}`, r, `+${r.overflow.excess}px`);
  for (const t of r.tapTargets || []) add('zona tocable', `${t.el.split('«')[0]} (${t.w}×${t.h})`, r);
  for (const s of r.smallText || []) add('lletra petita', `${s.el.split('«')[0]} ${s.size}px`, r);
  for (const c of r.contrast || []) add('contrast', `${c.el.split('«')[0]} ${c.ratio}:1 (cal ${c.need})`, r);
  for (const o of r.occluded || []) add('element tapat', o.el.split('«')[0], r);
  for (const i of r.images?.broken || []) add('imatge trencada', i.src.slice(0, 60), r);
  for (const i of r.images?.upscaled || []) add('foto ampliada', `${i.src} (${i.natural}px per ${i.css}px@${i.dpr}x)`, r);
  for (const i of r.images?.oversized || []) add('foto sobredimensionada', `${i.src} (${i.natural}px per ${i.css}px)`, r);
  for (const i of r.images?.noAlt || []) add('imatge sense alt', i.src.slice(0, 60), r);
  for (const t of r.tables || []) add('taula que desborda', `${t.el.split('«')[0]} ${t.width}px`, r);
  for (const u of r.unnamed || []) add('control sense nom', `${u.el.split('«')[0]} → ${u.href}`, r);
  for (const d of r.duplicateIds || []) add('id duplicat', `#${d.id} ×${d.count}`, r);
  for (const s of r.headings?.skips || []) add('salt d’encapçalament', `${s.from}→${s.to}`, r);
  for (const f of r.failed || []) add('petició fallida', `${f.url} ${f.status || f.reason || ''}`.slice(0, 70), r);
  for (const k of r.keyboardFocus?.invisible || []) add('focus invisible', k.split('«')[0], r);
  if (r.headings?.h1 !== 1) add('h1', `n=${r.headings?.h1}`, r);
  if (r.viewportMeta && /user-scalable\s*=\s*no|maximum-scale\s*=\s*1/.test(r.viewportMeta)) add('zoom bloquejat', r.viewportMeta.slice(0, 50), r);
  if (!r.landmarks?.main) add('sense <main>', '', r);
}

const rows = [...fam.values()].sort((a, b) => b.pagines.size - a.pagines.size);
const perTipus = new Map();
for (const r of rows) perTipus.set(r.tipus, (perTipus.get(r.tipus) || 0) + r.pagines.size);

console.log('── Per família ──');
for (const [t, n] of [...perTipus.entries()].sort((a, b) => b[1] - a[1])) {
  console.log(`  ${String(n).padStart(5)}  ${t}`);
}
console.log('\n── Causes concretes (pàgines afectades) ──');
for (const r of rows.slice(0, +(process.env.TOP || 60))) {
  console.log(`  ${String(r.pagines.size).padStart(4)}  [${r.tipus}] ${r.clau}${r.mostra ? '  ' + r.mostra : ''}`);
  if (r.pagines.size <= 3) console.log(`         ${[...r.pagines].join(', ')}`);
}
