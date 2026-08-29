/**
 * CB Grup Barna · Afegit per a l'Apps Script que JA està desplegada
 * ─────────────────────────────────────────────────────────────────────────
 * QUÈ ÉS AIXÒ, I PER QUÈ EXISTEIX
 *
 * Hi ha dues maneres de fer funcionar la llista d'espera del campus:
 *
 *   A) Desplegar una Apps Script NOVA  →  scripts/apps-script-campus.gs
 *      Full de càlcul propi, projecte propi, desplegament propi. Més net,
 *      però són sis passos i un desplegament des de zero.
 *
 *   B) Afegir aquest tros a l'Apps Script que el club JA té desplegada
 *      (la de la bústia, la que fa anar /bustia/ i /portes-obertes/).
 *      No cal crear cap full ni cap projecte: només enganxar això al final
 *      del codi que ja hi ha i tornar a desplegar.
 *
 * Aquest fitxer és l'opció B, que és la curta.
 *
 * ─── PASSOS (tres) ───────────────────────────────────────────────────────
 *  1. Obre l'Apps Script de la bústia (el full de càlcul de sempre →
 *     Extensions → Apps Script).
 *  2. Enganxa TOT aquest fitxer al final del codi que ja hi ha, sense
 *     esborrar res del que hi havia.
 *  3. Desplega → Gestiona desplegaments → edita el que ja existeix →
 *     Versió: «Nova versió» → Desplega.
 *     Google demanarà un permís nou (enviar correu): accepta'l.
 *
 * L'URL /exec no canvia, i js/canals.js ja hi apunta: no cal tocar el web.
 *
 * ─── QUÈ CAL QUE FACI EL doPost QUE JA HI HA ─────────────────────────────
 * Al final del doPost existent, just abans de retornar, afegeix-hi una línia:
 *
 *     avisaSiEsLlistaEspera(d);      // d = l'objecte amb les dades rebudes
 *
 * Si la variable amb les dades es diu d'una altra manera, passa-li aquella.
 * Aquesta funció no fa res si el formulari no és el de la llista d'espera,
 * així que la resta de canals (bústia, portes obertes, newsletter) segueixen
 * igual que sempre.
 *
 * ─── I LES DADES? ────────────────────────────────────────────────────────
 * Van a la mateixa full que la resta, marcades amb
 * source: 'campus-llista-espera'. No és cap novetat de protecció de dades:
 * /portes-obertes/ ja hi envia nom i any de naixement de criatures des del
 * primer dia. Si algun dia es vol separar, aleshores sí que toca l'opció A.
 * ─────────────────────────────────────────────────────────────────────────
 */

/** On arriba l'avís de cada alta nova. */
var CAMPUS_AVIS_A = 'marqueting@cbgrupbarna.info';

/**
 * Envia els dos correus d'una alta de la llista d'espera del campus.
 * No fa res si l'enviament ve de qualsevol altre formulari.
 */
function avisaSiEsLlistaEspera(d) {
  if (!d || String(d.source || '') !== 'campus-llista-espera') return;

  var nom = camp(d.nom), any = camp(d.any), tutor = camp(d.tutor);
  var correu = camp(d.correu), edicions = camp(d.edicions) || '—';

  // Primer l'avís al club: encara que la confirmació peti, el club se'n
  // assabenta i pot escriure a mà.
  try {
    MailApp.sendEmail({
      to: CAMPUS_AVIS_A,
      name: 'CB Grup Barna',
      replyTo: correu || CAMPUS_AVIS_A,
      subject: 'Llista d\'espera del campus · ' + nom + ' (' + any + ')',
      body:
        'Alta nova a la llista d\'espera del campus.\n\n' +
        'Jugador/a:  ' + nom + '\n' +
        'Any:        ' + any + '\n' +
        'Qui apunta: ' + tutor + '\n' +
        'Correu:     ' + correu + '\n' +
        'Telèfon:    ' + (camp(d.telefon) || '—') + '\n' +
        'Edicions:   ' + edicions + '\n' +
        'Idioma web: ' + camp(d.idioma) + '\n\n' +
        'Missatge:\n' + (camp(d.missatge) || '—') + '\n\n' +
        'La fila ja és a la full de sempre, amb source: campus-llista-espera.'
    });
  } catch (err) {}

  // I la confirmació a la família, en el seu idioma.
  if (!correu) return;
  var t = CAMPUS_TEXTOS[camp(d.idioma)] || CAMPUS_TEXTOS.ca;
  try {
    MailApp.sendEmail({
      to: correu,
      name: 'CB Grup Barna',
      replyTo: CAMPUS_AVIS_A,
      subject: t.assumpte,
      body: t.cos.replace('{tutor}', tutor).replace('{nom}', nom)
                 .replace('{any}', any).replace('{edicions}', edicions)
    });
  } catch (err) {}
}

var CAMPUS_TEXTOS = {
  ca: {
    assumpte: 'Ja ets a la llista d\'espera del campus del CB Grup Barna',
    cos:
      'Hola {tutor},\n\n' +
      'Ja tenim {nom} ({any}) a la llista d\'espera del campus de bàsquet del ' +
      'CB Grup Barna. Edicions que ens has dit: {edicions}.\n\n' +
      'Què passa ara: t\'escrivim quan obrim inscripcions, un dia abans de ' +
      'publicar-ho. El campus de Nadal s\'anuncia molt aviat; al gener ' +
      'publiquem Setmana Santa i estiu.\n\n' +
      'Tota la informació del campus:\n' +
      'https://cbgrupbarna.info/campus/\n\n' +
      'Qualsevol dubte, respon aquest correu o escriu-nos al WhatsApp del ' +
      'club: +34 698 425 153.\n\n' +
      'CB Grup Barna · La Nau del Clot\n' +
      'Carrer de la Llacuna 170-172, 08018 Barcelona'
  },
  es: {
    assumpte: 'Ya estás en la lista de espera del campus del CB Grup Barna',
    cos:
      'Hola {tutor}:\n\n' +
      'Ya tenemos a {nom} ({any}) en la lista de espera del campus de ' +
      'baloncesto del CB Grup Barna. Ediciones que nos has dicho: {edicions}.\n\n' +
      'Qué pasa ahora: te escribimos cuando abramos inscripciones, un día ' +
      'antes de publicarlo. El campus de Navidad se anuncia muy pronto; en ' +
      'enero publicamos Semana Santa y verano.\n\n' +
      'Toda la información del campus:\n' +
      'https://cbgrupbarna.info/es/campus/\n\n' +
      'Cualquier duda, responde a este correo o escríbenos al WhatsApp del ' +
      'club: +34 698 425 153.\n\n' +
      'CB Grup Barna · La Nau del Clot\n' +
      'Carrer de la Llacuna 170-172, 08018 Barcelona'
  },
  en: {
    assumpte: 'You are on the CB Grup Barna camp waiting list',
    cos:
      'Hi {tutor},\n\n' +
      '{nom} ({any}) is on the waiting list for the CB Grup Barna basketball ' +
      'camp. Editions you told us about: {edicions}.\n\n' +
      'What happens next: we write to you when registration opens, a day ' +
      'before we publish it. The Christmas camp is announced very soon; in ' +
      'January we publish Easter and summer.\n\n' +
      'Everything about the camp:\n' +
      'https://cbgrupbarna.info/en/campus/\n\n' +
      'Any questions, reply to this email or write to the club on WhatsApp: ' +
      '+34 698 425 153.\n\n' +
      'CB Grup Barna · La Nau del Clot\n' +
      'Carrer de la Llacuna 170-172, 08018 Barcelona'
  }
};

function camp(v) {
  return String(v === undefined || v === null ? '' : v).slice(0, 2000).trim();
}

/**
 * Prova sense passar pel web: tria «provaLlistaEspera» al desplegable de
 * l'editor i clica Executa. Envia els dos correus a CAMPUS_AVIS_A.
 */
function provaLlistaEspera() {
  avisaSiEsLlistaEspera({
    source: 'campus-llista-espera', idioma: 'ca',
    nom: 'PROVA', any: '2014', tutor: 'Prova', correu: CAMPUS_AVIS_A,
    telefon: '', edicions: 'nadal', missatge: 'Correu de prova.'
  });
  Logger.log('Enviats els dos correus a ' + CAMPUS_AVIS_A);
}
