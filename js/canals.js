/* CB Grup Barna · Configuració dels canals d'entrada
   ───────────────────────────────────────────────────────────────
   Aquest és l'ÚNIC fitxer que cal tocar per activar la newsletter,
   la bústia de suggeriments i el canal de protecció del menor.
   No cal tocar cap HTML.
   ─────────────────────────────────────────────────────────────── */
window.CANALS = {

  /* 1 · BREVO · el CRM del club ───────────────────────────────────
     Tots els formularis del web han d'acabar a Brevo. Cadascun té el
     seu propi formulari a Brevo, i cada formulari de Brevo aboca a la
     seva pròpia llista: així les altes de la newsletter no es barregen
     amb qui només demana informació, que no ha donat cap permís
     comercial.

     Com s'omple cada línia (es fa un cop per formulari):
       1. Entra a brevo.com amb el compte del club.
       2. Contactes → Formularis → Crea un formulari.
       3. Posa-hi els camps que diu /js/README-brevo.md per aquest
          canal i tria la llista de destí.
       4. Publica'l i obre «Comparteix → Codi HTML».
       5. Del codi, copia el valor de action="…" de l'etiqueta <form>.
          Té aquesta pinta: https://sibforms.com/serve/MUIFAK...
       6. Enganxa'l a la línia que toca aquí sota i desa. Res més.

     Mentre una línia estigui buida, aquell formulari segueix funcionant
     exactament com fins ara (full de càlcul, Formspree o WhatsApp): no
     es perd cap alta, però no arriba al CRM. Es poden activar d'un en un.

     ⚠️  Aquí no hi va MAI cap clau d'API de Brevo. La web és estàtica i
     qualsevol pot llegir aquest fitxer. Els formularis allotjats a Brevo
     no en necessiten cap.                                            */
  brevo: {

    formularis: {
      newsletter:     '',   // /newsletter/            → llista «Newsletter»
      portada:        '',   // formulari gran de la portada → «Vull informació»
      informacio:     '',   // /escriu-nos/            → «Vull informació»
      portesObertes:  '',   // /portes-obertes/        → «Portes obertes»
      bustia:         '',   // /bustia/ (només si deixen el correu) → «Bústia»
      ressenya:       '',   // /opina/                 → «Ressenyes»
      descarrega:     '',   // finestra de descàrrega de documents → «Descàrregues»
      galeria:        ''    // /fotos/ i /galeria-3x3-glories/ → «Galeria»
    },

    /* Noms dels atributs a Brevo. Només cal tocar-ho si al compte del
       club se'n diuen d'una altra manera. La llista completa, amb el
       tipus de cada atribut, és a /js/README-brevo.md.               */
    camps: {
      email:     'EMAIL',
      nom:       'NOM',
      telefon:   'TELEFON',
      idioma:    'IDIOMA',
      origen:    'ORIGEN',
      interes:   'INTERES',
      tema:      'TEMA',
      missatge:  'MISSATGE',
      any:       'ANY_NAIX',
      contacte:  'CONTACTE',
      estrelles: 'ESTRELLES',
      consent:   'CONSENT',
      campanya:  'CAMPANYA',
      font:      'FONT',
      mitja:     'MITJA',
      referent:  'REFERENT',
      entrada:   'ENTRADA'
    }
  },

  /* Compatibilitat: si algú ja tenia posat l'action de la newsletter
     aquí, segueix valent. El lloc nou és brevo.formularis.newsletter. */
  brevoAction: '',
  brevoCamps: { email: 'EMAIL', nom: 'NOM' },


  /* 2 · BÚSTIA DE SUGGERIMENTS ────────────────────────────────────
     Va a la mateixa Apps Script que la resta de formularis del web,
     marcada amb source: 'bustia' perquè es pugui filtrar a la full.  */
  bustiaEndpoint: 'https://script.google.com/macros/s/AKfycbwXY1zBr9TH-gwOS3fo6tUqj9Sj7ExHv33un3VLtBHz58QNThlR3DdUnrB-xjtQri9g/exec',


  /* 3 · CANAL DE PROTECCIÓ DEL MENOR ──────────────────────────────
     ⚠️  DELIBERADAMENT BUIT. No hi posis l'endpoint de dalt.

     El que s'envia per aquest canal són comunicacions sobre la
     seguretat d'infants, i NO poden acabar a la mateixa full de
     càlcul que les inscripcions i els suggeriments: hi té accés
     més gent de la que ha de veure això.

     Mentre estigui buit, la pàgina /proteccio-menor/comunicar/
     amaga el formulari i mostra el correu de la Delegada de
     Protecció, que és un canal vàlid i ja funciona. No hi ha res
     trencat: és el comportament segur.

     Per activar-lo cal una Apps Script NOVA, amb un full de càlcul
     NOU, compartit NOMÉS amb la Delegada de Protecció al Menor.
     Instruccions a /js/README-canals.md                            */
  proteccioEndpoint: '',
};
