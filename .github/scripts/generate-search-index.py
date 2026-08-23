#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera /cerca-index.json: l'índex que fa servir el cercador del web
(/js/cerca.js i la pàgina /cerca/).

Recull dues coses:

  1. Les PÀGINES (títol, descripció, encapçalaments, un tros de text).
  2. Les PREGUNTES I RESPOSTES que ja hi ha escrites al JSON-LD `FAQPage` de
     tot el lloc — 477 repartides per 98 pàgines. Són respostes redactades
     pel club, i per això el cercador les pot ensenyar tal qual, sense
     inventar-se res i sense demanar-ho a cap servei extern. Aquesta és la
     part que fa que el cercador respongui, no només enllaci.

Recorre els .html del repositori, en treu títol, descripció, encapçalaments i
un tros de text visible, i ho desa tot en un únic JSON compacte que el
navegador es baixa la primera vegada que algú obre el cercador.

  python3 .github/scripts/generate-search-index.py

Regles:
  - No indexa pàgines amb `noindex`, ni /admin/, ni els residus llegats
    (/patrocinis/, /presentacio/, /dossier-patrocinis/), ni l'app /galeria/,
    ni /tests/.
  - L'idioma surt de l'atribut lang o del prefix /es/ · /en/.
  - Les equivalències entre idiomes surten de i18n/routes.yml, que s'edita
    a mà i mana (vegeu la capçalera d'aquell fitxer).
"""

import json
import os
import re
import sys
from html import unescape
from html.parser import HTMLParser

ARREL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SORTIDA = os.path.join(ARREL, "cerca-index.json")

# Carpetes que no s'indexen mai.
EXCLOSES = (
    ".git", ".github", ".claude", "node_modules", "tests", "galeria",
    "admin", "patrocinis", "presentacio", "dossier-patrocinis",
    "assets", "fonts", "img", "css", "js", "scripts", "workers", "i18n",
)

# Pàgines que valen més que la resta quan hi ha empat: són les portes
# d'entrada reals del club, no un article de blog de fa dos anys.
PES_RUTA = {
    "/": 100,
    "/escoleta/": 92, "/partits/": 90, "/partits/equips/": 90,
    "/campus/": 88, "/portes-obertes/": 88, "/femeni/": 86,
    "/club/": 84, "/faq/": 84, "/partits/calendaris/": 84,
    "/basquet-formatiu/": 82, "/magics/": 80, "/cistella-petita/": 80,
    "/3x3/": 78, "/fotos/": 76, "/patrocinadors/": 76, "/empreses/": 76,
    "/contacte/": 76, "/blog/": 72, "/historia/": 72, "/organigrama/": 72,
    "/instal-lacions/": 72, "/documents/": 70, "/premsa/": 68,
}

BUITS = re.compile(r"\s+")

# Text que surt a totes (o gairebé totes) les pàgines i només fa que l'índex
# pesi més sense ajudar ningú a trobar res.
SOROLL = [
    "Saltar al contingut", "Saltar al contenido", "Skip to content",
    "Obrir el menú", "Menú complet",
    "CAT CAST ENG", "CAT CAST", "CA ES EN",
]


def treu_soroll(text):
    """Fora la palla repetida i les frases que es diuen dues vegades seguides."""
    for frase in SOROLL:
        text = text.replace(frase, " ")
    # La portada repeteix el ticker tres cops perquè l'animació el necessita;
    # a l'índex hi ha de constar una sola vegada.
    parts = [t.strip() for t in re.split(r"\s+·\s+|\.\s+", text) if t.strip()]
    vistes, unics = set(), []
    for t in parts:
        clau = t.lower()
        if clau in vistes:
            continue
        vistes.add(clau)
        unics.append(t)
    return BUITS.sub(" ", " · ".join(unics)).strip()


class Extractor(HTMLParser):
    """Treu del document el que serveix per cercar-hi i prou."""

    IGNORA = {"script", "style", "noscript", "svg", "template", "iframe"}
    ENCAPCALAMENTS = {"h1", "h2", "h3"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.lang = ""
        self.titol = ""
        self.descripcio = ""
        self.robots = ""
        self.canonical = ""
        self.encapcalaments = []
        self.text = []
        self._pila_ignora = 0
        self._dins_titol = False
        self._dins_h = None
        self._buffer_h = []
        self._dins_main = 0
        self._nav = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html":
            self.lang = (a.get("lang") or "").split("-")[0].lower()
        elif tag == "meta":
            nom = (a.get("name") or a.get("property") or "").lower()
            cont = a.get("content") or ""
            if nom == "description" and not self.descripcio:
                self.descripcio = cont
            elif nom == "robots":
                self.robots = cont.lower()
            elif nom == "og:description" and not self.descripcio:
                self.descripcio = cont
        elif tag == "link" and (a.get("rel") or "").lower() == "canonical":
            self.canonical = a.get("href") or ""
        elif tag == "title":
            self._dins_titol = True
        elif tag in self.IGNORA:
            self._pila_ignora += 1
        elif tag in ("nav", "header", "footer"):
            self._nav += 1
        elif tag == "main":
            self._dins_main += 1
        elif tag in self.ENCAPCALAMENTS and not self._nav:
            self._dins_h = tag
            self._buffer_h = []

    def handle_endtag(self, tag):
        if tag == "title":
            self._dins_titol = False
        elif tag in self.IGNORA:
            self._pila_ignora = max(0, self._pila_ignora - 1)
        elif tag in ("nav", "header", "footer"):
            self._nav = max(0, self._nav - 1)
        elif tag == "main":
            self._dins_main = max(0, self._dins_main - 1)
        elif tag in self.ENCAPCALAMENTS and self._dins_h == tag:
            h = neteja("".join(self._buffer_h))
            if h:
                self.encapcalaments.append(h)
            self._dins_h = None
            self._buffer_h = []

    def handle_data(self, data):
        if self._pila_ignora:
            return
        if self._dins_titol:
            self.titol += data
            return
        if self._dins_h is not None:
            self._buffer_h.append(data)
        # El menú i el peu són iguals a totes les pàgines: si s'indexessin,
        # cada cerca donaria 254 resultats idèntics.
        if not self._nav:
            self.text.append(data)


def neteja(s):
    return BUITS.sub(" ", unescape(s or "")).strip()


RE_LD = re.compile(
    r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
    re.I | re.S)


def recorre(node):
    """Tot el JSON-LD és un arbre irregular: @graph, llistes, objectes solts."""
    if isinstance(node, dict):
        yield node
        for v in node.values():
            for x in recorre(v):
                yield x
    elif isinstance(node, list):
        for v in node:
            for x in recorre(v):
                yield x


def preguntes_de(cru):
    """Treu les parelles pregunta/resposta del JSON-LD d'una pàgina.

    No es fa amb expressions regulars sobre l'HTML a posta: el JSON-LD ja és
    dada estructurada i validada per Google, i llegir-la com a JSON evita
    arrossegar marcatge dins de la resposta.
    """
    fora = []
    for tros in RE_LD.findall(cru):
        try:
            dades = json.loads(tros)
        except (ValueError, TypeError):
            continue
        for node in recorre(dades):
            if node.get("@type") != "Question":
                continue
            q = neteja(node.get("name") or "")
            resp = node.get("acceptedAnswer") or {}
            if isinstance(resp, list):
                resp = resp[0] if resp else {}
            r = neteja((resp or {}).get("text") or "")
            # Una pregunta sense resposta no serveix de res, i una resposta
            # d'una línia sol ser un titular, no una resposta.
            if len(q) > 6 and len(r) > 25:
                fora.append((q, r))
    return fora


def ruta_publica(cami):
    """De la ruta al disc a la URL que veu la gent."""
    rel = os.path.relpath(cami, ARREL).replace(os.sep, "/")
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[: -len("index.html")]
    return "/" + rel


def idioma(url, lang_atribut):
    if url.startswith("/es/"):
        return "es"
    if url.startswith("/en/"):
        return "en"
    if lang_atribut in ("ca", "es", "en"):
        return lang_atribut
    return "ca"


def pes(url):
    if url in PES_RUTA:
        return PES_RUTA[url]
    # Les traduccions hereten el pes de la pàgina en català.
    for prefix in ("/es/", "/en/"):
        if url.startswith(prefix):
            break
    base = 50
    fondaria = url.strip("/").count("/")
    return max(20, base - fondaria * 6)


def carrega_routes():
    """Llegeix i18n/routes.yml sense dependre de PyYAML (format pla i estable)."""
    cami = os.path.join(ARREL, "i18n", "routes.yml")
    parelles = []
    if not os.path.exists(cami):
        return parelles
    actual = None
    with open(cami, encoding="utf-8") as f:
        for linia in f:
            m = re.match(r"^-\s+ca:\s*(\S+)", linia)
            if m:
                if actual:
                    parelles.append(actual)
                actual = {"ca": None if m.group(1) == "null" else m.group(1)}
                continue
            m = re.match(r"^\s+(es|en):\s*(\S+)", linia)
            if m and actual is not None:
                actual[m.group(1)] = None if m.group(2) == "null" else m.group(2)
    if actual:
        parelles.append(actual)
    return parelles


def cal_indexar(cami):
    rel = os.path.relpath(cami, ARREL).replace(os.sep, "/")
    primer = rel.split("/")[0]
    if primer in EXCLOSES:
        return False
    for lang in ("es", "en"):
        if rel.startswith(lang + "/"):
            segon = rel.split("/")[1] if "/" in rel[len(lang) + 1:] else ""
            if segon in EXCLOSES:
                return False
    return True


def main():
    pagines = []
    faq = []
    vistes_faq = set()
    saltades = {"noindex": 0, "redireccio": 0, "buida": 0}

    for arrel, dirs, fitxers in os.walk(ARREL):
        dirs[:] = [d for d in dirs if d not in EXCLOSES and not d.startswith(".")]
        for fitxer in fitxers:
            if not fitxer.endswith(".html"):
                continue
            cami = os.path.join(arrel, fitxer)
            if not cal_indexar(cami):
                continue
            url = ruta_publica(cami)
            if url == "/404.html":
                continue

            try:
                with open(cami, encoding="utf-8", errors="replace") as f:
                    cru = f.read()
            except OSError:
                continue

            p = Extractor()
            try:
                p.feed(cru)
            except Exception:
                pass

            if "noindex" in p.robots:
                saltades["noindex"] += 1
                continue
            # Redireccions: pàgines que només porten a una altra.
            if re.search(r'http-equiv=["\']refresh', cru, re.I):
                saltades["redireccio"] += 1
                continue

            titol = neteja(p.titol)
            # «Escoleta de bàsquet · CB Grup Barna» → volem la primera part
            # per al resultat, però la segona també és cercable.
            cos = treu_soroll(neteja(" ".join(p.text)))
            if not titol and not cos:
                saltades["buida"] += 1
                continue

            for q, r in preguntes_de(cru):
                # La mateixa pregunta surt sovint a més d'una pàgina (i a les
                # tres versions d'idioma). Ens quedem amb la primera, que per
                # l'ordre de recorregut sol ser la pàgina més important.
                clau = (idioma(url, p.lang), BUITS.sub(" ", q.lower()))
                if clau in vistes_faq:
                    continue
                vistes_faq.add(clau)
                faq.append({
                    "q": q,
                    "r": r[:600],
                    "u": url,
                    "l": idioma(url, p.lang),
                })

            registre = {
                "u": url,
                "l": idioma(url, p.lang),
                "t": titol,
                "d": neteja(p.descripcio)[:260],
                "h": p.encapcalaments[:14],
                "c": cos[:700],
                "p": pes(url),
            }
            pagines.append(registre)

    pagines.sort(key=lambda r: (-r["p"], r["u"]))

    # Ordre estable: així el fitxer no canvia si no ha canviat el contingut,
    # i el workflow no fa un commit per res.
    faq.sort(key=lambda x: (x["l"], x["u"], x["q"]))

    index = {
        "versio": 2,
        "pagines": pagines,
        "faq": faq,
        "idiomes": sorted({r["l"] for r in pagines}),
        "rutes": [r for r in carrega_routes() if r.get("ca")],
    }

    with open(SORTIDA, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, separators=(",", ":"))

    pes_kb = os.path.getsize(SORTIDA) / 1024
    per_idioma = {}
    for r in pagines:
        per_idioma[r["l"]] = per_idioma.get(r["l"], 0) + 1
    faq_idioma = {}
    for r in faq:
        faq_idioma[r["l"]] = faq_idioma.get(r["l"], 0) + 1
    print(f"cerca-index.json · {len(pagines)} pàgines · "
          f"{len(faq)} preguntes amb resposta · {pes_kb:.0f} KB")
    print("  preguntes per idioma: " +
          ", ".join(f"{k}={v}" for k, v in sorted(faq_idioma.items())))
    print("  per idioma: " + ", ".join(f"{k}={v}" for k, v in sorted(per_idioma.items())))
    print("  saltades: " + ", ".join(f"{k}={v}" for k, v in saltades.items()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
