#!/usr/bin/env python3
"""Passa tot el lloc pel sistema visual de l'artefacte «Franges i Extensa».

Fa dues coses, i només dues, perquè es puguin revisar d'una llegida:

1. COLOR  · tradueix els valors que no són del sistema als de la taula de la
            skill web-cbgb: un sol vermell (#E20613), el seu fosc (#A8040E),
            la tinta (#10100E), la crema (#F4F1EC) i el gris d'etiqueta
            (#6B6560). Sobre fons fosc el vermell s'aclareix a #FF3B41.
2. LLETRA · deixa dues famílies i prou: Anton per a display i Inter per a text.
            Treu Jost, Bebas Neue, Outfit i Cormorant Garamond dels enllaços de
            Google Fonts i de les declaracions de `font-family`.

El que NO toca, a posta:
  · /orgull/            la bandera de l'Orgull no és decoració
  · /opina/print/       peces per imprimir, altre mitjà
  · admin i eines       pàgines internes, no són cara pública
  · marques d'altri     Instagram, WhatsApp i TikTok porten el seu color
  · semàntics de partit --win i --loss de /partits/

Ús:
    python3 scripts/aplica-estetica.py --dry-run   # només informa
    python3 scripts/aplica-estetica.py             # escriu
"""

import argparse
import re
import sys
from pathlib import Path

ARREL = Path(__file__).resolve().parent.parent

EXCLOU_DIRS = {".git", "tests", "node_modules"}
EXCLOU_PATRONS = (
    "vendor/",
    "css/fonts.css",
    "orgull/",
    "opina/print/",
    "admin/",
    "/admin.html",
    "briefing/admin.html",
)

# ── Color ────────────────────────────────────────────────────────────────────
# Vermells que no són el de l'escut.
VERMELLS = ["c8102e", "e31e24", "e8002d", "e63329", "fd030c", "e6001e", "d81e26"]
# Vermells foscos fora de sistema.
VERMELLS_FOSCOS = ["b7231b", "8f0d16", "a30510"]
# Negres i quasi negres que fan de tinta.
# Només els que fan de tinta o de fons de pàgina: els negres més clars
# (#111111, #161616...) són superfícies de les presentacions fosques i, si es
# tradueixen, el fons queda més clar que el panell que hi va a sobre.
TINTES = ["0a0a0a", "0f0f0f", "0a0908", "0e1116"]
# Cremes i papers trencats.
CREMES = ["f2ede6", "ede7de", "f6f4f1", "faf9f5", "f7f4f0", "f4f1ea"]
# Grisos d'etiqueta que no arriben al contrast mínim.
# #706c67 va arribar d'una revisió d'accessibilitat i també passa AA, però el
# gris de la guia és el #6B6560: un de sol, com el vermell.
GRISOS = ["8a8681", "9a9691", "8b8b8b", "706c67"]
# Accents que no són de marca (el verd neó de la galeria del 3x3).
ACCENTS_FORA = ["00ff57", "00e04c"]

SUBSTITUCIONS_HEX = (
    [(h, "#E20613") for h in VERMELLS + ACCENTS_FORA]
    + [(h, "#A8040E") for h in VERMELLS_FOSCOS]
    + [(h, "#10100E") for h in TINTES]
    + [(h, "#F4F1EC") for h in CREMES]
    + [(h, "#6B6560") for h in GRISOS]
)

# Els mateixos colors escrits en rgb()/rgba(), que el hex no atrapa.
# Els mateixos colors escrits en rgb()/rgba(), que el hex no atrapa. Hi ha més
# de cinc-centes aparicions de rgba(200,16,46) —el vermell antic— i de
# rgba(242,237,230) —la crema antiga— repartides pel lloc.
def _rgb(orig: str, nou: str):
    a, b, c = orig.split(",")
    patro = re.compile(
        r"rgba?\(\s*" + a + r"\s*,\s*" + b + r"\s*,\s*" + c + r"\s*([,)])", re.I
    )
    return (patro, "rgba(" + nou + r"\1")


SUBSTITUCIONS_RGBA = [
    _rgb("0,255,87", "226,6,19"),
    _rgb("200,16,46", "226,6,19"),
    _rgb("230,51,41", "226,6,19"),
    _rgb("227,30,36", "226,6,19"),
    _rgb("232,0,45", "226,6,19"),
    _rgb("242,237,230", "244,241,236"),
    _rgb("10,10,10", "16,16,14"),
    _rgb("15,15,15", "16,16,14"),
    _rgb("14,17,22", "16,16,14"),
    _rgb("10,9,8", "16,16,14"),
]

# ── Lletra ───────────────────────────────────────────────────────────────────
FAMILIES_FORA_DISPLAY = ["Bebas Neue", "Cormorant Garamond", "Jost", "Oswald"]
FAMILIES_FORA_TEXT = ["Outfit"]

PILA_DISPLAY = "'Anton', 'Haettenschweiler', 'Arial Narrow', sans-serif"
PILA_TEXT = "'Inter', -apple-system, BlinkMacSystemFont, system-ui, sans-serif"


def cal_saltar(cami: Path) -> bool:
    rel = "/" + str(cami.relative_to(ARREL))
    if any(part in EXCLOU_DIRS for part in cami.relative_to(ARREL).parts):
        return True
    return any(patro in rel for patro in EXCLOU_PATRONS)


def substitueix_colors(text: str) -> tuple[str, int]:
    canvis = 0
    for hexa, nou in SUBSTITUCIONS_HEX:
        patro = re.compile(r"#" + hexa + r"\b", re.I)
        text, n = patro.subn(nou, text)
        canvis += n
    for patro, nou in SUBSTITUCIONS_RGBA:
        text, n = patro.subn(nou, text)
        canvis += n
    return text, canvis


def substitueix_lletra(text: str) -> tuple[str, int]:
    canvis = 0

    # 1. Enllaços de Google Fonts: es refan sencers amb Anton + Inter.
    def refes_enllac(m: re.Match) -> str:
        href = m.group(0)
        families = re.findall(r"family=([^&\"']+)", href)
        noms = [f.split(":")[0].replace("+", " ") for f in families]
        vol_display = any(
            n in FAMILIES_FORA_DISPLAY or n == "Anton" for n in noms
        )
        peces = []
        if vol_display:
            peces.append("family=Anton")
        peces.append("family=Inter:wght@300;400;500;600;700;800;900")
        return (
            "https://fonts.googleapis.com/css2?"
            + "&".join(peces)
            + "&display=swap"
        )

    patro_enllac = re.compile(r"https://fonts\.googleapis\.com/css2\?[^\"']+")

    def cal_refer(m: re.Match) -> bool:
        return any(
            f.replace(" ", "+") in m.group(0)
            for f in FAMILIES_FORA_DISPLAY + FAMILIES_FORA_TEXT
        )

    trossos = []
    darrer = 0
    for m in patro_enllac.finditer(text):
        if cal_refer(m):
            trossos.append(text[darrer:m.start()])
            trossos.append(refes_enllac(m))
            darrer = m.end()
            canvis += 1
    if trossos:
        trossos.append(text[darrer:])
        text = "".join(trossos)

    # 2. Piles de fonts declarades a mà.
    for fam in FAMILIES_FORA_DISPLAY:
        patro = re.compile(r"\\?'" + fam + r"\\?'|\\?\"" + fam + r"\\?\"")
        text, n = patro.subn(lambda m: ("\\'Anton\\'" if m.group(0).startswith("\\") else "'Anton'"), text)
        canvis += n
    for fam in FAMILIES_FORA_TEXT:
        patro = re.compile(r"\\?'" + fam + r"\\?'|\\?\"" + fam + r"\\?\"")
        text, n = patro.subn(lambda m: ("\\'Inter\\'" if m.group(0).startswith("\\") else "'Inter'"), text)
        canvis += n

    # 3. El token --display i --body es deixen sempre a la pila sencera.
    text, n = re.subn(
        r"--display:\s*'Anton'[^;}]*", "--display: " + PILA_DISPLAY, text
    )
    canvis += n
    text, n = re.subn(
        r"--body:\s*'Inter'[^;}]*", "--body: " + PILA_TEXT, text
    )
    canvis += n

    # 4 bis. Anton no té cursiva: dins d'un bloc de declaracions que ja demana
    # la display, la cursiva se sintetitza i es nota. Fora.
    def _sense_cursiva(m: re.Match) -> str:
        bloc = m.group(0)
        if "Anton" not in bloc:
            return bloc
        return re.sub(r"font-style:\s*italic;?\s*", "", bloc)

    text, n = re.subn(r"\{[^{}]*\}", _sense_cursiva, text)
    text, n = re.subn(r'style="[^"]*"', _sense_cursiva, text)
    canvis += 0

    # 4. Anton no té cursiva ni serif de recanvi: la pila sencera i prou.
    def _pila(m: re.Match) -> str:
        if m.group(0).startswith("\\"):
            # dins d'una cadena de JavaScript les cometes van escapades
            return PILA_DISPLAY.replace("'", "\\'")
        return PILA_DISPLAY

    text, n = re.subn(r"\\?'Anton\\?',\s*(?:Georgia,\s*)?serif", _pila, text)
    canvis += n
    text, n = re.subn(
        r"(font-family:\s*\\?'Anton\\?'[^;}]*;\s*)font-style:\s*italic;\s*",
        r"\1",
        text,
    )
    canvis += n

    # 4. 'Anton', 'Anton' repetits per la substitució anterior.
    text = re.sub(r"'Anton',\s*'Anton'", "'Anton'", text)
    text = re.sub(r"'Inter',\s*'Inter'", "'Inter'", text)
    return text, canvis


ENLLAC_FONTS = '<link rel="stylesheet" href="/css/fonts.css">\n'


RE_FULL_GOOGLE = re.compile(r'<link[^>]*fonts\.googleapis\.com/css2[^>]*>')
RE_PRECONNECT = re.compile(r'\s*<link[^>]*fonts\.(?:googleapis|gstatic)\.com"?[^>]*>')


def treu_google_fonts(text: str) -> tuple[str, int]:
    """Cap pàgina demana res a fonts.googleapis.com: les dues famílies viuen a
    /fonts/ i es carreguen amb /css/fonts.css. És el criteri RGPD del club."""
    if "fonts.googleapis.com" not in text:
        return text, 0
    primer = [True]

    def sub(m: re.Match) -> str:
        if "stylesheet" in m.group(0) and primer[0]:
            primer[0] = False
            return ENLLAC_FONTS.strip()
        return ""

    text = RE_FULL_GOOGLE.sub(sub, text)
    text = RE_PRECONNECT.sub("", text)
    if primer[0]:  # només hi havia preloads o preconnects
        text = re.sub(
            r"(<meta charset=[^>]*>)", r"\1\n" + ENLLAC_FONTS.strip(), text, count=1
        )
    return text, 1


def assegura_fonts(text: str) -> tuple[str, int]:
    """Si una pàgina demana Anton, l'ha de carregar. Si no, cau a un serif del
    sistema i el titular deixa de ser del club."""
    if "Anton" not in text:
        return text, 0
    if any(t in text for t in ("css/barna.css", "css/fonts.css", "@font-face", "family=Anton")):
        return text, 0
    m = re.search(r"https://fonts\.googleapis\.com/css2\?family=", text)
    if m:
        text = text[:m.end()] + "Anton&family=" + text[m.end():]
        return text, 1
    m = re.search(r"<head[^>]*>", text)
    if not m:
        return text, 0
    # Darrere del charset: la declaració de codificació ha d'anar primera.
    mc = re.search(r"<meta charset=[^>]*>", text[m.end():], re.I)
    tall = m.end() + (mc.end() if mc else 0)
    return text[:tall] + "\n" + ENLLAC_FONTS + text[tall:], 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("camins", nargs="*", help="fitxers concrets (per defecte, tot)")
    args = ap.parse_args()

    if args.camins:
        fitxers = [Path(c).resolve() for c in args.camins]
    else:
        fitxers = sorted(
            f
            for patro in ("*.html", "*.css", "*.js")
            for f in ARREL.rglob(patro)
        )

    tocats = 0
    for f in fitxers:
        if cal_saltar(f):
            continue
        original = f.read_text(encoding="utf-8")
        text, n_color = substitueix_colors(original)
        text, n_lletra = substitueix_lletra(text)
        text, n_google = treu_google_fonts(text)
        text, n_fonts = assegura_fonts(text)
        n_lletra += n_fonts + n_google
        if text == original:
            continue
        tocats += 1
        print(f"{f.relative_to(ARREL)}  color:{n_color}  lletra:{n_lletra}")
        if not args.dry_run:
            f.write_text(text, encoding="utf-8")

    print(f"\n{tocats} fitxers {'a canviar' if args.dry_run else 'canviats'}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
