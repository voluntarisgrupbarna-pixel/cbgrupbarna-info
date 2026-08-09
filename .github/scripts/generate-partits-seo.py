#!/usr/bin/env python3
"""
SEO / SEO IA · CB Grup Barna
Genera, a partir de partits/data.json, dos blocs de partits/index.html:

  1. SEO:EVENTS-JSONLD  — <head> — un @graph de SportsEvent (schema.org)
     amb els partits dels propers 60 dies, perquè cercadors i motors d'IA
     rebin dades estructurades del calendari sense haver d'executar JS.
  2. SEO:STATIC-CONTENT — <body> — un resum en text pla i real (visible,
     no ocult) amb els propers partits agrupats per equip, per als
     rastrejadors que no executen JavaScript (la majoria de bots d'IA).

Els dos blocs viuen entre marcadors HTML i es regeneren sencers cada
vegada: idempotent, no cal fer merge manual. Es crida automàticament
cada dia des de update-partits.yml, després d'actualitzar data.json.
"""
import html
import json
import re
from datetime import date, datetime, timedelta
from pathlib import Path

esc = html.escape

ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = ROOT / "partits" / "data.json"
INDEX_PATH = ROOT / "partits" / "index.html"
SITE = "https://cbgrupbarna.info"

JSONLD_WINDOW_DAYS = 60   # abast del bloc de dades estructurades
STATIC_PER_TEAM = 5       # partits mostrats per equip al resum visible

DIES_CA = ["dilluns", "dimarts", "dimecres", "dijous", "divendres", "dissabte", "diumenge"]
MESOS_CA = ["", "gener", "febrer", "març", "abril", "maig", "juny", "juliol", "agost",
            "setembre", "octubre", "novembre", "desembre"]


def tz_offset(d):
    """Aproximació d'horari d'estiu/hivern espanyol (darrer diumenge de març/octubre)."""
    return "+02:00" if 4 <= d.month <= 9 else "+01:00"


def iso_start(partit):
    d = datetime.strptime(partit["data"], "%Y-%m-%d").date()
    hora = partit.get("hora") or "00:00"
    return f"{partit['data']}T{hora}:00{tz_offset(d)}"


def human_date(d):
    return f"{DIES_CA[d.weekday()]} {d.day} {MESOS_CA[d.month]} {d.year}"


def sport_event(p, equip):
    home = p["local"]
    away = p["visitant"]
    node = {
        "@type": "SportsEvent",
        "@id": f"{SITE}/partits/#{p['id']}",
        "name": f"{home} vs {away}",
        "sport": "https://en.wikipedia.org/wiki/Basketball",
        "startDate": iso_start(p),
        "eventStatus": "https://schema.org/EventCompleted" if p["estat"] == "jugat" else "https://schema.org/EventScheduled",
        "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
        "homeTeam": {"@type": "SportsTeam", "name": home},
        "awayTeam": {"@type": "SportsTeam", "name": away},
        "location": {
            "@type": "Place",
            "name": p.get("pista") or "Per confirmar",
            "address": p.get("adreca") or "Barcelona",
        },
        "superEvent": {"@type": "SportsEvent", "name": p.get("categoria") or equip.get("competicio") or ""},
        "organizer": {"@type": "SportsOrganization", "name": "Federació Catalana de Basquetbol", "url": "https://www.basquetcatala.cat"},
    }
    if p["estat"] == "jugat" and p.get("puntsLocal") is not None and p.get("puntsVisitant") is not None:
        node["description"] = f"Resultat: {home} {p['puntsLocal']} - {p['puntsVisitant']} {away}"
    return node


def build_jsonld(data, avui):
    limit = avui + timedelta(days=JSONLD_WINDOW_DAYS)
    equips = {e["id"]: e for e in data["equips"]}
    partits = [
        p for p in data["partits"]
        if avui <= datetime.strptime(p["data"], "%Y-%m-%d").date() <= limit
    ]
    partits.sort(key=lambda p: (p["data"], p.get("hora") or "00:00"))
    events = [sport_event(p, equips.get(p["equipId"], {})) for p in partits]
    graph = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "SportsTeam",
                "@id": f"{SITE}/#club",
                "name": "CB Grup Barna",
                "sport": "Basketball",
            },
            {
                "@type": "ItemList",
                "name": f"Calendari de partits · propers {JSONLD_WINDOW_DAYS} dies",
                "numberOfItems": len(events),
                "itemListElement": [
                    {"@type": "ListItem", "position": i + 1, "item": ev}
                    for i, ev in enumerate(events)
                ],
            },
        ],
    }
    return json.dumps(graph, ensure_ascii=False, separators=(",", ":"))


def build_static_html(data, avui):
    equips = {e["id"]: e for e in data["equips"]}
    by_team = {}
    for p in data["partits"]:
        d = datetime.strptime(p["data"], "%Y-%m-%d").date()
        if d < avui:
            continue
        by_team.setdefault(p["equipId"], []).append(p)
    for lst in by_team.values():
        lst.sort(key=lambda p: (p["data"], p.get("hora") or "00:00"))

    total_pendents = sum(len(v) for v in by_team.values())
    n_equips = len(data["equips"])
    temporada = data.get("temporada", "")
    last_update = data.get("lastUpdate", "")

    parts = []
    parts.append(
        f'<p><strong>CB Grup Barna</strong> és un club de bàsquet base del barri del Clot '
        f'(Districte de Sant Martí, Barcelona) amb <strong>{n_equips} equips federats</strong> a la '
        f'Federació Catalana de Basquetbol per a la temporada <strong>{temporada}</strong>. '
        f'Aquest calendari es genera automàticament cada dia (darrera actualització: {last_update}) '
        f'a partir del Calendari Global de la FCBQ i mostra els {total_pendents} partits pendents de la temporada, '
        f'jornada a jornada, amb dia, hora, rival, casa o fora i pavelló. '
        f'El calendari complet i descarregable en PDF per equip és a '
        f'<a href="/partits/calendaris/">cbgrupbarna.info/partits/calendaris/</a>, '
        f'i les dades en brut (JSON, obert) a '
        f'<a href="/partits/data.json">cbgrupbarna.info/partits/data.json</a>.</p>'
    )

    for eq in data["equips"]:
        matches = by_team.get(eq["id"], [])
        if not matches:
            continue
        parts.append(f'<h3>{esc(eq["nom"])}</h3>')
        parts.append(f'<p class="seo-team-meta">{esc(eq.get("competicio") or "")}</p>')
        rows = []
        for p in matches[:STATIC_PER_TEAM]:
            d = datetime.strptime(p["data"], "%Y-%m-%d").date()
            casa_fora = "Casa" if p["casa"] else "Fora"
            rival = p["visitant"] if p["casa"] else p["local"]
            res = "—"
            if p["estat"] == "jugat" and p.get("puntsLocal") is not None:
                res = f'{p["puntsLocal"]}-{p["puntsVisitant"]}'
            pista = p.get("pista") or "Per confirmar"
            rows.append(
                f'<tr><td>{esc(human_date(d))}, {esc(p.get("hora") or "")}</td><td>{casa_fora}</td>'
                f'<td>{esc(rival)}</td><td>{esc(pista)}</td><td class="res">{esc(res)}</td></tr>'
            )
        remaining = len(matches) - STATIC_PER_TEAM
        caption = f"Pròxims partits de {eq['nom']}"
        if remaining > 0:
            caption += f" · {remaining} més aquesta temporada al calendari complet"
        parts.append(
            '<table><caption>' + esc(caption) + '</caption>'
            '<thead><tr><th>Data</th><th>Casa/Fora</th><th>Rival</th><th>Pavelló</th><th>Resultat</th></tr></thead>'
            '<tbody>' + "".join(rows) + '</tbody></table>'
        )

    body = "\n".join(parts)
    return (
        '<details class="seo-static" id="calendari-text">\n'
        '<summary>Veure el calendari complet en text (per a cercadors i lectors de pantalla)</summary>\n'
        f'<h2>Calendari de partits del CB Grup Barna · Temporada {temporada}</h2>\n'
        f'{body}\n'
        '</details>'
    )


def replace_between(text, start_marker, end_marker, new_content):
    pattern = re.compile(
        re.escape(start_marker) + r".*?" + re.escape(end_marker), re.S
    )
    replacement = start_marker + "\n" + new_content + "\n" + end_marker
    if not pattern.search(text):
        raise SystemExit(f"Marcadors no trobats: {start_marker} … {end_marker}")
    return pattern.sub(lambda _: replacement, text, count=1)


def bump_sitemap(avui):
    sitemap_path = ROOT / "sitemap.xml"
    if not sitemap_path.exists():
        return
    xml = sitemap_path.read_text(encoding="utf-8")
    for loc in (f"{SITE}/partits/", f"{SITE}/partits/calendaris/"):
        block_re = re.compile(
            r"(<loc>" + re.escape(loc) + r"</loc>\s*<lastmod>)[^<]*(</lastmod>)"
        )
        xml, n = block_re.subn(rf"\g<1>{avui.isoformat()}\g<2>", xml)
    sitemap_path.write_text(xml, encoding="utf-8")


def main():
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    avui = date.today()

    jsonld = build_jsonld(data, avui)
    static_html = build_static_html(data, avui)

    page = INDEX_PATH.read_text(encoding="utf-8")
    page = replace_between(
        page,
        "<!-- SEO:EVENTS-JSONLD:START · generat automàticament per .github/scripts/generate-partits-seo.py a partir de partits/data.json. No editar a mà: els canvis es perdran en la propera execució diària. -->",
        "<!-- SEO:EVENTS-JSONLD:END -->",
        f'<script type="application/ld+json">{jsonld}</script>',
    )
    page = replace_between(
        page,
        '<!-- SEO:STATIC-CONTENT:START · generat automàticament per .github/scripts/generate-partits-seo.py a partir de partits/data.json. Contingut real i visible (no ocult), pensat perquè cercadors i agents d\'IA que no executen JavaScript vegin el calendari sencer. No editar a mà: els canvis es perdran en la propera execució diària. -->',
        "<!-- SEO:STATIC-CONTENT:END -->",
        static_html,
    )
    INDEX_PATH.write_text(page, encoding="utf-8")
    bump_sitemap(avui)
    print(f"OK: {len(data['partits'])} partits al JSON de dades, "
          f"bloc JSON-LD amb finestra de {JSONLD_WINDOW_DAYS} dies, "
          f"resum estàtic per a {len(data['equips'])} equips.")


if __name__ == "__main__":
    main()
