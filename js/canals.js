/* CB Grup Barna · Configuració dels canals d'entrada
   ───────────────────────────────────────────────────────────────
   Aquest és l'ÚNIC fitxer que cal tocar per activar la newsletter,
   la bústia de suggeriments i el canal de protecció del menor.
   No cal tocar cap HTML.
   ─────────────────────────────────────────────────────────────── */
window.CANALS = {

  /* 1 · NEWSLETTER ────────────────────────────────────────────────
     Mentre `brevoAction` estigui buit, les altes es guarden a la
     mateixa full de càlcul que ja fem servir a /fotos/ (funciona,
     però els correus s'han d'enviar a mà).

     Per activar Brevo:
       1. Entra a brevo.com amb el compte del club.
       2. Contactes → Formularis → Crea un formulari.
       3. Publica'l i tria «Comparteix l'enllaç» o «Codi HTML».
       4. Del codi, copia el valor de action="…" del <form>.
          Té aquesta pinta:
          https://sibforms.com/serve/MUIFAK...  (o .../integration/...)
       5. Enganxa'l aquí sota i desa. Res més.                       */
  brevoAction: '',

  /* Noms dels camps al formulari de Brevo. Només cal canviar-los si
     a Brevo has anomenat els atributs d'una altra manera.           */
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
