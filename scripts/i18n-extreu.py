#!/usr/bin/env python3
"""
Treu d'una pàgina catalana tot el text que s'ha de traduir, i prou.

    python3 scripts/i18n-extreu.py /club/ es
    python3 scripts/i18n-extreu.py /club/ es en          # els dos idiomes

Deixa la feina a i18n/feina/<idioma>/<ruta>.json: una llista de trossos de
text amb la posició exacta que ocupaven a l'original. Qui tradueix només ha
d'omplir el camp buit de cada tros; scripts/i18n-munta.py els torna a posar
al seu lloc i refà la pàgina.

Per què així i no traduint l'HTML sencer. Un traductor automàtic a qui li
dones HTML et retorna HTML *semblant*: es menja un atribut, canvia una
adreça, tanca una etiqueta on no toca, i tu no te n'adones fins que la
pàgina està publicada. Aquí el que viatja és només text; les etiquetes, les
adreces i l'estructura no surten mai de casa.

Què s'agafa:

  · El text que es veu, tret del que hi ha dins de <script>, <style> i <code>.
  · El <title>, la descripció, les paraules clau i els textos d'Open Graph i
    Twitter, que són el que surt a Google i quan es comparteix l'enllaç.
  · Els `alt` de les imatges i els `aria-label`, que són el que sent qui fa
    servir un lector de pantalla.
  · Els textos de dins del JSON-LD (el nom, la descripció, les preguntes i
    les respostes), que són els que Google llegeix per fer-ne fitxa.

Què NO s'agafa, i és a posta: adreces, classes, noms de fitxer, dates,
números solts i qualsevol tros que no tingui cap lletra.
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FEINA = ROOT / "i18n" / "feina"

# Zones que no es toquen mai.
RE_ZONA_MORTA = re.compile(r'(?is)<(script|style|code|pre)\b[^>]*>.*?</\1>')
# La capçalera i el peu no es tradueixen: els torna a dibuixar
# scripts/i18n_chrome.py des del diccionari, que és qui sap com es diu cada
# secció en cada idioma. Traduir-los aquí seria obrir una segona font.
RE_CHROME = re.compile(
    r'(?is)<header class="head".*?</header>'
    r'|<footer class="foot".*?</footer>'
    r'|<a href="#main" class="skip">.*?</a>')
# El <title> ja s'agafa com a atribut; si el text que hi ha a dins també
# s'agafés com a text visible, el mateix tros sortiria dues vegades i en
# muntar la pàgina els dos trossos es trepitjarien.
RE_TITOL = re.compile(r'(?is)<title[^>]*>.*?</title>')
RE_LD = re.compile(r'(?is)(<script[^>]*ld\+json[^>]*>)(.*?)(</script>)')
RE_TAG = re.compile(r'(?s)<[^>]+>')
RE_LLETRA = re.compile(r'[A-Za-zÀ-ÿ]')

# Atributs amb text de cara al públic.
def atribut(nom):
    """Un atribut, amb la cometa de tancament lligada a la d'obertura.

    Amb ["\'] a totes dues bandes, un aria-label="Fil d'Ariadna" es talla a
    l'apòstrof i el que se'n va a traduir és «Fil d».
    """
    return re.compile(r'(?i)(<[^>]*' + nom + r'=(["\']))((?:(?!\2)[^>])*)(\2)')


ATRIBUTS = [
    (re.compile(r'(?is)(<title[^>]*>)()(.*?)(</title>)'), "títol de la pestanya i de Google"),
    (atribut(r'name=["\']description["\'][^>]*content'), "descripció de Google"),
    (atribut(r'name=["\']keywords["\'][^>]*content'), "paraules clau"),
    (atribut(r'property=["\']og:(?:title|description|site_name)["\'][^>]*content'),
     "text en compartir l'enllaç"),
    (atribut(r'name=["\']twitter:(?:title|description)["\'][^>]*content'),
     "text en compartir l'enllaç"),
    (atribut(r'alt'), "descripció de la imatge"),
    (atribut(r'aria-label'), "etiqueta per a lectors de pantalla"),
    (atribut(r'placeholder'), "text d'exemple d'un camp"),
]

# Claus del JSON-LD que porten text de cara al públic.
CLAUS_LD = {"name", "headline", "description", "text", "alternateName", "jobTitle",
            "articleSection", "caption", "abstract", "slogan"}


def val(text):
    """Val la pena traduir aquest tros?"""
    net = text.strip()
    return bool(net) and bool(RE_LLETRA.search(net)) and not net.startswith(("http", "/", "#"))


def zones_mortes(html):
    return ([(m.start(), m.end()) for m in RE_ZONA_MORTA.finditer(html)]
            + [(m.start(), m.end()) for m in RE_CHROME.finditer(html)])


def dins(pos, zones):
    return any(a <= pos < b for a, b in zones)


def extreu(html):
    """Els trossos de text de la pàgina, amb on comença i acaba cadascun."""
    zones = zones_mortes(html)
    zones_text = zones + [(m.start(), m.end()) for m in RE_TITOL.finditer(html)]
    trossos = []

    # 1. El text que es veu: el que queda entre etiqueta i etiqueta.
    fi = 0
    for m in RE_TAG.finditer(html):
        tros = html[fi:m.start()]
        if val(tros) and not dins(fi, zones_text):
            esquerra = len(tros) - len(tros.lstrip())
            dreta = len(tros) - len(tros.rstrip())
            trossos.append({"de": fi + esquerra, "a": m.start() - dreta,
                            "tipus": "text", "ca": tros.strip()})
        fi = m.end()

    # 2. Els atributs.
    for patro, context in ATRIBUTS:
        for m in patro.finditer(html):
            if dins(m.start(), zones) or not val(m.group(3)):
                continue
            trossos.append({"de": m.start(3), "a": m.end(3),
                            "tipus": "atribut", "context": context, "ca": m.group(3)})

    # 3. El JSON-LD, clau per clau.
    for m in RE_LD.finditer(html):
        try:
            dades = json.loads(m.group(2))
        except json.JSONDecodeError:
            print(f"  avís: hi ha un JSON-LD que no es pot llegir; el deixo estar")
            continue
        camins = []

        def recorre(node, cami):
            if isinstance(node, dict):
                for k, v in node.items():
                    if k in CLAUS_LD and isinstance(v, str) and val(v):
                        camins.append((cami + [k], v))
                    else:
                        recorre(v, cami + [k])
            elif isinstance(node, list):
                for i, v in enumerate(node):
                    recorre(v, cami + [i])

        recorre(dades, [])
        for cami, text in camins:
            trossos.append({"json_ld": m.start(2), "cami": cami,
                            "tipus": "json-ld", "ca": text})

    trossos.sort(key=lambda t: t.get("de", t.get("json_ld", 0)))
    for i, t in enumerate(trossos):
        t["id"] = f"s{i:03d}"
    return trossos


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ruta", help="ruta de la pàgina catalana, p. ex. /club/")
    ap.add_argument("idiomes", nargs="+", choices=["es", "en"])
    args = ap.parse_args()

    resta = args.ruta.lstrip("/")
    fitxer = ROOT / (resta + "index.html" if args.ruta.endswith("/") else resta)
    if not fitxer.exists():
        print(f"No hi ha cap pàgina a {args.ruta}")
        return 1

    html = fitxer.read_text(encoding="utf-8")
    trossos = extreu(html)
    paraules = sum(len(t["ca"].split()) for t in trossos)

    for idioma in args.idiomes:
        desti = FEINA / idioma / (args.ruta.strip("/").replace("/", "__") or "portada")
        desti = desti.with_suffix(".json")
        desti.parent.mkdir(parents=True, exist_ok=True)
        anterior = {}
        if desti.exists():
            anterior = {t["ca"]: t.get(idioma, "")
                        for t in json.loads(desti.read_text(encoding="utf-8"))["trossos"]}
        feina = [dict(t, **{idioma: anterior.get(t["ca"], "")}) for t in trossos]
        desti.write_text(json.dumps(
            {"origen": args.ruta, "idioma": idioma, "trossos": feina},
            ensure_ascii=False, indent=1), encoding="utf-8")
        fets = sum(1 for t in feina if t[idioma])
        print(f"  {desti.relative_to(ROOT)} · {len(trossos)} trossos, {paraules} paraules"
              + (f" · {fets} ja traduïts" if fets else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
