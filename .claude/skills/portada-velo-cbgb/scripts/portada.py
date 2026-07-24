#!/usr/bin/env python3
"""portada.py — genera la portada 9:16 d'un reel CBGB amb l'estil VALIDAT
(les portades reals del club). Capes:
  foto + vel Roig Barna + línia vermella al voltant + escut dalt a la dreta
  + etiqueta-ganxo dalt a l'esquerra (+ xip CAP.) + antetítol + títol Bebas
  gran alineat a l'ESQUERRA + accent (caixa vermella o barra vertical) + firma.

Ús:
  python3 portada.py --foto jugadora.jpg \
      --etiqueta "L'EFECTE CLARK." --cap "CAP. 01" \
      --antetitol "SÈRIE · BÀSQUET FEMENÍ" \
      --titol "QUÈ ESTÀ|PASSANT AL|BÀSQUET|FEMENÍ?" \
      --caixa "AQUÍ, TAMBÉ." [--barra]   # --barra = accent de barra en lloc de caixa
      [--sub "CB GRUP BARNA · EL CLOT"] [--out portada.png]

Tokens oficials (Manual d'Identitat Visual v1.1): Roig Barna #E31E24 ·
Negre #0A0A0C · Blanc #FFFFFF · Bebas Neue + Montserrat.
"""
import argparse
import os

from PIL import Image, ImageDraw, ImageEnhance, ImageFile, ImageFont

ImageFile.LOAD_TRUNCATED_IMAGES = True

W, H = 1080, 1920
RED = (227, 30, 36)        # #E31E24 Roig Barna
DARK = (10, 10, 12)        # #0A0A0C
WHITE = (255, 255, 255)
GREY = (185, 187, 190)
MARGIN = 80
INSET = 44                 # línia vermella al voltant
LINE_W = 6
LOGO_H = 150               # escut a dalt a la dreta
GRID_TOP, GRID_BOT = 285, 1635   # retall de graella (format post 4:5)

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "..", "assets")
BEBAS = os.path.join(ASSETS, "BebasNeue.ttf")
MONT = os.path.join(ASSETS, "Montserrat.ttf")
CREST = os.path.join(ASSETS, "escut_transp.png")


def font(path, px):
    return ImageFont.truetype(path, px)


def fill_crop(path, vbias=0.30):
    im = Image.open(path).convert("RGB")
    iw, ih = im.size
    s = max(W / iw, H / ih)
    im = im.resize((int(iw * s), int(ih * s)), Image.LANCZOS)
    x = (im.width - W) // 2
    y = int((im.height - H) * vbias)
    return im.crop((max(0, x), max(0, y), max(0, x) + W, max(0, y) + H))


def track(d, xy, text, fnt, fill, tr=0):
    x, y = xy
    for c in text:
        d.text((x, y), c, font=fnt, fill=fill)
        x += d.textlength(c, font=fnt) + tr
    return x - xy[0]


def build(foto, titol, etiqueta=None, cap=None, antetitol=None, caixa=None,
          barra=False, sub="CB GRUP BARNA · EL CLOT", out="portada.png",
          velo=0.42, vbias=0.30, dark=0.16, logo_y=88):
    # 1-3. FOTO + vel roig + capa fosca + vinyeta inferior
    bg = fill_crop(foto, vbias)
    bg = ImageEnhance.Color(bg).enhance(0.8)
    bg = ImageEnhance.Contrast(bg).enhance(1.06)
    bg = Image.blend(bg, Image.new("RGB", (W, H), RED), velo)
    bg = Image.blend(bg, Image.new("RGB", (W, H), DARK), dark)
    grad = Image.new("L", (1, H), 0)
    for yy in range(H):
        t = yy / H
        grad.putpixel((0, yy), int(max(0.0, (t - 0.5) / 0.5) ** 1.5 * 120))
    bg = Image.composite(Image.new("RGB", (W, H), DARK), bg, grad.resize((W, H)))

    bg = bg.convert("RGBA")
    d = ImageDraw.Draw(bg)

    # 4. LÍNIA VERMELLA al voltant (marc roig obligatori)
    d.rectangle([INSET, INSET, W - INSET, H - INSET], outline=RED, width=LINE_W)

    # 5. ESCUT dalt a la dreta
    crest = Image.open(CREST).convert("RGBA")
    r = LOGO_H / crest.height
    crest = crest.resize((int(crest.width * r), LOGO_H), Image.LANCZOS)
    bg.alpha_composite(crest, (W - MARGIN - crest.width, logo_y))

    # 6. ETIQUETA-ganxo dalt a l'esquerra (caixa vermella + Bebas)
    if etiqueta:
        ef = font(BEBAS, 66)
        tw = d.textlength(etiqueta, font=ef)
        d.rectangle([MARGIN, 70, MARGIN + tw + 28, 70 + 84], fill=RED)
        d.text((MARGIN + 14, 78), etiqueta, font=ef, fill=WHITE)
    # xip CAP. (caixa negra) sota l'etiqueta
    if cap:
        cf = font(BEBAS, 42)
        tw = d.textlength(cap, font=cf)
        d.rectangle([MARGIN, 200, MARGIN + tw + 24, 252], fill=DARK)
        d.text((MARGIN + 12, 204), cap, font=cf, fill=WHITE)

    # 7. Bloc de títol a la franja central (sobreviu el retall de graella).
    lines = [l.strip().upper() for l in titol.split("|") if l.strip()]
    accent_h = 96 if caixa and not barra else (72 if caixa else 0)
    # mides: títol 150 px; si hi ha moltes línies, encongeix
    size = 150 if len(lines) <= 3 else 120
    lh = int(size * 0.92)
    ov_h = 60 if antetitol else 0
    block = ov_h + lh * len(lines) + (40 + accent_h if caixa else 0)
    top = (GRID_TOP + GRID_BOT) // 2 - block // 2
    top = max(GRID_TOP + 40, top)
    y = top
    if antetitol:
        track(d, (MARGIN, y), antetitol.upper(), font(MONT, 30), GREY, tr=3)
        y += ov_h
    tf = font(BEBAS, size)
    for ln in lines:
        d.text((MARGIN, y), ln, font=tf, fill=WHITE)
        y += lh
    # 8. ACCENT: caixa vermella (paraula clau) o barra vertical + subtítol
    if caixa:
        y += 40
        if barra:
            d.rectangle([MARGIN, y + 4, MARGIN + 12, y + 68], fill=RED)
            d.text((MARGIN + 34, y + 2), caixa.upper(), font=font(BEBAS, 62), fill=WHITE)
        else:
            kf = font(BEBAS, 78)
            tw = d.textlength(caixa.upper(), font=kf)
            d.rectangle([MARGIN, y, MARGIN + tw + 40, y + 96], fill=RED)
            d.text((MARGIN + 20, y + 6), caixa.upper(), font=kf, fill=WHITE)

    # 9. FIRMA fixa a baix a l'esquerra
    if sub:
        track(d, (MARGIN, 1770), sub, font(MONT, 38), WHITE, tr=1)

    bg.convert("RGB").save(out)
    print(f"Portada -> {out}  (estil validat: etiqueta+títol esquerra+accent)")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Portada de reel CBGB (estil validat)")
    p.add_argument("--foto", required=True)
    p.add_argument("--titol", required=True, help="'|' separa línies; alineat a l'esquerra")
    p.add_argument("--etiqueta", default=None, help="ganxo dalt-esquerra (caixa vermella)")
    p.add_argument("--cap", default=None, help="xip de capítol, ex. 'CAP. 01'")
    p.add_argument("--antetitol", default=None, help="línia petita sobre el títol")
    p.add_argument("--caixa", default=None, help="paraula clau (caixa vermella) o subtítol")
    p.add_argument("--barra", action="store_true",
                   help="accent de barra vertical en lloc de caixa vermella")
    p.add_argument("--sub", default="CB GRUP BARNA · EL CLOT")
    p.add_argument("--out", default="portada.png")
    p.add_argument("--velo", type=float, default=0.42)
    p.add_argument("--vbias", type=float, default=0.30)
    p.add_argument("--dark", type=float, default=0.16)
    p.add_argument("--logo-y", type=int, default=88, dest="logo_y")
    a = p.parse_args()
    build(a.foto, a.titol, a.etiqueta, a.cap, a.antetitol, a.caixa, a.barra,
          a.sub, a.out, a.velo, a.vbias, a.dark, a.logo_y)
