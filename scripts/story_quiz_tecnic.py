#!/usr/bin/env python3
"""Generador d'Instagram Stories per a la serie 'Quiz Tecnic' del CB Grup Barna.

Regles fixes de disseny (no negociables, valen per a totes les peces d'aquesta serie):
  1. El logo del club sempre surt sencer a la dreta (badge fix, mai tapat per foto ni text).
  2. La foto real mai es retalla de manera que talli la cara dels jugadors/es: s'ajusta
     sencera dins la zona de foto (contain), amb un fons difuminat de la mateixa imatge
     per omplir els marges en comptes de fer un "cover crop".

Dos modes:
  --mode pregunta  -> nomes la situacio i les 3 opcions neutres (per fer votar a l'story
                       amb l'enquesta nativa d'Instagram). No revela la correcta.
  --mode resposta  -> la mateixa peca amb la opcio correcta marcada + el "Per que".

Us:
  python3 story_quiz_tecnic.py \
      --foto fotos/uploads/xxx/foto.jpeg \
      --situacio "Vas a tirar a cistella" \
      --opcio "Miro els peus" \
      --opcio "Miro la cistella" \
      --opcio "Miro el defensor" \
      --correcta 1 \
      --perque "La mirada fixa a la cistella dona precisio i equilibri al tir." \
      --mode pregunta \
      --out out/quiz_pregunta_01.png
"""
import argparse
import os
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

W, H = 1080, 1920

# Paleta del club
RED = (200, 30, 40)
DARK = (20, 20, 22)
INK = (28, 28, 30)
WHITE = (255, 255, 255)
GRAY = (150, 150, 155)
GRAY_BG = (44, 44, 48)
GREEN = (46, 160, 90)

FONT_DIR = "/usr/share/fonts/truetype/liberation"
F_BLACK = os.path.join(FONT_DIR, "LiberationSans-Bold.ttf")
F_REG = os.path.join(FONT_DIR, "LiberationSans-Regular.ttf")

LOGO_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logo.png")

# Zona de foto (contain, mai cover) i badge del logo, sempre a la dreta.
PHOTO_BOX = (0, 260, W, 1120)  # (left, top, right, bottom)
LOGO_BADGE_SIZE = 132
LOGO_MARGIN = 40


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap_text(draw, text, f, max_width):
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=f) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_multiline(draw, xy, lines, f, fill, line_gap=10, align="left", box_width=None):
    x, y = xy
    for line in lines:
        lw = draw.textlength(line, font=f)
        lx = x
        if align == "center" and box_width is not None:
            lx = x + (box_width - lw) / 2
        draw.text((lx, y), line, font=f, fill=fill)
        y += f.size + line_gap
    return y


def paste_photo_contain(canvas, photo_path, box):
    """Encaixa la foto sencera dins `box` sense retallar-la (contain),
    amb un fons difuminat de la mateixa foto per omplir els marges.
    Aixi mai es talla el cap ni la cara de cap jugador/a."""
    left, top, right, bottom = box
    bw, bh = right - left, bottom - top

    img = ImageOps.exif_transpose(Image.open(photo_path)).convert("RGB")

    # Fons: cover-crop molt difuminat (nomes decoratiu, no informatiu -> no importa que es talli)
    bg = ImageOps.fit(img, (bw, bh), method=Image.LANCZOS, centering=(0.5, 0.35))
    bg = bg.filter(ImageFilter.GaussianBlur(28))
    enhancer_overlay = Image.new("RGB", (bw, bh), DARK)
    bg = Image.blend(bg, enhancer_overlay, 0.35)
    canvas.paste(bg, (left, top))

    # Primer pla: foto sencera, sense retallar (contain)
    scale = min(bw / img.width, bh / img.height)
    fw, fh = int(img.width * scale), int(img.height * scale)
    fg = img.resize((fw, fh), Image.LANCZOS)
    fx = left + (bw - fw) // 2
    fy = top + (bh - fh) // 2
    canvas.paste(fg, (fx, fy))

    # Vores subtils perque no es vegi com un "sticker" flotant
    draw = ImageDraw.Draw(canvas)
    draw.rectangle([left, top, right, bottom], outline=(0, 0, 0, 0), width=0)
    return canvas


def paste_logo_badge(canvas):
    """El logo del club sempre a la dreta, sencer, en un badge circular blanc fix.
    Es dibuixa DESPRES de tot la resta perque mai quedi tapat."""
    logo = Image.open(LOGO_PATH).convert("RGBA")

    pad = 18
    inner = LOGO_BADGE_SIZE - pad * 2
    scale = min(inner / logo.width, inner / logo.height)
    lw, lh = int(logo.width * scale), int(logo.height * scale)
    logo = logo.resize((lw, lh), Image.LANCZOS)

    badge = Image.new("RGBA", (LOGO_BADGE_SIZE, LOGO_BADGE_SIZE), (0, 0, 0, 0))
    bd = ImageDraw.Draw(badge)
    bd.ellipse([0, 0, LOGO_BADGE_SIZE, LOGO_BADGE_SIZE], fill=(255, 255, 255, 255))
    badge.paste(logo, ((LOGO_BADGE_SIZE - lw) // 2, (LOGO_BADGE_SIZE - lh) // 2), logo)

    bx = W - LOGO_MARGIN - LOGO_BADGE_SIZE
    by = LOGO_MARGIN
    canvas.paste(badge, (bx, by), badge)


def build(args):
    canvas = Image.new("RGB", (W, H), INK)
    draw = ImageDraw.Draw(canvas)

    # --- Header: kicker (deixem marge a la dreta pel badge del logo) ---
    f_kicker = font(F_BLACK, 40)
    kicker = "QUIZ TÈCNIC"
    draw.text((60, 78), kicker, font=f_kicker, fill=RED)
    f_sub = font(F_REG, 30)
    draw.text((60, 130), "CB Grup Barna · Escola de Bàsquet", font=f_sub, fill=GRAY)

    # --- Foto (contain, no cover) ---
    paste_photo_contain(canvas, args.foto, PHOTO_BOX)

    y = PHOTO_BOX[3] + 60

    # --- Situacio ---
    f_situ = font(F_BLACK, 54)
    situ_lines = wrap_text(draw, args.situacio, f_situ, W - 120)
    y = draw_multiline(draw, (60, y), situ_lines, f_situ, WHITE, line_gap=8)
    y += 30

    # --- Opcions ---
    f_opt = font(F_BLACK, 38)
    opt_h = 108
    opt_gap = 24
    labels = ["A", "B", "C"]
    for i, text in enumerate(args.opcio):
        top = y + i * (opt_h + opt_gap)
        box = [60, top, W - 60, top + opt_h]

        is_correct = args.mode == "resposta" and i == args.correcta
        fill_color = GREEN if is_correct else GRAY_BG
        draw.rounded_rectangle(box, radius=20, fill=fill_color)

        # Etiqueta A/B/C dins cercle
        circ_d = 64
        cx, cy = box[0] + 30, top + opt_h // 2
        draw.ellipse([cx - circ_d / 2, cy - circ_d / 2, cx + circ_d / 2, cy + circ_d / 2],
                     fill=(255, 255, 255, 255) if is_correct else DARK)
        f_label = font(F_BLACK, 34)
        lw = draw.textlength(labels[i], font=f_label)
        draw.text((cx - lw / 2, cy - 22), labels[i], font=f_label,
                   fill=GREEN if is_correct else WHITE)

        text_x = box[0] + 80
        avail_w = (box[2] - box[0]) - 100 - (60 if is_correct else 0)
        opt_lines = wrap_text(draw, text, f_opt, avail_w)
        line_block_h = len(opt_lines) * (f_opt.size + 6)
        ty = cy - line_block_h / 2
        draw_multiline(draw, (text_x, ty), opt_lines, f_opt, WHITE, line_gap=6)

        if is_correct:
            f_check = font(F_BLACK, 46)
            draw.text((box[2] - 70, cy - 26), "✓", font=f_check, fill=WHITE)

    y = y + len(args.opcio) * (opt_h + opt_gap) + 10

    # --- Peu ---
    if args.mode == "pregunta":
        f_cta = font(F_BLACK, 36)
        cta = "VOTA A L'ENQUESTA ↑"
        cw = draw.textlength(cta, font=f_cta)
        draw.text(((W - cw) / 2, y + 30), cta, font=f_cta, fill=RED)
    else:
        f_why_label = font(F_BLACK, 34)
        draw.text((60, y + 20), "PER QUÈ?", font=f_why_label, fill=RED)
        f_why = font(F_REG, 36)
        why_lines = wrap_text(draw, args.perque, f_why, W - 120)
        draw_multiline(draw, (60, y + 75), why_lines, f_why, WHITE, line_gap=10)

    # --- Logo: sempre a sobre de tot, sempre a la dreta ---
    paste_logo_badge(canvas)

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    canvas.save(args.out, "PNG")
    print(f"OK -> {args.out}")


def parse_args(argv):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--foto", required=True, help="Ruta a la foto real del jugador/a")
    p.add_argument("--situacio", required=True, help="Text de la situacio/pregunta")
    p.add_argument("--opcio", action="append", required=True, help="Opcio de resposta (repetir 3 cops)")
    p.add_argument("--correcta", type=int, required=True, help="Index (0-based) de la opcio correcta")
    p.add_argument("--perque", default="", help="Explicacio, nomes usada en --mode resposta")
    p.add_argument("--mode", choices=["pregunta", "resposta"], required=True)
    p.add_argument("--out", required=True, help="Ruta de sortida PNG")
    args = p.parse_args(argv)
    if len(args.opcio) != 3:
        p.error("cal exactament 3 --opcio")
    if not (0 <= args.correcta < 3):
        p.error("--correcta ha de ser 0, 1 o 2")
    if args.mode == "resposta" and not args.perque:
        p.error("--perque es obligatori en --mode resposta")
    return args


if __name__ == "__main__":
    build(parse_args(sys.argv[1:]))
