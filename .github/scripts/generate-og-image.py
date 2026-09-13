#!/usr/bin/env python3
"""
Genera og-image.jpg, la imatge que surt quan algú comparteix cbgrupbarna.info
per WhatsApp o quan la pàgina apareix a Google.

És un script i no un fitxer fet a mà perquè la portada rota cada temporada i
aquesta imatge ha de rotar amb ella. Canvia les constants de CONTINGUT i torna'l
a executar.

Regles del sistema visual que aplica (i que no s'han de trencar aquí):
  · Només tres colors: el vermell de l'escut, la tinta i el blanc.
  · Fons clar. Mai una peça tota negra.
  · Cap cara tallada: la foto s'ancora a DALT, de manera que el que es perd en
    retallar és el terra, mai el cap.
  · Res amb data de caducitat. Si anuncia un esdeveniment que ja ha passat,
    l'hem de canviar.
  · La foto va en columna estreta a propòsit: així no s'amplia i no es veu tova.

Ús:  python3 .github/scripts/generate-og-image.py            → og-image.jpg
     python3 .github/scripts/generate-og-image.py --campanya → og-prova-2018.jpg

La variant `--campanya` fa la imatge de la prova del 19 de setembre, que és la
que les tres portades ensenyen mentre dura. **Caduca el 20 de setembre**: aquell
dia s'ha de treure `og-prova-2018.jpg` de les tres portades i deixar-hi
`og-image.jpg` una altra vegada. Està apuntat a PENDENTS-WEB.md.
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
FONTS = ROOT / ".github" / "scripts" / "fonts"

# ---------- CONTINGUT (això és el que es canvia cada temporada) ----------
FOTO = ROOT / "img" / "hero-player.webp"
EYEBROW = "BÀSQUET BASE AL CLOT"
EYEBROW_2 = "BARCELONA  ·  DES DE 1965"
NOM_1, NOM_2 = "CB GRUP", "BARNA"
CLAIM = "Acadèmia i club de bàsquet base."
SOTA_1 = "34 equips federats i paritat real entre la"
SOTA_2 = "línia femenina i la masculina."

# ---------- CONTINGUT DE LA CAMPANYA (--campanya) ----------
# Res de números de places aquí: una imatge compartida per WhatsApp es queda
# guardada a la conversa i el número canvia cada dia. El que no caduca en sis
# dies és la crida i la data.
C_FOTO = ROOT / "img" / "escoleta@2x.webp"
C_EYEBROW = "PORTES OBERTES  ·  ESCOLETA"
C_EYEBROW_2 = "LA NAU DEL CLOT  ·  BARCELONA"
C_NOM_1, C_NOM_2 = "LES DEL", "2018"
C_CLAIM = "Dissabte 19 de setembre, de 9 a 10.30 h."
C_SOTA_1 = "Prova de bàsquet gratuïta per a noies"
C_SOTA_2 = "nascudes el 2018. Places comptades."
C_SORTIDA = "og-prova-2018.jpg"

# ---------- SISTEMA ----------
W, H = 1200, 630
COL_FOTO = 450          # estreta a posta: la foto no s'ha d'ampliar mai
INK = (16, 16, 14)
RED = (226, 6, 19)      # mostrejat de logo.png, el vermell de l'escut
PAPER = (255, 255, 255)
MUTED = (107, 101, 96)
HAIRLINE = (226, 222, 216)
MARGIN = 68


def _font(name, size):
    return ImageFont.truetype(str(FONTS / name), size)


def _tracked(draw, xy, text, font, fill, spacing):
    """Text amb interlletratge. Inter en caixa alta necessita aire."""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        x += draw.textlength(ch, font=font) + spacing
    return x


def build(campanya=False):
    foto = C_FOTO if campanya else FOTO
    eyebrow = C_EYEBROW if campanya else EYEBROW
    eyebrow_2 = C_EYEBROW_2 if campanya else EYEBROW_2
    nom_1 = C_NOM_1 if campanya else NOM_1
    nom_2 = C_NOM_2 if campanya else NOM_2
    claim = C_CLAIM if campanya else CLAIM
    sota_1 = C_SOTA_1 if campanya else SOTA_1
    sota_2 = C_SOTA_2 if campanya else SOTA_2
    sortida = C_SORTIDA if campanya else "og-image.jpg"

    im = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(im)

    # Foto: retall ancorat a DALT perquè el cap no es toqui mai.
    ph = Image.open(foto).convert("RGB")
    pw, phh = ph.size
    ratio = COL_FOTO / H
    if pw / phh > ratio:
        nw = int(phh * ratio)
        ph = ph.crop(((pw - nw) // 2, 0, (pw - nw) // 2 + nw, phh))
    else:
        ph = ph.crop((0, 0, pw, int(pw / ratio)))
    escala = COL_FOTO / ph.size[0]
    ph = ph.resize((COL_FOTO, H), Image.LANCZOS)
    im.paste(ph, (W - COL_FOTO, 0))
    d.rectangle([W - COL_FOTO - 3, 0, W - COL_FOTO, H], fill=RED)

    anton = lambda s: _font("anton.ttf", s)
    inter = lambda s: _font("inter-regular.ttf", s)
    inter_b = lambda s: _font("inter-bold.ttf", s)

    logo = Image.open(ROOT / "logo.png").convert("RGBA")
    logo.thumbnail((62, 62), Image.LANCZOS)
    im.paste(logo, (MARGIN, 50), logo)

    _tracked(d, (MARGIN + 80, 52), eyebrow, inter_b(15), RED, 3.4)
    _tracked(d, (MARGIN + 80, 76), eyebrow_2, inter(15), MUTED, 3.0)

    # El nom, col·locat per la caixa real de cada línia i no a ull.
    f = anton(126)
    y = 158
    for line in (nom_1, nom_2):
        top, bottom = f.getbbox(line)[1], f.getbbox(line)[3]
        d.text((MARGIN, y - top), line, font=f, fill=INK)
        y += bottom - top + 12
    y -= 12

    y += 26
    d.rectangle([MARGIN, y, MARGIN + 92, y + 5], fill=RED)
    y += 39

    d.text((MARGIN, y), claim, font=inter_b(22), fill=INK)
    d.text((MARGIN, y + 32), sota_1, font=inter(22), fill=MUTED)
    d.text((MARGIN, y + 61), sota_2, font=inter(22), fill=MUTED)

    right = W - COL_FOTO - 56
    d.rectangle([MARGIN, H - 84, right, H - 83], fill=HAIRLINE)
    _tracked(d, (MARGIN, H - 58), "CBGRUPBARNA.INFO", inter_b(15), INK, 3.2)
    _tracked(d, (MARGIN + 322, H - 58), "@CBGRUPBARNA", inter(15), MUTED, 3.2)

    out = ROOT / sortida
    im.save(out, "JPEG", quality=90, optimize=True, progressive=True)
    print(f"[og] {out.relative_to(ROOT)} · {W}x{H} · "
          f"{out.stat().st_size // 1024} KB · foto a escala {escala:.2f}")
    if escala > 1:
        print("[og] AVÍS: la foto s'està ampliant. Fes servir un original més gran.")


if __name__ == "__main__":
    import sys
    build(campanya="--campanya" in sys.argv)
