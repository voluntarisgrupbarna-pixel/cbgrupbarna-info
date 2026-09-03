/* CB Grup Barna · Avís de les Portes Obertes de l'Escoleta
   ─────────────────────────────────────────────────────────────────────────
   Una barra fina a dalt de tot, a totes les pàgines del web, que porta a
   /portes-obertes/. És la campanya de setembre: mentre hi hagi places,
   qualsevol pàgina del club ha de poder-hi portar.

   Es pinta amb JavaScript, com el botó ≡ i l'avís de galetes, perquè no
   calgui tocar el marcatge de ~380 pàgines. L'aplica
   scripts/avis-aplica.py.

   Tres coses que fa bé:
     · Es tanca, i recorda que s'ha tancat (localStorage) fins que canvia
       la campanya. Un avís que no es pot fer callar és publicitat.
     · CADUCA SOLA el 27 de setembre: passada la data, no es pinta. Res
       caducat a la portada, que és la regla 5 del sistema.
     · No surt a /portes-obertes/, que és on porta: allà ja hi ets.
   ───────────────────────────────────────────────────────────────────────── */
(function () {
  'use strict';

  /* Fins quan es veu. L'endemà de l'últim dissabte deixa de pintar-se sol:
     no cal recordar-se de treure'l. Format any-mes-dia (mes de 0 a 11). */
  var CADUCA = new Date(2026, 8, 27, 23, 59);

  /* Puja aquesta clau si es canvia el text: qui l'havia tancat el torna a
     veure una vegada, perquè l'avís nou no neix ja amagat. */
  var CLAU = 'cbgb-avis-po-2026-09';

  var DESTI = { ca: '/portes-obertes/#po-form', es: '/es/puertas-abiertas/#po-form', en: '/en/open-days/#po-form' };

  var TEXTOS = {
    ca: {
      etiqueta: 'Escoleta',
      text: 'Portes obertes els dissabtes 19 i 26 de setembre, a les 9 h',
      crida: 'Reserva la plaça',
      tanca: 'Tanca l\'avís'
    },
    es: {
      etiqueta: 'Escoleta',
      text: 'Puertas abiertas los sábados 19 y 26 de septiembre, a las 9 h',
      crida: 'Reserva la plaza',
      tanca: 'Cerrar el aviso'
    },
    en: {
      etiqueta: 'Escoleta',
      text: 'Open days on Saturday 19 and 26 September, at 9 am',
      crida: 'Book a place',
      tanca: 'Close this notice'
    }
  };

  // Passada la data, res. Abans que qualsevol altra comprovació.
  if (new Date() > CADUCA) return;

  // A la pàgina de destinació no hi pinta res.
  var ruta = location.pathname;
  if (/\/(portes-obertes|puertas-abiertas|open-days)\//.test(ruta)) return;

  // Ni a l'admin ni a les peces per imprimir.
  if (ruta.indexOf('/admin/') === 0 || /\/(flyer|print)\//.test(ruta)) return;

  try {
    if (localStorage.getItem(CLAU) === 'tancat') return;
  } catch (e) { /* sense localStorage, l'avís surt igual */ }

  var codi = (document.documentElement.lang || 'ca').slice(0, 2).toLowerCase();
  var t = TEXTOS[codi] || TEXTOS.ca;
  var desti = DESTI[codi] || DESTI.ca;

  var est = document.createElement('style');
  est.textContent =
    '.cbgb-po{position:relative;z-index:130;background:#E20613;color:#fff;' +
    "font-family:'Inter',-apple-system,BlinkMacSystemFont,system-ui,sans-serif}" +
    '.cbgb-po-in{max-width:1240px;margin:0 auto;padding:9px clamp(14px,4vw,44px);' +
    'display:flex;align-items:center;gap:12px;flex-wrap:wrap}' +
    ".cbgb-po b{font-family:'Anton','Haettenschweiler','Arial Narrow',sans-serif;" +
    'font-weight:400;font-size:11px;letter-spacing:.22em;text-transform:uppercase;' +
    'background:#10100E;color:#fff;padding:5px 10px;flex-shrink:0}' +
    '.cbgb-po p{margin:0;font-size:13px;line-height:1.45;flex:1 1 auto;min-width:0}' +
    /* El groc només a la lletra i sobre el vermell fosc, mai al fons blanc:
       és la regla del sistema (web-cbgb, punt 1). */
    '.cbgb-po a.cbgb-po-cta{color:#EEFF00;font-weight:700;text-decoration:underline;' +
    'text-underline-offset:3px;font-size:12.5px;letter-spacing:.06em;white-space:nowrap;' +
    'flex-shrink:0;padding:4px 0}' +
    '.cbgb-po a.cbgb-po-cta:hover{color:#fff}' +
    '.cbgb-po button{appearance:none;background:transparent;border:1px solid rgba(255,255,255,.45);' +
    'color:#fff;width:30px;height:30px;min-width:30px;cursor:pointer;font-size:15px;line-height:1;' +
    'flex-shrink:0;margin-left:auto;border-radius:50%}' +
    '.cbgb-po button:hover{background:#fff;color:#E20613;border-color:#fff}' +
    '.cbgb-po :focus-visible{outline:3px solid #fff;outline-offset:2px}' +
    '@media(max-width:560px){.cbgb-po p{font-size:12px;flex-basis:100%;order:3}' +
    '.cbgb-po button{order:2}}' +
    '@media print{.cbgb-po{display:none}}';
  document.head.appendChild(est);

  var barra = document.createElement('aside');
  barra.className = 'cbgb-po';
  barra.setAttribute('aria-label', t.etiqueta);

  var dins = document.createElement('div');
  dins.className = 'cbgb-po-in';

  var etiqueta = document.createElement('b');
  etiqueta.textContent = t.etiqueta;

  var text = document.createElement('p');
  text.textContent = t.text;

  var cta = document.createElement('a');
  cta.className = 'cbgb-po-cta';
  cta.href = desti;
  cta.textContent = t.crida + ' →';
  cta.setAttribute('data-cta', 'avis-portes-obertes');

  var tanca = document.createElement('button');
  tanca.type = 'button';
  tanca.setAttribute('aria-label', t.tanca);
  tanca.textContent = '×';
  tanca.addEventListener('click', function () {
    barra.remove();
    try { localStorage.setItem(CLAU, 'tancat'); } catch (e) {}
  });

  dins.appendChild(etiqueta);
  dins.appendChild(text);
  dins.appendChild(cta);
  dins.appendChild(tanca);
  barra.appendChild(dins);

  // A dalt de tot, abans de la capçalera enganxada: així no la tapa ni li
  // menja l'espai quan es fa scroll.
  function planta() {
    if (document.body.firstChild) document.body.insertBefore(barra, document.body.firstChild);
    else document.body.appendChild(barra);
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', planta);
  } else {
    planta();
  }
})();
