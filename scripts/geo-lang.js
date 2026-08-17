/* CB Grup Barna · suggeriment d'idioma segons zona geogràfica
 * Catalunya -> es queda en català (per defecte)
 * Resta d'Espanya -> suggereix castellà
 * Estranger -> suggereix anglès
 * No redirigeix mai automàticament: només mostra un avís descartable,
 * seguint la recomanació de Google d'evitar redireccions silencioses
 * per idioma/localització (que poden perjudicar l'experiència i el SEO).
 */
(function () {
  "use strict";
  try {
    if (localStorage.getItem("cbgb-geo-dismissed")) return;
  } catch (e) { return; }

  var caLink = document.querySelector('.lang-switch a[hreflang="ca"]');
  if (!caLink || !caLink.classList.contains("active")) return; // only on the Catalan version

  var esLink = document.querySelector('.lang-switch a[hreflang="es"]');
  var enLink = document.querySelector('.lang-switch a[hreflang="en"]');
  if (!esLink && !enLink) return;

  function dismiss() {
    try { localStorage.setItem("cbgb-geo-dismissed", "1"); } catch (e) {}
    var bar = document.getElementById("cbgb-geo-bar");
    if (bar) bar.remove();
  }

  function showBar(targetLink, label, msg) {
    if (!targetLink) return;
    var css = document.createElement("style");
    css.textContent =
      "#cbgb-geo-bar{position:fixed;left:0;right:0;bottom:0;z-index:200;" +
      "display:flex;align-items:center;justify-content:center;gap:16px;flex-wrap:wrap;" +
      "background:#0a0a0a;color:#fff;padding:12px 20px;" +
      "font-family:'Jost','Futura','Century Gothic',-apple-system,sans-serif;" +
      "font-size:11px;letter-spacing:.05em;box-shadow:0 -2px 14px rgba(0,0,0,.18);" +
      "animation:cbgbGeoIn .5s ease}" +
      "@keyframes cbgbGeoIn{from{transform:translateY(100%)}to{transform:translateY(0)}}" +
      "#cbgb-geo-bar a.cbgb-geo-go{color:#fff;font-weight:500;text-transform:uppercase;" +
      "letter-spacing:.2em;font-size:10px;border-bottom:1px solid #E31E24;padding-bottom:3px}" +
      "#cbgb-geo-bar button.cbgb-geo-x{background:none;border:0;color:rgba(255,255,255,.5);" +
      "font-size:16px;line-height:1;cursor:pointer;padding:4px}" +
      "#cbgb-geo-bar button.cbgb-geo-x:hover{color:#fff}" +
      "@media(max-width:520px){#cbgb-geo-bar{font-size:10.5px;padding:10px 14px}}";
    document.head.appendChild(css);

    var bar = document.createElement("div");
    bar.id = "cbgb-geo-bar";
    bar.setAttribute("role", "region");
    bar.setAttribute("aria-label", "Suggeriment d'idioma");

    var text = document.createElement("span");
    text.textContent = msg;
    bar.appendChild(text);

    var go = document.createElement("a");
    go.className = "cbgb-geo-go";
    go.href = targetLink.href;
    go.textContent = label;
    bar.appendChild(go);

    var x = document.createElement("button");
    x.className = "cbgb-geo-x";
    x.setAttribute("aria-label", "Tancar");
    x.textContent = "×";
    x.addEventListener("click", dismiss);
    bar.appendChild(x);

    document.body.appendChild(bar);
  }

  function isCatalonia(region, regionCode) {
    if (regionCode && regionCode.toUpperCase() === "CT") return true;
    if (!region) return false;
    var r = region.toLowerCase();
    return r.indexOf("catal") !== -1;
  }

  fetch("https://ipwho.is/", { cache: "no-store" })
    .then(function (r) { return r.ok ? r.json() : null; })
    .then(function (d) {
      if (!d || d.success === false || !d.country_code) return;

      if (d.country_code === "ES") {
        if (isCatalonia(d.region, d.region_code)) return; // ja hi som, no cal suggerir res
        showBar(
          esLink,
          "Ver en castellano",
          "Parece que estás fuera de Catalunya. ¿Prefieres ver la web en castellano?"
        );
      } else {
        showBar(
          enLink,
          "View in English",
          "Looks like you're visiting from abroad. Prefer to read this in English?"
        );
      }
    })
    .catch(function () { /* fail silent: es queda en català per defecte */ });
})();
