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
  // El Magics va estar temps sense versió castellana i la prova demanava la
  // catalana. Ara ja en té: qui busca en castellà ha de rebre la castellana.
  ['es', 'baloncesto inclusivo', '/es/magics/'],
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
  // «fotos» va deixar de ser un cas de «cap resposta» el 23/08/2026: una
  // paraula rara i sola SÍ que és una pregunta, i el que calia arreglar no
  // era la regla sinó el contingut —/fotos/ només tenia escrita la pregunta
  // del dret d'imatge, i ara també la que la gent fa de debò.
  ['ca', 'fotos', 'les fotos dels partits'],
  // «campus» surt a 23 preguntes: sola no distingeix res i segueix sense
  // treure resposta, que és el que ha de fer.
  ['ca', 'campus', null],
  ['ca', 'asdfghjkl', null],
  // Però amb dues paraules, sí: ja és una pregunta.
  ['ca', 'treure una foto del meu fill', 'no surti a les fotos'],
  ['es', 'quitar una foto de mi hija', 'no salga en las fotos'],
  ['ca', 'quin equip li toca pel seu any', "l'any de naixement"],
  ['en', 'how many trainings a week', 'training sessions'],
];

// ── Auditoria del 24/08/2026 · les setze respostes equivocades ────────────
// DOS CASOS QUE NO HI SÓN, i val més dir-ho que amagar-ho: «quin metro em va
// bé» (8,7 punts) i «cómo doy de baja a mi hijo» es queden just per sota del
// llindar quan la consulta porta una sola paraula de contingut i molta
// palla. Totes dues tornen els enllaços bons. Abaixar el llindar per
// guanyar-les en faria entrar de dolentes: està mesurat que per sota de 9
// les respostes bones i les dolentes es barregen.
// Cada línia d'aquí sota era una resposta que el cercador donava malament, o
// una pregunta escrita al web que no sabia trobar. Van sortir de passar-hi
// 111 consultes escrites com les escriu la gent. Si una torna a fallar, és
// que s'ha desfet la correcció que la va arreglar.
RESPOSTES.push(
  // 1 · Perdonar faltes no pot voler dir canviar de tema. La regla d'arrel
  //     només ajunta dues paraules si el començament compartit val per la
  //     meitat de la paraula llarga (mateixaParaula, js/cerca.js).
  ['ca', 'instalacions', null],       // abans: «Quan obren les inscripcions…»
  ['es', 'precio', null],             // abans: «¿Qué premios hay?»
  ['ca', 'entranador', null],         // abans: «Es pot entrar a mig curs?»
  ['ca', 'equipasio', null],          // abans: «Quins equips té el club?»
  ['ca', 'metro', 'metro'],
  ['ca', 'qui es el president', 'presideix'],

  // 2 · Una paraula que no surt a cap pregunta no és rara: és muda. El pes
  //     per raresa la prenia per la paraula que decidia la consulta.
  ['ca', 'quantes entrenadores teniu', 'entrenadores'],
  ['ca', 'cal fer-se una prova medica', 'revisió mèdica'],

  // 3 · Preguntes escrites al web que el cercador no trobava.
  ['ca', 'com em dono de baixa', 'baixa'],
  ['es', 'darse de baja a mitad de curso', 'baja'],
  ['ca', 'es pot entrar a mitja temporada', 'mig curs'],
  ['ca', 'que passa si falta a un entrenament', 'falta a un entrenament'],
  ['es', 'dónde compro la ropa del club', 'equipación'],
  ['es', 'hace falta certificado médico', 'revisión médica'],

  // 4 · Contingut escrit a partir de l'auditoria: no hi havia resposta.
  ['ca', 'com contacto amb el club', 'contacto amb el club'],
  ['en', 'how do I contact the club', 'contact the club'],
  ['es', 'dirección del pabellón', 'dirección del pabellón'],
  ['ca', 'quan es el campus d\'estiu', 'campus d\'estiu'],
  ['en', 'summer basketball camp dates', 'summer camp'],
  ['ca', 'hi ha equip senior', 'sènior'],
  ['ca', 'quants anys te el club', 'quants anys'],
  ['ca', 'sou el millor club de barcelona', 'millor club'],
  ['ca', 'que passa si es lesiona', 'lesiona'],
  ['ca', 'quan juga el meu fill', 'quan juga el meu fill'],
);

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
