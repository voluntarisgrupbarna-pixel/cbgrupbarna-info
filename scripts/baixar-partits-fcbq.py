#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Baixa els partits d'un equip del CB Grup Barna des de basquetcatala.cat (FCBQ).

Només fa servir la biblioteca estàndard de Python 3 (res de pip install).

ÚS RÀPID
--------
  # 1) Veure quins equips té el club i el seu identificador
  python3 scripts/baixar-partits-fcbq.py --llistar

  # 2) Baixar els partits del Sènior B Femení (per nom, cerca aproximada)
  python3 scripts/baixar-partits-fcbq.py --equip "senior b femeni"

  # 3) O directament per identificador d'equip, si ja el saps
  python3 scripts/baixar-partits-fcbq.py --equip 70538

  # 4) Calendari global del club sencer en PDF (tots els equips)
  python3 scripts/baixar-partits-fcbq.py --pdf

Genera, dins de --sortida (per defecte "partits/"):
  <equip>.json   dades estructurades (per alimentar la web / data.json)
  <equip>.csv    per obrir amb Excel o Google Sheets
  <equip>.ics    calendari importable a Google Calendar / iPhone

Si el parseig falla perquè la FCBQ ha canviat l'HTML, executa amb --desa-html
i tindràs el HTML cru desat al costat per poder-hi mirar.
"""

import argparse
import csv
import json
import os
import re
import sys
import unicodedata
import urllib.error
import urllib.request
from datetime import datetime, timedelta
from html import unescape

BASE = "https://www.basquetcatala.cat"
CLUB_ID_PER_DEFECTE = "24"  # CLUB BASQUET GRUP BARNA
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)

BLOQUEJAT = (
    "\nACCÉS BLOQUEJAT en connectar amb %s\n"
    "El proxy ha respost 403. Passa quan s'executa des d'un entorn amb\n"
    "política de xarxa restringida (per exemple Claude Code al núvol o una\n"
    "xarxa corporativa), que no deixa sortir cap al domini basquetcatala.cat.\n"
    "Solució: executa aquest script des del teu ordinador, amb la teva\n"
    "connexió normal, i funcionarà sense tocar res.\n"
)

# ---------------------------------------------------------------- utilitats


def normalitza(text):
    """minúscules, sense accents i sense signes: per comparar noms d'equip."""
    text = unicodedata.normalize("NFKD", text or "")
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = text.lower()
    return re.sub(r"[^a-z0-9]+", " ", text).strip()


def baixa(url, binari=False):
    peticio = urllib.request.Request(url, headers={
        "User-Agent": USER_AGENT,
        "Accept-Language": "ca,es;q=0.9",
    })
    try:
        with urllib.request.urlopen(peticio, timeout=45) as resposta:
            dades = resposta.read()
    except urllib.error.HTTPError as err:
        if err.code in (403, 407):
            sys.exit(BLOQUEJAT % url)
        sys.exit("ERROR HTTP %s en accedir a %s" % (err.code, url))
    except urllib.error.URLError as err:
        if re.search(r"40[37]|tunnel", str(err.reason), re.IGNORECASE):
            sys.exit(BLOQUEJAT % url)
        sys.exit("ERROR de xarxa en accedir a %s: %s" % (url, err.reason))
    if binari:
        return dades
    for codi in ("utf-8", "iso-8859-1"):
        try:
            return dades.decode(codi)
        except UnicodeDecodeError:
            continue
    return dades.decode("utf-8", "replace")


def net(html_fragment):
    """Treu etiquetes i espais sobrants d'un tros d'HTML."""
    text = re.sub(r"(?is)<(script|style).*?</\1>", " ", html_fragment)
    text = re.sub(r"(?i)<br\s*/?>", " ", text)
    text = re.sub(r"(?s)<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", unescape(text)).strip()


# ------------------------------------------------------------ equips (club)


def llista_equips(club_id):
    """Retorna [{'id': ..., 'nom': ...}] a partir de la pàgina del club."""
    html = baixa("%s/club/%s" % (BASE, club_id))
    equips, vistos = [], set()
    patro = re.compile(
        r'<a[^>]+href="[^"]*?/club/%s/(\d+)"[^>]*>(.*?)</a>' % club_id,
        re.IGNORECASE | re.DOTALL,
    )
    for equip_id, etiqueta in patro.findall(html):
        nom = net(etiqueta)
        if not nom or equip_id in vistos:
            continue
        vistos.add(equip_id)
        equips.append({"id": equip_id, "nom": nom})
    return equips


def tria_equip(equips, cerca):
    """Resol --equip: pot ser un id numèric o un tros del nom."""
    if re.fullmatch(r"\d+", cerca):
        for equip in equips:
            if equip["id"] == cerca:
                return equip
        return {"id": cerca, "nom": "equip-%s" % cerca}

    objectiu = normalitza(cerca)
    paraules = objectiu.split()
    candidats = [e for e in equips if all(p in normalitza(e["nom"]) for p in paraules)]
    if len(candidats) == 1:
        return candidats[0]
    if not candidats:
        sys.exit(
            "No s'ha trobat cap equip que encaixi amb %r.\n"
            "Executa --llistar per veure'ls tots." % cerca
        )
    print("Hi ha més d'un equip que encaixa amb %r:" % cerca, file=sys.stderr)
    for equip in candidats:
        print("  %-8s %s" % (equip["id"], equip["nom"]), file=sys.stderr)
    sys.exit("Torna a executar indicant l'identificador exacte amb --equip <id>.")


# ----------------------------------------------------------------- partits

DATA = re.compile(r"\b(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})\b")
HORA = re.compile(r"\b(\d{1,2}):(\d{2})\b")
RESULTAT = re.compile(r"\b(\d{1,3})\s*[-–]\s*(\d{1,3})\b")


def files_de_taula(html):
    """Trosseja l'HTML en files de taula i, si no n'hi ha, en blocs de llista."""
    files = re.findall(r"(?is)<tr[^>]*>(.*?)</tr>", html)
    if files:
        for fila in files:
            celles = [net(c) for c in re.findall(r"(?is)<t[dh][^>]*>(.*?)</t[dh]>", fila)]
            yield [c for c in celles if c]
        return
    for bloc in re.findall(r"(?is)<li[^>]*>(.*?)</li>|<div[^>]*class=\"[^\"]*(?:partit|match|game)[^\"]*\"[^>]*>(.*?)</div>", html):
        text = net(bloc[0] or bloc[1])
        if text:
            yield [text]


def extreu_partits(html):
    """Converteix la pàgina de l'equip en una llista de partits."""
    partits = []
    for celles in files_de_taula(html):
        text = " | ".join(celles)
        data = DATA.search(text)
        if not data:
            continue

        dia, mes, any_ = (int(x) for x in data.groups())
        if any_ < 100:
            any_ += 2000
        hora = HORA.search(text)

        # Els equips solen ser les celles llargues sense xifres de data/hora.
        noms = [
            c for c in celles
            if len(c) > 3 and not DATA.search(c) and not HORA.fullmatch(c.strip())
            and not re.fullmatch(r"[\d\s\-–:]+", c)
        ]
        # "LOCAL - VISITANT" dins d'una mateixa cel·la
        if len(noms) == 1 and " - " in noms[0]:
            noms = [p.strip() for p in noms[0].split(" - ", 1)]

        resultat = ""
        for c in celles:
            marcador = RESULTAT.fullmatch(c.strip())
            if marcador:
                resultat = "%s-%s" % marcador.groups()
                break

        partits.append({
            "data": "%04d-%02d-%02d" % (any_, mes, dia),
            "hora": "%02d:%02d" % (int(hora.group(1)), int(hora.group(2))) if hora else "",
            "local": noms[0] if noms else "",
            "visitant": noms[1] if len(noms) > 1 else "",
            "resultat": resultat,
            "pavello": noms[2] if len(noms) > 2 else "",
            "linia": text,
        })

    # Fora duplicats, i ordenats per data i hora.
    unics, clau_vistes = [], set()
    for partit in partits:
        clau = (partit["data"], partit["hora"], partit["local"], partit["visitant"])
        if clau in clau_vistes:
            continue
        clau_vistes.add(clau)
        unics.append(partit)
    unics.sort(key=lambda p: (p["data"], p["hora"]))
    return unics


# ----------------------------------------------------------------- sortida


def escriu_json(cami, equip, partits):
    with open(cami, "w", encoding="utf-8") as fitxer:
        json.dump(
            {"equip": equip["nom"], "equipId": equip["id"],
             "font": "%s/club/%s/%s" % (BASE, CLUB_ID_PER_DEFECTE, equip["id"]),
             "partits": partits},
            fitxer, ensure_ascii=False, indent=2,
        )


def escriu_csv(cami, partits):
    columnes = ["data", "hora", "local", "visitant", "resultat", "pavello"]
    with open(cami, "w", encoding="utf-8-sig", newline="") as fitxer:
        escriptor = csv.DictWriter(fitxer, fieldnames=columnes, extrasaction="ignore")
        escriptor.writeheader()
        escriptor.writerows(partits)


def escriu_ics(cami, equip, partits):
    linies = [
        "BEGIN:VCALENDAR", "VERSION:2.0",
        "PRODID:-//CB Grup Barna//Partits FCBQ//CA",
        "X-WR-CALNAME:%s" % equip["nom"],
    ]
    for i, partit in enumerate(partits):
        comenca = datetime.strptime(
            "%s %s" % (partit["data"], partit["hora"] or "00:00"), "%Y-%m-%d %H:%M")
        acaba = comenca + timedelta(hours=2)  # un partit dura ~2 h amb escalfament
        inici = comenca.strftime("%Y%m%dT%H%M%S")
        fi = acaba.strftime("%Y%m%dT%H%M%S")
        titol = "%s vs %s" % (partit["local"] or "?", partit["visitant"] or "?")
        linies += [
            "BEGIN:VEVENT",
            "UID:fcbq-%s-%d@cbgrupbarna.info" % (equip["id"], i),
            "DTSTART;TZID=Europe/Madrid:%s" % inici,
            "DTEND;TZID=Europe/Madrid:%s" % fi,
            "SUMMARY:%s" % titol,
            "LOCATION:%s" % partit.get("pavello", ""),
            "DESCRIPTION:%s" % equip["nom"],
            "END:VEVENT",
        ]
    linies.append("END:VCALENDAR")
    with open(cami, "w", encoding="utf-8") as fitxer:
        fitxer.write("\r\n".join(linies) + "\r\n")


# -------------------------------------------------------------------- main


def main():
    analitzador = argparse.ArgumentParser(
        description="Baixa els partits d'un equip del club des de basquetcatala.cat",
    )
    analitzador.add_argument("--club", default=CLUB_ID_PER_DEFECTE,
                             help="identificador de club a la FCBQ (per defecte 24, Grup Barna)")
    analitzador.add_argument("--equip", help="identificador o tros del nom de l'equip")
    analitzador.add_argument("--llistar", action="store_true",
                             help="només llistar els equips del club i sortir")
    analitzador.add_argument("--pdf", action="store_true",
                             help="baixar el calendari global del club en PDF")
    analitzador.add_argument("--sortida", default="partits",
                             help="carpeta on desar els fitxers (per defecte: partits/)")
    analitzador.add_argument("--desa-html", action="store_true",
                             help="desar també l'HTML cru, per depurar el parseig")
    arguments = analitzador.parse_args()

    os.makedirs(arguments.sortida, exist_ok=True)

    if arguments.pdf:
        url = "%s/partits/calendari_club_global/pdf/%s" % (BASE, arguments.club)
        desti = os.path.join(arguments.sortida, "calendari-club-%s.pdf" % arguments.club)
        with open(desti, "wb") as fitxer:
            fitxer.write(baixa(url, binari=True))
        print("Calendari global desat a %s" % desti)
        if not arguments.equip:
            return

    equips = llista_equips(arguments.club)
    if arguments.llistar or not arguments.equip:
        if not equips:
            sys.exit("No s'ha pogut llegir cap equip de %s/club/%s" % (BASE, arguments.club))
        print("Equips del club %s:" % arguments.club)
        for equip in equips:
            print("  %-8s %s" % (equip["id"], equip["nom"]))
        if not arguments.equip:
            print("\nAra torna a executar amb, per exemple: --equip \"senior b femeni\"")
        return

    equip = tria_equip(equips, arguments.equip)
    url = "%s/club/%s/%s" % (BASE, arguments.club, equip["id"])
    html = baixa(url)

    base_nom = re.sub(r"[^a-z0-9]+", "-", normalitza(equip["nom"])).strip("-") or equip["id"]
    if arguments.desa_html:
        cami_html = os.path.join(arguments.sortida, base_nom + ".html")
        with open(cami_html, "w", encoding="utf-8") as fitxer:
            fitxer.write(html)
        print("HTML cru desat a %s" % cami_html)

    partits = extreu_partits(html)
    if not partits:
        sys.exit(
            "S'ha llegit la pàgina de %s però no s'hi ha trobat cap partit.\n"
            "Torna-ho a provar amb --desa-html i revisa l'HTML desat: probablement\n"
            "la FCBQ ha canviat l'estructura de la pàgina." % equip["nom"]
        )

    escriu_json(os.path.join(arguments.sortida, base_nom + ".json"), equip, partits)
    escriu_csv(os.path.join(arguments.sortida, base_nom + ".csv"), partits)
    escriu_ics(os.path.join(arguments.sortida, base_nom + ".ics"), equip, partits)

    print("Equip: %s (id %s)" % (equip["nom"], equip["id"]))
    print("Partits trobats: %d" % len(partits))
    for partit in partits:
        print("  %s %s  %s - %s  %s" % (
            partit["data"], partit["hora"] or "--:--",
            partit["local"], partit["visitant"], partit["resultat"]))
    print("\nDesat a %s/%s.{json,csv,ics}" % (arguments.sortida, base_nom))


if __name__ == "__main__":
    main()
