/* CB Grup Barna · Porta d'accés amb contrasenya
 * Protegeix les pàgines d'administració del club amb una contrasenya compartida.
 *
 * NOTA DE SEGURETAT: això és una porta al NAVEGADOR per evitar accessos casuals,
 * no protecció real de dades sensibles (qualsevol pot llegir aquest fitxer). El
 * que realment autoritza a escriure al repositori és el token de GitHub que cal
 * introduir a /fotos/admin.html i similars.
 *
 * Per canviar la contrasenya: genera el hash SHA-256 del text nou (per exemple,
 * amb `echo -n "LaMevaContrasenya" | shasum -a 256` a un terminal) i substitueix
 * el valor de PASS_HASH.
 */
(function (global) {
  'use strict';

  var PASS_HASH = '41d74e142b2d9d8b18514cfcc1154932370803ba82c30fb7f9088a1535312422';
  var KEY = 'cbgb_admin_pass_ok';

  function el(tag, css, html) {
    var e = document.createElement(tag);
    if (css) e.setAttribute('style', css);
    if (html) e.innerHTML = html;
    return e;
  }

  async function sha256(text) {
    var buf = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(text));
    return Array.from(new Uint8Array(buf)).map(function (b) { return b.toString(16).padStart(2, '0'); }).join('');
  }

  function saved() {
    try { return localStorage.getItem(KEY) === '1'; } catch (e) { return false; }
  }

  /**
   * CBGBGate.protect(onReady)
   * Tapa la pàgina fins que algú introdueix la contrasenya correcta.
   */
  function protect(onReady) {
    if (saved()) { if (onReady) onReady({ email: 'admin' }); return; }

    var hide = el('style');
    hide.textContent = 'body{visibility:hidden!important}';
    (document.head || document.documentElement).appendChild(hide);

    function unlock() {
      try { localStorage.setItem(KEY, '1'); } catch (e) {}
      var g = document.getElementById('cbgb-pgate');
      if (g) g.remove();
      hide.remove();
      document.body.style.visibility = '';
      if (onReady) onReady({ email: 'admin' });
    }

    function paint() {
      hide.textContent = '';
      document.body.style.visibility = 'visible';

      var fontLink = document.createElement('link');
      fontLink.rel = 'stylesheet';
      fontLink.href = 'https://fonts.googleapis.com/css2?family=Jost:wght@200;300;400;500&family=Inter:wght@300;400;500;600&display=swap';
      document.head.appendChild(fontLink);

      var gate = el('div', 'position:fixed;inset:0;z-index:99999;background:#ffffff;display:flex;align-items:center;justify-content:center;padding:2rem;font-family:Inter,-apple-system,system-ui,sans-serif;font-weight:300;color:#0a0a0a');
      gate.id = 'cbgb-pgate';

      var box = el('div', 'text-align:center;max-width:360px;width:100%');
      box.appendChild(el('img', 'height:60px;margin-bottom:1.5rem'));
      box.firstChild.src = '/logo.png';
      box.firstChild.alt = 'CB Grup Barna';
      box.appendChild(el('div', 'font-family:Jost,\'Futura\',sans-serif;font-weight:300;text-transform:uppercase;font-size:1.4rem;letter-spacing:.08em', 'ÀREA D\'<span style="color:#E20613">ADMINISTRACIÓ</span>'));
      box.appendChild(el('p', 'color:#46433f;font-size:.85rem;margin:.6rem 0 1.75rem', 'Introdueix la contrasenya del club per continuar.'));

      var form = el('form', 'display:flex;flex-direction:column;gap:.75rem');
      var input = el('input', 'width:100%;background:#f6f4f1;border:1px solid #e4e1dd;color:#0a0a0a;padding:.75rem .9rem;font-family:Inter,sans-serif;font-size:.95rem;outline:none;text-align:center;letter-spacing:.04em');
      input.type = 'password';
      input.placeholder = 'Contrasenya';
      input.autocomplete = 'current-password';
      form.appendChild(input);

      var btn = el('button', 'width:100%;background:#0a0a0a;border:1px solid #0a0a0a;color:#fff;padding:.75rem 1rem;font-family:Jost,sans-serif;font-size:10px;letter-spacing:.24em;text-transform:uppercase;cursor:pointer', 'Entrar');
      btn.type = 'submit';
      form.appendChild(btn);

      var err = el('p', 'display:none;color:#E20613;font-size:.8rem;margin-top:1rem;line-height:1.4', 'Contrasenya incorrecta.');
      err.id = 'cbgb-pgerr';

      box.appendChild(form);
      box.appendChild(err);
      box.appendChild(el('p', 'font-family:Jost,sans-serif;color:#8a8681;font-size:9px;letter-spacing:.16em;text-transform:uppercase;margin-top:2rem;line-height:1.6',
        'Accés reservat a l\'equip del CB Grup Barna.'));

      gate.appendChild(box);
      document.body.appendChild(gate);

      form.addEventListener('submit', async function (e) {
        e.preventDefault();
        btn.disabled = true;
        var hash = await sha256(input.value);
        if (hash === PASS_HASH) {
          unlock();
        } else {
          err.style.display = 'block';
          input.value = '';
          input.focus();
          btn.disabled = false;
        }
      });

      setTimeout(function () { input.focus(); }, 50);
    }

    if (document.body) paint();
    else document.addEventListener('DOMContentLoaded', paint);
  }

  function signOut() {
    try { localStorage.removeItem(KEY); } catch (e) {}
    location.reload();
  }

  global.CBGBGate = { protect: protect, signOut: signOut, user: function () { return saved() ? { email: 'admin' } : null; } };
})(window);
