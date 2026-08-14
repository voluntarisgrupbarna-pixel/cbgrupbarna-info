#!/usr/bin/env python3
"""
Calendaris .ics (subscripció) · CB Grup Barna
Genera un fitxer iCalendar per equip a partits/calendaris/ics/{equip}.ics
a partir de partits/data.json, més un de conjunt amb tot el club. Qui
s'hi subscriu (Google Calendar, Apple Calendar, Outlook...) rep els
partits del seu equip automàticament i, com que el robot el regenera
cada dia, els canvis d'hora o pista arriben sols la propera vegada que
l'aplicació de calendari sincronitzi — no cal descarregar res de nou.

Disseny defensiu: si data.json no es pot llegir, no es toca res.
"""
import json
import re
import unicodedata
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "partits" / "data.json"
OUT_DIR = ROOT / "partits" / "calendaris" / "ics"
DURADA_MINUTS = 90


def slugify(s):
    s = unicodedata.normalize("NFD", (s or "").lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def esc(s):
    """Escapament de text per a camps iCalendar (RFC 5545)."""
    s = (s or "")
    return (s.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,")
             .replace("\n", "\\n"))


def fold(line):
    """Les línies iCalendar de més de 75 octets s'han de plegar amb un salt
    de línia + espai (RFC 5545 §3.1)."""
    out, rest = [], line
    while len(rest.encode("utf-8")) > 75:
        cut = 74
        while len(rest[:cut].encode("utf-8")) > 74:
            cut -= 1
        out.append(rest[:cut])
        rest = " " + rest[cut:]
    out.append(rest)
    return "\r\n".join(out)


def build_event(p, eq_nom, ara):
    dt = datetime.strptime(f"{p['data']} {p['hora']}", "%Y-%m-%d %H:%M")
    dtstart = dt.strftime("%Y%m%dT%H%M%S")
    dtend = (dt + timedelta(minutes=DURADA_MINUTS)).strftime("%Y%m%dT%H%M%S")
    resultat = ""
    if p.get("puntsLocal") is not None and p.get("puntsVisitant") is not None:
        resultat = f" ({p['puntsLocal']}-{p['puntsVisitant']})"
    summary = f"{p['local']} - {p['visitant']}{resultat}"
    desc = f"{eq_nom} · {p.get('categoria', '')}\nMés informació: https://cbgrupbarna.info/partits/"
    loc = ", ".join(x for x in [p.get("pista"), p.get("adreca")] if x)
    return "\r\n".join([
        "BEGIN:VEVENT",
        fold(f"UID:{p['id']}@cbgrupbarna.info"),
        f"DTSTAMP:{ara}",
        f"DTSTART;TZID=Europe/Madrid:{dtstart}",
        f"DTEND;TZID=Europe/Madrid:{dtend}",
        fold(f"SUMMARY:{esc(summary)}"),
        fold(f"DESCRIPTION:{esc(desc)}"),
        fold(f"LOCATION:{esc(loc)}"),
        fold("URL:https://cbgrupbarna.info/partits/"),
        "END:VEVENT",
    ])


def build_calendar(nom, partits, equips_index, ara):
    events = "\r\n".join(build_event(p, equips_index.get(p["equipId"], ""), ara) for p in partits)
    header = "\r\n".join([
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//CB Grup Barna//Partits i Resultats//CA",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        fold(f"X-WR-CALNAME:{esc(nom)}"),
        fold("X-WR-CALDESC:" + esc(f"Calendari de {nom} · CB Grup Barna. Font: cbgrupbarna.info/partits/")),
        "X-WR-TIMEZONE:Europe/Madrid",
        "REFRESH-INTERVAL;VALUE=DURATION:P1D",
        "X-PUBLISHED-TTL:P1D",
    ])
    footer = "END:VCALENDAR"
    body = header + ("\r\n" + events if events else "") + "\r\n" + footer + "\r\n"
    return body


def main():
    if not DATA.exists():
        print("[ics] falta partits/data.json — no es fa res")
        return 0
    try:
        data = json.loads(DATA.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"[ics] data.json illegible ({exc}) — no es toca res")
        return 0

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ara = date.today().strftime("%Y%m%dT060000Z")
    equips_index = {e["id"]: e.get("nom", "") for e in data["equips"]}

    n_fitxers = 0
    for e in data["equips"]:
        partits = sorted(
            (p for p in data["partits"] if p["equipId"] == e["id"]),
            key=lambda p: (p["data"], p["hora"]),
        )
        cal = build_calendar(f"{e.get('nom', e['id'])} · CB Grup Barna", partits, equips_index, ara)
        (OUT_DIR / f"{e['id']}.ics").write_text(cal, encoding="utf-8", newline="")
        n_fitxers += 1

    tots = sorted(data["partits"], key=lambda p: (p["data"], p["hora"]))
    cal_club = build_calendar("CB Grup Barna · Tots els equips", tots, equips_index, ara)
    (OUT_DIR / "tots-els-equips.ics").write_text(cal_club, encoding="utf-8", newline="")

    print(f"[ics] OK → {n_fitxers} calendaris per equip + 1 combinat, a {OUT_DIR.relative_to(ROOT)}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
