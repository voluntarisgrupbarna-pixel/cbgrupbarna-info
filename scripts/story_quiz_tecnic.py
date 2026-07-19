#!/usr/bin/env python3
"""Generador d'Instagram Stories per a la serie 'Quiz Tecnic' del CB Grup Barna.

Patro fix (definit per l'usuari, no negociable, val per a totes les peces d'aquesta serie):
  - Fons blanc, marc vermell al voltant de tota la peca.
  - Kicker vermell "QUIZ TECNIC · <TEMA>" a dalt a l'esquerra.
  - Titol gran en majuscules: primera part en negre, la resta (el concepte clau) en vermell.
  - Subtitol "TRIA LA MILLOR OPCIO / RESPON A L'ENQUESTA!" en gris fosc.
  - Foto real d'un jugador/a, ample de contingut, MAI retallada per dalt (el cap/cara no es
    talla mai mai: si la foto es massa alta pel forat, el retall nomes menja per la part
    de baix, no per dalt).
  - 3 opcions A/B/C: cercle vermell + text negre per les incorrectes, cercle verd + text
    verd + check per la correcta.
  - Caixa negra arrodonida "MOLT BE!" amb l'explicacio de la resposta.
  - Peu "CB GRUP BARNA — EL CLOT, BARCELONA".
  - El logo del club sempre surt sencer a la dreta (badge fix a dalt a la dreta, mai tapat).

Us:
  python3 story_quiz_tecnic.py \
      --tema TIR \
      --foto path/a/la/foto.jpg \
      --titol-negre "Quina es la millor" \
      --titol-vermell "posicio dels peus en un tir?" \
      --opcio "Peus junts i en linia recta" \
      --opcio "Un peu una miqueta davant de l'altre" \
      --opcio "Peus molt oberts i en parallel" \
      --correcta 2 \
      --perque "La posicio correcta dels peus dona estabilitat, equilibri i et permet un bon control del tir." \
      --out out/quiz_tir_01.png
"""
import argparse
import os
import sys

from PIL import Image, ImageDraw, ImageFont, ImageOps

W, H = 1080, 1920

RED = (200, 16, 46)
BLACK = (10, 10, 10)
WHITE = (255, 255, 255)
DARK_GRAY = (60, 60, 60)
MID_GRAY = (120, 120, 120)
LINE_GRAY = (225, 225, 225)
GREEN = (34, 197, 94)

FONT_DIR = "/usr/share/fonts/truetype/liberation"
F_BOLD = os.path.join(FONT_DIR, "LiberationSans-Bold.ttf")
F_REG = os.path.join(FONT_DIR, "LiberationSans-Regular.ttf")
# LiberationSans-Bold no te un glif real de "check" (mostra un requadre buit);
# DejaVu si que en te un, s'usa nomes per aquest simbol.
F_SYMBOL = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGO_PATH = os.path.join(REPO_ROOT, "logo.png")

MARGIN = 76
BORDER_MARGIN = 14
BORDER_WIDTH = 12
MAX_PHOTO_H = 620


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


def draw_multiline(draw, xy, lines, f, fill, line_gap=8):
    x, y = xy
    for line in lines:
        draw.text((x, y), line, font=f, fill=fill)
        y += f.size + line_gap
    return y


def draw_frame(canvas):
    draw = ImageDraw.Draw(canvas)
    draw.rectangle(
        [BORDER_MARGIN, BORDER_MARGIN, W - BORDER_MARGIN, H - BORDER_MARGIN],
        outline=RED, width=BORDER_WIDTH,
    )


def paste_photo(canvas, photo_path, top):
    """Encaixa la foto a l'ample de contingut. Si l'alcada resultant es mes
    gran que el forat disponible, el retall es fa NOMES per la part de baix
    (mai per dalt), perque el cap/cara del jugador/a no es talli mai."""
    box_w = W - 2 * MARGIN
    img = ImageOps.exif_transpose(Image.open(photo_path)).convert("RGB")

    scale = box_w / img.width
    scaled_h = int(img.height * scale)
    fit = img.resize((box_w, scaled_h), Image.LANCZOS)

    if scaled_h > MAX_PHOTO_H:
        fit = fit.crop((0, 0, box_w, MAX_PHOTO_H))
        photo_h = MAX_PHOTO_H
    else:
        photo_h = scaled_h

    canvas.paste(fit, (MARGIN, top))
    return photo_h


def paste_logo_badge(canvas):
    """Logo sencer, sempre a la dreta, per sobre de tota la resta."""
    logo = Image.open(LOGO_PATH).convert("RGBA")
    target_h = 210
    scale = target_h / logo.height
    lw, lh = int(logo.width * scale), target_h
    logo = logo.resize((lw, lh), Image.LANCZOS)
    lx = W - BORDER_MARGIN - 30 - lw
    ly = 10
    canvas.paste(logo, (lx, ly), logo)


def build(args):
    canvas = Image.new("RGB", (W, H), WHITE)
    draw = ImageDraw.Draw(canvas)
    content_w = W - 2 * MARGIN

    # --- Kicker ---
    f_kicker = font(F_BOLD, 34)
    kicker = f"QUIZ TÈCNIC · {args.tema.upper()}"
    y = 96
    draw.text((MARGIN, y), kicker, font=f_kicker, fill=RED)
    y += 58
    draw.line([(MARGIN, y), (MARGIN + 60, y)], fill=RED, width=6)
    y += 34

    # --- Titol: primera part negra, resta vermella ---
    f_title = font(F_BOLD, 62)
    black_lines = wrap_text(draw, args.titol_negre.upper(), f_title, content_w)
    red_lines = wrap_text(draw, args.titol_vermell.upper(), f_title, content_w)
    y = draw_multiline(draw, (MARGIN, y), black_lines, f_title, BLACK, line_gap=6)
    y = draw_multiline(draw, (MARGIN, y), red_lines, f_title, RED, line_gap=6)
    y += 26

    draw.line([(MARGIN, y), (MARGIN + 60, y)], fill=BLACK, width=6)
    y += 30

    # --- Subtitol ---
    f_sub = font(F_BOLD, 32)
    for line in ["TRIA LA MILLOR OPCIÓ", "I RESPON A L'ENQUESTA!"]:
        draw.text((MARGIN, y), line, font=f_sub, fill=DARK_GRAY)
        y += f_sub.size + 8
    y += 34

    # --- Foto (mai retallada per dalt) ---
    photo_h = paste_photo(canvas, args.foto, y)
    y += photo_h + 46

    # --- Opcions A/B/C ---
    f_opt = font(F_BOLD, 36)
    labels = ["A", "B", "C"]
    circ_d = 60
    for i, text in enumerate(args.opcio):
        is_correct = i == args.correcta
        color = GREEN if is_correct else RED
        text_color = GREEN if is_correct else BLACK

        avail_w = content_w - (circ_d + 30) - (70 if is_correct else 0)
        opt_lines = wrap_text(draw, text.upper(), f_opt, avail_w)
        row_h = max(circ_d, len(opt_lines) * (f_opt.size + 6))

        cx, cy = MARGIN + circ_d / 2, y + row_h / 2
        draw.ellipse([cx - circ_d / 2, cy - circ_d / 2, cx + circ_d / 2, cy + circ_d / 2], fill=color)
        f_label = font(F_BOLD, 30)
        lw = draw.textlength(labels[i], font=f_label)
        draw.text((cx - lw / 2, cy - f_label.size / 2 - 2), labels[i], font=f_label, fill=WHITE)

        text_x = MARGIN + circ_d + 30
        block_h = len(opt_lines) * (f_opt.size + 6)
        draw_multiline(draw, (text_x, cy - block_h / 2), opt_lines, f_opt, text_color, line_gap=6)

        if is_correct:
            f_check = font(F_SYMBOL, 46)
            draw.text((MARGIN + content_w - 50, cy - f_check.size / 2 - 4), "✓", font=f_check, fill=GREEN)

        y += row_h + 26
        if i < len(args.opcio) - 1:
            draw.line([(MARGIN, y - 13), (MARGIN + content_w, y - 13)], fill=LINE_GRAY, width=2)

    y += 14

    # --- Caixa "MOLT BE!" ---
    f_why_title = font(F_BOLD, 38)
    f_why = font(F_REG, 32)
    why_lines = wrap_text(draw, args.perque, f_why, content_w - 130)
    box_h = 60 + len(why_lines) * (f_why.size + 10) + 30
    box = [MARGIN, y, MARGIN + content_w, y + box_h]
    draw.rounded_rectangle(box, radius=26, fill=BLACK)

    icon_d = 60
    icx, icy = box[0] + 44, box[1] + 44
    draw.ellipse([icx - icon_d / 2, icy - icon_d / 2, icx + icon_d / 2, icy + icon_d / 2], fill=WHITE)
    bar_w, gap = 8, 6
    bars = [14, 22, 16]
    bx = icx - (len(bars) * bar_w + (len(bars) - 1) * gap) / 2
    base_y = icy + 16
    for h in bars:
        draw.rectangle([bx, base_y - h, bx + bar_w, base_y], fill=RED)
        bx += bar_w + gap

    tx = box[0] + 44 + icon_d + 26
    ty = box[1] + 30
    draw.text((tx, ty), "MOLT BÉ!", font=f_why_title, fill=WHITE)
    draw_multiline(draw, (tx, ty + f_why_title.size + 12), why_lines, f_why, (225, 225, 225), line_gap=10)

    y = box[3] + 40

    # --- Peu ---
    draw.line([(MARGIN, y), (MARGIN + content_w, y)], fill=BLACK, width=3)
    y += 24
    f_foot = font(F_BOLD, 28)
    foot = "CB GRUP BARNA — EL CLOT, BARCELONA"
    fw = draw.textlength(foot, font=f_foot)
    draw.text((MARGIN + (content_w - fw) / 2, y), foot, font=f_foot, fill=BLACK)

    # --- Marc + logo: sempre per sobre de tota la resta ---
    draw_frame(canvas)
    paste_logo_badge(canvas)

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    canvas.save(args.out, "PNG")
    print(f"OK -> {args.out}")


def parse_args(argv):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--tema", required=True, help="Tema del quiz (p.ex. TIR, DEFENSA, PASSADA)")
    p.add_argument("--foto", required=True, help="Ruta a la foto real del jugador/a")
    p.add_argument("--titol-negre", dest="titol_negre", required=True)
    p.add_argument("--titol-vermell", dest="titol_vermell", required=True)
    p.add_argument("--opcio", action="append", required=True, help="Repetir 3 cops")
    p.add_argument("--correcta", type=int, required=True, help="Index (0-based) de la opcio correcta")
    p.add_argument("--perque", required=True)
    p.add_argument("--out", required=True)
    args = p.parse_args(argv)
    if len(args.opcio) != 3:
        p.error("cal exactament 3 --opcio")
    if not (0 <= args.correcta < 3):
        p.error("--correcta ha de ser 0, 1 o 2")
    return args


if __name__ == "__main__":
    build(parse_args(sys.argv[1:]))
