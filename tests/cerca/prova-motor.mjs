/* Prova el motor de /js/cerca.js contra l'índex real, sense navegador.
   node tests/cerca/prova-motor.mjs

   Dues tandes:
     1. RESULTATS — què s'escriu, en quin idioma, i quina pàgina ha de sortir
        entre els cinc primers.
     2. RESPOSTES — quina de les 460 preguntes ja escrites al web ha de sortir
        resolta a dalt de tot, i —igual d'important— quines consultes NO han
        de treure'n cap. Una resposta que no toca fa més mal que no respondre.

   Si toques SINONIMS, DESTINS o RESPOSTES de js/cerca.js, afegeix el cas nou
   aquí. És el que impedeix que arreglar una cerca en trenqui tres. */
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
// ---- Tanda 2 · les respostes ----------------------------------------------
// El tercer camp és un tros de la pregunta que ha de respondre, o `null` si
// aquesta consulta NO ha de treure cap resposta (massa vaga, o cap pregunta
// del web la respon de debò).
const RESPOSTES = [
  ['ca', 'quant costa apuntar-se', 'quant costa apuntar-se'],
  ['ca', 'com m\'apunto', "com m'apunto"],
  ['ca', 'on entrena', 'on entrena'],
  ['ca', 'a partir de quina edat', 'a partir de quina edat'],
  ['ca', "hi ha pla d'igualtat", "pla d'igualtat"],
  ['ca', 'quan es el campus de nadal', 'dates del campus de nadal'],
  ['es', 'cuanto cuesta', 'cuánto cuesta'],
  ['es', 'donde entrena', 'dónde entrena'],
  ['es', 'a que edad se empieza', 'a qué edad'],
  ['en', 'how much does it cost', 'how much does it cost'],
  // Escrites a i18n/faq.yml i repartides per generate-faq.py. Fins al
  // 23/08/2026 cap d'aquestes tenia resposta al web.
  ['ca', 'que porto el primer dia', 'què cal portar'],
  ['ca', 'em puc quedar a mirar', 'quedar a mirar'],
  ['ca', 'on es la nau del clot', 'la nau del clot'],
  ['es', 'donde esta la nau del clot', 'la nau del clot'],
  ['es', 'en que pistas entrena', 'en qué pistas'],
  ['en', 'where is la nau del clot', 'la nau del clot'],
  // Cap resposta: una paraula solta és un tema, no una pregunta; i un
  // teclat aixafat no ha de treure res.
  ['ca', 'fotos', null],
  ['ca', 'campus', null],
  ['ca', 'asdfghjkl', null],
  // Però amb dues paraules, sí: ja és una pregunta.
  ['ca', 'treure una foto del meu fill', 'no surti a les fotos'],
  ['es', 'quitar una foto de mi hija', 'no salga en las fotos'],
  ['ca', 'quin equip li toca pel seu any', "l'any de naixement"],
  ['en', 'how many trainings a week', 'training sessions'],
];

console.log('\n---- respostes ----');
for (const [lang, consulta, esperat] of RESPOSTES) {
  const r = motors[lang].resposta(consulta);
  const te = r ? r.q.toLowerCase() : '';
  const passa = esperat ? te.includes(esperat.toLowerCase()) : r === null;
  console.log((passa ? '  ok  ' : '  FALLA ') + `[${lang}] "${consulta}"` +
    (esperat ? ` → esperat «${esperat}»` : ' → cap resposta') +
    `\n        ${r ? r.q + '  (' + r.u + ' · ' + r.punts + ')' : '(cap)'}`);
  passa ? ok++ : ko++;
}

console.log(`\n${ok} bé · ${ko} malament`);
process.exit(ko ? 1 : 0);
