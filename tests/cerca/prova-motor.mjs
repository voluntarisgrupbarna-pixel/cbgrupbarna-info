/* Prova el motor de /js/cerca.js contra l'índex real, sense navegador.
   node tests/cerca/prova-motor.mjs
   Cada cas diu: què s'escriu, en quin idioma, i quina pàgina ha de sortir
   entre els primers resultats. Si un cas falla, la cerca ha empitjorat. */
import fs from 'node:fs';
import vm from 'node:vm';

const index = JSON.parse(fs.readFileSync('cerca-index.json', 'utf8'));
const codi = fs.readFileSync('js/cerca.js', 'utf8');

function motor(lang) {
  const sandbox = {
    console,
    location: { pathname: lang === 'ca' ? '/' : '/' + lang + '/', href: 'https://cbgrupbarna.info/', search: '' },
    navigator: { connection: { saveData: true } },
    localStorage: { getItem: () => null, setItem: () => {}, removeItem: () => {} },
    fetch: () => Promise.resolve({ ok: true, json: () => Promise.resolve(index) }),
    setTimeout, URL, URLSearchParams,
    document: {
      documentElement: { lang, classList: { add(){}, remove(){} } },
      readyState: 'complete',
      addEventListener(){}, querySelector: () => null,
      getElementById: () => null,
      createElement: () => ({ style:{}, classList:{add(){},remove(){},toggle(){}}, setAttribute(){}, appendChild(){}, addEventListener(){} }),
      body: { appendChild(){} }
    }
  };
  sandbox.window = sandbox;
  vm.createContext(sandbox);
  vm.runInContext(codi, sandbox);
  return sandbox.CBGBCerca._motor;
}

const CASOS = [
  ['ca', 'escoleta', '/escoleta/'],
  ['ca', 'escoleta 5 anys', '/escoleta/'],
  ['ca', 'basquet', null],
  ['ca', 'quant costa', '/faq/'],
  ['ca', 'a quina hora juga el cadet', '/partits/'],
  ['ca', 'com apuntar el meu fill', '/portes-obertes/'],
  ['ca', 'on entrenem', '/instal-lacions/'],
  ['ca', 'escoleata', '/escoleta/'],          // falta d'ortografia
  ['ca', 'basquet femeni', '/femeni/'],
  ['ca', 'patrocinadors', '/patrocinadors/'],
  ['es', 'cuanto cuesta', '/es/faq/'],
  ['es', 'como apuntar a mi hija', '/es/escoleta/'],
  ['es', 'horarios de partidos', '/es/partits/'],
  ['es', 'baloncesto femenino', '/es/baloncesto-femenino/'],
  ['es', 'donde entrenais', '/es/instalaciones/'],
  // /magics/ no té versió castellana: ha de sortir la catalana, no amagar-se
  ['es', 'baloncesto inclusivo', '/magics/'],
  ['en', 'how much does it cost', '/en/faq/'],
  ['en', 'summer camp', '/en/campus/'],
  ['en', 'where do you train', '/en/facilities/'],
  ['en', 'how to sign up my son', null],
  ['ca', 'campus de nadal', '/campus-nadal-basquet-barcelona/'],
  ['ca', 'telefon del club', null],
  ['ca', 'historia del club', '/historia/'],
  ['ca', 'junta directiva', '/organigrama/'],
  ['ca', 'fotos del partit', '/fotos/'],
  ['ca', '3x3', '/3x3/'],
  ['ca', 'asdfghjkl', null]
];

let ok = 0, ko = 0;
const motors = {};
for (const lang of ['ca', 'es', 'en']) {
  motors[lang] = motor(lang);
  await motors[lang].carrega();
}

for (const [lang, consulta, esperat] of CASOS) {
  const r = motors[lang].cerca(consulta);
  const top = r.slice(0, 5).map(x => x.u);
  const passa = esperat ? top.includes(esperat)
    : (consulta === 'asdfghjkl' ? top.length === 0 : top.length > 0);
  console.log((passa ? '  ok  ' : '  FALLA ') + `[${lang}] "${consulta}"` +
    (esperat ? ` → esperat ${esperat}` : '') + `\n        ${top.join('  ') || '(cap resultat)'}`);
  passa ? ok++ : ko++;
}
console.log(`\n${ok} bé · ${ko} malament`);
process.exit(ko ? 1 : 0);
