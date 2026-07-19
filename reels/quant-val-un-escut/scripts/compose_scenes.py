#!/usr/bin/env python3
"""Genera les 7 escenes del reel 'Quant val un escut?' (mateixa plantilla que la portada)."""
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageChops, ImageFile
import os
ImageFile.LOAD_TRUNCATED_IMAGES = True

W, H = 1080, 1920
BORDER = 34
IW, IH = W - BORDER * 2, H - BORDER * 2

RED = (230, 51, 41)          # #E63329
DARK = (14, 17, 22)          # #0E1116
DARK_SHADOW = (18, 8, 8)
WHITE = (245, 245, 247)

ASSETS = os.path.expanduser("~/.claude/skills/reel-fotos-cbgb/assets")
ANTON = f"{ASSETS}/Anton.ttf"
INTER = f"{ASSETS}/Inter.ttf"
CREST_PATH = f"{ASSETS}/escut_transp.png"
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(f"{HERE}/../../..")   # arrel del repo (reels/quant-val-un-escut/scripts/..)

OUT = os.path.join(HERE, "..", "scenes")
os.makedirs(OUT, exist_ok=True)

def font(p, s): return ImageFont.truetype(p, s)

def fit_font(path, size, text, tr, maxw, minsize=30):
    while size > minsize:
        f = ImageFont.truetype(path, size)
        d = ImageDraw.Draw(Image.new("RGB", (4, 4)))
        w = sum(d.textlength(c, font=f) + tr for c in text) - tr
        if w <= maxw:
            return f
        size -= 4
    return ImageFont.truetype(path, size)

def spaced(d, xy, text, fnt, fill, tr=0, cx=None, shadow=None, sdx=7, sdy=7):
    ws = [d.textlength(c, font=fnt) + tr for c in text]
    tot = sum(ws) - (tr if text else 0)
    x, y = xy
    if cx is not None:
        x = cx - tot / 2
    if shadow is not None:
        xs = x
        for c, w in zip(text, ws):
            d.text((xs + sdx, y + sdy), c, font=fnt, fill=shadow)
            xs += w
    for c, w in zip(text, ws):
        d.text((x, y), c, font=fnt, fill=fill)
        x += w
    return tot

def lh(f):
    a, dd = f.getmetrics()
    return a + dd

def fill_crop(path, vbias=0.5, zoom=1.0, size=(IW, IH)):
    w, h = size
    im = Image.open(path).convert("RGB")
    iw, ih = im.size
    s = max(w / iw, h / ih) * zoom
    nw, nh = int(iw * s), int(ih * s)
    im = im.resize((nw, nh), Image.LANCZOS)
    x = (nw - w) // 2
    y = int((nh - h) * vbias)
    x = max(0, min(x, nw - w))
    y = max(0, min(y, nh - h))
    return im.crop((x, y, x + w, y + h))

def brand_grade(im, w, h, dark_bottom=0.62):
    im = ImageEnhance.Color(im).enhance(0.80)
    im = ImageEnhance.Contrast(im).enhance(1.08)
    im = ImageEnhance.Brightness(im).enhance(1.02)
    tint = Image.new("RGB", (w, h), (196, 52, 40))
    mult = ImageChops.multiply(im, tint)
    base = Image.blend(im, mult, 0.40)
    g = Image.new("L", (1, h), 0)
    for yy in range(h):
        t = yy / h
        b = max(0, (t - dark_bottom) / (1 - dark_bottom)) ** 1.5 * 235
        g.putpixel((0, yy), int(min(255, b)))
    g = g.resize((w, h))
    dark_layer = Image.new("RGB", (w, h), (12, 6, 6))
    return Image.composite(dark_layer, base, g).convert("RGB")

def new_art(photo_path=None, vbias=0.3, zoom=1.1, dark_bottom=0.62):
    if photo_path:
        photo = fill_crop(photo_path, vbias=vbias, zoom=zoom)
        photo = brand_grade(photo, IW, IH, dark_bottom)
        art = photo.convert("RGBA")
    else:
        art = Image.new("RGBA", (IW, IH), DARK + (255,))
    return art

def crest_topright(art, size=140, margin=34):
    crest = Image.open(CREST_PATH).convert("RGBA")
    r = size / crest.height
    crest = crest.resize((int(crest.width * r), size), Image.LANCZOS)
    pos = (IW - crest.width - margin, 30)
    alpha_shadow = crest.split()[3].point(lambda a: int(a * 0.55))
    shadow_layer = Image.new("RGBA", crest.size, DARK_SHADOW + (0,))
    shadow_layer.putalpha(alpha_shadow)
    art.alpha_composite(shadow_layer, (pos[0] + 6, pos[1] + 8))
    art.alpha_composite(crest, pos)

def save(art, name):
    canvas = Image.new("RGB", (W, H), RED)
    canvas.paste(art.convert("RGB"), (BORDER, BORDER))
    canvas.save(f"{OUT}/{name}.png", quality=95)
    print("scene ->", name)

# ============ ESCENA 0 — HOOK (portada) ============
art = new_art(f"{REPO}/premidonaesport/assets/img/p05.webp", vbias=0.16, zoom=1.12, dark_bottom=0.62)
d = ImageDraw.Draw(art)

banner_h, banner_w = 128, 640
d.rectangle([-40, -30, banner_w, banner_h], fill=RED + (255,))
eb = fit_font(ANTON, 76, "NO ES VEN.", 2, banner_w - 40)
spaced(d, (36, banner_h - lh(eb) + 6), "NO ES VEN.", eb, WHITE, tr=2, shadow=DARK_SHADOW, sdx=5, sdy=5)

chip_y = banner_h + 40
tag = "PREGUNTA 01"
tag_f = font(ANTON, 44)
tag_w = spaced(ImageDraw.Draw(Image.new("RGB", (4, 4))), (0, 0), tag, tag_f, WHITE, tr=3)
pad = 20
d.rectangle([36, chip_y, 36 + tag_w + pad * 2, chip_y + lh(tag_f) + pad], fill=RED + (255,))
spaced(d, (36 + pad, chip_y + pad // 2), tag, tag_f, WHITE, tr=3)

small_y = int(IH * 0.435)
small_f = font(INTER, 32)
spaced(d, (36, small_y), "QUANT VAL UN ESCUT", small_f, WHITE, tr=6, shadow=DARK_SHADOW, sdx=3, sdy=3)

lines = ["QUANT VAL", "UN ESCUT?"]
head_f = min((fit_font(ANTON, 196, l, 2, IW - 72) for l in lines), key=lambda f: f.size)
line_h = int(head_f.size * 1.10)
y = small_y + 92
for l in lines:
    spaced(d, (36, y), l, head_f, WHITE, tr=2, shadow=DARK_SHADOW, sdx=8, sdy=8)
    y += line_h

bar_y = y + 46
d.rectangle([36, bar_y, 48, bar_y + 54], fill=RED + (255,))
sub_f = font(ANTON, 46)
spaced(d, (66, bar_y), "LA RESPOSTA, DINS.", sub_f, WHITE, tr=2, shadow=DARK_SHADOW, sdx=4, sdy=4)

cap_f = font(INTER, 32)
d.text((36, IH - 90), "CB GRUP BARNA · EL CLOT", font=cap_f, fill=WHITE + (235,))

crest_topright(art)
save(art, "s0_hook")

# ============ helper: escena d'estadística ============
def stat_scene(name, photo, vbias, big, small, tag_txt, zoom=1.15):
    art = new_art(photo, vbias=vbias, zoom=zoom, dark_bottom=0.30)
    d = ImageDraw.Draw(art)
    crest_topright(art)
    # tag petit a dalt esquerra
    tag_f = font(ANTON, 40)
    tw = spaced(ImageDraw.Draw(Image.new("RGB", (4, 4))), (0, 0), tag_txt, tag_f, WHITE, tr=3)
    pad = 18
    d.rectangle([0, 40, tw + pad * 2, 40 + lh(tag_f) + pad], fill=RED + (255,))
    spaced(d, (pad, 40 + pad // 2), tag_txt, tag_f, WHITE, tr=3)
    # numero gegant centrat
    big_f = fit_font(ANTON, 420 if len(big) <= 3 else 320, big, 4, IW - 80)
    by = IH // 2 - lh(big_f) // 2 - 40
    spaced(d, (0, by), big, big_f, WHITE, tr=4, cx=IW // 2, shadow=DARK_SHADOW, sdx=10, sdy=10)
    # etiqueta petita sota, amb barra vermella
    small_f = fit_font(ANTON, 84, small, 6, IW - 120)
    sw = spaced(ImageDraw.Draw(Image.new("RGB", (4, 4))), (0, 0), small, small_f, WHITE, tr=6)
    yb = by + lh(big_f) + 30
    d.rectangle([IW // 2 - sw / 2 - 34, yb - 4, IW // 2 + sw / 2 + 34, yb + lh(small_f) + 6], fill=RED + (255,))
    spaced(d, (0, yb), small, small_f, WHITE, tr=6, cx=IW // 2)
    save(art, name)

# ============ ESCENA 1 — 61 ANYS ============
stat_scene("s1_stat61",
           f"{REPO}/fotos/uploads/fotos-equips-temporada-25-26-records/1781613116837-nc3id.jpg",
           vbias=0.10, big="61", small="ANYS AL BARRI", tag_txt="DES DE 1965")

# ============ ESCENA 2 — 34 EQUIPS ============
stat_scene("s2_stat34",
           f"{REPO}/fotos/uploads/fotos-equips-temporada-25-26-records/1781613069472-40zhy.jpg",
           vbias=0.08, big="34", small="EQUIPS", tag_txt="TOTES LES CATEGORIES")

# ============ ESCENA 3 — 450+ FAMÍLIES ============
stat_scene("s3_stat450",
           f"{REPO}/premidonaesport/assets/img/a09.webp",
           vbias=0.20, big="450+", small="FAMÍLIES", tag_txt="CADA DISSABTE", zoom=1.05)

# ============ ESCENA 4 — BUILD (linia emotiva) ============
art = new_art(None)
d = ImageDraw.Draw(art)
d.rectangle([0, 0, IW, IH], fill=DARK + (255,))
lines4 = ["CAP NÚMERO", "HO DIU TOT."]
f4 = min((fit_font(ANTON, 150, l, 2, IW - 80) for l in lines4), key=lambda f: f.size)
lh4 = int(f4.size * 1.05)
y0 = IH // 2 - lh4 * len(lines4) // 2 - 40
d.rectangle([54, y0 - 40, 174, y0 - 28], fill=RED + (255,))
y = y0
for l in lines4:
    spaced(d, (36, y), l, f4, WHITE, tr=2, cx=IW // 2)
    y += lh4
f4b = font(ANTON, 60)
spaced(d, (0, y + 26), "PERÒ TOTS HI SOM.", f4b, RED, tr=2, cx=IW // 2)
crest_topright(art)
save(art, "s4_build")

# ============ ESCENA 5 — DROP (escut heroi + claim) ============
art = new_art(None)
d = ImageDraw.Draw(art)
d.rectangle([0, 0, IW, IH], fill=DARK + (255,))
crest = Image.open(CREST_PATH).convert("RGBA")
chh = 520
r = chh / crest.height
crest_big = crest.resize((int(crest.width * r), chh), Image.LANCZOS)
art.alpha_composite(crest_big, (IW // 2 - crest_big.width // 2, 210))
d.rectangle([IW // 2 - 260, 210 + chh + 46, IW // 2 + 260, 210 + chh + 58], fill=RED + (255,))
mf = font(ANTON, 96)
spaced(d, (0, 210 + chh + 90), "AIXÒ VAL", mf, WHITE, tr=4, cx=IW // 2)
spaced(d, (0, 210 + chh + 90 + int(96 * 1.05)), "UN ESCUT.", mf, RED, tr=4, cx=IW // 2)
spaced(d, (0, 210 + chh + 90 + int(96 * 1.05) * 2 + 34), "CB GRUP BARNA · DES DE 1965", font(INTER, 44), WHITE, tr=6, cx=IW // 2)
save(art, "s5_drop")

# ============ ESCENA 6 — CTA ============
art = new_art(None)
d = ImageDraw.Draw(art)
d.rectangle([0, 0, IW, IH], fill=RED + (255,))
crest2 = Image.open(CREST_PATH).convert("RGBA")
chh2 = 260
r2 = chh2 / crest2.height
crest2 = crest2.resize((int(crest2.width * r2), chh2), Image.LANCZOS)
art.alpha_composite(crest2, (IW // 2 - crest2.width // 2, 260))
f6 = font(ANTON, 110)
spaced(d, (0, 260 + chh2 + 70), "SEGUEIX LA", f6, WHITE, tr=4, cx=IW // 2)
spaced(d, (0, 260 + chh2 + 70 + int(110 * 1.02)), "HISTÒRIA.", f6, DARK, tr=4, cx=IW // 2)
spaced(d, (0, 260 + chh2 + 70 + int(110 * 1.02) * 2 + 40), "@cbgrupbarna", font(INTER, 56), WHITE, tr=4, cx=IW // 2)
save(art, "s6_cta")

print("Totes les escenes generades a", OUT)
