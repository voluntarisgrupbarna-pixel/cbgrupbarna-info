#!/usr/bin/env python3
"""
SEO / SEO-IA · CB Grup Barna
Genera dins de partits/index.html un resum ESTATIC (sense JavaScript) dels
propers partits, els ultims resultats i un bloc JSON-LD amb els partits com
a SportsEvent. La majoria de bots d'IA (GPTBot, ClaudeBot, PerplexityBot...)
no executen JavaScript: sense aixo, veurien una pagina buida perque tot el
calendari es pinta amb fetch('data.json') + JS. El bloc estatic viu dins
<noscript>, així que els navegadors amb JavaScript el sobreescriuen a
l'instant (renderJornada() substitueix tot #jornada-list) i mai es veu.

S'executa cada dia, just despres d'update-partits.py, per reflectir sempre
data.json al dia. Disseny defensiu: si data.json no es pot llegir o no hi
ha partits, deixa els blocs buits en comptes de trencar la pagina.
"""
import json
import re
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "partits" / "data.json"
HTML = ROOT / "partits" / "index.html"
CAL_MANIFEST = ROOT / "partits" / "calendaris" / "manifest.json"
CAL_HTML = ROOT / "partits" / "calendaris" / "index.html"

DIES = ["Dilluns", "Dimarts", "Dimecres", "Dijous", "Divendres", "Dissabte", "Diumenge"]
MESOS = ["gen", "feb", "mar", "abr", "maig", "juny", "jul", "ag", "set", "oct", "nov", "des"]
FINESTRA_EVENTS_DIES = 21  # quants dies de partits futurs entren al JSON-LD
MAX_RESULTATS = 10


def fmt_dia(iso):
    d = date.fromisoformat(iso)
    return f"{DIES[d.weekday()]} {d.day} {MESOS[d.month - 1]}"


def monday_of(iso):
    d = date.fromisoformat(iso)
    return d - timedelta(days=d.weekday())


def esc(s):
    return (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def linia_partit(p, eq_nom):
    return (f"<li><strong>{fmt_dia(p['data'])}, {esc(p['hora'])}</strong> — "
            f"{esc(p['local'])} vs {esc(p['visitant'])} "
            f"({esc(eq_nom)}) · {esc(p['pista'])}</li>")


def linia_resultat(p, eq_nom):
    return (f"<li><strong>{fmt_dia(p['data'])}</strong> — "
            f"{esc(p['local'])} {p['puntsLocal']}–{p['puntsVisitant']} {esc(p['visitant'])} "
            f"({esc(eq_nom)})</li>")


def build_snapshot(data, avui):
    equips = {e["id"]: e.get("nom", "") for e in data["equips"]}
    pendents = sorted((p for p in data["partits"] if p["data"] >= avui), key=lambda p: (p["data"], p["hora"]))
    setmana = []
    if pendents:
        wk = monday_of(pendents[0]["data"]).isoformat()
        setmana = sorted(
            (p for p in data["partits"] if monday_of(p["data"]).isoformat() == wk),
            key=lambda p: (p["data"], p["hora"]),
        )
    jugats = sorted(
        (p for p in data["partits"] if p.get("puntsLocal") is not None),
        key=lambda p: (p["data"], p["hora"]),
        reverse=True,
    )[:MAX_RESULTATS]

    out = ["<h2>Pròxims partits del CB Grup Barna</h2>"]
    if setmana:
        out.append("<ul>" + "".join(linia_partit(p, equips.get(p["equipId"], "")) for p in setmana) + "</ul>")
    else:
        out.append("<p>Encara no hi ha partits carregats per a les properes setmanes.</p>")
    if jugats:
        out.append("<h2>Últims resultats</h2>")
        out.append("<ul>" + "".join(linia_resultat(p, equips.get(p["equipId"], "")) for p in jugats) + "</ul>")
    return "".join(out), len(setmana), len(jugats)


def resultat(p):
    """Mateixa lògica que model() al JS: W/L/E des del punt de vista del Barna."""
    if p.get("puntsLocal") is None or p.get("puntsVisitant") is None:
        return None
    barna = p["puntsLocal"] if p["casa"] else p["puntsVisitant"]
    rival = p["puntsVisitant"] if p["casa"] else p["puntsLocal"]
    return "W" if barna > rival else ("L" if barna < rival else "E")


def build_equips_fallback(data):
    """Llista de tots els equips amb categoria/competició i balanç V-D —
    contingut estàtic amb el nom de cada equip, que és el que la gent busca
    ("Cadet Femení A CB Grup Barna", "Sènior Masculí B Grup Barna"...)."""
    items = []
    for e in data["equips"]:
        jugats = [resultat(p) for p in data["partits"] if p["equipId"] == e["id"]]
        jugats = [r for r in jugats if r]
        w, l = jugats.count("W"), jugats.count("L")
        posicio = f" · {e['posicio']}a posició" if e.get("posicio") else ""
        items.append(
            f"<li><strong>{esc(e['nom'])}</strong> — {esc(e.get('competicio', ''))} "
            f"· {w}-{l} (V-D){posicio}</li>"
        )
    if not items:
        return ""
    return "<ul>" + "".join(items) + "</ul>"


def build_events(data, avui):
    equips = {e["id"]: e.get("nom", "") for e in data["equips"]}
    fi = (date.fromisoformat(avui) + timedelta(days=FINESTRA_EVENTS_DIES)).isoformat()
    pendents = sorted((p for p in data["partits"] if p["data"] >= avui), key=lambda p: (p["data"], p["hora"]))
    propers = [p for p in pendents if p["data"] <= fi]
    if not propers and pendents:
        # fora de temporada la finestra de N dies pot no arribar al primer
        # partit (p.ex. a l'estiu): en aquest cas s'agafa igualment el
        # proper cap de setmana amb partits, per no deixar el bloc buit.
        wk = monday_of(pendents[0]["data"]).isoformat()
        propers = [p for p in pendents if monday_of(p["data"]).isoformat() == wk]
    events = []
    for p in propers:
        eq_nom = equips.get(p["equipId"], "")
        events.append({
            "@type": "SportsEvent",
            "name": f"{p['local']} - {p['visitant']} ({eq_nom})".strip(),
            "startDate": f"{p['data']}T{p['hora']}:00+01:00",
            "sport": "Basketball",
            "eventStatus": "https://schema.org/EventScheduled",
            "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
            "location": {
                "@type": "Place",
                "name": p.get("pista") or "Per confirmar",
                "address": p.get("adreca") or "",
            },
            "homeTeam": {"@type": "SportsTeam", "name": p["local"]},
            "awayTeam": {"@type": "SportsTeam", "name": p["visitant"]},
            "organizer": {"@type": "SportsOrganization", "name": "CB Grup Barna", "url": "https://cbgrupbarna.info"},
        })
    if not events:
        return "", 0
    ld = {"@context": "https://schema.org", "@graph": events}
    return f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>', len(events)


def build_calendaris_fallback():
    if not CAL_MANIFEST.exists():
        return "", 0
    try:
        manifest = json.loads(CAL_MANIFEST.read_text(encoding="utf-8"))
    except Exception:
        return "", 0
    files = {p.stem: p.name for p in (ROOT / "partits" / "calendaris" / "descarrega").glob("*")} \
        if (ROOT / "partits" / "calendaris" / "descarrega").exists() else {}
    items = []
    for eq_id, info in sorted(manifest.items(), key=lambda kv: kv[1].get("nom", kv[0])):
        fitxer = files.get(eq_id)
        if not fitxer:
            continue
        tipus = (info.get("tipus") or "png").upper()
        items.append(
            f'<li><a href="/partits/calendaris/descarrega/{esc(fitxer)}">'
            f'{esc(info.get("nom", eq_id))} — descarrega el calendari ({tipus}, '
            f'{info.get("jornades", "?")} jornades)</a></li>'
        )
    if not items:
        return "", 0
    return "<ul>" + "".join(items) + "</ul>", len(items)


def replace_between(html, marker, content):
    start, end = f"<!-- {marker}:START -->", f"<!-- {marker}:END -->"
    pattern = re.escape(start) + r".*?" + re.escape(end)
    return re.sub(pattern, start + content + end, html, count=1, flags=re.S)


def main():
    if not DATA.exists() or not HTML.exists():
        print("[seo] falten partits/data.json o partits/index.html — no es fa res")
        return 0
    try:
        data = json.loads(DATA.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"[seo] data.json illegible ({exc}) — no es toca res")
        return 0

    avui = date.today().isoformat()
    snapshot, n_propers, n_resultats = build_snapshot(data, avui)
    events_html, n_events = build_events(data, avui)
    equips_html = build_equips_fallback(data)

    html = HTML.read_text(encoding="utf-8")
    if "<!-- SEO-SNAPSHOT:START -->" not in html or "<!-- SEO-EVENTS:START -->" not in html:
        print("[seo] falten els marcadors SEO-SNAPSHOT/SEO-EVENTS a index.html — no es toca res")
        return 0
    if "<!-- SEO-EQUIPS:START -->" in html:
        html = replace_between(html, "SEO-EQUIPS", equips_html)
    html = replace_between(html, "SEO-SNAPSHOT", snapshot)
    html = replace_between(html, "SEO-EVENTS", events_html)
    HTML.write_text(html, encoding="utf-8")
    print(f"[seo] OK → {n_propers} partits al resum, {n_resultats} resultats, {n_events} events JSON-LD, "
          f"{len(data['equips'])} equips al llistat estàtic")

    if CAL_HTML.exists():
        cal_html = CAL_HTML.read_text(encoding="utf-8")
        if "<!-- SEO-CALENDARIS:START -->" in cal_html:
            cal_fallback, n_cal = build_calendaris_fallback()
            cal_html = replace_between(cal_html, "SEO-CALENDARIS", cal_fallback)
            CAL_HTML.write_text(cal_html, encoding="utf-8")
            print(f"[seo] calendaris → {n_cal} enllaços de descàrrega al resum estàtic")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
