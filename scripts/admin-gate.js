/* CB Grup Barna · Porta d'accés amb contrasenya
 * Protegeix les pàgines d'administració del club amb una contrasenya compartida.
 *
 * NOTA DE SEGURETAT: això és una porta al NAVEGADOR per evitar accessos casuals,
 * no protecció real de dades sensibles (qualsevol pot llegir aquest fitxer). El
 * que realment autoritza a escriure al repositori és el token de GitHub. Des de
 * /admin/token.html el token es pot deixar XIFRAT amb aquesta contrasenya a
 * admin/token.enc.json: aleshores entrar la contrasenya a la porta ja el
 * recupera i no cal enganxar-lo a cada dispositiu. Això vol dir que qui
 * tingui la contrasenya té el token: si es filtra, revoca el token a GitHub
 * i canvia la contrasenya.
 *
 * Per canviar la contrasenya: genera el hash SHA-256 del text nou (per exemple,
 * amb `echo -n "LaMevaContrasenya" | shasum -a 256` a un terminal) i substitueix
 * el valor de PASS_HASH.
 */
(function (global) {
  'use strict';

  var PASS_HASH = '64ac9d2d5cd538bce4ceba823cd943c668b17b584f8b0cb4d23580ba2c210d64';
  var KEY = 'cbgb_admin_pass_ok';

  /* La caixa forta del token de GitHub: admin/token.enc.json guarda el token
   * xifrat (AES-GCM, clau derivada de la contrasenya del club amb PBKDF2).
   * Quan algú entra la contrasenya a la porta, el token es desxifra i es desa
   * a localStorage amb la clau que ja fan servir totes les eines d'admin, de
   * manera que no cal tornar-lo a enganxar mai a cap dispositiu.
   * Es gestiona des de /admin/token.html. */
  var VAULT_URL = '/admin/token.enc.json';
  var TOKEN_KEY = 'gh_admin_token';

  function b64ToBytes(b64) {
    return Uint8Array.from(atob(b64), function (c) { return c.charCodeAt(0); });
  }
  function bytesToB64(bytes) {
    var s = '';
    new Uint8Array(bytes).forEach(function (b) { s += String.fromCharCode(b); });
    return btoa(s);
  }

  async function deriveKey(pass, saltBytes) {
    var base = await crypto.subtle.importKey('raw', new TextEncoder().encode(pass), 'PBKDF2', false, ['deriveKey']);
    return crypto.subtle.deriveKey(
      { name: 'PBKDF2', salt: saltBytes, iterations: 210000, hash: 'SHA-256' },
      base, { name: 'AES-GCM', length: 256 }, false, ['encrypt', 'decrypt']);
  }

  /** Baixa la caixa forta i, si la contrasenya la pot obrir, desa el token. */
  async function openVault(pass) {
    try {
      var r = await fetch(VAULT_URL, { cache: 'no-store' });
      if (!r.ok) return false;
      var v = await r.json();
      var key = await deriveKey(pass, b64ToBytes(v.salt));
      var pt = await crypto.subtle.decrypt({ name: 'AES-GCM', iv: b64ToBytes(v.iv) }, key, b64ToBytes(v.ct));
      var tok = new TextDecoder().decode(pt).trim();
      if (!tok) return false;
      try { localStorage.setItem(TOKEN_KEY, tok); } catch (e) {}
      return true;
    } catch (e) { return false; }
  }

  /** Xifra un token amb la contrasenya del club. Retorna l'objecte per desar. */
  async function sealVault(pass, token) {
    var salt = crypto.getRandomValues(new Uint8Array(16));
    var iv = crypto.getRandomValues(new Uint8Array(12));
    var key = await deriveKey(pass, salt);
    var ct = await crypto.subtle.encrypt({ name: 'AES-GCM', iv: iv }, key, new TextEncoder().encode(token));
    return { v: 1, alg: 'AES-GCM/PBKDF2-SHA256-210k', salt: bytesToB64(salt), iv: bytesToB64(iv), ct: bytesToB64(ct) };
  }

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
    var hasTok = false;
    try { hasTok = !!localStorage.getItem(TOKEN_KEY); } catch (e) {}
    if (saved() && hasTok) { if (onReady) onReady({ email: 'admin' }); return; }

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
      fontLink.href = '/css/fonts.css';
      document.head.appendChild(fontLink);

      var gate = el('div', 'position:fixed;inset:0;z-index:99999;background:#ffffff;display:flex;align-items:center;justify-content:center;padding:2rem;font-family:Inter,-apple-system,system-ui,sans-serif;font-weight:300;color:#10100E');
      gate.id = 'cbgb-pgate';

      var box = el('div', 'text-align:center;max-width:360px;width:100%');
      box.appendChild(el('img', 'height:60px;margin-bottom:1.5rem'));
      box.firstChild.src = '/logo.png';
      box.firstChild.alt = 'CB Grup Barna';
      box.appendChild(el('div', 'font-family:Jost,\'Futura\',sans-serif;font-weight:300;text-transform:uppercase;font-size:1.4rem;letter-spacing:.08em', 'ÀREA D\'<span style="color:#E20613">ADMINISTRACIÓ</span>'));
      box.appendChild(el('p', 'color:#46433f;font-size:.85rem;margin:.6rem 0 1.75rem', 'Introdueix la contrasenya del club per continuar.'));

      var form = el('form', 'display:flex;flex-direction:column;gap:.75rem');
      var input = el('input', 'width:100%;background:#FFFFFF;border:1px solid #e4e1dd;color:#10100E;padding:.75rem .9rem;font-family:Inter,sans-serif;font-size:.95rem;outline:none;text-align:center;letter-spacing:.04em');
      input.type = 'password';
      input.placeholder = 'Contrasenya';
      input.autocomplete = 'current-password';
      form.appendChild(input);

      var btn = el('button', 'width:100%;background:#10100E;border:1px solid #10100E;color:#fff;padding:.75rem 1rem;font-family:Jost,sans-serif;font-size:10px;letter-spacing:.24em;text-transform:uppercase;cursor:pointer', 'Entrar');
      btn.type = 'submit';
      form.appendChild(btn);

      var err = el('p', 'display:none;color:#E20613;font-size:.8rem;margin-top:1rem;line-height:1.4', 'Contrasenya incorrecta.');
      err.id = 'cbgb-pgerr';

      box.appendChild(form);
      box.appendChild(err);
      box.appendChild(el('p', 'font-family:Jost,sans-serif;color:#6B6560;font-size:9px;letter-spacing:.16em;text-transform:uppercase;margin-top:2rem;line-height:1.6',
        'Accés reservat a l\'equip del CB Grup Barna.'));

      gate.appendChild(box);
      document.body.appendChild(gate);

      form.addEventListener('submit', async function (e) {
        e.preventDefault();
        btn.disabled = true;
        var hash = await sha256(input.value);
        if (hash === PASS_HASH) {
          // La mateixa contrasenya obre la caixa forta del token de GitHub,
          // si n'hi ha: així no cal enganxar el token a cada dispositiu.
          await openVault(input.value);
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

    function start() {
      if (document.body) paint();
      else document.addEventListener('DOMContentLoaded', paint);
    }

    if (saved()) {
      // Porta ja oberta però sense token en aquest dispositiu: si hi ha caixa
      // forta al repositori, tornem a demanar la contrasenya una vegada per
      // obrir-la; si no n'hi ha, tot segueix com sempre.
      fetch(VAULT_URL, { method: 'HEAD', cache: 'no-store' })
        .then(function (r) { return r.ok; })
        .catch(function () { return false; })
        .then(function (hasVault) {
          if (hasVault) {
            try { localStorage.removeItem(KEY); } catch (e) {}
            start();
          } else {
            hide.remove();
            if (document.body) document.body.style.visibility = '';
            if (onReady) onReady({ email: 'admin' });
          }
        });
      return;
    }
    start();
  }

  function signOut() {
    try { localStorage.removeItem(KEY); } catch (e) {}
    location.reload();
  }

  global.CBGBGate = {
    protect: protect, signOut: signOut,
    user: function () { return saved() ? { email: 'admin' } : null; },
    /* Eines de la caixa forta del token, per a /admin/token.html */
    vault: {
      open: openVault,
      seal: sealVault,
      checkPass: async function (pass) { return (await sha256(pass)) === PASS_HASH; },
    },
  };
})(window);
