#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Passa les preguntes freqüents que encara viuen dins d'una pàgina cap a la font
única, i deixa la pàgina preparada perquè les hi escrigui el generador.

  python3 scripts/faq-migra.py --llista            # què queda per migrar
  python3 scripts/faq-migra.py /campus/ --dry-run  # què faria amb aquesta
  python3 scripts/faq-migra.py /campus/            # ho fa
  python3 scripts/faq-migra.py --automatiques      # totes les que són segures

QUÈ FA, PER A CADA PÀGINA
  1. En treu les preguntes del JSON-LD `FAQPage`, EN L'ORDRE DE LA PÀGINA,
     de les tres versions d'idioma.
  2. Les aparella i les escriu a `i18n/faq.yml`.
  3. Posa els marcadors a l'HTML i treu el FAQPage vell del @graph, perquè no
     n'hi quedin dos.

L'APARELLAMENT ÉS EL PUNT DELICAT
Les traduccions es van fer de la pàgina catalana, i per tant solen anar en el
mateix ordre; però no sempre (a /basquet-formatiu/ el castellà anava
capgirat). Aparellar malament vol dir publicar la resposta d'una pregunta sota
una altra, en un altre idioma, sense que ningú se n'adoni.

Per això aquí NO s'aparella a cegues per posició. Cada parella passa una
comprovació de plausibilitat: les xifres, els noms propis i les paraules
llargues que hi ha a la pregunta catalana han de tornar a sortir a la
traducció. Les tres llengües comparteixen prou lèxic («Escoleta»,
«Barcelona», «federada/federado», «2026») perquè això sigui un senyal fiable.
Si una parella no arriba al mínim, la pàgina sencera es marca com a
**no automàtica** i s'ha de mirar a mà. Val més parar-se que endevinar.
"""

import argparse
import html
import io
import json
import os
import re
import sys
import unicodedata

try:
    import yaml
except ImportError:
    sys.exit("Cal PyYAML:  pip install pyyaml")

ARREL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT = os.path.join(ARREL, "i18n", "faq.yml")
RUTES = os.path.join(ARREL, "i18n", "routes.yml")
IDIOMES = ("ca", "es", "en")

RE_LD = re.compile(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
                   re.I | re.S)

TITOL_FAQ = {"ca": "Preguntes freqüents",
             "es": "Preguntas frecuentes",
             "en": "Frequently asked questions"}


# ── lectura ────────────────────────────────────────────────────────────────

def carrega_rutes():
    dades = yaml.safe_load(io.open(RUTES, encoding="utf-8")) or {}
    mapa = {}
    for r in dades.get("rutes", []):
        if r.get("ca"):
            mapa[r["ca"]] = {"ca": r["ca"], "es": r.get("es"), "en": r.get("en")}
    return mapa


def cami_de(url):
    n = url.strip("/")
    if not n:
        return os.path.join(ARREL, "index.html")
    if n.endswith(".html"):
        return os.path.join(ARREL, *n.split("/"))
    return os.path.join(ARREL, *n.split("/"), "index.html")


def recorre(n):
    if isinstance(n, dict):
        yield n
        for v in n.values():
            for x in recorre(v):
                yield x
    elif isinstance(n, list):
        for v in n:
            for x in recorre(v):
                yield x


def preguntes_de(url):
    """Les preguntes del JSON-LD, en l'ordre en què són a la pàgina."""
    p = cami_de(url)
    if not os.path.exists(p):
        return None
    s = io.open(p, encoding="utf-8", errors="replace").read()
    fora = []
    for tros in RE_LD.findall(s):
        try:
            d = json.loads(tros)
        except ValueError:
            continue
        for n in recorre(d):
            if n.get("@type") != "FAQPage":
                continue
            for q in n.get("mainEntity") or []:
                if not isinstance(q, dict) or q.get("@type") != "Question":
                    continue
                a = q.get("acceptedAnswer") or {}
                if isinstance(a, list):
                    a = a[0] if a else {}
                nom = (q.get("name") or "").strip()
                txt = ((a or {}).get("text") or "").strip()
                if nom and txt:
                    fora.append({"q": nom, "r": txt})
    return fora


# ── plausibilitat de l'aparellament ────────────────────────────────────────

# Paraules que comencen amb majúscula només perquè obren la frase, o perquè
# són el nom d'un mes o d'un dia: no són noms propis i no valen com a senyal.
NO_SON_PROPIS = set("""
El La Els Les Un Una Al Als Del Des De Per Que Qui Quan Quin Quina Quines Quins
Com On Tot Tota Tots Totes Hi Si No Es Son Cal Aixo Aquest Aquesta Aquests
Los Las Uno Unos Unas Para Por Con Sin Como Donde Cuando Cuanto Cuanta Cual
The A An And Or For To In On At Is Are Do Does Did You Your We Our They It
What When Where Which Who How Why There This That These Those Yes
Gener Febrer Marc Abril Maig Juny Juliol Agost Setembre Octubre Novembre Desembre
Enero Febrero Marzo Mayo Junio Julio Agosto Septiembre Octubre Noviembre Diciembre
January February March April May June July August September October November December
""".split())


def senyals(text):
    """El que ha de sobreviure a una traducció: les XIFRES i els NOMS PROPIS.

    Les paraules corrents no serveixen. Entre català i castellà se semblen
    prou («categoria/categoría») i tempten a fer-les servir, però entre
    català i anglès no s'assemblen gens, i llavors qualsevol parella
    correcta sembla dolenta. Amb xifres i noms propis, en canvi, el senyal és
    el mateix en els tres idiomes: un 2026 és un 2026, i «LOPIVI», «Julio
    Torralba» o «La Nau del Clot» no es tradueixen.
    """
    t = unicodedata.normalize("NFD", text)
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    xifres = set(re.findall(r"\d+", t))
    propis = set(w for w in re.findall(r"\b[A-Z][a-zA-Z]{2,}\b", t)
                 if w not in NO_SON_PROPIS)
    return xifres, propis


def prou(a, b, minim):
    """Quina part dels senyals de l'original torna a sortir a la traducció."""
    if not a:
        return True
    return len(a & b) / len(a) >= minim


def ordre_correcte(ca, alt):
    """L'ordre de la traducció, és el mateix que el del català?

    Aparellar una a una i mirar si cada parella «sembla bé» és massa
    exigent: sempre n'hi ha alguna que perd tots els senyals (una pregunta
    curta i sense cap xifra ni nom propi). El que sí que és concloent és
    COMPARAR: si l'ordre tal com està encaixa millor que qualsevol
    desplaçament de la llista, l'ordre és el bo. Una llista mal ordenada no
    guanya el seu propi desplaçament.
    """
    n = len(ca)
    if n != len(alt) or n == 0:
        return False
    if n == 1:
        return plausible(ca[0], alt[0])

    def punts(desp):
        return sum(plausible(ca[i], alt[(i + desp) % n]) for i in range(n)) / n

    directe = punts(0)
    if directe < 0.6:
        return False
    return all(directe > punts(d) for d in range(1, n))


def plausible(ca, altre):
    """Pot ser l'una traducció de l'altra?

    És una comprovació de PLAUSIBILITAT, no de correcció: només ha de servir
    per aturar-nos quan una parella és clarament impossible. Davant del dubte
    passa, i la pàgina es mira a mà igualment abans de publicar.
    """
    xa, pa = senyals(ca["q"] + " " + ca["r"])
    xb, pb = senyals(altre["q"] + " " + altre["r"])
    # Les xifres han de sobreviure gairebé sempre; els noms propis, sovint
    # (un pot desaparèixer per una perífrasi).
    return prou(xa, xb, 0.6) and prou(pa, pb, 0.5)


# ── escriptura ─────────────────────────────────────────────────────────────

def identificador(url, i, usats):
    tros = [t for t in url.strip("/").split("/") if t] or ["portada"]
    base = re.sub(r"[^a-z0-9]+", "-", tros[-1].lower()).strip("-")[:26] or "pag"
    ident = f"{base}-{i + 1}"
    n = 1
    while ident in usats:
        n += 1
        ident = f"{base}-{i + 1}-{n}"
    usats.add(ident)
    return ident


def treu_faqpage(s):
    def refes(m):
        try:
            d = json.loads(m.group(1))
        except ValueError:
            return m.group(0)
        graf = d.get("@graph")
        if isinstance(graf, list):
            nou = [n for n in graf if not (isinstance(n, dict) and n.get("@type") == "FAQPage")]
            if len(nou) == len(graf):
                return m.group(0)
            d["@graph"] = nou
            return ('<script type="application/ld+json">\n'
                    + json.dumps(d, ensure_ascii=False, indent=2) + '\n</script>')
        if d.get("@type") == "FAQPage":
            return ""          # el bloc sencer era la FAQ: fora
        return m.group(0)
    return RE_LD.sub(refes, s)


def prepara_pagina(url, idioma):
    """Deixa la pàgina amb els marcadors i sense el FAQPage vell."""
    p = cami_de(url)
    s = io.open(p, encoding="utf-8").read()
    if "FAQ:START" in s and "FAQ-LD:START" in s:
        return "ja preparada"

    if "FAQ:START" not in s:
        m = re.search(r'<div class="faq"[^>]*>', s)
        if m:
            # Ja hi ha secció de preguntes: el seu contingut passa a ser
            # territori del generador.
            i = m.end()
            fi = s.rfind("</details>", i)
            j = s.index("</div>", fi if fi > 0 else i)
            s = s[:i] + "<!-- FAQ:START --><!-- FAQ:END -->" + s[j:]
        else:
            bloc = (
                '\n<!-- ==== PREGUNTES FREQÜENTS ====\n'
                "     El que hi ha entre els marcadors FAQ i FAQ-LD el manté\n"
                "     .github/scripts/generate-faq.py des d'i18n/faq.yml. No s'edita aquí. -->\n"
                '<div class="wrap section">\n  <div class="narrow">\n'
                f'    <h2 id="faq">{TITOL_FAQ[idioma]}</h2>\n'
                '    <div class="faq"><!-- FAQ:START --><!-- FAQ:END --></div>\n'
                "  </div>\n</div>\n")
            ancora = "</main>" if "</main>" in s else (
                "<footer" if "<footer" in s else None)
            if not ancora:
                return "no sé on posar la secció de preguntes"
            i = s.index(ancora)
            s = s[:i] + bloc + s[i:]

    if "FAQ-LD:START" not in s:
        ancora = "</main>" if "</main>" in s else "<footer"
        i = s.index(ancora)
        s = s[:i] + "<!-- FAQ-LD:START --><!-- FAQ-LD:END -->\n" + s[i:]

    s = treu_faqpage(s)
    io.open(p, "w", encoding="utf-8").write(s)
    return "preparada"


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pagina", nargs="?", help="ruta catalana, p. ex. /campus/")
    ap.add_argument("--llista", action="store_true")
    ap.add_argument("--automatiques", action="store_true",
                    help="migra totes les que passen la comprovació")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    rutes = carrega_rutes()
    font = yaml.safe_load(io.open(FONT, encoding="utf-8")) or {}
    entrades = font.get("preguntes", [])
    ja = {e["pagina"] for e in entrades}
    usats = {e["id"] for e in entrades}

    # Què hi ha per migrar, i de quina mena.
    candidates = {}
    for ca, m in sorted(rutes.items()):
        if ca in ja:
            continue
        pc = preguntes_de(ca)
        if not pc:
            continue
        traduccions, estat = {}, "automatica"
        for idioma in ("es", "en"):
            url = m[idioma]
            if not url:
                continue
            alt = preguntes_de(url)
            if alt is None:
                continue
            if len(alt) != len(pc):
                estat = "a-ma"
                continue
            if not ordre_correcte(pc, alt):
                estat = "a-ma"
                continue
            traduccions[idioma] = alt
        candidates[ca] = (pc, traduccions, estat, m)

    if args.llista:
        for mena in ("automatica", "a-ma"):
            grup = {k: v for k, v in candidates.items() if v[2] == mena}
            print(f"\n=== {mena} · {len(grup)} pàgines · "
                  f"{sum(len(v[0]) for v in grup.values())} preguntes")
            for ca, (pc, tr, _, m) in sorted(grup.items()):
                diu = "+".join(sorted(tr)) or "només ca"
                print(f"  {len(pc):2} preguntes · {diu:8} · {ca}")
        return 0

    objectiu = ([args.pagina] if args.pagina
                else [k for k, v in candidates.items() if v[2] == "automatica"]
                if args.automatiques else [])
    if not objectiu:
        print("Digues una pàgina, o --automatiques, o --llista.")
        return 1

    noves = []
    for ca in objectiu:
        if ca not in candidates:
            print(f"  {ca}: res a migrar (o ja migrada)")
            continue
        pc, traduccions, estat, m = candidates[ca]
        if estat == "a-ma" and not args.pagina:
            continue
        for i, tros in enumerate(pc):
            e = {"id": identificador(ca, i, usats), "pagina": ca, "ca": tros}
            for idioma, llista in traduccions.items():
                e[idioma] = llista[i]
            noves.append(e)
        print(f"  {len(pc):2} preguntes · {'+'.join(sorted(traduccions)) or 'només ca'} · {ca}"
              + ("   ⚠ aparellament no comprovat" if estat == "a-ma" else ""))

    if not noves:
        print("Res per migrar.")
        return 0
    if args.dry_run:
        print(f"\n(prova) {len(noves)} preguntes anirien a i18n/faq.yml")
        return 0

    entrades.extend(noves)
    font["preguntes"] = entrades
    io.open(FONT, "w", encoding="utf-8").write(
        yaml.safe_dump(font, allow_unicode=True, sort_keys=False, width=88))

    for ca in {e["pagina"] for e in noves}:
        for idioma in IDIOMES:
            url = rutes.get(ca, {}).get(idioma)
            if url and os.path.exists(cami_de(url)):
                print(f"    {url}: {prepara_pagina(url, idioma)}")

    print(f"\n{len(noves)} preguntes a i18n/faq.yml. Ara:\n"
          "  python3 .github/scripts/generate-faq.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
