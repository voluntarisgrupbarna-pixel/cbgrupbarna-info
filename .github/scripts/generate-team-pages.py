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

Les fa en els tres idiomes: /partits/equips/, /es/partits/equips/ i
/en/partits/equips/. Aquestes pàgines no es poden traduir a mà —el robot les
reescriu cada dia i la traducció quedaria vella l'endemà—, així que el que
sap tres idiomes és el generador. Els noms dels equips no es toquen: «Cadet
Femení A» és com es diu a la fitxa de la FCBQ, i és el que la gent busca.
"""
import importlib.util
import json
import re
import sys
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

# La capçalera i el peu surten del diccionari de i18n/, com a la resta del
# lloc, en comptes de tenir-ne una còpia aquí. El nom del fitxer porta guions
# i per això s'importa a mà.
_spec = importlib.util.spec_from_file_location("i18n_chrome", ROOT / "scripts" / "i18n_chrome.py")
_chrome = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_chrome)
DATA = ROOT / "partits" / "data.json"
OUT_DIR = ROOT / "partits" / "equips"
BASE_URL = "https://cbgrupbarna.info"

DIES = {
    "ca": ["Dilluns", "Dimarts", "Dimecres", "Dijous", "Divendres", "Dissabte", "Diumenge"],
    "es": ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"],
    "en": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
}
MESOS = {
    "ca": ["gen", "feb", "mar", "abr", "maig", "juny", "jul", "ag", "set", "oct", "nov", "des"],
    "es": ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"],
    "en": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
}
# Les categories de la FCBQ. El nom de l'equip no es tradueix mai; el títol
# de la secció de l'índex, sí, perquè és text nostre.
CATEGORIES = ["Sènior", "Júnior", "Cadet", "Infantil", "Preinfantil", "Mini", "Premini"]
CATEGORIA_TRAD = {
    "es": {"Sènior": "Sénior", "Júnior": "Júnior", "Cadet": "Cadete", "Infantil": "Infantil",
           "Preinfantil": "Preinfantil", "Mini": "Mini", "Premini": "Premini", "Altres": "Otros"},
    "en": {"Sènior": "Senior", "Júnior": "Under-18", "Cadet": "Under-16", "Infantil": "Under-14",
           "Preinfantil": "Under-13", "Mini": "Under-12", "Premini": "Under-10", "Altres": "Other"},
}

T = {
  "ca": {
    "locale": "ca_ES", "inici": "Inici", "partits": "Calendari", "equips": "Equips",
    "crumb_aria": "Fil d'Ariadna",
    "victoria": "victòria", "derrota": "derrota", "empat": "empat",
    "posicio": "{n}a posició del seu grup",
    "balanc": "Balanç d'aquesta temporada: <strong>{w}-{l}</strong> (V-D){pos}. Calendari i "
              "resultats sincronitzats cada dia amb el calendari oficial de la FCBQ.",
    "vd": "(V-D)",
    "tots_partits": "Tots els dies de partit del club", "subscriu": "🔔 Subscriu-te al calendari",
    "propers": "Propers partits", "ultims": "Últims resultats",
    "complet": "Calendari complet de la temporada ({n} partits)",
    "sense_propers": "Encara no hi ha propers partits carregats per a aquest equip.",
    "sense_jugats": "Encara no s'ha jugat cap partit aquesta temporada.",
    "sense_calendari": "Encara no hi ha calendari carregat per a aquest equip.",
    "titol_equip": "{nom} · Calendari i resultats | CB Grup Barna",
    "desc_equip": "Calendari i resultats de {nom} ({comp}) del CB Grup Barna: balanç {w}-{l}{pos}. "
                  "Actualitzat cada dia des del calendari oficial de la FCBQ.",
    "titol_index": "Tots els equips · CB Grup Barna", "h1_index": "Tots els equips",
    "temporada": "Temporada {t}",
    "desc_index": "Tots els equips federats del CB Grup Barna, per categoria: cadet, infantil, "
                  "júnior i sènior, femení i masculí. Calendari, resultats i balanç de cadascun.",
    "lede_index": "{n} equips federats del CB Grup Barna. Toca un equip per veure el seu calendari, "
                  "els últims resultats i subscriure't per rebre els canvis automàticament.",
  },
  "es": {
    "locale": "es_ES", "inici": "Inicio", "partits": "Calendario", "equips": "Equipos",
    "crumb_aria": "Ruta de navegación",
    "victoria": "victoria", "derrota": "derrota", "empat": "empate",
    "posicio": "{n}ª posición de su grupo",
    "balanc": "Balance de esta temporada: <strong>{w}-{l}</strong> (V-D){pos}. Calendario y "
              "resultados sincronizados cada día con el calendario oficial de la FCBQ.",
    "vd": "(V-D)",
    "tots_partits": "Todos los días de partido del club", "subscriu": "🔔 Suscríbete al calendario",
    "propers": "Próximos partidos", "ultims": "Últimos resultados",
    "complet": "Calendario completo de la temporada ({n} partidos)",
    "sense_propers": "Todavía no hay próximos partidos cargados para este equipo.",
    "sense_jugats": "Todavía no se ha jugado ningún partido esta temporada.",
    "sense_calendari": "Todavía no hay calendario cargado para este equipo.",
    "titol_equip": "{nom} · Calendario y resultados | CB Grup Barna",
    "desc_equip": "Calendario y resultados de {nom} ({comp}) del CB Grup Barna: balance {w}-{l}{pos}. "
                  "Actualizado cada día desde el calendario oficial de la FCBQ.",
    "titol_index": "Todos los equipos · CB Grup Barna", "h1_index": "Todos los equipos",
    "temporada": "Temporada {t}",
    "desc_index": "Todos los equipos federados del CB Grup Barna, por categoría: cadete, infantil, "
                  "júnior y sénior, femenino y masculino. Calendario, resultados y balance de cada uno.",
    "lede_index": "{n} equipos federados del CB Grup Barna. Toca un equipo para ver su calendario, "
                  "los últimos resultados y suscribirte para recibir los cambios automáticamente.",
  },
  "en": {
    "locale": "en_US", "inici": "Home", "partits": "Calendar", "equips": "Teams",
    "crumb_aria": "Breadcrumb",
    "victoria": "win", "derrota": "loss", "empat": "draw",
    "posicio": "{n}th in their group",
    "balanc": "This season's record: <strong>{w}-{l}</strong> (W-L){pos}. Fixtures and results "
              "synced daily with the official FCBQ calendar.",
    "vd": "(W-L)",
    "tots_partits": "Every club match day", "subscriu": "🔔 Subscribe to the calendar",
    "propers": "Next fixtures", "ultims": "Latest results",
    "complet": "Full season fixture list ({n} games)",
    "sense_propers": "No upcoming fixtures loaded for this team yet.",
    "sense_jugats": "No games played yet this season.",
    "sense_calendari": "No fixture list loaded for this team yet.",
    "titol_equip": "{nom} · Fixtures and results | CB Grup Barna",
    "desc_equip": "Fixtures and results for {nom} ({comp}) of CB Grup Barna: record {w}-{l}{pos}. "
                  "Updated daily from the official FCBQ calendar.",
    "titol_index": "All teams · CB Grup Barna", "h1_index": "All teams",
    "temporada": "{t} season",
    "desc_index": "Every registered CB Grup Barna team, by age group: under-14 to senior, girls' and "
                  "boys'. Fixtures, results and record for each one.",
    "lede_index": "{n} registered CB Grup Barna teams. Tap a team to see its fixtures, its latest "
                  "results and to subscribe for changes automatically.",
  },
}
IDIOMES = ("ca", "es", "en")
MAX_RESULTATS = 8


def prefix(idioma):
    return "" if idioma == "ca" else f"/{idioma}"


def fmt_dia(iso, idioma):
    d = date.fromisoformat(iso)
    if idioma == "en":
        return f"{DIES['en'][d.weekday()]} {d.day} {MESOS['en'][d.month - 1]}"
    return f"{DIES[idioma][d.weekday()]} {d.day} {MESOS[idioma][d.month - 1]}"


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


def head_html(title, desc, canonical, og_image, extra_ld, idioma):
    return f"""<!DOCTYPE html>
<html lang="{idioma}">
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
<meta property="og:locale" content="{T[idioma]['locale']}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og_image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@cbgrupbarna">
<link rel="icon" href="/logo.png">
<link rel="apple-touch-icon" href="/icon-192.png">
<link rel="manifest" href="/manifest.json">
<link rel="stylesheet" href="/css/fonts.css">
<link rel="stylesheet" href="/css/barna.css">
<!-- El cercador: el full i el motor. El botó de la lupa no s'escriu
     aquí, el planta /js/cerca.js dins de la capçalera. -->
<link rel="stylesheet" href="/css/cerca.css">
<script type="application/ld+json">{json.dumps(extra_ld, ensure_ascii=False)}</script>
<script src="/js/galetes.js"></script>
<script src="/js/cerca.js" defer></script>
</head>
"""


def header_html(idioma):
    return f"""<body>
<a href="#main" class="skip">{_chrome.text("salta", idioma)}</a>
<header class="head">
  <div class="head-in">
    <a class="head-brand" href="{prefix(idioma)}/" aria-label="{_chrome.text("inici_aria", idioma)}">
      <img src="/logo.png" alt="{_chrome.text("escut_alt", idioma)}" width="30" height="30">
      <span>CB Grup Barna</span>
    </a>
{_chrome.navegacio(idioma)}
  </div>
</header>
"""


def match_line(p, eq_nom, idioma):
    t = T[idioma]
    resultat_txt = ""
    r = resultat(p)
    if r:
        com = t["victoria"] if r == "W" else t["derrota"] if r == "L" else t["empat"]
        resultat_txt = f" · <strong>{p['puntsLocal']}-{p['puntsVisitant']}</strong> ({com})"
    return (f"<li>{fmt_dia(p['data'], idioma)}, {esc(p['hora'])} — "
            f"{esc(p['local'])} vs {esc(p['visitant'])} · {esc(p.get('pista', ''))}{resultat_txt}</li>")


def team_page(e, data, avui, idioma):
    t = T[idioma]
    pre = prefix(idioma)
    partits = sorted((p for p in data["partits"] if p["equipId"] == e["id"]), key=lambda p: (p["data"], p["hora"]))
    propers = [p for p in partits if p["data"] >= avui]
    jugats = [p for p in partits if resultat(p)]
    resultats_recents = sorted(jugats, key=lambda p: (p["data"], p["hora"]), reverse=True)[:MAX_RESULTATS]
    w = sum(1 for p in jugats if resultat(p) == "W")
    l = sum(1 for p in jugats if resultat(p) == "L")
    nom = e.get("nom", e["id"])
    competicio = e.get("competicio", "")
    canonical = f"{BASE_URL}{pre}/partits/equips/{e['id']}/"
    posicio_txt = " · " + t["posicio"].format(n=e["posicio"]) if e.get("posicio") else ""
    desc = clamp_desc(t["desc_equip"].format(nom=nom, comp=competicio, w=w, l=l, pos=posicio_txt))
    title = t["titol_equip"].format(nom=nom)
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
                    {"@type": "ListItem", "position": 1, "name": "CB Grup Barna", "item": f"{BASE_URL}{pre}/"},
                    {"@type": "ListItem", "position": 2, "name": t["partits"], "item": f"{BASE_URL}{pre}/partits/"},
                    {"@type": "ListItem", "position": 3, "name": t["equips"], "item": f"{BASE_URL}{pre}/partits/equips/"},
                    {"@type": "ListItem", "position": 4, "name": nom, "item": canonical},
                ],
            },
        ],
    }

    propers_html = ("<ul>" + "".join(match_line(p, nom, idioma) for p in propers[:MAX_RESULTATS]) + "</ul>") \
        if propers else f"<p class=\"lede\">{t['sense_propers']}</p>"
    resultats_html = ("<ul>" + "".join(match_line(p, nom, idioma) for p in resultats_recents) + "</ul>") \
        if resultats_recents else f"<p class=\"lede\">{t['sense_jugats']}</p>"
    calendari_html = ("<ul>" + "".join(match_line(p, nom, idioma) for p in partits) + "</ul>") \
        if partits else f"<p class=\"lede\">{t['sense_calendari']}</p>"

    body = f"""{header_html(idioma)}
<main id="main">
<div class="wrap"><nav class="crumb" aria-label="{t['crumb_aria']}"><a href="{pre}/">{t['inici']}</a> · <a href="{pre}/partits/">{t['partits']}</a> · <a href="{pre}/partits/equips/">{t['equips']}</a> · <span>{esc(nom)}</span></nav></div>
<div class="wrap">
  <div class="phead narrow">
    <p class="eyebrow red">{esc(competicio)}</p>
    <h1>{esc(nom)}</h1>
    <p class="lede">{t['balanc'].format(w=w, l=l, pos=posicio_txt)}</p>
    <div class="btn-row">
      <a href="{pre}/partits/" class="btn red" data-cta="team-app-{e['id']}">{t['tots_partits']}</a>
      <a href="webcal://cbgrupbarna.info/partits/calendaris/ics/{e['id']}.ics" class="btn ghost" data-cta="team-ics-{e['id']}">{t['subscriu']}</a>
    </div>
  </div>

  <div class="narrow">
    <h2 style="font-family:var(--display);font-size:clamp(16px,2.1vw,22px);margin:28px 0 14px">{t['propers']}</h2>
    {propers_html}
    <h2 style="font-family:var(--display);font-size:clamp(16px,2.1vw,22px);margin:28px 0 14px">{t['ultims']}</h2>
    {resultats_html}
    <details style="margin-top:28px"><summary style="font-family:var(--display);font-size:clamp(16px,2.1vw,22px);cursor:pointer">{t['complet'].format(n=len(partits))}</summary>
    <div style="margin-top:14px">{calendari_html}</div></details>
  </div>
</div>
</main>
{_chrome.peu(idioma).replace("</main>", "", 1)}"""
    return head_html(title, desc, canonical, og_image, ld, idioma) + body


def index_page(data, avui, idioma):
    t = T[idioma]
    pre = prefix(idioma)
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
                f'<li><a href="{pre}/partits/equips/{e["id"]}/"><strong>{esc(e.get("nom", e["id"]))}</strong></a> '
                f'— {esc(e.get("competicio", ""))} · {w}-{l} {t["vd"]}</li>'
            )
        titol_cat = CATEGORIA_TRAD.get(idioma, {}).get(cat, cat)
        sections.append(f"<h2 style=\"font-family:var(--display);font-size:clamp(16px,2.1vw,22px);margin:28px 0 14px\">{esc(titol_cat)}</h2><ul>" + "".join(items) + "</ul>")

    canonical = f"{BASE_URL}{pre}/partits/equips/"
    title = t["titol_index"]
    desc = clamp_desc(t["desc_index"])
    ld = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "CollectionPage", "name": title, "description": desc, "url": canonical,
             "inLanguage": T[idioma]["locale"].replace("_", "-")},
            {"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "CB Grup Barna", "item": f"{BASE_URL}{pre}/"},
                {"@type": "ListItem", "position": 2, "name": t["partits"], "item": f"{BASE_URL}{pre}/partits/"},
                {"@type": "ListItem", "position": 3, "name": t["equips"], "item": canonical},
            ]},
        ],
    }
    body = f"""{header_html(idioma)}
<main id="main">
<div class="wrap"><nav class="crumb" aria-label="{t['crumb_aria']}"><a href="{pre}/">{t['inici']}</a> · <a href="{pre}/partits/">{t['partits']}</a> · <span>{t['equips']}</span></nav></div>
<div class="wrap">
  <div class="phead narrow">
    <p class="eyebrow red">{t['temporada'].format(t=esc(data.get('temporada', '')))}</p>
    <h1>{t['h1_index']}</h1>
    <p class="lede">{t['lede_index'].format(n=len(data['equips']))}</p>
  </div>
  <div class="narrow">{''.join(sections)}</div>
</div>
</main>
{_chrome.peu(idioma).replace("</main>", "", 1)}"""
    return head_html(title, desc, canonical, f"{BASE_URL}/og-image.jpg", ld, idioma) + body


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
    for idioma in IDIOMES:
        out = ROOT / (prefix(idioma).lstrip("/") or ".") / "partits" / "equips"
        out.mkdir(parents=True, exist_ok=True)
        for e in data["equips"]:
            d = out / e["id"]
            d.mkdir(parents=True, exist_ok=True)
            (d / "index.html").write_text(team_page(e, data, avui, idioma), encoding="utf-8")
        (out / "index.html").write_text(index_page(data, avui, idioma), encoding="utf-8")
        print(f"[equips] {idioma} → {len(data['equips'])} pàgines d'equip + 1 índex, a {out.relative_to(ROOT)}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
