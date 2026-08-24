#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comprova que les traduccions estan TRADUÏDES, no només que el fitxer existeix.

Per què existeix: scripts/i18n-paritat.py mira dates i fitxers. Diu si la
pàgina castellana existeix i si és més vella que la catalana. No obre cap de
les dues. El 24/08/2026 això va deixar passar coses com aquestes:

  · /3x3/ tenia 12 seccions en català i 6 en castellà i anglès;
  · /premsa/ en tenia 4 i 1;
  · les preguntes freqüents de /partits/ estaven partides pel mig, amb la
    cua traduïda i el cap en català, també dins del JSON-LD que llegeix
    Google.

Cap de les tres feia saltar res, perquè els fitxers hi eren i tenien la data
bona. Aquest script els obre i els compara.

Mira tres coses, de més fiable a menys:

  1. SECCIONS  · quants <h2> té l'original i quants la traducció. És el senyal
     més net: si en falten, hi ha contingut que no s'ha traduït.
  2. LLARGADA  · quantes paraules. Una traducció molt més curta vol dir que
     s'ha quedat pel camí.
  3. PARAULES CATALANES dins d'una traducció. És el més sorollós, i per això
     abans de mirar-ho es treuen els comentaris HTML, els noms propis del
     glossari i les adreces impreses com a text.

El que no sap distingir sol —una cita literal en català, el nom d'un rival,
una plantilla que s'ofereix en català a propòsit— va a i18n/excepcions-
contingut.yml amb el motiu escrit.

  python3 scripts/i18n-contingut.py            # tot el lloc
  python3 scripts/i18n-contingut.py /3x3/      # només una pàgina

Torna 1 si troba res que no estigui declarat.
"""
import html
import os
import re
import sys

try:
    import yaml
except ImportError:
    sys.exit("Cal pyyaml: pip install pyyaml")

ARREL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDIOMES = ("es", "en")

RE_COMENTARI = re.compile(r"<!--.*?-->", re.S)
RE_SCRIPT = re.compile(r"<(script|style)\b.*?</\1>", re.S | re.I)
RE_ETIQUETA = re.compile(r"<[^>]+>")
RE_H2 = re.compile(r"<h2\b", re.I)
RE_TITOL = re.compile(r"<title>(.*?)</title>", re.S | re.I)
RE_DESC = re.compile(r'<meta\s+name="description"\s+content="(.*?)"', re.S | re.I)
RE_REDIR = re.compile(r'http-equiv=["\']refresh', re.I)
RE_ADRECA = re.compile(r"\S*cbgrupbarna\S*|\S+\.(?:info|com|cat|es|org)\S*", re.I)

# Paraules que existeixen en català i no en castellà ni en anglès. No hi posem
# res que s'assembli a una paraula castellana: el que es busca és un senyal
# clar, no enxampar-ho tot.
CATALANES = [
    "amb", "aquest", "aquesta", "aquests", "aquestes", "però", "això", "què",
    "també", "perquè", "anys", "dies", "són", "més", "molt", "equips",
    "partits", "setmana", "tots", "totes", "seva", "seves", "hi ha",
]
# Quantes paraules catalanes calen per avisar. Amb una de sola s'enxampen
# massa noms de rivals i titulars citats; amb dues, el senyal ja és bo.
MINIM_CATALANES = 2
# Per sota d'aquesta proporció de paraules respecte de l'original, s'avisa.
PROPORCIO_MINIMA = 0.55
# Pàgines més curtes que això no diuen res: són índexs i portades de secció.
PARAULES_MINIMES = 40


def fitxer_de(url):
    p = url.lstrip("/")
    return os.path.join(ARREL, p if p.endswith(".html") else os.path.join(p, "index.html"))


def carrega(cami):
    with open(cami, encoding="utf-8", errors="replace") as fh:
        return fh.read()


def text_visible(brut):
    cos = brut.split("<body", 1)[-1]
    cos = RE_COMENTARI.sub(" ", cos)      # notes internes: no es veuen
    cos = RE_SCRIPT.sub(" ", cos)
    cos = RE_ETIQUETA.sub(" ", cos)
    return re.sub(r"\s+", " ", html.unescape(cos)).strip()


def meta(brut, rx):
    m = rx.search(brut)
    return re.sub(r"\s+", " ", html.unescape(m.group(1))).strip() if m else None


def carrega_excepcions():
    cami = os.path.join(ARREL, "i18n", "excepcions-contingut.yml")
    if not os.path.exists(cami):
        return {}, []
    with open(cami, encoding="utf-8") as fh:
        d = yaml.safe_load(fh) or {}
    fora, prefixos = {}, []
    for e in (d.get("no_mirar") or []):
        quines = set(e.get("comprovacions") or ["totes"])
        if e.get("prefix"):
            prefixos.append((e["prefix"], quines))
        else:
            fora.setdefault(e["ruta"], set()).update(quines)
    return fora, prefixos


def sense_soroll(text, noms):
    """Treu el que legítimament pot anar en català dins d'una traducció."""
    text = RE_ADRECA.sub(" ", text)        # cbgrupbarna.info/partits/equips/
    for n in noms:
        text = text.replace(n, " ")        # noms propis del glossari
    return text


def main():
    nomes = sys.argv[1] if len(sys.argv) > 1 else None

    with open(os.path.join(ARREL, "i18n", "glossari.yml"), encoding="utf-8") as fh:
        noms = sorted(yaml.safe_load(fh)["noms_propis"], key=len, reverse=True)
    with open(os.path.join(ARREL, "i18n", "routes.yml"), encoding="utf-8") as fh:
        rutes = yaml.safe_load(fh).get("rutes", [])
    fora, prefixos = carrega_excepcions()

    avisos = {"seccions": [], "llargada": [], "catala": [], "titol": []}
    mirades = 0

    for r in rutes:
        ca = r.get("ca")
        if not ca or (nomes and ca != nomes):
            continue
        f_ca = fitxer_de(ca)
        if not os.path.exists(f_ca):
            continue
        brut_ca = carrega(f_ca)
        if RE_REDIR.search(brut_ca[:4000]):
            continue

        text_ca = text_visible(brut_ca)
        n_ca = len(text_ca.split())
        if n_ca < PARAULES_MINIMES:
            continue
        h2_ca = len(RE_H2.findall(brut_ca))
        titol_ca = meta(brut_ca, RE_TITOL)
        exempta = set(fora.get(ca, set()))
        for pre, quines in prefixos:
            if ca.startswith(pre):
                exempta |= quines

        for idioma in IDIOMES:
            desti = r.get(idioma)
            if not desti:
                continue
            f = fitxer_de(desti)
            if not os.path.exists(f):
                continue
            mirades += 1
            brut = carrega(f)
            text = text_visible(brut)

            def salta(qui):
                return "totes" in exempta or qui in exempta

            h2 = len(RE_H2.findall(brut))
            if h2_ca and h2 < h2_ca and not salta("seccions"):
                avisos["seccions"].append(f"{desti} · {h2} seccions, l'original en té {h2_ca}")

            n = len(text.split())
            if n_ca and n < n_ca * PROPORCIO_MINIMA and not salta("llargada"):
                avisos["llargada"].append(
                    f"{desti} · {n} paraules, l'original en té {n_ca}")

            net = sense_soroll(text, noms).lower()
            trobades = sorted({
                w for w in CATALANES
                if re.search(r"(?<![\w·'])" + re.escape(w) + r"(?![\w·])", net)
            })
            if len(trobades) >= MINIM_CATALANES and not salta("catala"):
                avisos["catala"].append(f"{desti} · {', '.join(trobades[:6])}")

            if titol_ca and meta(brut, RE_TITOL) == titol_ca and not salta("titol"):
                avisos["titol"].append(f"{desti} · «{titol_ca[:70]}»")

    noms_avis = {
        "seccions": "SECCIONS QUE FALTEN A LA TRADUCCIÓ",
        "llargada": "TRADUCCIÓ MOLT MÉS CURTA QUE L'ORIGINAL",
        "catala": "TEXT EN CATALÀ DINS D'UNA TRADUCCIÓ",
        "titol": "<title> IDÈNTIC AL DE L'ORIGINAL",
    }
    total = sum(len(v) for v in avisos.values())
    print(f"Traduccions obertes i comparades: {mirades}\n")
    if not total:
        print("Cap avís: el contingut de les traduccions es correspon amb l'original.")
        return 0

    for clau, titol in noms_avis.items():
        v = avisos[clau]
        if not v:
            continue
        print(f"{titol} · {len(v)}")
        for x in v:
            print(f"    {x}")
        print()

    print("Si algun d'aquests és correcte tal com està —una cita literal en")
    print("català, el nom d'un rival, una plantilla que s'ofereix en català a")
    print("propòsit— escriu-ho a i18n/excepcions-contingut.yml amb el motiu.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
