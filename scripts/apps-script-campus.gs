/**
 * CB Grup Barna · Llista d'espera del campus
 * ──────────────────────────────────────────────────────────────────────────
 * Aquest fitxer NO s'executa al web: és el codi que ha de viure a Google
 * Apps Script. El web només hi envia un POST amb JSON (js/llista-espera.js).
 *
 * Fa tres coses, per aquest ordre:
 *   1. Escriu una fila a la full de càlcul de la llista d'espera.
 *   2. Envia un avís al club (AVIS_A) dient que hi ha una inscripció nova.
 *   3. Envia una confirmació a qui s'ha apuntat, amb còpia del que ha escrit.
 *
 * Si el correu de confirmació falla (adreça inventada, quota diària esgotada),
 * la fila ja és a la full i l'avís al club ja ha sortit: no es perd ningú.
 *
 * ─── COM ES POSA EN MARXA (10 minuts, una sola vegada) ────────────────────
 *  1. Crea un full de càlcul nou a Google Drive amb el compte del club i
 *     posa-li de nom «Campus · llista d'espera».
 *  2. Dins del full: Extensions → Apps Script.
 *  3. Esborra el que hi hagi i enganxa TOT aquest fitxer.
 *  4. Canvia AVIS_A si el correu d'avís ha d'anar a una altra adreça.
 *  5. Desa i fes Desplega → Nou desplegament → tipus «Aplicació web»:
 *        Executa com a:        jo (el compte del club)
 *        Qui hi té accés:      Qualsevol
 *     Google demanarà permisos (full de càlcul i enviar correu): accepta'ls.
 *  6. Copia l'URL que acaba en /exec i enganxa'l a js/canals.js, al camp
 *     `campusEndpoint`. Res més: el formulari ja hi apunta.
 *
 * Per provar-ho: apunta't tu mateix des de /campus/#llista-espera i mira
 * que arribin els dos correus i la fila.
 * ─────────────────────────────────────────────────────────────────────────
 */

/** On arriba l'avís de cada inscripció nova. */
var AVIS_A = 'marqueting@cbgrupbarna.info';

/** Nom que veurà qui rebi els correus. */
var REMITENT = 'CB Grup Barna';

/** Full de dins del document on s'escriuen les files. */
var FULLA = 'Llista espera';

var CAPCALERES = [
  'Data', 'Jugador/a', 'Any', 'Qui apunta', 'Correu', 'Telèfon',
  'Edicions', 'Missatge', 'Idioma', 'Origen'
];

function doPost(e) {
  var d = {};
  try {
    d = JSON.parse(e.postData.contents) || {};
  } catch (err) {
    return resposta({ ok: false, error: 'json' });
  }

  var fila = [
    new Date(),
    net(d.nom), net(d.any), net(d.tutor), net(d.correu), net(d.telefon),
    net(d.edicions), net(d.missatge), net(d.idioma), net(d.source)
  ];

  desa(fila);

  // L'avís al club va primer: encara que la confirmació peti, el club se
  // n'assabenta igual i pot escriure a mà.
  try { avisaClub(d); } catch (err) {}
  try { confirmaFamilia(d); } catch (err) {}

  return resposta({ ok: true });
}

/** Escriu la fila, creant el full i les capçaleres el primer cop. */
function desa(fila) {
  var doc = SpreadsheetApp.getActiveSpreadsheet();
  var full = doc.getSheetByName(FULLA);
  if (!full) {
    full = doc.insertSheet(FULLA);
    full.appendRow(CAPCALERES);
    full.getRange(1, 1, 1, CAPCALERES.length).setFontWeight('bold');
    full.setFrozenRows(1);
  }
  full.appendRow(fila);
}

function avisaClub(d) {
  var assumpte = 'Llista d\'espera del campus · ' + net(d.nom) + ' (' + net(d.any) + ')';
  var cos =
    'Inscripció nova a la llista d\'espera del campus.\n\n' +
    'Jugador/a:   ' + net(d.nom) + '\n' +
    'Any:         ' + net(d.any) + '\n' +
    'Qui apunta:  ' + net(d.tutor) + '\n' +
    'Correu:      ' + net(d.correu) + '\n' +
    'Telèfon:     ' + (net(d.telefon) || '—') + '\n' +
    'Edicions:    ' + (net(d.edicions) || '—') + '\n' +
    'Idioma web:  ' + net(d.idioma) + '\n\n' +
    'Missatge:\n' + (net(d.missatge) || '—') + '\n\n' +
    'La fila ja és a la full de càlcul de la llista d\'espera.';
  MailApp.sendEmail({ to: AVIS_A, subject: assumpte, body: cos, name: REMITENT,
                      replyTo: net(d.correu) || AVIS_A });
}

function confirmaFamilia(d) {
  var correu = net(d.correu);
  if (!correu) return;
  var t = TEXTOS[net(d.idioma)] || TEXTOS.ca;
  var cos = t.cos
    .replace('{tutor}', net(d.tutor) || '')
    .replace('{nom}', net(d.nom) || '')
    .replace('{any}', net(d.any) || '')
    .replace('{edicions}', net(d.edicions) || t.cap_edicio);
  MailApp.sendEmail({ to: correu, subject: t.assumpte, body: cos, name: REMITENT,
                      replyTo: AVIS_A });
}

/* Confirmació en els tres idiomes del web: qui s'apunta en anglès no ha de
   rebre un correu en català. */
var TEXTOS = {
  ca: {
    assumpte: 'Ja ets a la llista d\'espera del campus del CB Grup Barna',
    cap_edicio: 'totes',
    cos:
      'Hola {tutor},\n\n' +
      'Ja tenim {nom} ({any}) a la llista d\'espera del campus de bàsquet del ' +
      'CB Grup Barna. Edicions que ens has dit: {edicions}.\n\n' +
      'Què passa ara: t\'escrivim quan obrim inscripcions, un dia abans de ' +
      'publicar-ho. El campus de Nadal s\'anuncia molt aviat; al gener ' +
      'publiquem Setmana Santa i estiu.\n\n' +
      'Mentrestant, tota la informació del campus és aquí:\n' +
      'https://cbgrupbarna.info/campus/\n' +
      'I la presentació del campus, aquí:\n' +
      'https://cbgrupbarna.info/presentacions/campus-timechamber/\n\n' +
      'Si tens qualsevol dubte, respon aquest correu o escriu-nos al ' +
      'WhatsApp del club: +34 698 425 153.\n\n' +
      'CB Grup Barna · La Nau del Clot\n' +
      'Carrer de la Llacuna 170-172, 08018 Barcelona'
  },
  es: {
    assumpte: 'Ya estás en la lista de espera del campus del CB Grup Barna',
    cap_edicio: 'todas',
    cos:
      'Hola {tutor}:\n\n' +
      'Ya tenemos a {nom} ({any}) en la lista de espera del campus de ' +
      'baloncesto del CB Grup Barna. Ediciones que nos has dicho: {edicions}.\n\n' +
      'Qué pasa ahora: te escribimos cuando abramos inscripciones, un día ' +
      'antes de publicarlo. El campus de Navidad se anuncia muy pronto; en ' +
      'enero publicamos Semana Santa y verano.\n\n' +
      'Mientras tanto, toda la información del campus está aquí:\n' +
      'https://cbgrupbarna.info/es/campus/\n' +
      'Y la presentación del campus, aquí:\n' +
      'https://cbgrupbarna.info/es/presentaciones/campus-timechamber/\n\n' +
      'Si tienes cualquier duda, responde a este correo o escríbenos al ' +
      'WhatsApp del club: +34 698 425 153.\n\n' +
      'CB Grup Barna · La Nau del Clot\n' +
      'Carrer de la Llacuna 170-172, 08018 Barcelona'
  },
  en: {
    assumpte: 'You are on the CB Grup Barna camp waiting list',
    cap_edicio: 'all of them',
    cos:
      'Hi {tutor},\n\n' +
      '{nom} ({any}) is on the waiting list for the CB Grup Barna basketball ' +
      'camp. Editions you told us about: {edicions}.\n\n' +
      'What happens next: we write to you when registration opens, a day ' +
      'before we publish it. The Christmas camp is announced very soon; in ' +
      'January we publish Easter and summer.\n\n' +
      'In the meantime, everything about the camp is here:\n' +
      'https://cbgrupbarna.info/en/campus/\n' +
      'And the camp presentation is here:\n' +
      'https://cbgrupbarna.info/en/presentations/campus-timechamber/\n\n' +
      'Any questions, reply to this email or write to the club on WhatsApp: ' +
      '+34 698 425 153.\n\n' +
      'CB Grup Barna · La Nau del Clot\n' +
      'Carrer de la Llacuna 170-172, 08018 Barcelona'
  }
};

function net(v) {
  return String(v === undefined || v === null ? '' : v).slice(0, 2000).trim();
}

function resposta(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
