#!/usr/bin/env python3
"""
Portada oficial de reels CBGB — plantilla "capítol" (marc vermell + duotò).

Genera una portada VERTICAL 1080x1920 amb:
  - fons: foto/frame del reel en DUOTÒ vermell de marca
  - marc vermell perimetral
  - ticker gegant tallat a l'esquerra (final de frase, efecte marquesina)
  - badge de capítol ("CAP. 01") per a sèries
  - kicker petit + TITULAR Anton apilat en blanc amb ombra càlida
  - subratllat de cop ("punch") amb barra vermella i cursiva
  - peu "CB GRUP BARNA · EL CLOT" i escut a dalt a la dreta

Ús:
  python3 portada.py --bg foto.jpg \
      --ticker "NO CABEN AIXÍ." \
      --cap "CAP. 01" \
      --kicker "LA FEINA QUE NO ES VEU" \
      --title "LA FEINA|QUE NO|ES VEU" \
      --punch "EL RESULTAT, SÍ." \
      --out portada.jpg

  # des d'un vídeo (necessita ffmpeg):
  python3 portada.py --video reel.mp4 --t 12.5 --title "..." ...

El titular s'auto-ajusta d'amplada. Línies separades amb "|".
"""

import argparse
import os
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "..", "assets")

W, H = 1080, 1920
FRAME = 36                     # gruix del marc vermell perimetral
MARGE = 68                     # marge esquerre del bloc de text

# Paleta (duotò + marca) — vermell CBGB de la plantilla
VERMELL = (240, 63, 42)        # marc, ticker, badge, barra punch
SALMO = (248, 178, 160)        # text del ticker sobre vermell
BLANC = (255, 255, 255)
OMBRA = (74, 10, 5)            # ombra càlida del titular
DUO_FOSC = (70, 10, 5)         # ombres del duotò
DUO_MIG = (226, 66, 44)        # migtons del duotò
DUO_CLAR = (255, 196, 178)     # llums del duotò


def font(name, size):
    return ImageFont.truetype(os.path.join(ASSETS, name), size)


def text_size(fnt, txt, tracking=0):
    d = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    w = d.textlength(txt, font=fnt) + tracking * max(0, len(txt) - 1)
    asc, desc = fnt.getmetrics()
    return int(w), asc + desc


def draw_tracked(draw, xy, txt, fnt, fill, tracking=0):
    """Text amb tracking manual (Pillow no en té de natiu)."""
    x, y = xy
    for ch in txt:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + tracking


def grab_frame(video, t):
    """Extreu un fotograma del vídeo amb ffmpeg."""
    out = tempfile.NamedTemporaryFile(suffix=".png", delete=False).name
    cmd = ["ffmpeg", "-y", "-ss", str(t), "-i", video,
           "-frames:v", "1", "-q:v", "2", out]
    try:
        subprocess.run(cmd, check=True, capture_output=True)
    except (FileNotFoundError, subprocess.CalledProcessError) as e:
        sys.exit(f"ERROR: no s'ha pogut extreure el frame (cal ffmpeg): {e}")
    return out


def cover_crop(im, w, h):
    """Retalla la imatge per cobrir exactament w×h (com object-fit: cover)."""
    ratio = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * ratio), round(im.height * ratio)),
                   Image.LANCZOS)
    left = (im.width - w) // 2
    top = (im.height - h) // 2
    return im.crop((left, top, left + w, top + h))


def duotone(im):
    """Duotò vermell de marca: unifica qualsevol foto amb el sistema CBGB."""
    g = ImageOps.grayscale(im)
    g = ImageOps.autocontrast(g, cutoff=1)
    g = ImageEnhance.Contrast(g).enhance(1.1)
    return ImageOps.colorize(g, black=DUO_FOSC, white=DUO_CLAR,
                             mid=DUO_MIG).convert("RGB")


def fit_title_font(lines, max_w, base=186, floor=110):
    """Mida única per a totes les línies del titular, la més gran que hi cap."""
    size = base
    while size > floor:
        f = font("Anton.ttf", size)
        if all(text_size(f, ln)[0] <= max_w for ln in lines):
            return f, size
        size -= 4
    return font("Anton.ttf", floor), floor


def build(args):
    # ── fons ──────────────────────────────────────────────────────────
    src = args.bg or grab_frame(args.video, args.t)
    bg = Image.open(src).convert("RGB")
    canvas = duotone(cover_crop(bg, W, H))
    d = ImageDraw.Draw(canvas)

    # ── marc vermell perimetral ──────────────────────────────────────
    for i in range(FRAME):
        d.rectangle([i, i, W - 1 - i, H - 1 - i], outline=VERMELL)

    # ── ticker gegant tallat a l'esquerra ────────────────────────────
    # Final de frase que entra tallat des de fora del llenç (marquesina).
    if args.ticker:
        f_tick = font("Anton.ttf", 168)
        tw, th = text_size(f_tick, args.ticker)
        end_x = 590            # on acaba el text (deixa aire a l'escut)
        pad = 34
        block_h = th + 2 * pad - 26
        d.rectangle([0, FRAME, end_x + pad + 10, FRAME + block_h], fill=VERMELL)
        d.text((end_x - tw, FRAME + pad - 18), args.ticker,
               font=f_tick, fill=SALMO)

    # ── escut a dalt a la dreta ──────────────────────────────────────
    escut = Image.open(os.path.join(ASSETS, "escut_transp.png")).convert("RGBA")
    ew = 168
    escut = escut.resize((ew, round(escut.height * ew / escut.width)),
                         Image.LANCZOS)
    canvas.paste(escut, (W - FRAME - ew - 26, FRAME + 22), escut)

    # ── badge de capítol (sèrie) ─────────────────────────────────────
    y = 268
    if args.cap:
        f_cap = font("Anton.ttf", 56)
        cw, chh = text_size(f_cap, args.cap)
        pad_x, pad_y = 28, 12
        d.rectangle([MARGE, y, MARGE + cw + 2 * pad_x, y + chh + 2 * pad_y],
                    fill=VERMELL)
        d.text((MARGE + pad_x, y + pad_y - 4), args.cap,
               font=f_cap, fill=BLANC)

    # ── bloc central: kicker + titular + punch ───────────────────────
    lines = [ln.strip() for ln in args.title.split("|") if ln.strip()]
    max_w = W - MARGE - FRAME - 60
    f_tit, size = fit_title_font(lines, max_w)
    leading = round(size * 1.06)  # aire per a accents (À, Í) entre línies

    # Alçada total del bloc (kicker + titular + punch) per recol·locar-lo:
    # com més gran el bloc, més amunt comença, i el peu sempre respira.
    f_p = font("Anton.ttf", 92)
    ph = text_size(f_p, args.punch)[1] if args.punch else 0
    block_h = (96 if args.kicker else 0) + leading * len(lines)
    if args.punch:
        block_h += round(size * 0.30) + ph + 30
    y = max(470, min(600, 1400 - block_h - 70))
    if args.kicker:
        f_kick = font("Inter.ttf", 42)
        draw_tracked(d, (MARGE, y), args.kicker.upper(), f_kick, BLANC,
                     tracking=5)
        y += 96

    # Titular apilat amb ombra càlida (llegible a 300px)
    for ln in lines:
        d.text((MARGE + 7, y + 11), ln, font=f_tit, fill=OMBRA)
        d.text((MARGE, y), ln, font=f_tit, fill=BLANC)
        y += leading
    y += round(size * 0.30)  # gap perquè el punch no trepitgi el titular

    # Punch: barra vermella + text amb cursiva falsa (shear)
    if args.punch:
        pw = text_size(f_p, args.punch)[0]
        layer = Image.new("RGBA", (pw + 60, ph + 20), (0, 0, 0, 0))
        dl = ImageDraw.Draw(layer)
        dl.text((30, 0), args.punch, font=f_p, fill=BLANC)
        shear = 0.16
        layer = layer.transform(
            (layer.width + int(shear * layer.height), layer.height),
            Image.AFFINE, (1, shear, -shear * layer.height, 0, 1, 0),
            resample=Image.BICUBIC)
        bar_h = round(ph * 0.72)
        d.rectangle([MARGE, y + 14, MARGE + 14, y + 14 + bar_h], fill=VERMELL)
        canvas.paste(layer, (MARGE + 26, y - 6), layer)
        y += ph + 30

    # ── peu (dinàmic: sota el bloc, mai dins la franja que menja la UI) ──
    f_foot = font("Inter.ttf", 40)
    foot = args.footer.upper()
    d = ImageDraw.Draw(canvas)
    y_foot = max(1432, y + 40)  # sota el bloc, sobre la franja de la UI
    draw_tracked(d, (MARGE, y_foot), foot, f_foot, BLANC, tracking=4)

    canvas.save(args.out, quality=92)
    print(f"OK → {args.out}  ({W}x{H})")


def main():
    p = argparse.ArgumentParser(description="Portada de reel CBGB (plantilla capítol)")
    src = p.add_mutually_exclusive_group(required=True)
    src.add_argument("--bg", help="foto o frame de fons (jpg/png)")
    src.add_argument("--video", help="vídeo del reel (extreu frame amb ffmpeg)")
    p.add_argument("--t", type=float, default=1.0,
                   help="segon del vídeo per al frame (amb --video)")
    p.add_argument("--ticker", default="",
                   help="final de frase del ticker superior (surt tallat), ex: 'CABEN AIXÍ.'")
    p.add_argument("--cap", default="", help="badge de capítol, ex: 'CAP. 01'")
    p.add_argument("--kicker", default="", help="línia petita sobre el titular")
    p.add_argument("--title", required=True,
                   help="titular, línies separades amb '|' (3-5 paraules màx)")
    p.add_argument("--punch", default="", help="subratllat de cop, ex: 'EL RESULTAT, SÍ.'")
    p.add_argument("--footer", default="CB GRUP BARNA · EL CLOT")
    p.add_argument("--out", default="portada.jpg")
    build(p.parse_args())


if __name__ == "__main__":
    main()
