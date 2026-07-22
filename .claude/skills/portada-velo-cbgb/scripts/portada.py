#!/usr/bin/env python3
"""portada.py — genera la portada 9:16 d'un reel CBGB amb l'estil validat:
foto + vel vermell + línia al voltant + escut dalt a la dreta + títol Anton.

Ús:
  python3 portada.py --foto jugadora.jpg --titulo "FITXATGE|26/27" \
      [--sub "SEGUEIX EL BARNA"] [--out portada.png]

Tokens de marca: sistema-visual-cbgb (#0E1116 / #E63329 / #F5F5F7 / Anton / Inter).
"""
import argparse
import os

from PIL import Image, ImageDraw, ImageEnhance, ImageFile, ImageFont

ImageFile.LOAD_TRUNCATED_IMAGES = True

W, H = 1080, 1920
DARK = (14, 17, 22)        # #0E1116
RED = (230, 51, 41)        # #E63329
WHITE = (245, 245, 247)    # #F5F5F7
MARGIN = 80                # marge de marca
LINE_INSET = 44            # la línia al voltant, a 44 px del borde
LINE_W = 6
LOGO_H = 150               # alçada de l'escut, sempre igual

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "..", "assets")
ANTON = os.path.join(ASSETS, "Anton.ttf")
INTER = os.path.join(ASSETS, "Inter.ttf")
CREST = os.path.join(ASSETS, "escut_transp.png")


def fill_crop(path, vbias=0.30):
    """Omple 1080x1920 a sang; vbias 0=dalt 1=baix decideix quin tros de foto es veu."""
    im = Image.open(path).convert("RGB")
    iw, ih = im.size
    s = max(W / iw, H / ih)
    nw, nh = int(iw * s), int(ih * s)
    im = im.resize((nw, nh), Image.LANCZOS)
    x = (nw - W) // 2
    y = int((nh - H) * vbias)
    x = max(0, min(x, nw - W))
    y = max(0, min(y, nh - H))
    return im.crop((x, y, x + W, y + H))


def spaced(draw, y, text, fnt, fill, tracking=4):
    """Text centrat amb tracking manual (Anton queda millor amb una mica d'aire)."""
    widths = [draw.textlength(c, font=fnt) + tracking for c in text]
    total = sum(widths) - (tracking if text else 0)
    x = W / 2 - total / 2
    for c, w in zip(text, widths):
        draw.text((x, y), c, font=fnt, fill=fill)
        x += w
    return total


def fit_font(path, size, text, tracking=4, maxw=W - 2 * MARGIN):
    d = ImageDraw.Draw(Image.new("RGB", (4, 4)))
    while size > 40:
        f = ImageFont.truetype(path, size)
        w = sum(d.textlength(c, font=f) + tracking for c in text) - tracking
        if w <= maxw:
            return f
        size -= 6
    return ImageFont.truetype(path, size)


def line_height(f):
    a, d = f.getmetrics()
    return a + d


def build(foto, titulo, sub=None, out="portada.png", velo=0.38, vbias=0.30,
          dark=0.15, logo_y=88, sinvelo=False, sinlinia=False):
    # 1. FOTO a sang, lleu desaturació i contrast perquè el vel unifiqui
    bg = fill_crop(foto, vbias)
    bg = ImageEnhance.Color(bg).enhance(0.85)
    bg = ImageEnhance.Contrast(bg).enhance(1.05)

    # 2. VEL VERMELL — la firma de la sèrie
    if not sinvelo:
        bg = Image.blend(bg, Image.new("RGB", (W, H), RED), velo)

    # 3. Capa fosca global + degradat inferior perquè el text blanc llegeixi
    bg = Image.blend(bg, Image.new("RGB", (W, H), DARK), dark)
    grad = Image.new("L", (1, H), 0)
    for yy in range(H):
        t = yy / H
        grad.putpixel((0, yy), int(max(0.0, (t - 0.55) / 0.45) ** 1.5 * 140))
    grad = grad.resize((W, H))
    bg = Image.composite(Image.new("RGB", (W, H), DARK), bg, grad)

    d = ImageDraw.Draw(bg)

    # 4. LÍNIA AL VOLTANT — marc blanc fi, res la trepitja
    if not sinlinia:
        d.rectangle([LINE_INSET, LINE_INSET, W - LINE_INSET, H - LINE_INSET],
                    outline=WHITE, width=LINE_W)

    # 5. ESCUT dalt a la dreta, mida i posició fixes (és un segell)
    crest = Image.open(CREST).convert("RGBA")
    r = LOGO_H / crest.height
    crest = crest.resize((int(crest.width * r), LOGO_H), Image.LANCZOS)
    bg = bg.convert("RGBA")
    bg.alpha_composite(crest, (W - MARGIN - crest.width, logo_y))
    bg = bg.convert("RGB")
    d = ImageDraw.Draw(bg)

    # 6. TÍTOL Anton al centre vertical (zona que sobreviu a tots els retalls)
    lines = [l.strip().upper() for l in titulo.split("|") if l.strip()][:2]
    fnt = min((fit_font(ANTON, 170, l) for l in lines), key=lambda f: f.size)
    lh = int(line_height(fnt) * 0.88)
    block = lh * len(lines) + (70 if sub else 0)
    y = (H - block) // 2
    for l in lines:
        spaced(d, y, l, fnt, WHITE)
        y += lh
    # barra curta blanca de remat
    d.rectangle([W / 2 - 70, y + 14, W / 2 + 70, y + 26], fill=WHITE)
    if sub:
        sf = ImageFont.truetype(INTER, 46)
        spaced(d, y + 58, sub.upper(), sf, WHITE, tracking=10)

    bg.save(out)
    print(f"Portada -> {out}  (velo {int(velo*100)}%, logo dalt-dreta y={logo_y})")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Portada de reel CBGB (estil validat)")
    p.add_argument("--foto", required=True)
    p.add_argument("--titulo", required=True, help="≤5 paraules; '|' separa 2 línies")
    p.add_argument("--sub", default=None)
    p.add_argument("--out", default="portada.png")
    p.add_argument("--velo", type=float, default=0.38)
    p.add_argument("--vbias", type=float, default=0.30)
    p.add_argument("--dark", type=float, default=0.15)
    p.add_argument("--logo-y", type=int, default=88, dest="logo_y",
                   help="260 si la portada sera PIN i l'escut ha de sobreviure la graella")
    p.add_argument("--sinvelo", action="store_true", help="nomes proves A/B")
    p.add_argument("--sinlinia", action="store_true", help="nomes proves A/B")
    a = p.parse_args()
    build(a.foto, a.titulo, a.sub, a.out, a.velo, a.vbias, a.dark, a.logo_y,
          a.sinvelo, a.sinlinia)
