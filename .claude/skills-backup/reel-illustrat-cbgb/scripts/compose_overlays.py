#!/usr/bin/env python3
"""
compose_overlays.py — genera els PNGs transparents de text (una capa per línia del
guió) i la targeta de tancament (escut + programa + claim) per al format
"reel il·lustrat" de CB Grup Barna: UNA il·lustració fixa amb push-in + línies de
text que van entrant en seqüència.

Ús:   LANG_REEL=ca python3 compose_overlays.py   (o LANG_REEL=es)
Sortida: overlays/line_00.png, line_01.png, ... (transparents, 1080x1920) +
         overlays/closing.png (targeta de tancament, opaca).

Edita el diccionari GUIO més avall — és l'ÚNIC que cal tocar per fer una peça nova.
Tokens de marca (colors/fonts/marges): sistema-visual-cbgb.
"""
from PIL import Image, ImageDraw, ImageFont, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
import os, json

W, H = 1080, 1920
DARK = (14, 17, 22)     # #0E1116
RED = (230, 51, 41)     # #E63329
WHITE = (245, 245, 247) # #F5F5F7
MARGIN = 80
LANG = os.environ.get("LANG_REEL", os.environ.get("LANG", "ca"))[:2]
LANG = LANG if LANG in ("ca", "es") else "ca"
HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "..", "assets")
ANTON = os.path.join(ASSETS, "Anton.ttf")
INTER = os.path.join(ASSETS, "Inter.ttf")
CRESTP = os.path.join(ASSETS, "escut_transp.png")
OUT = "overlays"
os.makedirs(OUT, exist_ok=True)
CREST = Image.open(CRESTP).convert("RGBA")


def T(ca, es):
    return ca if LANG == "ca" else es

# ============================================================================
# GUIÓ — edita això per a cada peça nova. Mateixa estructura, tema diferent.
# t0/t1 = segons dins del reel en què la línia és visible (deixa un forat entre
# línies perquè no se solapin). "big"=True per a la línia de tancament de l'hook
# (la que resol l'argument). "color" white|red — vermell només per remarcar UNA
# paraula/línia clau, mai més d'una vegada per peça (regla sistema-visual-cbgb).
# ============================================================================
GUIO = [
    dict(t0=0.0, t1=2.4,
         lines=lambda: [T("No cal una pista bonica.", "No hace falta una pista bonita.")],
         color="white", size=104),
    dict(t0=3.0, t1=5.4,
         lines=lambda: [T("No cal material.", "No hace falta material.")],
         color="white", size=104),
    dict(t0=6.0, t1=8.4,
         lines=lambda: [T("No cal saber jugar.", "No hace falta saber jugar.")],
         color="red", size=104),
    dict(t0=9.0, t1=12.6,
         lines=lambda: [T("Només cal una pilota.", "Solo hace falta un balón."),
                         T("I ganes.", "Y ganas.")],
         color="white", size=118, big=True),
]

CLOSING = dict(
    program="ESCOLETA BARNA",
    claim=lambda: T("4-6 anys · El Clot", "4-6 años · El Clot"),
)

DURATION_TOTAL = 12.6  # s de la part il·lustrada (sense comptar el tancament)
CLOSING_DURATION = 3.0  # s de la targeta de tancament

# ---------------------------------------------------------------------------
# helpers (mateix patró que reel-fotos-cbgb/scripts/compose_reel.py)
# ---------------------------------------------------------------------------

def font(p, s):
    return ImageFont.truetype(p, s)


def col(name):
    return RED if name == "red" else WHITE


def fit_font(path, size, text, tr, maxw=W - 2 * MARGIN):
    while size > 40:
        f = ImageFont.truetype(path, size)
        d = ImageDraw.Draw(Image.new("RGB", (4, 4)))
        w = sum(d.textlength(c, font=f) + tr for c in text) - tr
        if w <= maxw:
            return f
        size -= 6
    return ImageFont.truetype(path, size)


def spaced(d, xy, text, fnt, fill, tr=0, cx=None):
    ws = [d.textlength(c, font=fnt) + tr for c in text]
    tot = sum(ws) - (tr if text else 0)
    x, y = xy
    if cx is not None:
        x = cx - tot / 2
    for c, w in zip(text, ws):
        d.text((x, y), c, font=fnt, fill=fill)
        x += w
    return tot


def lh(f):
    a, dd = f.getmetrics()
    return a + dd


# ---------------------------------------------------------------------------
# renderer de línia: capa TRANSPARENT amb el text al terç superior (zona segura
# IG — mai al 22% inferior ni pegat al marge dret, regla sistema-visual-cbgb).
# ---------------------------------------------------------------------------

def render_line(idx, block):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    lines = block["lines"]()
    size = block.get("size", 104)
    fnt = min((fit_font(ANTON, size, l.upper(), 3) for l in lines), key=lambda f: f.size)
    lhh = int(fnt.size * 1.05)
    blk_h = lhh * len(lines)
    y0 = int(H * 0.20)  # terç superior, zona segura
    # barra d'accent vermella a sobre del bloc
    d.rectangle([MARGIN, y0 - 34, MARGIN + 120, y0 - 22], fill=RED)
    y = y0
    for i, l in enumerate(lines):
        c = col(block.get("color", "white"))
        # ombra lleu per llegibilitat sobre qualsevol il·lustració
        spaced(d, (2, y + 2), l.upper(), fnt, (0, 0, 0, 160), tr=2, cx=W // 2 + 2)
        spaced(d, (0, y), l.upper(), fnt, c, tr=2, cx=W // 2)
        y += lhh
    im.save(f"{OUT}/line_{idx:02d}.png")
    return dict(idx=idx, t0=block["t0"], t1=block["t1"])


def render_closing():
    bg = Image.new("RGB", (W, H), DARK)
    d = ImageDraw.Draw(bg)
    c = CREST.copy()
    ch = 460
    r = ch / c.height
    c = c.resize((int(c.width * r), ch), Image.LANCZOS)
    bg.paste(c, (W // 2 - c.width // 2, 300), c)
    d.rectangle([W // 2 - 260, 300 + ch + 46, W // 2 + 260, 300 + ch + 58], fill=RED)
    mf = font(ANTON, 100)
    spaced(d, (0, 300 + ch + 95), CLOSING["program"], mf, WHITE, tr=3, cx=W // 2)
    spaced(d, (0, 300 + ch + 95 + int(100 * 1.05) + 20), CLOSING["claim"](), font(INTER, 50), WHITE, tr=8, cx=W // 2)
    bg.save(f"{OUT}/closing.png")


if __name__ == "__main__":
    manifest = [render_line(i, b) for i, b in enumerate(GUIO)]
    render_closing()
    meta = dict(lang=LANG, duration_total=DURATION_TOTAL,
                closing_duration=CLOSING_DURATION, lines=manifest)
    with open(f"{OUT}/manifest.json", "w") as f:
        json.dump(meta, f, indent=2)
    print(f"[{LANG}] {len(manifest)} línies + closing.png generats a {OUT}/")
