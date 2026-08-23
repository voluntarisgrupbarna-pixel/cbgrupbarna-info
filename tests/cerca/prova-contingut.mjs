/* Auditoria de CONTINGUT del cercador: què troba de debò la gent que busca.
   node tests/cerca/prova-contingut.mjs           informe + comprovacions
   node tests/cerca/prova-contingut.mjs --tot     ensenya també les que passen

   prova-motor.mjs comprova casos concrets que no s'han de trencar mai.
   Això és una altra cosa: una llista de com escriuen les famílies de debò
   —amb faltes, en tres idiomes i amb frases senceres— per veure on el
   cercador encara no arriba. Les que fallen no són errors de codi: són
   forats de contingut, i la manera d'arreglar-los sol ser escriure una
   pregunta a i18n/faq.yml, no tocar el motor. */
import fs from 'node:fs';
import vm from 'node:vm';

const index = JSON.parse(fs.readFileSync('cerca-index.json', 'utf8'));
const codi = fs.readFileSync('js/cerca.js', 'utf8');
const TOT = process.argv.includes('--tot');

function motor(lang) {
  const s = {
    console, setTimeout, URL, URLSearchParams,
    location: { pathname: lang === 'ca' ? '/' : '/' + lang + '/', href: 'https://x/', search: '' },
    navigator: { connection: { saveData: true } },
    localStorage: { getItem: () => null, setItem() {}, removeItem() {} },
    fetch: () => Promise.resolve({ ok: true, json: () => Promise.resolve(index) }),
    document: {
      documentElement: { lang, classList: { add() {}, remove() {} } },
      readyState: 'complete', addEventListener() {}, querySelector: () => null,
      getElementById: () => null, body: { appendChild() {} },
      createElement: () => ({ style: {}, classList: { add() {}, remove() {}, toggle() {} },
        setAttribute() {}, appendChild() {}, addEventListener() {} }),
    },
  };
  s.window = s;
  vm.createContext(s);
  vm.runInContext(codi, s);
  return s.CBGBCerca._motor;
}

/* Cada cas: [idioma, què s'escriu, què ha de passar]
     'resposta'   → ha de sortir una resposta escrita a dalt de tot
     '/una/ruta/' → aquesta pàgina ha de ser entre les 3 primeres
     'res'        → no ha de tornar res (i està bé que no en torni)
     null         → només informe: volem veure què fa                     */
const CASOS = [
  // ── Diners. Avui la resposta és «contacta amb el club»: és el forat gros.
  ['ca', 'quant costa', 'resposta'],
  ['ca', 'quant val la temporada', null],
  ['ca', 'preu escoleta', null],
  ['es', 'cuánto cuesta apuntarse', 'resposta'],
  ['es', 'precio de la temporada', null],
  ['en', 'how much is it', 'resposta'],
  ['ca', 'hi ha beques', null],
  ['ca', 'es pot pagar a terminis', null],

  // ── Apuntar-s'hi
  ['ca', 'com apunto el meu fill', 'resposta'],
  ['ca', 'vull que la meva filla jugui a basquet', null],
  ['ca', 'es pot provar abans', 'resposta'],
  ['ca', 'que porto el primer dia', 'resposta'],
  ['ca', 'em puc quedar a mirar', 'resposta'],
  ['es', 'quiero apuntar a mi hija', null],
  ['es', 'se puede probar antes', 'resposta'],
  ['en', 'how do i sign my son up', null],
  ['en', 'can we try a session first', 'resposta'],

  // ── Edats i categories
  ['ca', 'te 5 anys on va', null],
  ['ca', 'quin equip li toca', 'resposta'],
  ['ca', 'que vol dir cadet', 'resposta'],
  ['ca', 'a partir de quina edat', 'resposta'],
  ['es', 'mi hijo tiene 9 años', null],
  ['en', 'my daughter is 7', null],

  // ── Horaris, pistes, partits
  ['ca', 'a quina hora entrenen', null],
  ['ca', 'quan juga el cadet femeni', null],
  ['ca', 'on es la nau del clot', 'resposta'],
  ['ca', 'a quines pistes entrenen', 'resposta'],
  ['ca', 'calendari del meu equip', '/partits/calendaris/'],
  ['ca', 'resultats del cap de setmana', '/partits/'],
  ['es', 'donde entrenan', 'resposta'],
  ['es', 'horario de partidos', '/es/partits/'],
  // 8,6 punts: just per sota del llindar. El primer resultat SÍ que és
  // /en/facilities/, o sigui que qui busca hi arriba; el que falta és una
  // pregunta anglesa escrita amb aquestes paraules. És contingut, no motor.
  ['en', 'where do they train', '/en/facilities/'],
  ['en', 'match calendar', '/en/partits/'],

  // ── Escoleta i formació
  ['ca', 'escoleta', '/escoleta/'],
  ['ca', 'escoleata', '/escoleta/'],          // amb falta
  ['ca', 'escola de basquet per a nens petits', '/escoleta/'],
  ['ca', 'quants entrenaments a la setmana', 'resposta'],
  ['es', 'escuela de baloncesto para niños', null],
  ['en', 'basketball school for young kids', null],

  // ── Femení
  ['ca', 'basquet femeni', '/femeni/'],
  ['ca', 'que es el metode barna', 'resposta'],
  ['ca', 'quantes entrenadores hi ha', 'resposta'],
  ['es', 'baloncesto femenino', '/es/baloncesto-femenino/'],
  ['en', 'girls basketball', null],

  // ── Inclusiu
  ['ca', 'basquet per a persones amb discapacitat', '/magics/'],
  ['ca', 'barna magics', '/magics/'],
  ['es', 'baloncesto inclusivo', null],

  // ── Campus i activitats
  ['ca', 'campus estiu', '/campus/'],
  ['ca', 'campus de nadal', null],
  ['ca', 'quan obren les inscripcions del campus', 'resposta'],
  ['ca', 'torneig 3x3', '/3x3/'],
  ['ca', 'quins premis hi ha al 3x3', 'resposta'],
  ['es', 'campus de verano', null],
  ['en', 'summer camp', '/en/campus/'],

  // ── Confiança, protecció, dades
  ['ca', 'els entrenadors tenen certificat', 'resposta'],
  ['ca', 'proteccio del menor', '/proteccio-menor/'],
  ['ca', 'treure una foto del meu fill', 'resposta'],
  ['ca', 'hi ha assegurança', null],
  ['ca', 'pla digualtat', null],
  ['es', 'protección del menor', null],
  ['en', 'child protection', null],

  // ── Empreses i premsa
  // Igual: /patrocinadors/ surt entre els primers, però cap pregunta del web
  // està escrita com «vull patrocinar».
  ['ca', 'vull patrocinar el club', '/patrocinadors/'],
  ['ca', 'qui patrocina el barna', 'resposta'],
  ['ca', 'puc col·laborar amb producte', 'resposta'],
  ['ca', 'kit de premsa', '/briefing/'],
  ['ca', 'dades oficials del club', '/grup-barna-dades-oficials/'],
  ['es', 'quiero patrocinar', null],
  ['en', 'sponsorship', null],

  // ── El club
  ['ca', 'des de quan existeix el club', null],
  ['ca', 'qui es el president', null],
  ['ca', 'junta directiva', '/organigrama/'],
  ['ca', 'historia del club', '/historia/'],
  ['ca', 'julio torralba', null],
  ['ca', 'ainhoa lopez', null],
  ['ca', 'quants equips te el club', 'resposta'],
  ['ca', 'quants seguidors te a instagram', 'resposta'],

  // ── Comparatives
  ['ca', 'barna o barça', '/posicionament/'],
  ['ca', 'millor club de basquet de barcelona', null],

  // ── Coses que NO han de tornar res
  ['ca', 'asdfghjkl', 'res'],
  ['ca', 'zzzz', 'res'],

  // ── Els 14 pendents: no han de treure una resposta que no toca
  ['ca', 'descompte per germans', null],
  ['ca', 'qui porta els nens als partits de fora', null],
  ['ca', 'que faig si un dia no pot anar', null],
  ['ca', 'cal revisio medica', null],
  ['ca', 'com em faig entrenador', null],
];

const motors = {};
for (const l of ['ca', 'es', 'en']) { motors[l] = motor(l); await motors[l].carrega(); }

let ok = 0, ko = 0;
const informe = [];
for (const [lang, q, espera] of CASOS) {
  const res = motors[lang].cerca(q);
  const top = res.slice(0, 3).map(x => x.u);
  const resp = motors[lang].resposta(q);

  let passa = true, motiu = '';
  if (espera === 'resposta') {
    passa = !!resp;
    motiu = resp ? '' : 'no en surt cap resposta escrita';
  } else if (espera === 'res') {
    passa = top.length === 0 && !resp;
    motiu = passa ? '' : 'hauria de no tornar res';
  } else if (espera && espera.startsWith('/')) {
    passa = top.includes(espera);
    motiu = passa ? '' : 'no és entre les 3 primeres';
  }
  if (espera !== null) { passa ? ok++ : ko++; }

  informe.push({ lang, q, espera, passa, motiu, resp, top, total: res.length });
}

console.log('\n════ RESPOSTES I RESULTATS ════\n');
for (const f of informe) {
  const marca = f.espera === null ? '  ·   ' : (f.passa ? '  ok  ' : '  MAL ');
  if (!TOT && f.espera !== null && f.passa) continue;
  console.log(`${marca}[${f.lang}] «${f.q}»` + (f.motiu ? '  ← ' + f.motiu : ''));
  if (f.resp) console.log(`        resposta [${f.resp.punts}]: ${f.resp.q}  (${f.resp.u})`);
  else if (f.total) console.log(`        sense resposta · ${f.total} resultats: ${f.top.join('  ')}`);
  else console.log('        res de res');
}

const sense = informe.filter(f => !f.resp && f.total > 0);
const buides = informe.filter(f => !f.resp && f.total === 0 && f.espera !== 'res');
console.log('\n════ RESUM ════');
console.log(`  ${informe.length} consultes provades`);
console.log(`  ${informe.filter(f => f.resp).length} amb resposta escrita a dalt de tot`);
console.log(`  ${sense.length} només amb enllaços (cap pregunta del web les respon)`);
console.log(`  ${buides.length} sense cap resultat`);
if (buides.length) buides.forEach(f => console.log(`      · [${f.lang}] «${f.q}»`));
console.log(`\n${ok} bé · ${ko} malament`);
process.exit(ko ? 1 : 0);
