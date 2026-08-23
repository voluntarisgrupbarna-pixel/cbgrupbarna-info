// Bateria d'UX profunda: no mira el codi, recorre el lloc com una persona.
//
// La bateria `audit-browser.mjs` fotografia cada pàgina quieta a dalt de tot.
// Aquesta fa l'altra meitat de la feina: BAIXA, TORNA A PUJAR, GIRA EL MÒBIL,
// OBRE EL MENÚ i comprova què hi ha a cada moment. És el terreny on viuen els
// problemes de «apareix i desapareix sense coherència»: contingut que arrenca
// invisible i depèn d'un observador per veure's, barres fixes que tapen el que
// hi ha a sota, i coses que canvien només de girar el dispositiu.
//
//   node tests/ux-deep.mjs                        # totes les pàgines clau
//   node tests/ux-deep.mjs --pages /,/campus/     # només aquestes
//   node tests/ux-deep.mjs --devices mobil-360,tauleta-820
//   node tests/ux-deep.mjs --out tests/out
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

// ---------------------------------------------------------------------------
// Parc de dispositius. Mides reals de pantalla, no rodones inventades: el que
// es trenca sol trencar-se a les vores (320 px encara viu, i el mòbil ajagut
// és una pantalla de 360 px d'alçada que gairebé ningú prova).
// ---------------------------------------------------------------------------
const DEVICES = [
  { name: 'mobil-320',        width: 320,  height: 568,  dpr: 2, mobile: true,  nota: 'iPhone SE 1a gen · el mòbil més estret que encara es fa servir' },
  { name: 'mobil-360',        width: 360,  height: 740,  dpr: 3, mobile: true,  nota: 'Android mitjà · la mida més comuna del parc' },
  { name: 'mobil-375',        width: 375,  height: 667,  dpr: 2, mobile: true,  nota: 'iPhone SE 2/3 · pantalla curta' },
  { name: 'mobil-390',        width: 390,  height: 844,  dpr: 3, mobile: true,  nota: 'iPhone 13/14/15' },
  { name: 'mobil-430',        width: 430,  height: 932,  dpr: 3, mobile: true,  nota: 'iPhone 15 Pro Max' },
  { name: 'mobil-ajagut',     width: 844,  height: 390,  dpr: 3, mobile: true,  nota: 'iPhone girat · només 390 px d\'alçada' },
  { name: 'tauleta-768',      width: 768,  height: 1024, dpr: 2, mobile: true,  nota: 'iPad mini vertical · just al punt de ruptura' },
  { name: 'tauleta-820',      width: 820,  height: 1180, dpr: 2, mobile: true,  nota: 'iPad 10.9 vertical' },
  { name: 'tauleta-ajaguda',  width: 1180, height: 820,  dpr: 2, mobile: true,  nota: 'iPad 10.9 girat' },
  { name: 'tauleta-1024',     width: 1024, height: 1366, dpr: 2, mobile: true,  nota: 'iPad Pro 12.9 vertical · el límit dels media query' },
  { name: 'portatil-1280',    width: 1280, height: 800,  dpr: 2, mobile: false, nota: 'MacBook Air' },
  { name: 'escriptori-1440',  width: 1440, height: 900,  dpr: 2, mobile: false, nota: 'monitor habitual' },
  { name: 'escriptori-1920',  width: 1920, height: 1080, dpr: 1, mobile: false, nota: 'monitor gran · comprova que res es queda nan' },
];

// Pàgines clau: les que reben el trànsit i les que tenen lògica pròpia.
const PAGES_DEF = [
  '/', '/escoleta/', '/partits/', '/partits/calendaris/', '/campus/', '/femeni/',
  '/patrocinadors/', '/blog/', '/club/', '/faq/', '/opina/', '/3x3/',
  '/organigrama/', '/instal-lacions/', '/premsa/', '/newsletter/',
  '/es/', '/en/',
];

const PAGES = argVal('pages', PAGES_DEF.join(',')).split(',').filter(Boolean);
const ONLY_DEV = argVal('devices', '');
const DEVS = ONLY_DEV ? DEVICES.filter((d) => ONLY_DEV.split(',').includes(d.name)) : DEVICES;

// ---------------------------------------------------------------------------
// Funcions que corren DINS de la pàgina.
// ---------------------------------------------------------------------------

// Inventari de tot el que hauria de veure's: elements amb text o imatge
// propis. Els identifiquem amb una marca estable per poder-los comparar entre
// dos moments diferents del recorregut.
const MARCA = `(function () {
  var n = 0;
  document.querySelectorAll('body *').forEach(function (el) {
    if (!el.dataset.uxid) el.dataset.uxid = 'ux' + (n++);
  });
})()`;

// Un element «porta contingut» si té text propi o és una imatge/vídeo. No
// comptem els contenidors: si un contenidor està amagat, ja ho detectarem pel
// seu fill amb text, i així els informes no es repeteixen quinze vegades.
const VISIBLES = `(function () {
  function textPropi(el) {
    var t = '';
    for (var i = 0; i < el.childNodes.length; i++) {
      if (el.childNodes[i].nodeType === 3) t += el.childNodes[i].nodeValue;
    }
    return t.trim();
  }
  var fora = { SCRIPT: 1, STYLE: 1, NOSCRIPT: 1, TEMPLATE: 1, HEAD: 1, META: 1, LINK: 1, TITLE: 1 };
  // Un panell tancat no és contingut perdut: el menú desplegable, un <details>
  // sense obrir o la maquetació alternativa del commutador de la portada estan
  // amagats perquè algú els ha de demanar. Comptar-los diria que cada pàgina
  // amaga mig centenar de coses, i ofegaria el que sí que és un problema.
  var A_PROPOSIT = '.menu, [hidden], [aria-hidden="true"], dialog:not([open]),'
    + ' details:not([open]) > :not(summary), .only-extensa, .only-light,'
    + ' .modal, .popup, .drawer, .igf, .cbgb-gal';
  var out = {};
  document.querySelectorAll('body *').forEach(function (el) {
    if (fora[el.tagName]) return;
    var propi = textPropi(el);
    var media = el.tagName === 'IMG' || el.tagName === 'VIDEO' || el.tagName === 'SVG';
    if (!propi && !media) return;
    if (el.closest(A_PROPOSIT)) return;
    var r = el.getBoundingClientRect();
    if (r.width < 1 || r.height < 1) return;
    var cs = getComputedStyle(el);
    // Opacitat efectiva: la d'ell i la de tots els pares acumulada.
    var op = 1, p = el;
    while (p && p.nodeType === 1) { op *= parseFloat(getComputedStyle(p).opacity || '1'); p = p.parentElement; }
    out[el.dataset.uxid] = {
      tag: el.tagName.toLowerCase(),
      cls: (el.className && el.className.baseVal !== undefined ? el.className.baseVal : String(el.className || '')).slice(0, 80),
      text: (propi || el.getAttribute('alt') || '').slice(0, 70),
      op: +op.toFixed(3),
      vis: cs.visibility !== 'hidden' && cs.display !== 'none' && op > 0.01,
      top: Math.round(r.top + window.scrollY),
      h: Math.round(r.height),
    };
  });
  return out;
})()`;

// Desbordament horitzontal a la posició de scroll actual, amb el culpable.
const DESBORDA = `(function () {
  var de = document.documentElement;
  var excess = Math.round(de.scrollWidth - de.clientWidth);
  if (excess <= 1) return null;
  var amples = [];
  document.querySelectorAll('body *').forEach(function (el) {
    var r = el.getBoundingClientRect();
    if (r.width < 1 || r.height < 1) return;
    var dreta = Math.round(r.right + window.scrollX);
    if (dreta > de.clientWidth + 1) {
      amples.push({ id: el.dataset.uxid, tag: el.tagName.toLowerCase(),
        cls: String(el.className || '').slice(0, 60), sobra: dreta - de.clientWidth });
    }
  });
  amples.sort(function (a, b) { return b.sobra - a.sobra; });
  return { excess: excess, culpables: amples.slice(0, 4) };
})()`;

// Elements fixos/enganxats i què tapen. Mira el punt central de cada enllaç o
// botó visible: si qui respon al clic no és ell ni un fill seu, està tapat.
const TAPATS = `(function () {
  var fixos = [];
  document.querySelectorAll('body *').forEach(function (el) {
    var cs = getComputedStyle(el);
    if (cs.position !== 'fixed' && cs.position !== 'sticky') return;
    var r = el.getBoundingClientRect();
    if (r.width < 1 || r.height < 1) return;
    if (cs.visibility === 'hidden' || parseFloat(cs.opacity) < 0.05) return;
    if (r.bottom < 0 || r.top > innerHeight) return;
    fixos.push({ id: el.dataset.uxid, tag: el.tagName.toLowerCase(),
      cls: String(el.className || '').slice(0, 50), pos: cs.position,
      rect: [Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)] });
  });

  var tapats = [];
  document.querySelectorAll('a[href], button, input, select, textarea, summary').forEach(function (el) {
    var r = el.getBoundingClientRect();
    if (r.width < 1 || r.height < 1) return;
    if (r.bottom <= 0 || r.top >= innerHeight) return;      // fora de pantalla, no compta
    var cs = getComputedStyle(el);
    if (cs.visibility === 'hidden' || cs.display === 'none') return;
    var x = Math.min(Math.max(r.left + r.width / 2, 1), innerWidth - 1);
    var y = Math.min(Math.max(r.top + r.height / 2, 1), innerHeight - 1);
    var dalt = document.elementFromPoint(x, y);
    if (!dalt) return;
    if (dalt === el || el.contains(dalt) || dalt.contains(el)) return;
    // La capçalera enganxada tapa el que li passa per sota: és com funciona,
    // i el mateix element es veu perfectament unes passes més amunt. Només
    // compta si la pàgina ja no pot baixar més I l'element es queda a sota
    // seu per sempre, cosa que aquí es descarta perquè a mig recorregut era
    // visible. El que sí que compta és el que tapa una barra fixa de baix.
    var deDalt = dalt.closest && dalt.closest('header, .head');
    if (deDalt && getComputedStyle(deDalt).position === 'sticky') return;
    // Qui el tapa: pugem fins a trobar un element fix o enganxat.
    var p = dalt, tapador = null;
    while (p && p.nodeType === 1) {
      var pc = getComputedStyle(p).position;
      if (pc === 'fixed' || pc === 'sticky') { tapador = p; break; }
      p = p.parentElement;
    }
    tapats.push({
      id: el.dataset.uxid, tag: el.tagName.toLowerCase(),
      text: (el.textContent || el.value || el.getAttribute('aria-label') || '').trim().slice(0, 50),
      tapatPer: tapador
        ? (tapador.tagName.toLowerCase() + '.' + String(tapador.className || '').split(' ')[0])
        : (dalt.tagName.toLowerCase() + '.' + String(dalt.className || '').split(' ')[0]),
      fix: !!tapador,
    });
  });
  return { fixos: fixos, tapats: tapats };
})()`;

// Zones tocables massa petites, comptant la unió amb el seu <label>.
const TOCS = `(function () {
  var out = [];
  document.querySelectorAll('a[href], button, input:not([type=hidden]), select, textarea, summary, [role=button]').forEach(function (el) {
    var r = el.getBoundingClientRect();
    if (r.width < 1 || r.height < 1) return;
    var w = r.width, h = r.height;
    if (el.id) {
      var lab = document.querySelector('label[for="' + CSS.escape(el.id) + '"]');
      if (lab) { var lr = lab.getBoundingClientRect(); if (lr.height > 1) { w = Math.max(w, lr.width); h = Math.max(h, lr.height); } }
    }
    var pare = el.closest('label');
    if (pare && pare !== el) { var pr = pare.getBoundingClientRect(); if (pr.height > 1) { w = Math.max(w, pr.width); h = Math.max(h, pr.height); } }
    if (w >= 44 && h >= 44) return;
    // Els enllaços dins d'un paràgraf de text corregut no són botons: no s'hi
    // aplica la regla dels 44 px i marcar-los només faria soroll.
    if (el.tagName === 'A' && el.closest('p, li, figcaption, small')) return;
    out.push({ id: el.dataset.uxid, tag: el.tagName.toLowerCase(),
      text: (el.textContent || el.getAttribute('aria-label') || '').trim().slice(0, 45),
      w: Math.round(w), h: Math.round(h) });
  });
  return out;
})()`;

const AMAGATS = `(function () {
  var out = [];
  document.querySelectorAll('*').forEach(function (el) {
    var cs = getComputedStyle(el);
    if (parseFloat(cs.opacity) > 0.01 && cs.visibility !== 'hidden' && cs.display !== 'none') return;
    var t = (el.textContent || '').trim();
    if (t.length < 12) return;
    if (el.closest('script, style, noscript, template, head')) return;
    // Només el més amunt de cada branca amagada, per no comptar-ho tot dos cops.
    var p = el.parentElement, jaHiEs = false;
    while (p) { var pc = getComputedStyle(p);
      if (parseFloat(pc.opacity) <= 0.01 || pc.visibility === 'hidden' || pc.display === 'none') { jaHiEs = true; break; }
      p = p.parentElement; }
    if (jaHiEs) return;
    out.push({ clau: (el.tagName + '|' + String(el.className || '').slice(0, 40) + '|' + t.slice(0, 40)),
      cls: String(el.className || '').slice(0, 50), text: t.slice(0, 60), op: cs.opacity });
  });
  return out;
})()`;

// ---------------------------------------------------------------------------
// El recorregut: com baixa una persona de debò.
// ---------------------------------------------------------------------------
async function recorre(page, passos = 14) {
  const alt = await page.evaluate(() => document.documentElement.scrollHeight);
  const vh = await page.evaluate(() => innerHeight);
  const marques = [];
  const total = Math.max(alt - vh, 0);
  for (let i = 0; i <= passos; i++) {
    const y = Math.round((total * i) / passos);
    await page.evaluate((v) => window.scrollTo(0, v), y);
    await page.waitForTimeout(140);        // temps perquè l'observador dispari
    marques.push(y);
  }
  await page.waitForTimeout(500);          // que acabin les transicions de 0,9 s
  return { alt, vh, marques };
}

// ---------------------------------------------------------------------------
async function provaPagina(ctx, origin, url, dev, ferNoJs) {
  const page = await ctx.newPage();
  const errors = [];
  page.on('pageerror', (e) => errors.push(String(e).slice(0, 200)));
  page.on('console', (m) => { if (m.type() === 'error') errors.push('console: ' + m.text().slice(0, 200)); });

  // Tallem el trànsit extern: així la prova és determinista i, de passada, es
  // veu si alguna cosa del lloc depèn d'un tercer per aparèixer.
  await page.route('**/*', (route) => {
    const u = route.request().url();
    if (u.startsWith(origin)) return route.continue();
    return route.abort();
  });

  const r = {
    url, dispositiu: dev.name, problemes: [], errors: [],
  };
  const afegeix = (tipus, gravetat, detall) => r.problemes.push({ tipus, gravetat, ...detall });

  try {
    await page.goto(origin + url, { waitUntil: 'load', timeout: 30000 });
  } catch (e) {
    r.problemes.push({ tipus: 'carrega', gravetat: 'greu', msg: String(e).slice(0, 160) });
    await page.close();
    return r;
  }
  await page.waitForTimeout(400);

  // --- 0. Les galetes, primer -----------------------------------------------
  //     La barra de consentiment és fixa a baix de tot i tapa la barra
  //     d'accions del mòbil. Ho anotem un cop —és el que veu qui arriba per
  //     primera vegada— i després l'acceptem, perquè la resta del recorregut
  //     mesuri el lloc tal com el veu qui ja hi ha estat.
  var barraGaletes = await page.$('.cbgb-gal');
  if (barraGaletes) {
    const tapaCta = await page.evaluate(`(function () {
      var g = document.querySelector('.cbgb-gal');
      if (!g) return [];
      var gr = g.getBoundingClientRect();
      var out = [];
      document.querySelectorAll('.actionbar a, .fab-wa, a.btn, button.btn').forEach(function (el) {
        var r = el.getBoundingClientRect();
        if (r.height < 1) return;
        if (r.bottom > gr.top && r.top < gr.bottom) {
          out.push((el.textContent || el.getAttribute('aria-label') || '').trim().slice(0, 40));
        }
      });
      return out;
    })()`);
    if (tapaCta.length) {
      afegeix('galetes-tapen-la-crida-a-l-accio', 'mitja', {
        quants: tapaCta.length, exemples: tapaCta.slice(0, 5),
        detall: 'a la primera visita, la barra de galetes tapa aquests botons fins que es respon',
      });
    }
    await page.click('.cbgb-gal button[data-cbgb="si"]').catch(function () {});
    await page.waitForTimeout(400);
  }

  await page.evaluate(MARCA);

  // --- 1. Foto de sortida: què es veu abans de tocar res -------------------
  const inici = await page.evaluate(VISIBLES);
  const desbordaDalt = await page.evaluate(DESBORDA);
  if (desbordaDalt) {
    afegeix('desbordament-horitzontal', 'greu', {
      on: 'a dalt de tot', sobra: desbordaDalt.excess, culpables: desbordaDalt.culpables,
    });
  }

  // --- 2. Recorregut complet ----------------------------------------------
  const { alt, vh } = await recorre(page);
  r.alcada = alt; r.viewport = vh;

  // Desbordament que només apareix avall (barres fixes, taules, mapes…)
  await page.evaluate(() => window.scrollTo(0, document.documentElement.scrollHeight));
  await page.waitForTimeout(250);
  const desbordaBaix = await page.evaluate(DESBORDA);
  if (desbordaBaix && !desbordaDalt) {
    afegeix('desbordament-horitzontal', 'greu', {
      on: 'a baix de tot', sobra: desbordaBaix.excess, culpables: desbordaBaix.culpables,
    });
  }

  // --- 3. Barres fixes que tapen contingut (a baix de tot és el pitjor cas) -
  const capaBaix = await page.evaluate(TAPATS);
  for (const t of capaBaix.tapats.filter((x) => x.fix)) {
    afegeix('element-tapat', 'greu', {
      on: 'a baix de tot', element: `${t.tag} «${t.text}»`, tapatPer: t.tapatPer,
    });
  }
  r.fixos = capaBaix.fixos.map((f) => `${f.tag}.${f.cls.split(' ')[0]} (${f.pos})`);

  // --- 4. Tornem a dalt: què ha canviat -----------------------------------
  await page.evaluate(() => window.scrollTo(0, 0));
  await page.waitForTimeout(700);
  const final = await page.evaluate(VISIBLES);

  // 4a. Contingut que ARRENCA invisible i mai s'arregla. És el cor de la
  //     queixa: text que hi és al codi però que l'usuari no arriba a veure.
  const maiVist = [];
  for (const [id, el] of Object.entries(final)) {
    if (el.vis) continue;
    maiVist.push(el);
  }
  if (maiVist.length) {
    afegeix('contingut-invisible-despres-del-recorregut', 'greu', {
      quants: maiVist.length,
      exemples: maiVist.slice(0, 8).map((e) => `${e.tag}.${e.cls.split(' ')[0]} «${e.text}» op=${e.op}`),
    });
  }

  // 4b. Contingut que ES VEIA a l'inici i ha deixat de veure's. Això és
  //     literalment «desapareix»: l'usuari l'ha vist i després ja no hi és.
  const desaparegut = [];
  for (const [id, ini] of Object.entries(inici)) {
    const fi = final[id];
    if (ini.vis && fi && !fi.vis) desaparegut.push({ ...fi, opIni: ini.op });
  }
  if (desaparegut.length) {
    afegeix('contingut-que-desapareix', 'greu', {
      quants: desaparegut.length,
      exemples: desaparegut.slice(0, 8).map((e) => `${e.tag}.${e.cls.split(' ')[0]} «${e.text}» ${e.opIni}→${e.op}`),
    });
  }

  // 4c. El cas concret del revelat: elements .reveal que no han rebut mai la
  //     classe .visible tot i haver passat per pantalla.
  const revelatFallit = await page.evaluate(`(function () {
    var out = [];
    document.querySelectorAll('.reveal').forEach(function (el) {
      if (el.classList.contains('visible')) return;
      // Si viu dins d'una maquetació que ara no es mostra (el commutador
      // franges/extensa), no ha disparat perquè no li tocava.
      var alt = el.closest('.only-extensa, .only-light');
      if (alt && getComputedStyle(alt).display === 'none') return;
      var r = el.getBoundingClientRect();
      out.push({ cls: String(el.className), h: Math.round(r.height),
        text: (el.textContent || '').trim().slice(0, 60) });
    });
    return out;
  })()`);
  if (revelatFallit.length) {
    afegeix('revelat-no-disparat', 'greu', {
      quants: revelatFallit.length,
      exemples: revelatFallit.slice(0, 6).map((e) => `«${e.text}» (alçada ${e.h}px)`),
    });
  }

  // --- 5. El lloc sense JavaScript ----------------------------------------
  //     GitHub Pages serveix HTML pla; si el JS falla, es cau la connexió o un
  //     bloquejador el talla, el contingut ha de continuar sent visible.
  //     No depèn del dispositiu: només cal fer-ho un cop per pàgina.
  if (ferNoJs) {
    const ambJs = await page.evaluate(AMAGATS);
    const ctxNoJs = await ctx.browser().newContext({
      viewport: { width: dev.width, height: dev.height },
      deviceScaleFactor: dev.dpr, isMobile: dev.mobile, hasTouch: dev.mobile,
      locale: 'ca-ES', javaScriptEnabled: false,
    });
    const p2 = await ctxNoJs.newPage();
    await p2.route('**/*', (route) => (route.request().url().startsWith(origin) ? route.continue() : route.abort()));
    try {
      await p2.goto(origin + url, { waitUntil: 'load', timeout: 20000 });
      const amagat = await p2.evaluate(AMAGATS);
      // La comparació és el que fa la prova honesta: amb JS també hi ha coses
      // amagades (el menú tancat, la maquetació alternativa del commutador, el
      // que un media query retira al mòbil). Només és un problema el que
      // desapareix NOMÉS quan el JS no arrenca.
      const jaAmagatAmbJs = new Set(ambJs.map((a) => a.clau));
      const real = amagat.filter((a) => !jaAmagatAmbJs.has(a.clau))
        .filter((a) => !/menu|modal|dialog|popup|drawer|tooltip|sr-only|skip/i.test(a.cls));
      if (real.length) {
        afegeix('invisible-sense-javascript', 'greu', {
          quants: real.length,
          exemples: real.slice(0, 6).map((e) => `.${e.cls.split(' ')[0]} «${e.text}» op=${e.op}`),
        });
      }
    } catch { /* la pàgina no carrega sense JS: ja sortirà per una altra via */ }
    await ctxNoJs.close();
  }

  // --- 6. Zones tocables (només on hi ha dit, no amb ratolí) ---------------
  if (dev.mobile) {
    const petits = await page.evaluate(TOCS);
    if (petits.length) {
      afegeix('zona-tocable-petita', 'mitja', {
        quants: petits.length,
        exemples: petits.slice(0, 6).map((e) => `${e.tag} «${e.text}» ${e.w}×${e.h}px`),
      });
    }
  }

  // --- 7. El menú: obrir, mirar-ho tot, tancar -----------------------------
  const teBurger = await page.$('#burger, .head-burger, [aria-controls="menu"]');
  if (teBurger) {
    await page.evaluate(() => window.scrollTo(0, 0));
    await page.waitForTimeout(200);
    const scrollAbans = await page.evaluate(() => window.scrollY);
    try {
      await teBurger.click({ timeout: 4000 });
      await page.waitForTimeout(800);
      const m = await page.evaluate(`(function () {
        var menu = document.querySelector('#menu, .menu');
        if (!menu) return null;
        var cs = getComputedStyle(menu);
        var r = menu.getBoundingClientRect();
        var enll = [].slice.call(menu.querySelectorAll('a[href], button'));
        var fora = enll.filter(function (a) {
          var ar = a.getBoundingClientRect();
          return ar.height > 0 && (ar.bottom > innerHeight + 2 || ar.top < -2);
        });
        return {
          obert: cs.visibility !== 'hidden' && r.top > -r.height / 2,
          potFerScroll: menu.scrollHeight > menu.clientHeight + 2,
          overflow: cs.overflowY,
          enllacos: enll.length,
          foraDePantalla: fora.length,
          exempleFora: fora.slice(0, 3).map(function (a) { return (a.textContent || '').trim().slice(0, 30); }),
          bodyBloquejat: getComputedStyle(document.body).overflow === 'hidden'
            || getComputedStyle(document.documentElement).overflow === 'hidden'
            || getComputedStyle(document.body).position === 'fixed',
          expanded: (document.querySelector('#burger') || {}).getAttribute
            ? document.querySelector('#burger').getAttribute('aria-expanded') : null,
        };
      })()`);
      if (m) {
        r.menu = m;
        if (!m.obert) afegeix('menu-no-sobre', 'greu', { detall: 'el botó del menú no obre res' });
        if (m.foraDePantalla > 0 && !m.potFerScroll) {
          afegeix('menu-inabastable', 'greu', {
            quants: m.foraDePantalla, exemples: m.exempleFora,
            detall: 'hi ha entrades del menú fora de pantalla i el menú no fa scroll',
          });
        } else if (m.foraDePantalla > 0) {
          afegeix('menu-requereix-scroll', 'lleu', {
            quants: m.foraDePantalla, exemples: m.exempleFora,
            detall: 'cal fer scroll dins del menú per arribar a aquestes entrades',
          });
        }
        if (!m.bodyBloquejat) {
          afegeix('menu-sense-bloqueig-de-fons', 'mitja', {
            detall: 'amb el menú obert, la pàgina de sota encara fa scroll',
          });
        }
        if (m.expanded !== 'true' && m.obert) {
          afegeix('menu-aria-expanded', 'mitja', { detall: `aria-expanded="${m.expanded}" amb el menú obert` });
        }
      }
      // Tancar amb Escape: la sortida que espera tothom.
      await page.keyboard.press('Escape');
      await page.waitForTimeout(700);
      const tancatEsc = await page.evaluate(`(function () {
        var menu = document.querySelector('#menu, .menu');
        if (!menu) return true;
        var cs = getComputedStyle(menu);
        return cs.visibility === 'hidden' || menu.getBoundingClientRect().top < -menu.getBoundingClientRect().height / 2;
      })()`);
      if (!tancatEsc) {
        afegeix('menu-escape-no-tanca', 'mitja', { detall: 'la tecla Escape no tanca el menú' });
        await teBurger.click({ timeout: 4000 }).catch(() => {});
        await page.waitForTimeout(600);
      }
      const scrollDespres = await page.evaluate(() => window.scrollY);
      if (Math.abs(scrollDespres - scrollAbans) > 40) {
        afegeix('menu-perd-la-posicio', 'mitja', {
          detall: `en obrir i tancar el menú la pàgina ha saltat de ${scrollAbans}px a ${scrollDespres}px`,
        });
      }
    } catch (e) {
      afegeix('menu-no-clicable', 'greu', { detall: String(e).slice(0, 120) });
    }
  }

  // --- 8. Girar el dispositiu ---------------------------------------------
  if (dev.mobile) {
    await page.setViewportSize({ width: dev.height, height: dev.width });
    await page.waitForTimeout(600);
    const desbGirat = await page.evaluate(DESBORDA);
    if (desbGirat) {
      afegeix('desbordament-en-girar', 'greu', {
        sobra: desbGirat.excess, culpables: desbGirat.culpables,
        detall: `girat a ${dev.height}×${dev.width}`,
      });
    }
    const invisGirat = await page.evaluate(`(function () {
      var n = 0;
      document.querySelectorAll('.reveal').forEach(function (el) { if (!el.classList.contains('visible')) n++; });
      return n;
    })()`);
    if (invisGirat) {
      afegeix('revelat-perdut-en-girar', 'mitja', { quants: invisGirat });
    }
    await page.setViewportSize({ width: dev.width, height: dev.height });
    await page.waitForTimeout(300);
  }

  // --- 9. Zoom del text al 200 % (WCAG 1.4.4) ------------------------------
  await page.evaluate(() => { document.documentElement.style.fontSize = '32px'; });
  await page.waitForTimeout(400);
  const desbZoom = await page.evaluate(DESBORDA);
  if (desbZoom) {
    afegeix('desbordament-amb-text-gran', 'mitja', {
      sobra: desbZoom.excess, culpables: desbZoom.culpables,
      detall: 'amb la lletra al 200 % (arrel a 32px) el contingut se surt de l\'ample',
    });
  }
  await page.evaluate(() => { document.documentElement.style.fontSize = ''; });

  r.errors = [...new Set(errors)].slice(0, 6);
  if (r.errors.length) afegeix('errors-de-javascript', 'mitja', { quants: r.errors.length, exemples: r.errors });

  await page.close();
  return r;
}

// ---------------------------------------------------------------------------
const { origin, close } = await startServer(ROOT);
const browser = await chromium.launch();
const resultats = [];
const t0 = Date.now();

console.log(`Provant ${PAGES.length} pàgines × ${DEVS.length} dispositius = ${PAGES.length * DEVS.length} recorreguts\n`);

for (const dev of DEVS) {
  const ctx = await browser.newContext({
    viewport: { width: dev.width, height: dev.height },
    deviceScaleFactor: dev.dpr, isMobile: dev.mobile, hasTouch: dev.mobile,
    locale: 'ca-ES',
  });
  process.stdout.write(`${dev.name.padEnd(18)} `);
  for (const url of PAGES) {
    const r = await provaPagina(ctx, origin, url, dev, dev === DEVS[0]);
    resultats.push(r);
    const greus = r.problemes.filter((p) => p.gravetat === 'greu').length;
    process.stdout.write(greus ? '✗' : (r.problemes.length ? '·' : '✓'));
  }
  process.stdout.write('\n');
  await ctx.close();
}

await browser.close();
await close();

fs.mkdirSync(OUT, { recursive: true });
const dades = {
  data: new Date().toISOString(),
  segons: Math.round((Date.now() - t0) / 1000),
  dispositius: DEVS, pagines: PAGES, resultats,
};
fs.writeFileSync(path.join(OUT, 'ux-deep.json'), JSON.stringify(dades, null, 2));

// Resum per tipus de problema.
const perTipus = new Map();
for (const r of resultats) {
  for (const p of r.problemes) {
    const k = p.tipus;
    if (!perTipus.has(k)) perTipus.set(k, { gravetat: p.gravetat, casos: [] });
    perTipus.get(k).casos.push({ url: r.url, dispositiu: r.dispositiu, ...p });
  }
}
const ordre = { greu: 0, mitja: 1, lleu: 2 };
const llista = [...perTipus.entries()].sort((a, b) =>
  (ordre[a[1].gravetat] - ordre[b[1].gravetat]) || (b[1].casos.length - a[1].casos.length));

console.log(`\n${'─'.repeat(72)}\nRESUM · ${dades.segons}s · ${resultats.length} recorreguts\n${'─'.repeat(72)}`);
if (!llista.length) console.log('Cap problema detectat.');
for (const [tipus, info] of llista) {
  const pags = new Set(info.casos.map((c) => c.url)).size;
  const devs = new Set(info.casos.map((c) => c.dispositiu)).size;
  console.log(`\n[${info.gravetat.toUpperCase()}] ${tipus}`);
  console.log(`  ${info.casos.length} casos · ${pags} pàgines · ${devs} dispositius`);
  for (const c of info.casos.slice(0, 3)) {
    const extra = c.exemples ? '\n      ' + c.exemples.slice(0, 3).join('\n      ')
      : (c.detall || c.culpables ? '\n      ' + JSON.stringify(c.culpables || c.detall) : '');
    console.log(`    ${c.url} @ ${c.dispositiu}${c.quants ? ` (${c.quants})` : ''}${extra}`);
  }
  if (info.casos.length > 3) console.log(`    …i ${info.casos.length - 3} casos més (tots a ux-deep.json)`);
}
console.log(`\nDades completes: ${path.relative(ROOT, path.join(OUT, 'ux-deep.json'))}`);
