/* =========================================================
   AUTENTICACIÓ AMB GOOGLE · CB Grup Barna
   Compartida pel panell (/admin/) i per la app de partits (/partits/).
   Guarda la sessió a localStorage perquè no calgui repetir login.
   ========================================================= */
(function () {
  const KEY = 'cbgbAuthV1';
  const CFG = window.CBGB_ADMIN || {};

  function decodeJwt(token) {
    const part = token.split('.')[1];
    const json = decodeURIComponent(atob(part.replace(/-/g, '+').replace(/_/g, '/'))
      .split('').map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2)).join(''));
    return JSON.parse(json);
  }

  function validate(payload) {
    if (!payload) return 'Resposta de Google buida.';
    const iss = payload.iss || '';
    if (iss !== 'accounts.google.com' && iss !== 'https://accounts.google.com')
      return 'Emissor no vàlid.';
    if (CFG.GOOGLE_CLIENT_ID && payload.aud !== CFG.GOOGLE_CLIENT_ID)
      return 'Aquest accés no correspon a aquesta web.';
    if (payload.exp && Date.now() / 1000 > payload.exp) return 'La sessió de Google ha caducat.';
    if (payload.email_verified === false) return 'El correu de Google no està verificat.';
    const email = (payload.email || '').toLowerCase();
    const allowed = (CFG.ALLOWED_EMAILS || []).map(e => e.toLowerCase());
    const domainOk = CFG.ALLOWED_DOMAIN && email.endsWith('@' + CFG.ALLOWED_DOMAIN.toLowerCase());
    if (!allowed.includes(email) && !domainOk)
      return `El compte ${email} no té permís. Entra amb voluntarisgrupbarna@gmail.com.`;
    return null;
  }

  const Auth = {
    /** Sessió activa i vigent, o null */
    session() {
      try {
        const s = JSON.parse(localStorage.getItem(KEY) || 'null');
        if (!s) return null;
        if (Date.now() > s.expiresAt) { localStorage.removeItem(KEY); return null; }
        return s;
      } catch (e) { return null; }
    },
    isStaff() { return !!Auth.session(); },
    logout() { localStorage.removeItem(KEY); if (window.google?.accounts?.id) google.accounts.id.disableAutoSelect(); },

    /** Processa la credencial que retorna Google. onResult(error, session) */
    handleCredential(resp, onResult) {
      let payload;
      try { payload = decodeJwt(resp.credential); }
      catch (e) { return onResult('No s\'ha pogut llegir la resposta de Google.'); }
      const err = validate(payload);
      if (err) return onResult(err);
      const sess = {
        email: payload.email, name: payload.name || payload.email,
        picture: payload.picture || '',
        // la sessió local dura 12 h; després cal tornar a entrar amb Google
        expiresAt: Date.now() + 12 * 60 * 60 * 1000,
      };
      localStorage.setItem(KEY, JSON.stringify(sess));
      onResult(null, sess);
    },

    /** Pinta el botó oficial de Google dins d'un contenidor */
    renderButton(containerId, onResult) {
      if (!CFG.GOOGLE_CLIENT_ID) {
        onResult('NO_CONFIG');
        return;
      }
      const start = () => {
        google.accounts.id.initialize({
          client_id: CFG.GOOGLE_CLIENT_ID,
          callback: r => Auth.handleCredential(r, onResult),
          auto_select: false,
          cancel_on_tap_outside: true,
        });
        google.accounts.id.renderButton(document.getElementById(containerId),
          { theme: 'filled_black', size: 'large', shape: 'pill', text: 'signin_with', locale: 'ca' });
      };
      if (window.google?.accounts?.id) return start();
      const sc = document.createElement('script');
      sc.src = 'https://accounts.google.com/gsi/client';
      sc.async = true; sc.defer = true;
      sc.onload = start;
      sc.onerror = () => onResult('No s\'ha pogut carregar Google. Comprova la connexió.');
      document.head.appendChild(sc);
    },
  };

  window.CBGBAuth = Auth;
})();
