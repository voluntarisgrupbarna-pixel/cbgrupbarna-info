/* CB Grup Barna · Porta d'accés amb Google
 * Només els correus autoritzats poden entrar a l'àrea d'administració.
 *
 * CONFIGURACIÓ (un sol cop):
 *  1. Ves a https://console.cloud.google.com/apis/credentials
 *  2. Crea un "ID de cliente de OAuth" de tipus "Aplicación web".
 *  3. A "Orígenes autorizados de JavaScript" afegeix:  https://cbgrupbarna.info
 *  4. Copia l'ID (acaba en .apps.googleusercontent.com) i enganxa'l a CLIENT_ID.
 *
 * NOTA DE SEGURETAT: això és una porta al NAVEGADOR. El que realment autoritza
 * a escriure al repositori és el token de GitHub. Google serveix per saber QUI
 * entra i evitar accessos casuals, no per protegir dades sensibles.
 */
(function (global) {
  'use strict';

  var CLIENT_ID = ''; // ← enganxa aquí el teu ID de client de Google

  var ALLOWED = [
    'voluntarisgrupbarna@gmail.com',
    'cbgrupbarna@gmail.com',
    'anafernandezduran78@gmail.com'
  ];

  var KEY = 'cbgb_google_user';

  function el(tag, css, html) {
    var e = document.createElement(tag);
    if (css) e.setAttribute('style', css);
    if (html) e.innerHTML = html;
    return e;
  }

  function decodeJwt(t) {
    try {
      var p = t.split('.')[1].replace(/-/g, '+').replace(/_/g, '/');
      return JSON.parse(decodeURIComponent(escape(atob(p))));
    } catch (e) { return null; }
  }

  function saved() {
    try {
      var v = JSON.parse(sessionStorage.getItem(KEY) || 'null');
      if (v && v.email && ALLOWED.indexOf(v.email) > -1) return v;
    } catch (e) {}
    return null;
  }

  /**
   * CBGBGate.protect(onReady)
   * Tapa la pàgina fins que algú autoritzat s'identifica amb Google.
   */
  function protect(onReady) {
    var ok = saved();
    if (ok) { if (onReady) onReady(ok); return; }

    var hide = el('style');
    hide.textContent = 'body{visibility:hidden!important}';
    (document.head || document.documentElement).appendChild(hide);

    function unlock(user) {
      try { sessionStorage.setItem(KEY, JSON.stringify(user)); } catch (e) {}
      var g = document.getElementById('cbgb-ggate');
      if (g) g.remove();
      hide.remove();
      document.body.style.visibility = '';
      if (onReady) onReady(user);
    }

    function paint() {
      hide.textContent = '';
      document.body.style.visibility = 'visible';

      var fontLink = document.createElement('link');
      fontLink.rel = 'stylesheet';
      fontLink.href = 'https://fonts.googleapis.com/css2?family=Jost:wght@200;300;400;500&family=Inter:wght@300;400;500;600&display=swap';
      document.head.appendChild(fontLink);

      var gate = el('div', 'position:fixed;inset:0;z-index:99999;background:#ffffff;display:flex;align-items:center;justify-content:center;padding:2rem;font-family:Inter,-apple-system,system-ui,sans-serif;font-weight:300;color:#0a0a0a');
      gate.id = 'cbgb-ggate';

      var box = el('div', 'text-align:center;max-width:400px;width:100%');
      box.appendChild(el('img', 'height:60px;margin-bottom:1.5rem'));
      box.firstChild.src = '/logo.png';
      box.firstChild.alt = 'CB Grup Barna';
      box.appendChild(el('div', 'font-family:Jost,\'Futura\',sans-serif;font-weight:300;text-transform:uppercase;font-size:1.4rem;letter-spacing:.08em', 'ÀREA D\'<span style="color:#E31E24">ADMINISTRACIÓ</span>'));
      box.appendChild(el('p', 'color:#46433f;font-size:.85rem;margin:.6rem 0 1.75rem', 'Identifica\'t amb el compte de Google del club per continuar.'));

      var slot = el('div', 'display:flex;justify-content:center;min-height:44px');
      slot.id = 'cbgb-gbtn';
      box.appendChild(slot);

      var err = el('p', 'display:none;color:#E31E24;font-size:.8rem;margin-top:1rem;line-height:1.4');
      err.id = 'cbgb-gerr';
      box.appendChild(err);

      box.appendChild(el('p', 'font-family:Jost,sans-serif;color:#8a8681;font-size:9px;letter-spacing:.16em;text-transform:uppercase;margin-top:2rem;line-height:1.6',
        'Accés reservat a l\'equip del CB Grup Barna.'));

      gate.appendChild(box);
      document.body.appendChild(gate);

      if (!CLIENT_ID) {
        slot.innerHTML = '';
        var warn = el('div', 'text-align:left;background:#f6f4f1;border:1px solid #e4e1dd;padding:1rem 1.1rem;font-size:.78rem;line-height:1.6;color:#46433f',
          '<b style="color:#0a0a0a">Falta configurar Google.</b><br>Obre <code>scripts/google-gate.js</code> i enganxa el teu <i>Client ID</i> a la línia <code>CLIENT_ID</code>. ' +
          'El crees a <a href="https://console.cloud.google.com/apis/credentials" target="_blank" rel="noopener" style="color:#E31E24">console.cloud.google.com</a> ' +
          '(Aplicació web · origen autoritzat <code>https://cbgrupbarna.info</code>).');
        slot.appendChild(warn);
        var cont = el('button', 'margin-top:1rem;background:#0a0a0a;border:1px solid #0a0a0a;color:#fff;padding:.75rem 1.4rem;font-family:Jost,sans-serif;font-size:10px;letter-spacing:.24em;text-transform:uppercase;cursor:pointer', 'Continuar sense Google');
        cont.onclick = function () { unlock({ email: 'sense-google', name: 'Admin' }); };
        box.appendChild(cont);
        return;
      }

      var s = document.createElement('script');
      s.src = 'https://accounts.google.com/gsi/client';
      s.async = true;
      s.defer = true;
      s.onload = function () {
        global.google.accounts.id.initialize({
          client_id: CLIENT_ID,
          callback: function (resp) {
            var data = decodeJwt(resp.credential);
            var e2 = document.getElementById('cbgb-gerr');
            if (!data || !data.email || data.email_verified === false) {
              e2.textContent = 'No s\'ha pogut verificar el compte de Google.';
              e2.style.display = 'block';
              return;
            }
            if (ALLOWED.indexOf(data.email) === -1) {
              e2.innerHTML = 'El compte <b>' + data.email + '</b> no té accés a l\'administració del club.';
              e2.style.display = 'block';
              global.google.accounts.id.disableAutoSelect();
              return;
            }
            unlock({ email: data.email, name: data.name || '', picture: data.picture || '' });
          }
        });
        global.google.accounts.id.renderButton(document.getElementById('cbgb-gbtn'), {
          theme: 'outline', size: 'large', text: 'signin_with', shape: 'pill'
        });
      };
      s.onerror = function () {
        document.getElementById('cbgb-gerr').textContent = 'No s\'ha pogut carregar Google. Comprova la connexió.';
        document.getElementById('cbgb-gerr').style.display = 'block';
      };
      document.head.appendChild(s);
    }

    if (document.body) paint();
    else document.addEventListener('DOMContentLoaded', paint);
  }

  function signOut() {
    try { sessionStorage.removeItem(KEY); } catch (e) {}
    location.reload();
  }

  global.CBGBGate = { protect: protect, signOut: signOut, user: saved, ALLOWED: ALLOWED };
})(window);
