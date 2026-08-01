#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Partits d'un equip del CB Grup Barna, des de la FCBQ (basquetcatala.cat).

Dues fonts, la mateixa sortida:

  A) DES DEL PDF ja descarregat  ← recomanada, no cal entrar al web
     Descarrega un cop el "Calendari Global Club" des de
     https://www.basquetcatala.cat/partits/calendari_club_global/pdf/24
     i després, tantes vegades com vulguis, sense connexió:

       python3 scripts/baixar-partits-fcbq.py --des-de-pdf partits/calendari-global.pdf --llistar
       python3 scripts/baixar-partits-fcbq.py --des-de-pdf partits/calendari-global.pdf --categoria "senior b femeni"

  B) DES DEL WEB (raspa la fitxa de l'equip; requereix sortida a internet)

       python3 scripts/baixar-partits-fcbq.py --llistar
       python3 scripts/baixar-partits-fcbq.py --equip "senior b femeni"

Genera, dins de --sortida (per defecte "partits/"):
  <nom>.json   dades estructurades (per alimentar la web / data.json)
  <nom>.csv    per obrir amb Excel o Google Sheets
  <nom>.ics    calendari per importar o subscriure a Google Calendar / iPhone

Només fa servir la biblioteca estàndard de Python 3: res de pip install.
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
import zlib
from datetime import datetime, timedelta, timezone
from html import unescape

BASE = "https://www.basquetcatala.cat"
CLUB_ID_PER_DEFECTE = "24"  # CLUB BASQUET GRUP BARNA
CLUB_PATRO = re.compile(r"C[.,]?\s*B\.?\s+GRUP\s+BARNA", re.IGNORECASE)
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)

# Noms de casa -> categoria oficial a la FCBQ. La categoria canvia si l'equip
# puja o baixa de divisió: si algun dia no quadra, actualitza aquesta taula
# (--llistar sobre el PDF et diu les categories reals de la temporada).
ALIES_CATEGORIA = {
    "senior a femeni": "super copa femenina",
    "senior b femeni": "primera categoria femenina",
    "senior a masculi": "super copa masculina",
}

BLOQUEJAT = (
    "\nACCÉS BLOQUEJAT en connectar amb %s\n"
    "El proxy ha respost 403. Passa quan s'executa des d'un entorn amb\n"
    "política de xarxa restringida (per exemple Claude Code al núvol o una\n"
    "xarxa corporativa), que no deixa sortir cap al domini basquetcatala.cat.\n"
    "Solució: executa'l des del teu ordinador, o fes servir --des-de-pdf amb\n"
    "el calendari global ja descarregat, que funciona sense connexió.\n"
)

# ---------------------------------------------------------------- utilitats


def normalitza(text):
    """minúscules, sense accents i sense signes: per comparar noms."""
    text = unicodedata.normalize("NFKD", text or "")
    text = "".join(c for c in text if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def repara(text):
    """La FCBQ perd alguns apòstrofs i els deixa com a '?' (VALL D?EN BAS)."""
    return re.sub(r"(?<=[A-Za-zÀ-ÿ])\?(?=[A-Za-zÀ-ÿ])", "'", text).strip()


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


# ------------------------------------------------- font A: el PDF de la FCBQ

# El PDF de la federació el genera FPDF: cada cel·la és un "BT x y Td (text) Tj".
TROS_PDF = re.compile(
    rb"BT\s+(-?[\d.]+)\s+(-?[\d.]+)\s+Td\s*\((.*?)(?<!\\)\)\s*Tj", re.DOTALL)


def _desescapa(brut):
    """Passa una cadena literal de PDF (WinAnsi, amb \\( \\) \\\\) a text."""
    text = re.sub(rb"\\([()\\])", rb"\1", brut)
    text = re.sub(rb"\\(\d{1,3})",
                  lambda m: bytes([int(m.group(1), 8) & 0xFF]), text)
    return text.decode("cp1252", "replace")


def linies_del_pdf(cami):
    """Retorna les línies visibles del PDF, en ordre de lectura."""
    try:
        dades = open(cami, "rb").read()
    except OSError as err:
        sys.exit("No s'ha pogut obrir el PDF %s: %s" % (cami, err))

    linies = []
    for flux in re.findall(rb"stream\r?\n(.*?)\r?\nendstream", dades, re.DOTALL):
        try:
            contingut = zlib.decompress(flux)
        except zlib.error:
            contingut = flux  # el PDF pot venir sense comprimir
        trossos = {}
        for x, y, brut in TROS_PDF.findall(contingut):
            trossos.setdefault(round(float(y), 1), []).append(
                (float(x), _desescapa(brut)))
        # de dalt a baix dins de la pàgina, i d'esquerra a dreta dins la línia
        for y in sorted(trossos, reverse=True):
            text = " ".join(t for _, t in sorted(trossos[y])).strip()
            if text:
                linies.append(re.sub(r"\s{2,}", " ", text))
    if not linies:
        sys.exit(
            "No s'ha trobat text dins de %s.\n"
            "Assegura't que és el PDF del 'Calendari Global Club' de la FCBQ." % cami)
    return linies


FILA_PDF = re.compile(r"^(\d{2})-(\d{2})-(\d{4})\s+(\d{1,2}):(\d{2})\s+(.+)$")


def partits_del_pdf(cami):
    """Llegeix el calendari global i retorna tots els partits amb categoria."""
    linies = linies_del_pdf(cami)
    partits = []
    for i, linia in enumerate(linies):
        fila = FILA_PDF.match(linia)
        if not fila:
            continue
        dia, mes, any_, hh, mm, cua = fila.groups()

        # La cua és "LOCAL - VISITANT CATEGORIA". La categoria comença al primer
        # marcador conegut; la resta, per davant, és l'enfrontament.
        cat_inici = None
        for marcador in ("C.C.", "SUPER COPA", "COPA ", "LLIGA ", "SÈNIOR", "SENIOR"):
            pos = cua.find(marcador)
            if pos > 0 and (cat_inici is None or pos < cat_inici):
                cat_inici = pos
        enfrontament = repara(cua[:cat_inici] if cat_inici else cua)
        categoria = repara(cua[cat_inici:]) if cat_inici else ""

        local, _, visitant = enfrontament.partition(" - ")
        if not visitant:  # algun rival duu " - " al nom: partim pel darrer
            local, _, visitant = enfrontament.rpartition(" - ")

        instalacio = ""
        if i + 1 < len(linies) and linies[i + 1].startswith("Instal"):
            instalacio = repara(linies[i + 1].split(":", 1)[1])

        partits.append({
            "data": "%s-%s-%s" % (any_, mes, dia),
            "hora": "%02d:%s" % (int(hh), mm),
            "local": repara(local),
            "visitant": repara(visitant),
            "resultat": "",  # el calendari global no porta resultats
            "categoria": categoria,
            "instalacio": instalacio,
        })
    return partits


def filtra(partits, categoria):
    """Filtra per categoria, tolerant amb accents, majúscules i àlies."""
    objectiu = ALIES_CATEGORIA.get(normalitza(categoria), categoria)
    paraules = normalitza(objectiu).split()
    return [p for p in partits
            if all(mot in normalitza(p["categoria"]) for mot in paraules)]


# --------------------------------------------------- font B: el web de la FCBQ


def llista_equips(club_id):
    """Retorna [{'id': ..., 'nom': ...}] a partir de la pàgina del club."""
    html = baixa("%s/club/%s" % (BASE, club_id))
    equips, vistos = [], set()
    patro = re.compile(
        r'<a[^>]+href="[^"]*?/club/%s/(\d+)"[^>]*>(.*?)</a>' % club_id,
        re.IGNORECASE | re.DOTALL)
    for equip_id, etiqueta in patro.findall(html):
        nom = net(etiqueta)
        if nom and equip_id not in vistos:
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

    paraules = normalitza(cerca).split()
    candidats = [e for e in equips
                 if all(mot in normalitza(e["nom"]) for mot in paraules)]
    if len(candidats) == 1:
        return candidats[0]
    if not candidats:
        sys.exit("No hi ha cap equip que encaixi amb %r. Prova --llistar." % cerca)
    print("Hi ha més d'un equip que encaixa amb %r:" % cerca, file=sys.stderr)
    for equip in candidats:
        print("  %-8s %s" % (equip["id"], equip["nom"]), file=sys.stderr)
    sys.exit("Torna-hi indicant l'identificador exacte amb --equip <id>.")


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
    for bloc in re.findall(
            r"(?is)<li[^>]*>(.*?)</li>"
            r"|<div[^>]*class=\"[^\"]*(?:partit|match|game)[^\"]*\"[^>]*>(.*?)</div>", html):
        text = net(bloc[0] or bloc[1])
        if text:
            yield [text]


def extreu_partits(html):
    """Converteix la pàgina d'un equip en una llista de partits."""
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

        noms = [c for c in celles
                if len(c) > 3 and not DATA.search(c) and not HORA.fullmatch(c.strip())
                and not re.fullmatch(r"[\d\s\-–:]+", c)]
        if len(noms) == 1 and " - " in noms[0]:
            noms = [p.strip() for p in noms[0].split(" - ", 1)]

        resultat = ""
        for cella in celles:
            marcador = RESULTAT.fullmatch(cella.strip())
            if marcador:
                resultat = "%s-%s" % marcador.groups()
                break

        partits.append({
            "data": "%04d-%02d-%02d" % (any_, mes, dia),
            "hora": "%02d:%02d" % (int(hora.group(1)), int(hora.group(2))) if hora else "",
            "local": noms[0] if noms else "",
            "visitant": noms[1] if len(noms) > 1 else "",
            "resultat": resultat,
            "categoria": "",
            "instalacio": noms[2] if len(noms) > 2 else "",
        })
    return partits


def ordena(partits):
    """Treu duplicats i ordena per data i hora."""
    unics, vistos = [], set()
    for partit in partits:
        clau = (partit["data"], partit["hora"], partit["local"], partit["visitant"])
        if clau not in vistos:
            vistos.add(clau)
            unics.append(partit)
    unics.sort(key=lambda p: (p["data"], p["hora"]))
    return unics


# ----------------------------------------------------------------- sortida

COLUMNES = ["data", "hora", "local", "visitant", "resultat", "categoria", "instalacio"]


def escriu_json(cami, titol, font, partits):
    with open(cami, "w", encoding="utf-8") as fitxer:
        json.dump({"equip": titol, "font": font, "partits": partits},
                  fitxer, ensure_ascii=False, indent=2)
        fitxer.write("\n")


def escriu_csv(cami, partits):
    with open(cami, "w", encoding="utf-8-sig", newline="") as fitxer:
        escriptor = csv.DictWriter(fitxer, fieldnames=COLUMNES, extrasaction="ignore")
        escriptor.writeheader()
        escriptor.writerows(partits)


def _utc(data, hora):
    """Hora local de Barcelona -> UTC, per no dependre del TZID del client."""
    moment = datetime.strptime("%s %s" % (data, hora or "00:00"), "%Y-%m-%d %H:%M")
    try:
        from zoneinfo import ZoneInfo
        return moment.replace(tzinfo=ZoneInfo("Europe/Madrid")).astimezone(timezone.utc)
    except Exception:  # sense base de dades de zones: fem servir CET fix
        return moment.replace(tzinfo=timezone(timedelta(hours=1))).astimezone(timezone.utc)


def _esc(valor):
    """Escapa el text d'una propietat iCalendar (RFC 5545, 3.3.11)."""
    return (valor or "").replace("\\", "\\\\").replace(";", "\\;") \
                        .replace(",", "\\,").replace("\n", "\\n")


def _plega(linia):
    """Cap línia d'un .ics pot passar de 75 octets (RFC 5545, 3.1)."""
    if len(linia.encode("utf-8")) <= 75:
        return linia
    trossos, actual, limit = [], "", 75
    for caracter in linia:  # tallem per caràcters, mai enmig d'un UTF-8
        if len(actual.encode("utf-8")) + len(caracter.encode("utf-8")) > limit:
            trossos.append(actual)
            actual, limit = " ", 75  # les continuacions van amb un espai davant
        actual += caracter
    trossos.append(actual)
    return "\r\n".join(trossos)


def escriu_ics(cami, titol, partits):
    ara = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    linies = ["BEGIN:VCALENDAR", "VERSION:2.0", "CALSCALE:GREGORIAN",
              "PRODID:-//CB Grup Barna//Partits FCBQ//CA",
              "X-WR-CALNAME:%s" % titol, "X-WR-TIMEZONE:Europe/Madrid"]
    for i, partit in enumerate(partits):
        comenca = _utc(partit["data"], partit["hora"])
        acaba = comenca + timedelta(hours=2)  # partit + escalfament
        casa = bool(CLUB_PATRO.search(partit["local"]))
        linies += [
            "BEGIN:VEVENT",
            "UID:fcbq-%s-%d@cbgrupbarna.info" % (partit["data"].replace("-", ""), i),
            "DTSTAMP:%s" % ara,
            "DTSTART:%s" % comenca.strftime("%Y%m%dT%H%M%SZ"),
            "DTEND:%s" % acaba.strftime("%Y%m%dT%H%M%SZ"),
            "SUMMARY:%s" % _esc("%s %s - %s" % ("🏠" if casa else "🚌",
                                                partit["local"], partit["visitant"])),
            "LOCATION:%s" % _esc(partit.get("instalacio", "")),
            "DESCRIPTION:%s" % _esc(partit.get("categoria") or titol),
            "END:VEVENT",
        ]
    linies.append("END:VCALENDAR")
    with open(cami, "w", encoding="utf-8") as fitxer:
        fitxer.write("\r\n".join(_plega(l) for l in linies) + "\r\n")


def resumeix(titol, partits):
    casa = sum(1 for p in partits if CLUB_PATRO.search(p["local"]))
    print("%s — %d partits (%d a casa, %d a fora), del %s al %s"
          % (titol, len(partits), casa, len(partits) - casa,
             partits[0]["data"], partits[-1]["data"]))
    for partit in partits:
        print("  %s %s  %-3s %s - %s"
              % (partit["data"], partit["hora"],
                 "CASA" if CLUB_PATRO.search(partit["local"]) else "FORA",
                 partit["local"], partit["visitant"]))


# -------------------------------------------------------------------- main


def main():
    analitzador = argparse.ArgumentParser(
        description="Partits d'un equip del CB Grup Barna (FCBQ), des del PDF o del web")
    analitzador.add_argument("--des-de-pdf", metavar="FITXER",
                             help="llegir el calendari global ja descarregat (sense connexió)")
    analitzador.add_argument("--categoria",
                             help="categoria a filtrar del PDF, p. ex. \"senior b femeni\"")
    analitzador.add_argument("--equip", help="identificador o tros del nom de l'equip (font web)")
    analitzador.add_argument("--club", default=CLUB_ID_PER_DEFECTE,
                             help="identificador de club a la FCBQ (per defecte 24)")
    analitzador.add_argument("--llistar", action="store_true",
                             help="llistar categories (amb --des-de-pdf) o equips (font web)")
    analitzador.add_argument("--pdf", action="store_true",
                             help="descarregar el calendari global del club en PDF")
    analitzador.add_argument("--sortida", default="partits",
                             help="carpeta on desar els fitxers (per defecte: partits/)")
    analitzador.add_argument("--nom", help="nom base dels fitxers de sortida")
    analitzador.add_argument("--desa-html", action="store_true",
                             help="desar l'HTML cru, per depurar el parseig de la font web")
    arguments = analitzador.parse_args()

    os.makedirs(arguments.sortida, exist_ok=True)

    if arguments.pdf:
        url = "%s/partits/calendari_club_global/pdf/%s" % (BASE, arguments.club)
        desti = os.path.join(arguments.sortida, "calendari-global.pdf")
        with open(desti, "wb") as fitxer:
            fitxer.write(baixa(url, binari=True))
        print("Calendari global desat a %s" % desti)
        if not (arguments.categoria or arguments.equip or arguments.llistar):
            return
        arguments.des_de_pdf = arguments.des_de_pdf or desti

    # ---- font A: PDF
    if arguments.des_de_pdf:
        tots = partits_del_pdf(arguments.des_de_pdf)
        if not tots:
            sys.exit("No s'ha trobat cap partit dins de %s." % arguments.des_de_pdf)

        if arguments.llistar or not arguments.categoria:
            categories = {}
            for partit in tots:
                categories[partit["categoria"]] = categories.get(partit["categoria"], 0) + 1
            print("%d partits al PDF, en %d categories:" % (len(tots), len(categories)))
            for categoria in sorted(categories):
                print("  %3d  %s" % (categories[categoria], categoria))
            if not arguments.categoria:
                print("\nAra filtra'n una amb, per exemple: --categoria \"senior b femeni\"")
            return

        partits = ordena(filtra(tots, arguments.categoria))
        if not partits:
            sys.exit("Cap partit de la categoria %r. Prova --llistar." % arguments.categoria)
        titol = partits[0]["categoria"] or arguments.categoria
        font = os.path.basename(arguments.des_de_pdf)

    # ---- font B: web
    else:
        equips = llista_equips(arguments.club)
        if arguments.llistar or not arguments.equip:
            if not equips:
                sys.exit("No s'ha pogut llegir cap equip de %s/club/%s" % (BASE, arguments.club))
            print("Equips del club %s:" % arguments.club)
            for equip in equips:
                print("  %-8s %s" % (equip["id"], equip["nom"]))
            if not arguments.equip:
                print("\nAra torna-hi amb, per exemple: --equip \"senior b femeni\"")
            return

        equip = tria_equip(equips, arguments.equip)
        font = "%s/club/%s/%s" % (BASE, arguments.club, equip["id"])
        html = baixa(font)
        if arguments.desa_html:
            cami_html = os.path.join(arguments.sortida, "%s.html" % equip["id"])
            with open(cami_html, "w", encoding="utf-8") as fitxer:
                fitxer.write(html)
            print("HTML cru desat a %s" % cami_html)
        partits = ordena(extreu_partits(html))
        if not partits:
            sys.exit(
                "S'ha llegit la fitxa de %s però no s'hi ha trobat cap partit.\n"
                "Torna-hi amb --desa-html i revisa l'HTML desat: la FCBQ deu haver\n"
                "canviat l'estructura de la pàgina." % equip["nom"])
        titol = equip["nom"]

    base = arguments.nom or re.sub(r"[^a-z0-9]+", "-", normalitza(titol)).strip("-")
    escriu_json(os.path.join(arguments.sortida, base + ".json"), titol, font, partits)
    escriu_csv(os.path.join(arguments.sortida, base + ".csv"), partits)
    escriu_ics(os.path.join(arguments.sortida, base + ".ics"), titol, partits)

    resumeix(titol, partits)
    print("\nDesat a %s/%s.{json,csv,ics}" % (arguments.sortida, base))


if __name__ == "__main__":
    main()
