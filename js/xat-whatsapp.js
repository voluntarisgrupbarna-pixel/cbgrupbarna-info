/* ============================================================
   CB GRUP BARNA · Xat flotant connectat a WhatsApp
   ------------------------------------------------------------
   Botó flotant que ensenya un petit formulari (nom, telèfon,
   tema i missatge). En enviar-lo:
   1. Es desa a un Google Sheet i arriba un correu a l'Ana, via
      l'Apps Script descrit a FORMULARI-CONTACTE-WHATSAPP.md
      (cal desplegar-lo un cop i enganxar la URL a
      SHEETS_ENDPOINT, aquí sota).
   2. S'obre WhatsApp en una pestanya nova amb el mateix missatge
      ja escrit, perquè la persona el pugui enviar i l'Ana el
      rebi també allà — el contacte li arriba per dues vies.

   El pas 1 és "fire and forget": si SHEETS_ENDPOINT és buit o la
   petició falla (sense connexió, script no desplegat...), el
   formulari continua igualment cap a WhatsApp — mai bloqueja el
   contacte real per un problema del full de càlcul.

   Com que ara SÍ es recullen dades (nom i telèfon), el formulari
   porta la seva pròpia casella de consentiment que enllaça a la
   política de privacitat — igual que la resta de formularis del
   web. Això és diferent del consentiment de galetes
   (js/galetes.js): aquí la persona SEMPRE decideix activament
   escriure les seves dades i prémer «Enviar», per això no cal
   esperar cap banner per ensenyar aquest panell.

   Reobrir/tancar per codi: window.CBGB_XAT.obre() / .tanca()
   ============================================================ */
(function () {
  'use strict';

  var NUM = '34698425153'; // Ana · coordinadora, el mateix número que ja hi ha al peu

  // Enganxa aquí la URL de l'Apps Script (acaba en /exec) un cop desplegat.
  // Instruccions completes a FORMULARI-CONTACTE-WHATSAPP.md.
  var SHEETS_ENDPOINT = '';

  var TEXTOS = {
    ca: {
      launcherAria: 'Obre el xat de WhatsApp',
      launcherLbl: 'Contacta\'ns',
      tancarAria: 'Tanca el xat',
      titol: 'CB Grup Barna',
      subtitol: 'Ana · sol respondre en minuts',
      salutacio: 'Hola! 👋 Sóc l’Ana, coordinadora del club. Deixa\'m les teves dades i en què et puc ajudar:',
      etiqueta: 'Tema',
      nomLbl: 'El teu nom', nomPh: 'Nom i cognoms',
      telLbl: 'El teu telèfon', telPh: '600 000 000',
      missatgeLbl: 'Missatge (opcional)', missatgePh: 'Explica\'ns el que necessitis…',
      consentText: 'Accepto que CB Grup Barna faci servir aquestes dades per respondre\'m.',
      consentEnllac: 'Política de privacitat', consentHref: '/politica-de-privacitat/',
      enviar: 'Enviar i obrir WhatsApp',
      graciesTitol: 'Gràcies, ' , graciesText: 'S\'obre WhatsApp amb el missatge ja escrit: només cal que el premis enviar.',
      trucar: 'O truca al',
      temes: [
        { label: 'Informació general', text: 'Tinc una pregunta sobre el CB Grup Barna.' },
        { label: 'Escoleta i campus', text: 'M’interessa l’Escoleta o el Campus del CB Grup Barna. Podeu informar-me?' },
        { label: 'Patrocinis i empreses', text: 'Sóc una empresa interessada a col·laborar amb el CB Grup Barna.' },
        { label: 'Un altre tema', text: '' }
      ]
    },
    es: {
      launcherAria: 'Abrir el chat de WhatsApp',
      launcherLbl: 'Contáctanos',
      tancarAria: 'Cerrar el chat',
      titol: 'CB Grup Barna',
      subtitol: 'Ana · suele responder en minutos',
      salutacio: '¡Hola! 👋 Soy Ana, coordinadora del club. Déjame tus datos y en qué puedo ayudarte:',
      etiqueta: 'Tema',
      nomLbl: 'Tu nombre', nomPh: 'Nombre y apellidos',
      telLbl: 'Tu teléfono', telPh: '600 000 000',
      missatgeLbl: 'Mensaje (opcional)', missatgePh: 'Cuéntanos lo que necesites…',
      consentText: 'Acepto que CB Grup Barna use estos datos para responderme.',
      consentEnllac: 'Política de privacidad', consentHref: '/es/politica-de-privacidad/',
      enviar: 'Enviar y abrir WhatsApp',
      graciesTitol: '¡Gracias, ', graciesText: 'Se abre WhatsApp con el mensaje ya escrito: solo tienes que pulsar enviar.',
      trucar: 'O llama al',
      temes: [
        { label: 'Información general', text: 'Tengo una pregunta sobre el CB Grup Barna.' },
        { label: 'Escoleta y campus', text: 'Me interesa la Escoleta o el Campus del CB Grup Barna. ¿Podéis informarme?' },
        { label: 'Patrocinios y empresas', text: 'Soy una empresa interesada en colaborar con el CB Grup Barna.' },
        { label: 'Otro tema', text: '' }
      ]
    },
    en: {
      launcherAria: 'Open WhatsApp chat',
      launcherLbl: 'Contact us',
      tancarAria: 'Close chat',
      titol: 'CB Grup Barna',
      subtitol: 'Ana · usually replies within minutes',
      salutacio: 'Hi! 👋 I’m Ana, the club coordinator. Leave me your details and how I can help:',
      etiqueta: 'Topic',
      nomLbl: 'Your name', nomPh: 'Full name',
      telLbl: 'Your phone', telPh: '600 000 000',
      missatgeLbl: 'Message (optional)', missatgePh: 'Tell us what you need…',
      consentText: 'I agree that CB Grup Barna uses this data to reply to me.',
      consentEnllac: 'Privacy policy', consentHref: '/en/privacy-policy/',
      enviar: 'Send and open WhatsApp',
      graciesTitol: 'Thanks, ', graciesText: 'WhatsApp will open with the message ready — just press send.',
      trucar: 'Or call',
      temes: [
        { label: 'General information', text: 'I have a question about CB Grup Barna.' },
        { label: 'Escoleta & camps', text: 'I’m interested in the Escoleta or the Camp at CB Grup Barna. Could you tell me more?' },
        { label: 'Sponsorship & business', text: 'I’m a business interested in partnering with CB Grup Barna.' },
        { label: 'Something else', text: '' }
      ]
    }
  };

  function textos() {
    var codi = (document.documentElement.lang || 'ca').slice(0, 2).toLowerCase();
    return TEXTOS[codi] || TEXTOS.ca;
  }

  function enllacWa(text) {
    return 'https://wa.me/' + NUM + '?text=' + encodeURIComponent(text);
  }

  var ICONA_WA = '<svg viewBox="0 0 32 32" width="24" height="24" aria-hidden="true" focusable="false">' +
    '<path fill="#fff" d="M16.01 3C9.38 3 4 8.38 4 15.01c0 2.35.65 4.55 1.78 6.43L4 29l7.73-1.72a12 12 0 0 0 4.28.79h.01c6.63 0 12.01-5.38 12.01-12.01C28 8.38 22.64 3 16.01 3Zm0 21.88a9.85 9.85 0 0 1-5.02-1.37l-.36-.21-4.59 1.02 1.05-4.47-.24-.37a9.86 9.86 0 0 1-1.53-5.28c0-5.46 4.44-9.9 9.9-9.9 5.46 0 9.9 4.44 9.9 9.9 0 5.46-4.44 9.88-9.11 9.68Zm5.42-7.4c-.3-.15-1.75-.86-2.02-.96-.27-.1-.47-.15-.67.15-.2.3-.77.96-.94 1.15-.17.2-.35.22-.65.07-.3-.15-1.24-.46-2.36-1.46-.87-.78-1.46-1.74-1.63-2.04-.17-.3-.02-.46.13-.6.13-.13.3-.35.44-.52.15-.17.2-.3.3-.5.1-.2.05-.37-.02-.52-.07-.15-.67-1.62-.92-2.22-.24-.58-.49-.5-.67-.51h-.57c-.2 0-.52.07-.79.37-.27.3-1.04 1.02-1.04 2.48s1.07 2.88 1.22 3.08c.15.2 2.1 3.2 5.08 4.49.71.31 1.26.49 1.7.62.71.23 1.36.2 1.87.12.57-.09 1.75-.71 2-1.4.25-.68.25-1.27.17-1.4-.07-.12-.27-.2-.57-.35Z"/>' +
    '</svg>';

  var CSS = [
    '.cbgb-wa-launcher{position:fixed;left:18px;bottom:var(--cbgb-wa-bottom,18px);z-index:2147482900;',
    'height:54px;padding:0 20px 0 16px;border-radius:999px;background:#25D366;border:none;cursor:pointer;',
    'display:inline-flex;align-items:center;gap:9px;box-shadow:0 6px 24px rgba(16,16,14,.32);',
    'transition:bottom .25s ease,transform .2s ease,box-shadow .2s ease,padding .2s ease}',
    '.cbgb-wa-launcher:hover{background:#20b858;transform:translateY(-2px);box-shadow:0 10px 28px rgba(16,16,14,.4)}',
    '.cbgb-wa-launcher:focus-visible{outline:3px solid #10100E;outline-offset:3px}',
    ".cbgb-wa-launcher .lbl{font-family:'Anton','Futura',sans-serif;font-weight:400;font-size:11px;",
    'letter-spacing:.1em;text-transform:uppercase;color:#fff;white-space:nowrap}',
    '.cbgb-wa-launcher .x{display:none}',
    '.cbgb-wa-open .cbgb-wa-launcher{padding:0;width:54px;justify-content:center}',
    '.cbgb-wa-open .cbgb-wa-launcher .wa,.cbgb-wa-open .cbgb-wa-launcher .lbl{display:none}',
    '.cbgb-wa-open .cbgb-wa-launcher .x{display:block}',
    '@keyframes cbgbWaBounce{0%,20%,50%,80%,100%{transform:translateY(0)}40%{transform:translateY(-9px)}60%{transform:translateY(-4px)}}',
    '.cbgb-wa-launcher.avis{animation:cbgbWaBounce 1.4s ease 1}',
    '@media(prefers-reduced-motion:reduce){.cbgb-wa-launcher.avis{animation:none}}',
    '.cbgb-wa-panel{position:fixed;left:18px;bottom:calc(var(--cbgb-wa-bottom,18px) + 68px);z-index:2147482900;',
    'width:min(340px,calc(100vw - 32px));max-height:min(80vh,600px);overflow-y:auto;background:#fff;',
    'border-radius:16px;',
    "font-family:'Inter',-apple-system,BlinkMacSystemFont,system-ui,sans-serif;",
    'box-shadow:0 20px 60px rgba(16,16,14,.28);border:1px solid rgba(16,16,14,.1);',
    'transform-origin:bottom left;transform:scale(.92) translateY(8px);opacity:0;pointer-events:none;',
    'transition:transform .2s cubic-bezier(.22,1,.36,1),opacity .2s ease}',
    '.cbgb-wa-open .cbgb-wa-panel{transform:scale(1) translateY(0);opacity:1;pointer-events:auto}',
    '.cbgb-wa-head{position:sticky;top:0;background:#10100E;color:#fff;padding:16px 18px;',
    'border-left:3px solid #E20613;display:flex;align-items:center;gap:11px}',
    '.cbgb-wa-avatar{width:36px;height:36px;border-radius:50%;background:#E20613;flex-shrink:0;',
    "display:flex;align-items:center;justify-content:center;font-family:'Anton','Futura',sans-serif;",
    'font-weight:400;font-size:15px;color:#fff}',
    '.cbgb-wa-head h2{margin:0;font-size:13px;font-weight:600;line-height:1.3}',
    '.cbgb-wa-sub{margin:2px 0 0;font-size:11.5px;color:rgba(255,255,255,.7);display:flex;align-items:center;gap:6px}',
    '.cbgb-wa-dot{width:7px;height:7px;border-radius:50%;background:#3ddc73;flex-shrink:0;animation:cbgbWaPulse 2s infinite}',
    '@media(prefers-reduced-motion:reduce){.cbgb-wa-dot{animation:none}}',
    '@keyframes cbgbWaPulse{0%,100%{opacity:1}50%{opacity:.35}}',
    '.cbgb-wa-close{margin-left:auto;background:none;border:none;color:rgba(255,255,255,.7);',
    'cursor:pointer;padding:6px;line-height:0;flex-shrink:0}',
    '.cbgb-wa-close:hover,.cbgb-wa-close:focus-visible{color:#fff}',
    '.cbgb-wa-body{padding:16px 18px 18px}',
    '.cbgb-wa-bubble{background:#F4F1EC;color:#10100E;border-radius:4px 14px 14px 14px;',
    'padding:11px 13px;font-size:13.5px;line-height:1.5;margin:0 0 14px}',
    '.cbgb-wa-camp{margin:0 0 10px}',
    '.cbgb-wa-camp label{display:block;font-family:\'Anton\',\'Futura\',sans-serif;font-weight:400;',
    'font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:#6B6560;margin:0 0 5px}',
    '.cbgb-wa-camp input,.cbgb-wa-camp select,.cbgb-wa-camp textarea{width:100%;box-sizing:border-box;',
    "font-family:'Inter',sans-serif;font-size:13.5px;padding:9px 11px;border:1px solid rgba(16,16,14,.18);",
    'border-radius:9px;color:#10100E;background:#fff}',
    '.cbgb-wa-camp input:focus,.cbgb-wa-camp select:focus,.cbgb-wa-camp textarea:focus{outline:none;border-color:#25D366}',
    '.cbgb-wa-camp textarea{resize:vertical;min-height:56px}',
    '.cbgb-wa-consent{display:flex;align-items:flex-start;gap:8px;font-size:11.5px;color:#46433f;',
    'line-height:1.5;margin:2px 0 14px}',
    '.cbgb-wa-consent input{margin-top:2px;flex-shrink:0}',
    '.cbgb-wa-consent a{color:#46433f;border-bottom:1px solid rgba(16,16,14,.3);text-decoration:none}',
    '.cbgb-wa-consent a:hover{color:#A8040E;border-color:#A8040E}',
    '.cbgb-wa-submit{width:100%;background:#25D366;color:#fff;border:none;border-radius:10px;',
    "padding:12px 14px;font-family:'Anton','Futura',sans-serif;font-weight:400;font-size:11.5px;",
    'letter-spacing:.1em;text-transform:uppercase;cursor:pointer;transition:background .2s}',
    '.cbgb-wa-submit:hover{background:#20b858}',
    '.cbgb-wa-submit:disabled{opacity:.6;cursor:default}',
    '.cbgb-wa-foot{margin:12px 0 0;font-size:11.5px;color:#6B6560;text-align:center}',
    '.cbgb-wa-foot a{color:#46433f;border-bottom:1px solid rgba(16,16,14,.25);text-decoration:none}',
    '.cbgb-wa-foot a:hover{color:#A8040E;border-color:#A8040E}',
    '.cbgb-wa-gracies{padding:6px 2px 4px;font-size:13.5px;line-height:1.6;color:#10100E}',
    '.cbgb-wa-gracies b{display:block;font-family:\'Anton\',\'Futura\',sans-serif;font-weight:400;',
    'font-size:16px;letter-spacing:.02em;color:#178a45;margin:0 0 6px}',
    '@media(max-width:380px){.cbgb-wa-launcher{left:14px}.cbgb-wa-open .cbgb-wa-launcher{width:50px}',
    '.cbgb-wa-panel{left:14px;width:calc(100vw - 28px)}}'
  ].join('');

  var launcher, panel, wrap;

  function ajustaOffset() {
    var gal = document.querySelector('.cbgb-gal');
    var offset = gal ? Math.ceil(gal.getBoundingClientRect().height) + 14 : 18;
    document.documentElement.style.setProperty('--cbgb-wa-bottom', offset + 'px');
  }

  function tanca() {
    if (!wrap || !wrap.classList.contains('cbgb-wa-open')) return;
    wrap.classList.remove('cbgb-wa-open');
    launcher.setAttribute('aria-expanded', 'false');
    panel.setAttribute('aria-hidden', 'true');
    document.removeEventListener('keydown', escapa);
    document.removeEventListener('click', foraClic, true);
    launcher.focus();
  }

  function obre() {
    if (!wrap || wrap.classList.contains('cbgb-wa-open')) return;
    wrap.classList.add('cbgb-wa-open');
    launcher.setAttribute('aria-expanded', 'true');
    panel.setAttribute('aria-hidden', 'false');
    document.addEventListener('keydown', escapa);
    // El clic que obre el panell no l'ha de tancar de retruc.
    setTimeout(function () { document.addEventListener('click', foraClic, true); }, 0);
    var primer = panel.querySelector('input,select,button');
    if (primer) primer.focus();
  }

  function escapa(e) {
    if (e.key === 'Escape') tanca();
  }

  function foraClic(e) {
    if (wrap.contains(e.target)) return;
    tanca();
  }

  // Enviament: fire-and-forget cap al full de càlcul (si està configurat) i,
  // sempre, obertura de WhatsApp amb les mateixes dades ja escrites.
  function enviaDades(dades) {
    if (!SHEETS_ENDPOINT) return;
    try {
      fetch(SHEETS_ENDPOINT, {
        method: 'POST',
        mode: 'no-cors',
        body: JSON.stringify(dades)
      });
    } catch (e) { /* mai bloqueja el contacte per WhatsApp */ }
  }

  function pinta() {
    var est = document.createElement('style');
    est.textContent = CSS;
    document.head.appendChild(est);

    var t = textos();

    wrap = document.createElement('div');
    wrap.className = 'cbgb-wa';

    launcher = document.createElement('button');
    launcher.type = 'button';
    launcher.className = 'cbgb-wa-launcher';
    launcher.setAttribute('aria-haspopup', 'dialog');
    launcher.setAttribute('aria-expanded', 'false');
    launcher.setAttribute('aria-label', t.launcherAria);
    launcher.innerHTML = '<span class="wa">' + ICONA_WA + '</span>' +
      '<span class="lbl">' + t.launcherLbl + '</span>' +
      '<span class="x" aria-hidden="true" style="color:#fff;font-size:22px;font-weight:300;line-height:1">✕</span>';
    launcher.addEventListener('click', function () {
      if (wrap.classList.contains('cbgb-wa-open')) tanca(); else obre();
    });

    panel = document.createElement('div');
    panel.className = 'cbgb-wa-panel';
    panel.setAttribute('role', 'dialog');
    panel.setAttribute('aria-label', t.titol);
    panel.setAttribute('aria-hidden', 'true');

    var temesHtml = '';
    t.temes.forEach(function (tema, i) {
      temesHtml += '<option value="' + i + '">' + tema.label + '</option>';
    });

    panel.innerHTML =
      '<div class="cbgb-wa-head">' +
        '<div class="cbgb-wa-avatar">A</div>' +
        '<div>' +
          '<h2>' + t.titol + '</h2>' +
          '<p class="cbgb-wa-sub"><span class="cbgb-wa-dot" aria-hidden="true"></span>' + t.subtitol + '</p>' +
        '</div>' +
        '<button type="button" class="cbgb-wa-close" aria-label="' + t.tancarAria + '">' +
          '<svg width="18" height="18" viewBox="0 0 18 18" aria-hidden="true"><path stroke="currentColor" stroke-width="1.6" stroke-linecap="round" d="M2 2l14 14M16 2 2 16"/></svg>' +
        '</button>' +
      '</div>' +
      '<div class="cbgb-wa-body">' +
        '<p class="cbgb-wa-bubble">' + t.salutacio + '</p>' +
        '<form novalidate>' +
          '<div class="cbgb-wa-camp"><label for="cbgb-wa-nom">' + t.nomLbl + '</label>' +
            '<input type="text" id="cbgb-wa-nom" name="nom" placeholder="' + t.nomPh + '" autocomplete="name" required></div>' +
          '<div class="cbgb-wa-camp"><label for="cbgb-wa-tel">' + t.telLbl + '</label>' +
            '<input type="tel" id="cbgb-wa-tel" name="telefon" placeholder="' + t.telPh + '" autocomplete="tel" required></div>' +
          '<div class="cbgb-wa-camp"><label for="cbgb-wa-tema">' + t.etiqueta + '</label>' +
            '<select id="cbgb-wa-tema" name="tema">' + temesHtml + '</select></div>' +
          '<div class="cbgb-wa-camp"><label for="cbgb-wa-msg">' + t.missatgeLbl + '</label>' +
            '<textarea id="cbgb-wa-msg" name="missatge" placeholder="' + t.missatgePh + '"></textarea></div>' +
          '<label class="cbgb-wa-consent">' +
            '<input type="checkbox" id="cbgb-wa-consent" required>' +
            '<span>' + t.consentText + ' <a href="' + t.consentHref + '" target="_blank" rel="noopener">' + t.consentEnllac + '</a>.</span>' +
          '</label>' +
          '<button type="submit" class="cbgb-wa-submit">' + t.enviar + '</button>' +
        '</form>' +
        '<p class="cbgb-wa-foot">' + t.trucar + ' <a href="tel:+' + NUM + '">+34 698 425 153</a></p>' +
      '</div>';

    panel.querySelector('.cbgb-wa-close').addEventListener('click', tanca);

    panel.querySelector('form').addEventListener('submit', function (ev) {
      ev.preventDefault();
      var form = ev.target;
      if (!form.reportValidity()) return;

      var nom = form.nom.value.trim();
      var telefon = form.telefon.value.trim();
      var temaIdx = Number(form.tema.value);
      var tema = t.temes[temaIdx];
      var lliure = form.missatge.value.trim();

      var text = 'Hola! Sóc ' + nom + ' (tel. ' + telefon + '). ' + tema.label + '.';
      if (tema.text) text += ' ' + tema.text;
      if (lliure) text += ' ' + lliure;

      enviaDades({
        nom: nom, telefon: telefon, tema: tema.label, missatge: lliure,
        pagina: location.href, idioma: document.documentElement.lang || 'ca'
      });

      window.open(enllacWa(text), '_blank', 'noopener');

      panel.querySelector('.cbgb-wa-body').innerHTML =
        '<div class="cbgb-wa-gracies"><b>' + t.graciesTitol + nom + '</b>' + t.graciesText + '</div>' +
        '<p class="cbgb-wa-foot">' + t.trucar + ' <a href="tel:+' + NUM + '">+34 698 425 153</a></p>';
    });

    wrap.appendChild(launcher);
    wrap.appendChild(panel);
    document.body.appendChild(wrap);

    ajustaOffset();
    window.addEventListener('resize', ajustaOffset);

    // La barra de galetes es pinta o es tanca després d'aquest script:
    // vigilem el body per tornar a mesurar quan hi apareix o desapareix.
    if (window.MutationObserver) {
      new MutationObserver(ajustaOffset).observe(document.body, { childList: true });
    }

    // El botó ha de "veure's": un petit rebot als 1.2 s de carregar la
    // pàgina, un cop, perquè no passi desapercebut sota el plec.
    setTimeout(function () {
      if (!wrap.classList.contains('cbgb-wa-open')) launcher.classList.add('avis');
    }, 1200);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', pinta);
  } else {
    pinta();
  }

  window.CBGB_XAT = { obre: function () { obre(); }, tanca: function () { tanca(); } };
})();
