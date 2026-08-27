/* Proves d'ús i navegació del cercador, amb un navegador de debò.
   node tests/cerca/prova-ux.mjs            (cal un servidor a :8899)
   node tests/cerca/prova-ux.mjs http://…   per provar-lo contra un altre lloc

   Això NO prova què troba la cerca —d'això se n'ocupa prova-motor.mjs— sinó
   si es pot fer servir: teclat, focus, lector de pantalla, mòbil, tornar
   enrere i què passa sense JavaScript. */
import { chromium } from 'playwright';

const BASE = process.argv[2] || 'http://localhost:8899';
let ok = 0, ko = 0;
const falles = [];

function comprova(nom, condicio, detall = '') {
  if (condicio) { ok++; console.log('  ok    ' + nom); }
  else { ko++; falles.push(nom + (detall ? ' — ' + detall : '')); console.log('  FALLA ' + nom + (detall ? ' — ' + detall : '')); }
}

const navegador = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });

async function nova(opcions = {}) {
  const ctx = await navegador.newContext({ viewport: { width: 1280, height: 900 }, ...opcions });
  const p = await ctx.newPage();
  p.on('pageerror', e => { ko++; falles.push('error de JS: ' + e.message); });
  return p;
}

async function obreCapa(p) {
  await p.keyboard.press('Control+k');
  await p.waitForSelector('.cerca-capa:not([hidden])', { timeout: 3000 });
}

// ── 1 · Com s'obre ────────────────────────────────────────────────────────
console.log('\n1 · Com s\'obre');
{
  const p = await nova();
  await p.goto(BASE + '/faq/', { waitUntil: 'networkidle' });

  comprova('la lupa surt a la capçalera', await p.isVisible('[data-cerca-obrir]'));

  await p.click('[data-cerca-obrir]');
  comprova('la lupa obre la cerca', await p.isVisible('.cerca-capa .cerca-input'));
  await p.keyboard.press('Escape');

  await obreCapa(p);
  comprova('Ctrl+K obre la cerca', await p.isVisible('.cerca-capa .cerca-input'));
  await p.keyboard.press('Escape');

  await p.press('body', '/');
  await p.waitForTimeout(150);
  comprova('la tecla / obre la cerca', await p.isVisible('.cerca-capa .cerca-input'));
  await p.keyboard.press('Escape');

  comprova('el focus entra al camp en obrir',
    await (async () => { await obreCapa(p); await p.waitForTimeout(120);
      return p.evaluate(() => document.activeElement?.classList.contains('cerca-input')); })());
  await p.keyboard.press('Escape');
  await p.close();
}

// ── 2 · La tecla / no ha de molestar qui escriu ───────────────────────────
console.log('\n2 · La tecla / mentre s\'escriu');
{
  const p = await nova();
  await p.goto(BASE + '/portes-obertes/', { waitUntil: 'networkidle' });
  await p.click('#po-nom');
  await p.keyboard.type('Mar/ta');
  comprova('escrivint «/» en un formulari no s\'obre la cerca',
    !(await p.isVisible('.cerca-capa .cerca-input')));
  comprova('la «/» s\'escriu al camp',
    (await p.inputValue('#po-nom')).includes('/'), await p.inputValue('#po-nom'));
  await p.close();
}

// ── 3 · Teclat dins de la cerca ───────────────────────────────────────────
console.log('\n3 · Teclat dins de la cerca');
{
  const p = await nova();
  await p.goto(BASE + '/faq/', { waitUntil: 'networkidle' });
  await obreCapa(p);
  await p.fill('.cerca-input', 'escoleta');
  await p.waitForSelector('.cerca-llista a', { timeout: 3000 });

  comprova('el primer element navegable surt marcat',
    await p.evaluate(() =>
      document.querySelector('[data-cerca-r]')?.classList.contains('es-actiu')));

  await p.keyboard.press('ArrowDown');
  comprova('la fletxa avall mou la selecció',
    await p.evaluate(() => {
      const a = [...document.querySelectorAll('[data-cerca-r]')];
      return a.findIndex(x => x.classList.contains('es-actiu')) === 1;
    }));

  await p.keyboard.press('ArrowUp');
  await p.keyboard.press('ArrowUp');
  comprova('la fletxa amunt dona la volta pel final',
    await p.evaluate(() => {
      const a = [...document.querySelectorAll('[data-cerca-r]')];
      return a.findIndex(x => x.classList.contains('es-actiu')) === a.length - 1;
    }));

  comprova('el recompte de resultats s\'anuncia al lector de pantalla (role="status")',
    await p.evaluate(() => {
      const sr = document.querySelector('.cerca-sr');
      return sr?.getAttribute('role') === 'status' && /\d/.test(sr.textContent);
    }));

  // Enter obre el resultat seleccionat
  await p.keyboard.press('ArrowDown');
  const desti = await p.evaluate(() =>
    document.querySelector('[data-cerca-r].es-actiu')?.getAttribute('href'));
  await Promise.all([p.waitForURL('**' + desti, { timeout: 5000 }).catch(() => {}), p.keyboard.press('Enter')]);
  comprova('Enter obre el resultat seleccionat',
    new URL(p.url()).pathname === desti, p.url() + ' vs ' + desti);
  await p.close();
}

// ── 4 · Tancar i tornar ───────────────────────────────────────────────────
console.log('\n4 · Tancar');
{
  const p = await nova();
  await p.goto(BASE + '/faq/', { waitUntil: 'networkidle' });
  await p.click('[data-cerca-obrir]');
  await p.waitForSelector('.cerca-capa:not([hidden])');
  comprova('amb la cerca oberta la pàgina de sota no es desplaça',
    await p.evaluate(() => getComputedStyle(document.documentElement).overflow === 'hidden'));

  await p.keyboard.press('Escape');
  comprova('Escape la tanca', await p.isHidden('.cerca-capa'));
  comprova('el focus torna a la lupa',
    await p.evaluate(() => document.activeElement?.hasAttribute('data-cerca-obrir')));
  comprova('la pàgina torna a desplaçar-se',
    await p.evaluate(() => getComputedStyle(document.documentElement).overflow !== 'hidden'));

  await p.click('[data-cerca-obrir]');
  await p.waitForSelector('.cerca-capa:not([hidden])');
  await p.click('.cerca-fons', { position: { x: 20, y: 20 } });
  comprova('clicant a fora es tanca', await p.isHidden('.cerca-capa'));

  await p.click('[data-cerca-obrir]');
  await p.waitForSelector('.cerca-capa:not([hidden])');
  await p.click('.cerca-tanca');
  comprova('la creu la tanca', await p.isHidden('.cerca-capa'));
  await p.close();
}

// ── 5 · El focus no ha de fugir de la finestra ────────────────────────────
console.log('\n5 · El focus queda dins de la finestra');
{
  const p = await nova();
  await p.goto(BASE + '/faq/', { waitUntil: 'networkidle' });
  await obreCapa(p);
  await p.fill('.cerca-input', 'campus');
  await p.waitForSelector('.cerca-llista a');
  let fora = null;
  for (let i = 0; i < 25; i++) {
    await p.keyboard.press('Tab');
    const on = await p.evaluate(() => {
      const a = document.activeElement;
      return { dins: !!a?.closest('.cerca-capa'), que: a?.tagName + '.' + (a?.className || '') };
    });
    if (!on.dins) { fora = 'al pas ' + (i + 1) + ' el focus ha anat a ' + on.que; break; }
  }
  comprova('el tabulador no surt de la finestra de cerca', fora === null, fora || '');
  await p.close();
}

// ── 6 · Cerques recents ───────────────────────────────────────────────────
console.log('\n6 · Cerques recents');
{
  const p = await nova();
  await p.goto(BASE + '/faq/', { waitUntil: 'networkidle' });
  await obreCapa(p);
  await p.fill('.cerca-input', 'campus');
  await p.waitForSelector('.cerca-llista a');
  await p.click('.cerca-llista a');
  await p.waitForLoadState('domcontentloaded');
  await obreCapa(p);
  await p.waitForTimeout(200);
  comprova('la cerca feta queda a «les teves darreres cerques»',
    await p.isVisible('[data-recent="campus"]'));
  await p.click('[data-recent="campus"]');
  await p.waitForTimeout(300);
  comprova('clicant-la, torna a cercar', (await p.inputValue('.cerca-input')) === 'campus');
  await p.fill('.cerca-input', '');          // tornar a l'estat buit
  await p.waitForSelector('.cerca-esborra-recents');
  await p.click('.cerca-esborra-recents');
  await p.waitForTimeout(150);
  comprova('«esborrar» les treu', !(await p.isVisible('[data-recent]')));
  await p.close();
}

// ── 7 · Mòbil ─────────────────────────────────────────────────────────────
console.log('\n7 · Mòbil (390 px, tàctil)');
{
  const p = await nova({ viewport: { width: 390, height: 780 }, hasTouch: true, isMobile: true });
  await p.goto(BASE + '/faq/', { waitUntil: 'networkidle' });
  comprova('la lupa hi és', await p.isVisible('[data-cerca-obrir]'));
  const mida = await p.evaluate(() => {
    const b = document.querySelector('[data-cerca-obrir]').getBoundingClientRect();
    return Math.min(b.width, b.height);
  });
  comprova('la lupa és prou gran per al dit (≥ 32 px)', mida >= 32, mida + ' px');
  await p.tap('[data-cerca-obrir]');
  await p.waitForSelector('.cerca-capa:not([hidden])');
  const lletra = await p.evaluate(() =>
    parseFloat(getComputedStyle(document.querySelector('.cerca-input')).fontSize));
  comprova('el camp té 16 px o més (si no, l\'iPhone fa zoom)', lletra >= 16, lletra + ' px');
  await p.fill('.cerca-input', 'horaris');
  await p.waitForSelector('.cerca-llista a');
  comprova('a mòbil no desborda',
    !(await p.evaluate(() => document.documentElement.scrollWidth > window.innerWidth + 1)));
  const alt = await p.evaluate(() => {
    const c = document.querySelector('.cerca-panell').getBoundingClientRect();
    return c.bottom <= window.innerHeight + 1;
  });
  comprova('la finestra cap a la pantalla', alt);
  await p.close();
}

// ── 8 · Sense JavaScript ──────────────────────────────────────────────────
console.log('\n8 · Sense JavaScript');
{
  const p = await nova({ javaScriptEnabled: false });
  await p.goto(BASE + '/cerca/', { waitUntil: 'domcontentloaded' });
  comprova('/cerca/ ensenya igualment el mapa del web',
    (await p.$$eval('.cerca-mapa a', a => a.length)) > 10);
  comprova('sense JS no hi ha cap lupa que no faci res',
    !(await p.isVisible('[data-cerca-obrir]')));
  await p.close();
}

// ── 9 · La pàgina /cerca/ i l'adreça ──────────────────────────────────────
console.log('\n9 · La pàgina /cerca/');
{
  const p = await nova();
  // S'hi arriba des d'una altra pàgina, com hi arribaria qualsevol: així es
  // pot comprovar de debò què fa el botó de tornar enrere.
  await p.goto(BASE + '/faq/', { waitUntil: 'domcontentloaded' });
  await p.goto(BASE + '/cerca/?q=quant+costa', { waitUntil: 'networkidle' });
  comprova('?q= arriba escrit al camp', (await p.inputValue('.cerca-input')) === 'quant costa');
  await p.waitForSelector('.cerca-faq, .cerca-llista a', { timeout: 4000 });
  comprova('i ja ensenya la resposta', await p.isVisible('.cerca-faq'));
  await p.fill('.cerca-input', 'campus de nadal');
  await p.waitForTimeout(400);
  comprova('escrivint, l\'adreça s\'actualitza (es pot compartir)',
    p.url().includes('q=campus+de+nadal'), p.url());
  // Escriure fa servir replaceState a posta: si cada lletra deixés una
  // entrada a l'historial, per sortir de la cerca caldrien vint clics al
  // botó de tornar enrere. Amb replaceState, un sol clic torna d'on venies.
  await p.goBack();
  await p.waitForLoadState('domcontentloaded');
  comprova('tornar enrere porta a la pàgina d\'on venies, no a mitja cerca',
    new URL(p.url()).pathname === '/faq/', p.url());
  await p.close();
}

// ── 10 · Que respongui de pressa ──────────────────────────────────────────
console.log('\n10 · Velocitat');
{
  const p = await nova();
  await p.goto(BASE + '/faq/', { waitUntil: 'networkidle' });
  await obreCapa(p);
  await p.fill('.cerca-input', 'a');
  await p.waitForTimeout(300);
  const temps = await p.evaluate(() => {
    const inp = document.querySelector('.cerca-input');
    const t0 = performance.now();
    for (const q of ['e', 'es', 'esc', 'esco', 'escol', 'escole', 'escolet', 'escoleta']) {
      inp.value = q;
      inp.dispatchEvent(new Event('input', { bubbles: true }));
    }
    return performance.now() - t0;
  });
  comprova('escriure vuit lletres seguides es resol en menys de 600 ms',
    temps < 600, Math.round(temps) + ' ms');
  console.log('        (' + Math.round(temps) + ' ms per vuit tecles, '
    + Math.round(temps / 8) + ' ms per tecla)');
  await p.close();
}

// ── 11 · Lector de pantalla ───────────────────────────────────────────────
console.log('\n11 · Lector de pantalla');
{
  const p = await nova();
  await p.goto(BASE + '/faq/', { waitUntil: 'networkidle' });
  await obreCapa(p);
  const a = await p.evaluate(() => {
    const capa = document.querySelector('.cerca-capa');
    const inp = document.querySelector('.cerca-input');
    const llista = document.querySelector('.cerca-cos');
    return {
      dialog: capa.getAttribute('role'), modal: capa.getAttribute('aria-modal'),
      etiquetaCapa: !!(capa.getAttribute('aria-label') || capa.getAttribute('aria-labelledby')),
      combobox: inp.getAttribute('role'), etiquetaCamp: !!inp.getAttribute('aria-label'),
      controls: inp.getAttribute('aria-controls') === llista.id,
      llistaRol: llista.getAttribute('role'),
      botoEtiqueta: !!document.querySelector('[data-cerca-obrir]').getAttribute('aria-label'),
    };
  });
  comprova('la capa és un diàleg modal amb nom',
    a.dialog === 'dialog' && a.modal === 'true' && a.etiquetaCapa, JSON.stringify(a));
  /* Sense combobox ni listbox: el contenidor barreja títols, respostes i
     botons, i un listbox només admet opcions com a fills (axe-core:
     aria-required-children). El camp té nom i aria-controls; els resultats
     són enllaços normals i el recompte va per role="status". */
  comprova('el camp té nom accessible i està lligat a la llista',
    !a.combobox && a.etiquetaCamp && a.controls);
  comprova('la llista no es declara listbox (fills que no són opcions)',
    a.llistaRol !== 'listbox');
  comprova('la lupa té nom accessible', a.botoEtiqueta);
  await p.fill('.cerca-input', 'zzzzqqq');
  await p.waitForTimeout(300);
  comprova('sense resultats, ho diu amb paraules',
    (await p.textContent('.cerca-cos')).toLowerCase().includes('cap resultat'));
  await p.close();
}

// ── 12 · Quan no hi ha resposta: el formulari ─────────────────────────────
console.log('\n12 · Quan no hi ha resposta: el formulari');
{
  const p = await nova();
  // Res no ha de sortir cap a l'Apps Script mentre no es premi el botó: la
  // prova ho comprova de debò, interceptant la xarxa.
  const enviaments = [];
  await p.route('**script.google.com/**', r => { enviaments.push(r.request().url()); r.abort(); });
  await p.goto(BASE + '/faq/', { waitUntil: 'networkidle' });
  await obreCapa(p);
  await p.fill('.cerca-input', 'zzzzqqq');
  await p.waitForTimeout(350);

  comprova('sense cap resultat surt el formulari', await p.isVisible('.cerca-form'));
  comprova('la pregunta ja hi ve escrita',
    (await p.inputValue('.cerca-form textarea')) === 'zzzzqqq');
  comprova('cada camp té la seva etiqueta', await p.evaluate(() => {
    const camps = [...document.querySelectorAll('.cerca-form input, .cerca-form textarea')];
    return camps.length === 3 && camps.every(c => !!document.querySelector('label[for="' + c.id + '"]'));
  }));
  comprova('hi ha l\'avís de privacitat amb enllaç',
    await p.isVisible('.cerca-form-avis a'));

  // Enviar-ho buit no ha d'enviar res ni tancar el formulari.
  await p.fill('.cerca-form textarea', '');
  await p.click('.cerca-form-btn');
  await p.waitForTimeout(150);
  comprova('buit, avisa i no envia',
    await p.isVisible('.cerca-form-err') && await p.isVisible('.cerca-form') &&
    enviaments.length === 0, 'enviaments=' + enviaments.length);
  comprova('marca el camp que falta',
    (await p.getAttribute('.cerca-form [name=nom]', 'aria-invalid')) === 'true');

  await p.fill('.cerca-form [name=nom]', 'Anna Prova');
  await p.fill('.cerca-form [name=contacteVia]', '600000000');
  await p.fill('.cerca-form textarea', 'teniu equip de veterans?');
  await p.click('.cerca-form-btn');
  await p.waitForSelector('.cerca-form-fet:not([hidden])', { timeout: 8000 });
  comprova('després d\'enviar-ho, dona les gràcies', await p.isVisible('.cerca-form-fet'));
  comprova('i llavors sí que ofereix el WhatsApp',
    await p.isVisible('.cerca-form-fet a[href*="whatsapp"]'));
  const wa = await p.getAttribute('.cerca-form-fet a', 'href');
  comprova('el WhatsApp porta la pregunta escrita',
    decodeURIComponent(wa).includes('teniu equip de veterans?'), wa);
  comprova('el formulari desapareix quan ja s\'ha enviat',
    !(await p.isVisible('.cerca-form')));
  comprova('només s\'ha enviat en prémer el botó', enviaments.length === 1,
    'enviaments=' + enviaments.length);
  await p.close();
}

{
  const p = await nova();
  await p.goto(BASE + '/es/faq/', { waitUntil: 'networkidle' });
  await obreCapa(p);
  await p.fill('.cerca-input', 'zzzzqqq');
  await p.waitForTimeout(350);
  const t = (await p.textContent('.cerca-form')).toLowerCase();
  comprova('en castellà, el formulari va en castellà',
    t.includes('cómo te llamas') && t.includes('privacidad'), t.slice(0, 90));
  await p.close();
}

{
  const p = await nova();
  await p.goto(BASE + '/en/faq/', { waitUntil: 'networkidle' });
  await obreCapa(p);
  await p.fill('.cerca-input', 'zzzzqqq');
  await p.waitForTimeout(350);
  const t = (await p.textContent('.cerca-form')).toLowerCase();
  comprova('en anglès, el formulari va en anglès',
    t.includes('your name') && t.includes('privacy'), t.slice(0, 90));
  // El focus no pot escapar-se ara que hi ha camps de text a dins.
  await p.focus('.cerca-input');
  for (let i = 0; i < 20; i++) await p.keyboard.press('Tab');
  comprova('amb el formulari obert el focus continua dins de la capa',
    await p.evaluate(() => !!document.activeElement.closest('.cerca-capa')));
  await p.close();
}

{
  const p = await nova();
  await p.goto(BASE + '/faq/', { waitUntil: 'networkidle' });
  await obreCapa(p);
  // «campus» torna pàgines però cap resposta escrita: el formulari hi és,
  // però plegat, que la llista de resultats continua sent el que s'ha demanat.
  await p.fill('.cerca-input', 'campus');
  await p.waitForSelector('.cerca-llista a');
  comprova('amb enllaços però sense resposta, el formulari surt plegat',
    await p.isVisible('.cerca-plec > summary') && !(await p.isVisible('.cerca-form-btn')));
  // El resum queda sota el plec del llistat: es prem directament.
  await p.$eval('.cerca-plec > summary', el => el.click());
  await p.waitForTimeout(120);
  comprova('i s\'obre en prémer-lo', await p.isVisible('.cerca-form-btn'));
  // Amb resposta escrita no ha de sortir res de tot això.
  await p.fill('.cerca-input', 'que inclou la quota');
  await p.waitForSelector('.cerca-faq');
  comprova('quan sí que hi ha resposta, no hi ha formulari',
    !(await p.isVisible('.cerca-plec')) && !(await p.isVisible('.cerca-form')));
  await p.close();
}

await navegador.close();
console.log(`\n${ok} bé · ${ko} malament`);
if (falles.length) { console.log('\nFalles:'); falles.forEach(f => console.log('  · ' + f)); }
process.exit(ko ? 1 : 0);
