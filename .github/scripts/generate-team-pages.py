#!/usr/bin/env python3
"""
Pàgines pròpies per equip · SEO / SEO-IA · CB Grup Barna
Genera una pàgina estàtica real (HTML servit tal qual, sense dependre de
JavaScript) per a cada equip a partits/equips/{id}/index.html, més un índex
a partits/equips/index.html. Cada pàgina és una URL indexable amb el nom
de l'equip, la competició, el balanç i el calendari — el que la gent busca
literalment ("Cadet Femení A CB Grup Barna"), en lloc de viure només dins
l'estat intern de l'app de /partits/.

S'executa cada dia, just després d'update-partits.py, per reflectir
data.json al dia. Disseny defensiu: si data.json no es pot llegir, no es
toca res.
"""
import json
import re
from datetime import date
from pathlib import Path


def clamp_desc(text, limit=160):
    """Google en mostra uns 160 caràcters. Retallem per final de frase perquè
    el fragment de cerca no quedi penjat a mitja paraula."""
    text = " ".join(text.split())
    if len(text) <= limit:
        return text
    cut = text[:limit + 1]
    end = max(cut.rfind(". "), cut.rfind("? "), cut.rfind("! "))
    if end > limit * 0.55:
        return text[:end + 1].strip()
    sp = cut.rfind(" ")
    return text[:sp if sp > 0 else limit].rstrip(" ,;:·") + "…"


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "partits" / "data.json"
OUT_DIR = ROOT / "partits" / "equips"
BASE_URL = "https://cbgrupbarna.info"

DIES = ["Dilluns", "Dimarts", "Dimecres", "Dijous", "Divendres", "Dissabte", "Diumenge"]
MESOS = ["gen", "feb", "mar", "abr", "maig", "juny", "jul", "ag", "set", "oct", "nov", "des"]
CATEGORIES = ["Sènior", "Júnior", "Cadet", "Infantil", "Preinfantil", "Mini", "Premini"]
MAX_RESULTATS = 8


def fmt_dia(iso):
    d = date.fromisoformat(iso)
    return f"{DIES[d.weekday()]} {d.day} {MESOS[d.month - 1]}"


def esc(s):
    s = (s or "")
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def categoria_de(nom):
    for c in CATEGORIES:
        if (nom or "").startswith(c):
            return c
    return "Altres"


def resultat(p):
    if p.get("puntsLocal") is None or p.get("puntsVisitant") is None:
        return None
    barna = p["puntsLocal"] if p["casa"] else p["puntsVisitant"]
    rival = p["puntsVisitant"] if p["casa"] else p["puntsLocal"]
    return "W" if barna > rival else ("L" if barna < rival else "E")


HEAD_NAV = """<a href="/club/">Club</a>
      <a href="/escoleta/" class="opt">Escoleta</a>
      <a href="/partits/">Dies de partit</a>
      <a href="/patrocinadors/" class="opt">Patrocinadors</a>
      <a href="/campus/" class="opt">Campus</a>
      <a href="/3x3/" class="opt">3x3</a>
      <a href="/cistella-petita/" class="opt">Cistella Petita</a>
      <a href="/fotos/" class="opt">Galeria</a>
      <a href="/premsa/">Premsa</a>"""

FOOTER = """<footer class="foot">
  <div class="wrap">
    <div class="foot-grid">
      <div class="foot-col">
        <h3>El Barna</h3>
        <a href="/escoleta/">Escola de bàsquet</a>
        <a href="/campus/">Campus de bàsquet</a>
        <a href="/3x3/">Torneig 3x3</a>
        <a href="/grup-barna-dades-oficials/">Dades oficials</a>
      </div>
      <div class="foot-col">
        <h3>Temporada</h3>
        <a href="/partits/">Dies de partit</a>
        <a href="/partits/equips/">Tots els equips</a>
        <a href="/partits/calendaris/">Dies de partit per equip</a>
        <a href="/fotos/">Galeria de fotos</a>
        <a href="/blog/">Blog</a>
        <a href="/premsa/">Articles i premsa</a>
      </div>
      <div class="foot-col">
        <h3>Contacte</h3>
        <a href="/#info">Demanar informació</a>
        <a href="/faq/">Preguntes freqüents</a>
        <a href="mailto:marqueting@cbgrupbarna.info">marqueting@cbgrupbarna.info</a>
        <a href="https://wa.me/34698425153">+34 698 425 153</a>
        <p>La Nau del Clot · Sant Martí<br>08018 Barcelona</p>
      </div>
      <div class="foot-col">
        <h3>Xarxes</h3>
        <a href="https://www.instagram.com/cbgrupbarna/" target="_blank" rel="noopener">Instagram</a>
        <a href="https://www.tiktok.com/@cbgrupbarna" target="_blank" rel="noopener">TikTok</a>
      </div>
    </div>
    <div class="foot-btm">
      <div class="foot-mark">#Som<em>Clot</em></div>
      <div class="foot-legal">© 2026 CB Grup Barna · Bàsquet base al Clot des de 1965</div>
    </div>
  </div>
</footer>"""


def head_html(title, desc, canonical, og_image, extra_ld):
    return f"""<!DOCTYPE html>
<html lang="ca">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#F4F1EC">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1">
<meta property="og:type" content="article">
<meta property="og:site_name" content="CB Grup Barna">
<meta property="og:locale" content="ca_ES">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og_image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@cbgrupbarna">
<link rel="icon" href="/logo.png">
<link rel="apple-touch-icon" href="/icon-192.png">
<link rel="manifest" href="/manifest.json">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Jost:wght@200;300;400;500&family=Inter:wght@300;400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/css/barna.css">
<script type="application/ld+json">{json.dumps(extra_ld, ensure_ascii=False)}</script>
<script src="/js/galetes.js"></script>
</head>
"""


def header_html():
    return f"""<body>
<a href="#main" class="skip">Saltar al contingut</a>
<header class="head">
  <div class="head-in">
    <a class="head-brand" href="/" aria-label="CB Grup Barna · inici">
      <img src="/logo.png" alt="Escut del CB Grup Barna" width="30" height="30">
      <span>CB Grup Barna</span>
    </a>
    <nav class="head-nav" aria-label="Navegació principal">
      {HEAD_NAV}
    </nav>
  </div>
</header>
"""


def match_line(p, eq_nom):
    resultat_txt = ""
    r = resultat(p)
    if r:
        resultat_txt = f" · <strong>{p['puntsLocal']}-{p['puntsVisitant']}</strong> ({'victòria' if r == 'W' else 'derrota' if r == 'L' else 'empat'})"
    return (f"<li>{fmt_dia(p['data'])}, {esc(p['hora'])} — "
            f"{esc(p['local'])} vs {esc(p['visitant'])} · {esc(p.get('pista', ''))}{resultat_txt}</li>")


def team_page(e, data, avui):
    partits = sorted((p for p in data["partits"] if p["equipId"] == e["id"]), key=lambda p: (p["data"], p["hora"]))
    propers = [p for p in partits if p["data"] >= avui]
    jugats = [p for p in partits if resultat(p)]
    resultats_recents = sorted(jugats, key=lambda p: (p["data"], p["hora"]), reverse=True)[:MAX_RESULTATS]
    w = sum(1 for p in jugats if resultat(p) == "W")
    l = sum(1 for p in jugats if resultat(p) == "L")
    nom = e.get("nom", e["id"])
    competicio = e.get("competicio", "")
    canonical = f"{BASE_URL}/partits/equips/{e['id']}/"
    posicio_txt = f" · {e['posicio']}a posició del seu grup" if e.get("posicio") else ""
    desc = clamp_desc(f"Calendari i resultats de {nom} ({competicio}) del CB Grup Barna: "
                      f"balanç {w}-{l}{posicio_txt}. Actualitzat cada dia des del calendari oficial de la FCBQ.")
    title = f"{nom} · Calendari i resultats | CB Grup Barna"
    og_image = f"{BASE_URL}/partits/calendaris/img/{e['id']}.webp"

    ld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "SportsTeam",
                "name": f"{nom} · CB Grup Barna",
                "sport": "Basketball",
                "url": canonical,
                "memberOf": {"@type": "SportsOrganization", "name": "CB Grup Barna", "url": BASE_URL},
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "CB Grup Barna", "item": f"{BASE_URL}/"},
                    {"@type": "ListItem", "position": 2, "name": "Dies de partit", "item": f"{BASE_URL}/partits/"},
                    {"@type": "ListItem", "position": 3, "name": "Equips", "item": f"{BASE_URL}/partits/equips/"},
                    {"@type": "ListItem", "position": 4, "name": nom, "item": canonical},
                ],
            },
        ],
    }

    propers_html = ("<ul>" + "".join(match_line(p, nom) for p in propers[:MAX_RESULTATS]) + "</ul>") if propers \
        else "<p class=\"lede\">Encara no hi ha propers partits carregats per a aquest equip.</p>"
    resultats_html = ("<ul>" + "".join(match_line(p, nom) for p in resultats_recents) + "</ul>") if resultats_recents \
        else "<p class=\"lede\">Encara no s'ha jugat cap partit aquesta temporada.</p>"
    calendari_html = ("<ul>" + "".join(match_line(p, nom) for p in partits) + "</ul>") if partits \
        else "<p class=\"lede\">Encara no hi ha calendari carregat per a aquest equip.</p>"

    body = f"""{header_html()}
<main id="main">
<div class="wrap"><nav class="crumb" aria-label="Fil d'Ariadna"><a href="/">Inici</a> · <a href="/partits/">Dies de partit</a> · <a href="/partits/equips/">Equips</a> · <span>{esc(nom)}</span></nav></div>
<div class="wrap">
  <div class="phead narrow">
    <p class="eyebrow red">{esc(competicio)}</p>
    <h1>{esc(nom)}</h1>
    <p class="lede">Balanç d'aquesta temporada: <strong>{w}-{l}</strong> (V-D){posicio_txt}. Calendari i
    resultats sincronitzats cada dia amb el calendari oficial de la FCBQ.</p>
    <div class="btn-row">
      <a href="/partits/" class="btn red" data-cta="team-app-{e['id']}">Tots els dies de partit del club</a>
      <a href="webcal://cbgrupbarna.info/partits/calendaris/ics/{e['id']}.ics" class="btn ghost" data-cta="team-ics-{e['id']}">🔔 Subscriu-te al calendari</a>
    </div>
  </div>

  <div class="narrow">
    <h2 style="font-family:var(--display);font-size:clamp(16px,2.1vw,22px);margin:28px 0 14px">Propers partits</h2>
    {propers_html}
    <h2 style="font-family:var(--display);font-size:clamp(16px,2.1vw,22px);margin:28px 0 14px">Últims resultats</h2>
    {resultats_html}
    <details style="margin-top:28px"><summary style="font-family:var(--display);font-size:clamp(16px,2.1vw,22px);cursor:pointer">Calendari complet de la temporada ({len(partits)} partits)</summary>
    <div style="margin-top:14px">{calendari_html}</div></details>
  </div>
</div>
</main>
{FOOTER}
</body>
</html>
"""
    return head_html(title, desc, canonical, og_image, ld) + body


def index_page(data, avui):
    equips = data["equips"]
    grups = {}
    for e in equips:
        grups.setdefault(categoria_de(e.get("nom", "")), []).append(e)
    order = CATEGORIES + ["Altres"]

    sections = []
    for cat in order:
        llista = grups.get(cat)
        if not llista:
            continue
        items = []
        for e in sorted(llista, key=lambda x: x.get("nom", "")):
            jugats = [p for p in data["partits"] if p["equipId"] == e["id"] and resultat(p)]
            w = sum(1 for p in jugats if resultat(p) == "W")
            l = sum(1 for p in jugats if resultat(p) == "L")
            items.append(
                f'<li><a href="/partits/equips/{e["id"]}/"><strong>{esc(e.get("nom", e["id"]))}</strong></a> '
                f'— {esc(e.get("competicio", ""))} · {w}-{l} (V-D)</li>'
            )
        sections.append(f"<h2 style=\"font-family:var(--display);font-size:clamp(16px,2.1vw,22px);margin:28px 0 14px\">{esc(cat)}</h2><ul>" + "".join(items) + "</ul>")

    canonical = f"{BASE_URL}/partits/equips/"
    title = "Tots els equips · CB Grup Barna"
    desc = clamp_desc("Tots els equips federats del CB Grup Barna, per categoria: cadet, infantil, "
                      "júnior i sènior, femení i masculí. Calendari, resultats i balanç de cadascun.")
    ld = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "CollectionPage", "name": title, "description": desc, "url": canonical, "inLanguage": "ca-ES"},
            {"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "CB Grup Barna", "item": f"{BASE_URL}/"},
                {"@type": "ListItem", "position": 2, "name": "Dies de partit", "item": f"{BASE_URL}/partits/"},
                {"@type": "ListItem", "position": 3, "name": "Equips", "item": canonical},
            ]},
        ],
    }
    body = f"""{header_html()}
<main id="main">
<div class="wrap"><nav class="crumb" aria-label="Fil d'Ariadna"><a href="/">Inici</a> · <a href="/partits/">Dies de partit</a> · <span>Equips</span></nav></div>
<div class="wrap">
  <div class="phead narrow">
    <p class="eyebrow red">Temporada {esc(data.get('temporada', ''))}</p>
    <h1>Tots els equips</h1>
    <p class="lede">{len(data['equips'])} equips federats del CB Grup Barna. Toca un equip per veure el seu
    calendari, els últims resultats i subscriure't per rebre els canvis automàticament.</p>
  </div>
  <div class="narrow">{''.join(sections)}</div>
</div>
</main>
{FOOTER}
</body>
</html>
"""
    return head_html(title, desc, canonical, f"{BASE_URL}/og-image.jpg", ld) + body


def main():
    if not DATA.exists():
        print("[equips] falta partits/data.json — no es fa res")
        return 0
    try:
        data = json.loads(DATA.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"[equips] data.json illegible ({exc}) — no es toca res")
        return 0

    avui = date.today().isoformat()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for e in data["equips"]:
        d = OUT_DIR / e["id"]
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(team_page(e, data, avui), encoding="utf-8")

    (OUT_DIR / "index.html").write_text(index_page(data, avui), encoding="utf-8")
    print(f"[equips] OK → {len(data['equips'])} pàgines d'equip + 1 índex, a {OUT_DIR.relative_to(ROOT)}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
