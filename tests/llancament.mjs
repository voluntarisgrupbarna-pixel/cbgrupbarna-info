// El porter del llançament: una sola ordre, un sol veredicte.
//
//   node tests/llancament.mjs                 # tot (uns 20 min: obre el navegador)
//   node tests/llancament.mjs --rapid         # sense navegador (uns 2 min)
//   node tests/llancament.mjs --md tests/out/LLANCAMENT.md
//
// La resta de la bateria respon «què hi ha malament». Això respon una sola
// pregunta, la que es fa el dia abans de publicar: **es pot treure a fora o
// no?** I la respon amb un sí o un no, no amb 200 avisos i una decisió que
// algú s'ha de menjar a les onze de la nit.
//
// La diferència entre el que atura un llançament i el que no és una decisió
// presa aquí i escrita a BLOQUEIGS, no un criteri que canvia cada vegada.
// Un títol de 70 caràcters no atura res: és una pàgina que sortirà una mica
// pitjor a Google. Un formulari que no envia les dades enlloc, una foto que no
// existeix o un <script> amb una cometa de més sí que ho aturen: són coses que
// una persona veu el primer dia, i que fan que no torni.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { execFileSync } from 'node:child_process';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const OUT = path.join(ROOT, 'tests/out');
const args = process.argv.slice(2);
const RAPID = args.includes('--rapid');
// A CI el repositori es baixa sense imatges ni vídeos: es passa avall perquè la
// comprovació d'actius no els doni per absents.
const SENSE_BINARIS = args.includes('--sense-binaris');
const mdPath = args.includes('--md') ? args[args.indexOf('--md') + 1] : null;

/* ------------------------------------------------------------------
   Què atura un llançament
   ------------------------------------------------------------------ */
const BLOQUEIGS = {
  // De l'auditoria de preparació: tot el que hi surt com a error ja s'ha
  // triat pensant en el dia de publicar.
  llancament: () => true,

  // De l'SEO/GEO, només el que trenca alguna cosa de debò. Els avisos de
  // llargada de títol i companyia es llegeixen després, amb calma.
  seo: new Set([
    'enllaç-trencat', 'redireccio-trencada', 'redireccio-sense-canonical',
    'sitemap-404', 'llms-404', 'encoding', 'doctype', 'lang', 'charset',
    'viewport', 'zoom', 'canonical', 'canonical-relatiu', 'og-image-relativa',
    'title', 'idioma-divergent', 'hreflang-mort',
  ]),
};

const passos = [];
const registra = (nom, ok, detall, bloquejants = []) =>
  passos.push({ nom, ok, detall, bloquejants });

const executa = (nom, ordre, arg) => {
  process.stdout.write(`· ${nom}… `);
  try {
    const sortida = execFileSync(ordre, arg, { cwd: ROOT, encoding: 'utf8', stdio: 'pipe', maxBuffer: 256 * 1024 * 1024 });
    console.log('fet');
    return { codi: 0, sortida };
  } catch (e) {
    console.log('amb feina');
    return { codi: e.status ?? 1, sortida: (e.stdout || '') + (e.stderr || '') };
  }
};

const llegeix = (f) => {
  const p = path.join(OUT, f);
  return fs.existsSync(p) ? JSON.parse(fs.readFileSync(p, 'utf8')) : null;
};

console.log('\nBateria de llançament · cbgrupbarna.info');
console.log(RAPID ? '(mode ràpid: sense navegador)\n' : '(bateria sencera; el pas del navegador triga)\n');

/* ------------------------------------------------------------------
   1 · Preparació per publicar
   ------------------------------------------------------------------ */
executa('preparació per publicar', process.execPath, ['tests/audit-llancament.mjs', ...(SENSE_BINARIS ? ['--sense-binaris'] : [])]);
{
  const d = llegeix('llancament.json');
  const errors = (d?.troballes || []).filter((t) => t.nivell === 'error');
  const avisos = (d?.troballes || []).filter((t) => t.nivell === 'avís');
  registra('Preparació per publicar', errors.length === 0,
    `${errors.length} errors · ${avisos.length} avisos`,
    errors.map((t) => `${t.bloc} · ${t.msg}${t.pagina ? ` (${t.pagina})` : t.fitxer ? ` (${t.fitxer})` : ''}`));
}

/* ------------------------------------------------------------------
   2 · SEO i GEO
   ------------------------------------------------------------------ */
executa('SEO i GEO', process.execPath, ['tests/audit-seo-geo.mjs']);
{
  const d = llegeix('seo-geo.json');
  const totes = [];
  const recull = (o) => {
    if (!o) return;
    if (Array.isArray(o)) return o.forEach(recull);
    if (typeof o === 'object') {
      if (o.level && o.msg) totes.push(o);
      else Object.values(o).forEach(recull);
    }
  };
  recull(d);
  const errors = totes.filter((x) => x.level === 'error');
  const bloquegen = errors.filter((x) => BLOQUEIGS.seo.has(x.code));
  registra('SEO i GEO', bloquegen.length === 0,
    `${errors.length} errors (${bloquegen.length} bloquegen) · ${totes.filter((x) => x.level === 'avís').length} avisos`,
    bloquegen.map((x) => `${x.code} · ${x.msg}`));
}

/* ------------------------------------------------------------------
   3 · El cercador
   ------------------------------------------------------------------ */
{
  const m = executa('cercador · casos que no s\'han de trencar', process.execPath, ['tests/cerca/prova-motor.mjs']);
  const c = executa('cercador · consultes reals', process.execPath, ['tests/cerca/prova-contingut.mjs']);
  const resum = (s) => (s.match(/\d+ bé · \d+ malament/) || [''])[0];
  registra('Cercador', m.codi === 0 && c.codi === 0,
    `motor: ${resum(m.sortida)} · contingut: ${resum(c.sortida)}`,
    m.codi === 0 ? [] : (m.sortida.match(/^\s*FALLA.*$/gm) || ['el motor de cerca falla']).map((s) => s.trim()));
}

/* ------------------------------------------------------------------
   4 · Els tres idiomes van junts
   ------------------------------------------------------------------ */
{
  const r = executa('paritat dels tres idiomes', 'python3', ['scripts/i18n-paritat.py', '--tot']);
  registra('Els tres idiomes', r.codi === 0,
    r.sortida.trim().split('\n').pop() || '',
    r.codi === 0 ? [] : r.sortida.trim().split('\n').slice(-8));
}

/* ------------------------------------------------------------------
   5 · Com es veu de debò (només a la bateria sencera)
   ------------------------------------------------------------------ */
if (!RAPID) {
  executa('renderitzat real a 5 amplades', process.execPath, ['tests/audit-browser.mjs']);
  const d = llegeix('browser.json');
  const publica = (r) => !/premidonaesport|admin|\/print\//.test(r.page || '');
  const rs = (d?.results || []).filter(publica);
  const problema = [];
  const vistos = new Set();
  const anota = (s) => { if (!vistos.has(s)) { vistos.add(s); problema.push(s); } };
  for (const r of rs) {
    if (r.status && r.status !== 200) anota(`${r.page} respon ${r.status}`);
    if (r.overflow) anota(`${r.page} es desborda de banda a banda a ${r.width}px`);
    for (const c of r.console || []) {
      // Els ERR_FAILED són el tall de trànsit extern que fa la pròpia prova.
      if (c.type === 'pageerror') anota(`${r.page} · el JavaScript peta: ${c.text}`);
    }
    for (const f of r.failed || []) {
      if (!/^https?:/.test(f.url)) anota(`${r.page} demana ${f.url} i rep ${f.status}`);
    }
    // `images` ve per calaixos (`broken`, `upscaled`, `noAlt`…). Del de les
    // trencades només compten les pròpies: la prova talla el trànsit extern a
    // posta, i per tant tota imatge de fora hi surt com a trencada encara que
    // funcioni. Que n'hi hagi és una altra conversa —90 fotos servides des de
    // Google Drive—, però no és un defecte del lloc que aturi una publicació.
    for (const im of (r.images || {}).broken || []) {
      if (!/^(https?:)?\/\//.test(im.src || '')) anota(`${r.page} · imatge trencada: ${im.src}`);
    }
  }
  registra('Com es veu de debò', problema.length === 0,
    `${rs.length} càrregues a 5 amplades`, problema.slice(0, 20));
} else {
  registra('Com es veu de debò', true, 'omès (--rapid)', []);
}

/* ------------------------------------------------------------------
   Veredicte
   ------------------------------------------------------------------ */
const bloquejants = passos.flatMap((p) => p.bloquejants);
const apte = bloquejants.length === 0;

const linies = [];
const diu = (s = '') => { linies.push(s); console.log(s); };

diu();
diu('┌' + '─'.repeat(62) + '┐');
diu('│ ' + (apte
  ? 'APTE PER PUBLICAR · cap bloqueig obert'.padEnd(60)
  : `NO APTE · ${bloquejants.length} bloqueig${bloquejants.length === 1 ? '' : 's'} per resoldre`.padEnd(60)) + ' │');
diu('└' + '─'.repeat(62) + '┘');
diu();
for (const p of passos) {
  diu(`  ${p.ok ? '✓' : '✗'}  ${p.nom.padEnd(26)} ${p.detall}`);
}
if (!apte) {
  diu();
  diu('Cal resoldre abans de publicar:');
  for (const b of bloquejants) diu(`  · ${b}`);
}
diu();
diu('Els avisos no bloquegen. Es llegeixen amb `node tests/report.mjs`.');

if (mdPath) {
  const md = [
    '# Bateria de llançament · cbgrupbarna.info',
    '',
    `**${apte ? 'APTE PER PUBLICAR' : `NO APTE · ${bloquejants.length} bloquejos`}** · ${new Date().toLocaleString('ca-ES')}`,
    '',
    '| Comprovació | Estat | Resultat |',
    '|---|---|---|',
    ...passos.map((p) => `| ${p.nom} | ${p.ok ? '✓' : '✗'} | ${p.detall} |`),
    '',
    ...(apte ? ['Cap bloqueig obert.'] : ['## Cal resoldre abans de publicar', '', ...bloquejants.map((b) => `- ${b}`)]),
    '',
  ].join('\n');
  fs.mkdirSync(path.dirname(path.resolve(ROOT, mdPath)), { recursive: true });
  fs.writeFileSync(path.resolve(ROOT, mdPath), md);
  console.log(`Informe desat a ${mdPath}`);
}

process.exit(apte ? 0 : 1);
