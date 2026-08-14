/* CB Grup Barna · Premi Dona i Esport · Cercador
   Cerca instantània, tolerant a errades, amb sinònims — 100% client-side. */
(function () {
  'use strict';
  var DATA = window.CBGB_SEARCH_INDEX || [];
  if (!DATA.length) return;

  /* ── Estils (injectats per no tocar main.css a 27 pàgines) ── */
  var css = ''
    + '#cbgb-search-ov{position:fixed;inset:0;z-index:200000;background:rgba(4,4,4,.72);backdrop-filter:blur(4px);display:none;align-items:flex-start;justify-content:center;padding:8vh 1.2rem 2rem;}'
    + '#cbgb-search-ov.op{display:flex;}'
    + '#cbgb-search-box{width:min(640px,100%);background:#0c0c0c;border:1px solid rgba(200,16,46,.35);border-radius:12px;box-shadow:0 30px 80px rgba(0,0,0,.6);overflow:hidden;animation:cbgbSearchIn .22s ease;}'
    + '@keyframes cbgbSearchIn{from{opacity:0;transform:translateY(-10px) scale(.98)}to{opacity:1;transform:none}}'
    + '#cbgb-search-in-wrap{display:flex;align-items:center;gap:.7rem;padding:1rem 1.2rem;border-bottom:1px solid rgba(255,255,255,.08);}'
    + '#cbgb-search-in-wrap svg{flex-shrink:0;opacity:.5;}'
    + '#cbgb-search-in{flex:1;background:transparent;border:none;outline:none;color:#F2EDE6;font-family:Outfit,system-ui,sans-serif;font-size:1rem;}'
    + '#cbgb-search-in::placeholder{color:rgba(242,237,230,.35);}'
    + '#cbgb-search-esc{flex-shrink:0;font-size:.62rem;letter-spacing:.1em;text-transform:uppercase;color:rgba(242,237,230,.3);border:1px solid rgba(255,255,255,.12);border-radius:4px;padding:.25rem .5rem;cursor:pointer;background:none;font-family:inherit;}'
    + '#cbgb-search-results{max-height:56vh;overflow-y:auto;padding:.5rem;}'
    + '.cbgb-sr{display:flex;align-items:center;gap:.9rem;padding:.75rem .8rem;border-radius:8px;text-decoration:none;cursor:pointer;}'
    + '.cbgb-sr.on,.cbgb-sr:hover{background:rgba(200,16,46,.14);}'
    + '.cbgb-sr-main{flex:1;min-width:0;}'
    + '.cbgb-sr-t{font-size:.86rem;color:#F2EDE6;font-weight:500;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}'
    + '.cbgb-sr-t mark{background:none;color:#ff4d5a;font-weight:700;}'
    + '.cbgb-sr-c{font-size:.66rem;letter-spacing:.08em;text-transform:uppercase;color:rgba(242,237,230,.4);margin-top:.15rem;}'
    + '.cbgb-sr-go{flex-shrink:0;font-size:.7rem;color:rgba(242,237,230,.25);}'
    + '#cbgb-search-empty{padding:2.5rem 1rem;text-align:center;font-size:.82rem;color:rgba(242,237,230,.35);}'
    + '#cbgb-search-hint{padding:.6rem 1.2rem;border-top:1px solid rgba(255,255,255,.06);font-size:.65rem;letter-spacing:.06em;color:rgba(242,237,230,.3);display:flex;gap:1rem;}'
    + '#cbgb-search-trigger{display:flex;align-items:center;gap:.6rem;width:calc(100% - 1.6rem);margin:.9rem .8rem 0;padding:.65rem .85rem;background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.1);border-radius:8px;color:rgba(242,237,230,.5);font-family:Outfit,system-ui,sans-serif;font-size:.8rem;cursor:pointer;text-align:left;}'
    + '#cbgb-search-trigger:hover{border-color:rgba(200,16,46,.5);color:#F2EDE6;}'
    + '#cbgb-search-trigger kbd{margin-left:auto;font-size:.62rem;border:1px solid rgba(255,255,255,.15);border-radius:4px;padding:.1rem .4rem;flex-shrink:0;}'
    + '@media(max-width:600px){#cbgb-search-ov{padding-top:4vh}}';
  var styleEl = document.createElement('style');
  styleEl.textContent = css;
  document.head.appendChild(styleEl);

  /* ── Fuzzy scoring: exacte > prefix > paraula sencera > subseqüència ── */
  function score(query, entry) {
    var q = query.toLowerCase().trim();
    if (!q) return 0;
    var title = entry.t.toLowerCase();
    var hay = (entry.t + ' ' + entry.c + ' ' + (entry.k || '')).toLowerCase();
    var best = 0;
    if (title === q) best = 100;
    else if (title.indexOf(q) === 0) best = 90;
    else if (title.indexOf(q) !== -1) best = 75;
    else if (hay.indexOf(q) !== -1) best = 60;
    else {
      /* subseqüència: totes les lletres de q apareixen en ordre a hay (tolera errades/abreviacions) */
      var qi = 0;
      for (var i = 0; i < hay.length && qi < q.length; i++) {
        if (hay[i] === q[qi]) qi++;
      }
      if (qi === q.length) best = 30 - Math.min(20, hay.length / 20);
    }
    /* bonus per paraules soltes de la consulta trobades individualment */
    var words = q.split(/\s+/).filter(Boolean);
    if (words.length > 1) {
      var hits = 0;
      words.forEach(function (w) { if (hay.indexOf(w) !== -1) hits++; });
      best = Math.max(best, hits === words.length ? 65 : (hits / words.length) * 40);
    }
    return best;
  }

  function search(query) {
    if (!query.trim()) return DATA.slice(0, 8);
    return DATA
      .map(function (e) { return { e: e, s: score(query, e) }; })
      .filter(function (r) { return r.s > 0; })
      .sort(function (a, b) { return b.s - a.s; })
      .slice(0, 10)
      .map(function (r) { return r.e; });
  }

  function highlight(text, query) {
    var q = query.trim();
    if (!q) return text;
    var idx = text.toLowerCase().indexOf(q.toLowerCase());
    if (idx === -1) return text;
    return text.slice(0, idx) + '<mark>' + text.slice(idx, idx + q.length) + '</mark>' + text.slice(idx + q.length);
  }

  /* ── UI ── */
  var ov = document.createElement('div');
  ov.id = 'cbgb-search-ov';
  ov.innerHTML =
    '<div id="cbgb-search-box" role="dialog" aria-modal="true" aria-label="Cercador">'
    + '<div id="cbgb-search-in-wrap">'
    + '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>'
    + '<input id="cbgb-search-in" type="text" placeholder="Cerca una pàgina, informe, tesi o dossier…" autocomplete="off" spellcheck="false">'
    + '<button id="cbgb-search-esc" type="button">ESC</button>'
    + '</div>'
    + '<div id="cbgb-search-results"></div>'
    + '<div id="cbgb-search-hint"><span>↑↓ navegar</span><span>↵ obrir</span><span>' + DATA.length + ' resultats indexats</span></div>'
    + '</div>';
  document.body.appendChild(ov);

  var input = ov.querySelector('#cbgb-search-in');
  var resultsBox = ov.querySelector('#cbgb-search-results');
  var active = 0;
  var current = [];

  function render() {
    var q = input.value;
    current = search(q);
    active = 0;
    if (!current.length) {
      resultsBox.innerHTML = '<div id="cbgb-search-empty">Cap resultat per «' + q + '». Prova amb un altre terme.</div>';
      return;
    }
    resultsBox.innerHTML = current.map(function (e, i) {
      return '<a href="' + e.u + '" class="cbgb-sr' + (i === 0 ? ' on' : '') + '" data-i="' + i + '">'
        + '<div class="cbgb-sr-main"><div class="cbgb-sr-t">' + highlight(e.t, q) + '</div><div class="cbgb-sr-c">' + e.c + '</div></div>'
        + '<div class="cbgb-sr-go">→</div></a>';
    }).join('');
  }

  function setActive(i) {
    var items = resultsBox.querySelectorAll('.cbgb-sr');
    if (!items.length) return;
    active = (i + items.length) % items.length;
    items.forEach(function (el, idx) { el.classList.toggle('on', idx === active); });
    items[active].scrollIntoView({ block: 'nearest' });
  }

  function openSearch() {
    ov.classList.add('op');
    input.value = '';
    render();
    setTimeout(function () { input.focus(); }, 30);
    document.body.style.overflow = 'hidden';
    if (window.gtag) gtag('event', 'cerca_oberta');
  }
  function closeSearch() {
    ov.classList.remove('op');
    document.body.style.overflow = '';
  }

  input.addEventListener('input', render);
  ov.querySelector('#cbgb-search-esc').addEventListener('click', closeSearch);
  ov.addEventListener('click', function (e) { if (e.target === ov) closeSearch(); });
  input.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') { closeSearch(); }
    else if (e.key === 'ArrowDown') { e.preventDefault(); setActive(active + 1); }
    else if (e.key === 'ArrowUp') { e.preventDefault(); setActive(active - 1); }
    else if (e.key === 'Enter') {
      e.preventDefault();
      var sel = current[active];
      if (sel) {
        if (window.gtag) gtag('event', 'cerca_resultat', { terme: input.value, desti: sel.u });
        location.href = sel.u;
      }
    }
  });

  document.addEventListener('keydown', function (e) {
    var mod = e.metaKey || e.ctrlKey;
    if (mod && e.key.toLowerCase() === 'k') { e.preventDefault(); openSearch(); }
    else if (e.key === '/' && document.activeElement.tagName !== 'INPUT' && document.activeElement.tagName !== 'TEXTAREA') {
      e.preventDefault(); openSearch();
    }
  });

  /* ── Insereix el botó disparador a la capçalera del menú lateral ── */
  function mountTrigger() {
    var hd = document.querySelector('.sb .sb-hd');
    if (!hd) return;
    var btn = document.createElement('button');
    btn.id = 'cbgb-search-trigger';
    btn.type = 'button';
    btn.innerHTML = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>Cercar a tota la web<kbd>⌘K</kbd>';
    btn.addEventListener('click', openSearch);
    hd.insertAdjacentElement('afterend', btn);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', mountTrigger);
  else mountTrigger();

  window.cbgbOpenSearch = openSearch;
})();
