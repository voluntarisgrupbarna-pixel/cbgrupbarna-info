/* Cercador global del CB Grup Barna.
   Autocontingut (Shadow DOM) perque funcioni igual a qualsevol pagina del lloc,
   sigui quin sigui el seu propi CSS. Obre amb el boto flotant, la tecla "/" o Ctrl/Cmd+K. */
(function () {
  "use strict";
  if (window.__cbgbSearchLoaded) return;
  window.__cbgbSearchLoaded = true;

  var INDEX_URL = "/search-index.json";
  var indexData = null;
  var indexPromise = null;

  function loadIndex() {
    if (indexPromise) return indexPromise;
    indexPromise = fetch(INDEX_URL)
      .then(function (r) { return r.json(); })
      .then(function (data) { indexData = data; return data; })
      .catch(function () { indexData = []; return []; });
    return indexPromise;
  }

  function norm(s) {
    return (s || "")
      .toString()
      .normalize("NFD")
      .replace(/[̀-ͯ]/g, "")
      .toLowerCase();
  }

  function score(entry, terms) {
    var title = norm(entry.title);
    var full = norm(entry.full_title);
    var desc = norm(entry.desc);
    var cat = norm(entry.cat);
    var s = 0;
    for (var i = 0; i < terms.length; i++) {
      var t = terms[i];
      if (!t) continue;
      if (title === t) s += 40;
      else if (title.indexOf(t) === 0) s += 24;
      else if (title.indexOf(t) !== -1) s += 16;
      if (full.indexOf(t) !== -1) s += 6;
      if (cat.indexOf(t) !== -1) s += 8;
      if (desc.indexOf(t) !== -1) s += 4;
      if (s === 0) return 0;
    }
    return s;
  }

  function search(query) {
    var terms = norm(query).split(/\s+/).filter(Boolean);
    if (!terms.length || !indexData) return [];
    var results = [];
    for (var i = 0; i < indexData.length; i++) {
      var sc = score(indexData[i], terms);
      if (sc > 0) results.push({ entry: indexData[i], score: sc });
    }
    results.sort(function (a, b) { return b.score - a.score; });
    return results.slice(0, 8).map(function (r) { return r.entry; });
  }

  var CSS = "\n" +
    ":host{all:initial}\n" +
    "*{box-sizing:border-box;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Inter,Arial,sans-serif}\n" +
    ".fab{position:fixed;left:18px;bottom:18px;z-index:2147483000;width:52px;height:52px;border-radius:50%;background:#0A0A0A;color:#F5F5F5;border:1px solid rgba(255,255,255,.15);display:flex;align-items:center;justify-content:center;cursor:pointer;box-shadow:0 6px 20px rgba(0,0,0,.35);font-size:20px;transition:transform .2s ease}\n" +
    ".fab:hover{transform:scale(1.06)}\n" +
    ".overlay{position:fixed;inset:0;z-index:2147483001;background:rgba(6,6,8,.72);backdrop-filter:blur(2px);display:none;align-items:flex-start;justify-content:center;padding:9vh 16px 16px}\n" +
    ".overlay.open{display:flex}\n" +
    ".panel{width:100%;max-width:600px;background:#121214;border:1px solid rgba(255,255,255,.1);border-radius:16px;box-shadow:0 20px 60px rgba(0,0,0,.5);overflow:hidden;max-height:76vh;display:flex;flex-direction:column}\n" +
    ".inrow{display:flex;align-items:center;gap:10px;padding:14px 16px;border-bottom:1px solid rgba(255,255,255,.08)}\n" +
    ".inrow svg{flex:none;opacity:.5}\n" +
    "input{flex:1;background:transparent;border:0;outline:0;color:#F5F5F5;font-size:16px;padding:6px 0}\n" +
    "input::placeholder{color:rgba(245,245,245,.4)}\n" +
    ".esc{flex:none;font-size:11px;color:rgba(245,245,245,.4);border:1px solid rgba(255,255,255,.15);border-radius:6px;padding:2px 6px;cursor:pointer;background:transparent}\n" +
    ".results{overflow-y:auto;padding:6px}\n" +
    ".empty{padding:28px 18px;text-align:center;color:rgba(245,245,245,.45);font-size:13.5px;line-height:1.6}\n" +
    "a.res{display:block;padding:10px 12px;border-radius:10px;text-decoration:none;color:#F5F5F5;cursor:pointer}\n" +
    "a.res:hover,a.res.active{background:rgba(200,16,46,.16)}\n" +
    ".res .cat{font-size:10px;letter-spacing:.08em;text-transform:uppercase;color:#C8102E;font-weight:600}\n" +
    ".res .t{font-size:14.5px;font-weight:600;margin:2px 0 3px;color:#F5F5F5}\n" +
    ".res .d{font-size:12.5px;color:rgba(245,245,245,.55);line-height:1.45;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}\n" +
    ".foot{padding:8px 16px;border-top:1px solid rgba(255,255,255,.08);font-size:11px;color:rgba(245,245,245,.35);display:flex;gap:14px}\n" +
    "kbd{border:1px solid rgba(255,255,255,.2);border-radius:4px;padding:0 5px;font-family:inherit}\n" +
    "@media (max-width:520px){.fab{left:14px;bottom:14px;width:46px;height:46px;font-size:18px}.overlay{padding:6vh 10px 10px}}";

  var host = document.createElement("div");
  host.id = "cbgb-search-root";
  document.addEventListener("DOMContentLoaded", mount);
  if (document.readyState !== "loading") mount();

  function mount() {
    if (document.getElementById("cbgb-search-root")) return;
    document.body.appendChild(host);
    var root = host.attachShadow({ mode: "open" });
    var style = document.createElement("style");
    style.textContent = CSS;
    root.appendChild(style);

    var fab = document.createElement("button");
    fab.className = "fab";
    fab.setAttribute("aria-label", "Cercar al lloc");
    fab.innerHTML = "🔍";
    root.appendChild(fab);

    var overlay = document.createElement("div");
    overlay.className = "overlay";
    overlay.innerHTML =
      '<div class="panel" role="dialog" aria-modal="true" aria-label="Cercador del lloc">' +
      '<div class="inrow">' +
      '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>' +
      '<input type="text" placeholder="Cerca equips, escoleta, campus, blog, patrocinis…" autocomplete="off" spellcheck="false">' +
      '<button class="esc" type="button">esc</button>' +
      "</div>" +
      '<div class="results"></div>' +
      '<div class="foot"><span><kbd>/</kbd> obrir</span><span><kbd>↑↓</kbd> navegar</span><span><kbd>↵</kbd> anar-hi</span></div>' +
      "</div>";
    root.appendChild(overlay);

    var input = overlay.querySelector("input");
    var resultsEl = overlay.querySelector(".results");
    var escBtn = overlay.querySelector(".esc");
    var activeIndex = -1;
    var currentResults = [];

    function renderResults(list) {
      currentResults = list;
      activeIndex = list.length ? 0 : -1;
      if (!input.value.trim()) {
        resultsEl.innerHTML = '<div class="empty">Escriu per cercar a tot el lloc: escoleta, equips, campus, patrocinis, blog…</div>';
        return;
      }
      if (!list.length) {
        resultsEl.innerHTML = '<div class="empty">Cap resultat. Prova amb un altre terme.</div>';
        return;
      }
      resultsEl.innerHTML = "";
      list.forEach(function (e, i) {
        var a = document.createElement("a");
        a.className = "res" + (i === 0 ? " active" : "");
        a.href = e.url;
        a.innerHTML =
          '<div class="cat">' + e.cat + '</div>' +
          '<div class="t">' + e.title + '</div>' +
          '<div class="d">' + (e.desc || "") + '</div>';
        a.addEventListener("mouseenter", function () { setActive(i); });
        resultsEl.appendChild(a);
      });
    }

    function setActive(i) {
      var nodes = resultsEl.querySelectorAll("a.res");
      nodes.forEach(function (n) { n.classList.remove("active"); });
      if (nodes[i]) {
        nodes[i].classList.add("active");
        nodes[i].scrollIntoView({ block: "nearest" });
      }
      activeIndex = i;
    }

    function openOverlay() {
      overlay.classList.add("open");
      loadIndex().then(function () { renderResults(search(input.value)); });
      setTimeout(function () { input.focus(); }, 10);
      document.body.style.overflow = "hidden";
    }
    function closeOverlay() {
      overlay.classList.remove("open");
      document.body.style.overflow = "";
    }

    fab.addEventListener("click", openOverlay);
    escBtn.addEventListener("click", closeOverlay);
    overlay.addEventListener("mousedown", function (e) {
      if (e.target === overlay) closeOverlay();
    });

    input.addEventListener("input", function () {
      renderResults(search(input.value));
    });

    input.addEventListener("keydown", function (e) {
      var nodes = resultsEl.querySelectorAll("a.res");
      if (e.key === "ArrowDown") {
        e.preventDefault();
        setActive(Math.min(activeIndex + 1, nodes.length - 1));
      } else if (e.key === "ArrowUp") {
        e.preventDefault();
        setActive(Math.max(activeIndex - 1, 0));
      } else if (e.key === "Enter") {
        e.preventDefault();
        if (currentResults[activeIndex]) location.href = currentResults[activeIndex].url;
      } else if (e.key === "Escape") {
        closeOverlay();
      }
    });

    document.addEventListener("keydown", function (e) {
      var tag = (e.target && e.target.tagName || "").toLowerCase();
      var typing = tag === "input" || tag === "textarea" || (e.target && e.target.isContentEditable);
      if (overlay.classList.contains("open")) return;
      if (e.key === "/" && !typing) {
        e.preventDefault();
        openOverlay();
      } else if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
        e.preventDefault();
        openOverlay();
      }
    });

    loadIndex();
  }
})();
