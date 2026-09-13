#!/usr/bin/env python3
"""
Genera la story diària del comptador de la campanya de setembre.

La campanya de les noies del 2018 demana una story cada dia amb el número que
queda. Fer-la a mà cada matí és el camí segur cap a no fer-la, i per això és un
script: es canvien dos números i surt la peça, sempre igual de ben feta.

    python3 scripts/story-comptador.py                     # ho calcula tot sol
    python3 scripts/story-comptador.py --places 2          # queden 2 places
    python3 scripts/story-comptador.py --places 0          # «completes»
    python3 scripts/story-comptador.py --foto 3            # una altra foto

Surt a `escoleta/materials/story-comptador.png`, 1080x1920, a punt de pujar.

Regles del sistema visual que aplica, i que no s'han de trencar aquí:
  · Tres colors: el vermell de l'escut (#E20613), la tinta i el blanc.
  · Anton per al número, Inter per a la resta. Cap cursiva.
  · La foto no s'amplia MAI: es retalla des de dalt, de manera que el que es
    perd és el terra i no el cap. Si l'original no arriba, l'script avisa.
  · El text viu dins de la zona segura d'Instagram: la interfície es menja
    uns 250 px a dalt i uns 340 px a baix.
"""

import argparse
from datetime import date
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
FONTS = ROOT / ".github" / "scripts" / "fonts"
SORTIDA = ROOT / "escoleta" / "materials" / "story-comptador.png"

# ---------- LA CAMPANYA ----------
DIA_PROVA = date(2026, 9, 19)
HORA = "9.00 a 10.30 h"
LLOC = "La Nau del Clot"
GRUP = 5                       # places del grup de noies del 2018
FOTOS = [
    ROOT / "img" / "escoleta@2x.webp",
    ROOT / "img" / "escoleta-h1@2x.webp",
    ROOT / "img" / "escoleta-h2@2x.webp",
    ROOT / "img" / "escoleta-h3@2x.webp",
    ROOT / "img" / "escoleta-h4@2x.webp",
]

# ---------- SISTEMA ----------
W, H = 1080, 1920
INK = (16, 16, 14)
RED = (226, 6, 19)
PAPER = (255, 255, 255)
MUTED = (107, 101, 96)
MARGIN = 84
SEGUR_DALT = 250               # el que tapa la interfície d'Instagram
FOTO_H = 900

MESOS = ["gener", "febrer", "març", "abril", "maig", "juny",
         "juliol", "agost", "setembre", "octubre", "novembre", "desembre"]


def _font(nom, mida):
    return ImageFont.truetype(str(FONTS / nom), mida)


def _tracked(d, xy, text, font, fill, spacing):
    """Inter en caixa alta necessita aire entre lletres."""
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=font, fill=fill)
        x += d.textlength(ch, font=font) + spacing
    return x


def _linia(d, y, x1, x2, color, gruix=2):
    d.rectangle([x1, y, x2, y + gruix - 1], fill=color)


def texts(places, dies):
    """El que diu la peça segons on som. Cap frase que caduqui malament."""
    if places <= 0:
        return ("COMPLETES", "Les 5 places del 2018 ja estan reservades.",
                "Si vols venir igualment, escriu-nos: hi ha llista.")
    if dies < 0:
        return ("GRÀCIES", "La prova de les del 2018 ja s'ha jugat.",
                "Tot el setembre segueix sent de portes obertes.")
    if dies == 0:
        return (f"AVUI · {places}", f"Queden {places} places per a les nascudes el 2018.",
                f"{HORA} · {LLOC}.")
    cua = "plaça" if places == 1 else "places"
    quan = "Demà" if dies == 1 else f"D'aquí a {dies} dies"
    return (str(places), f"{cua.capitalize()} lliures per a les nascudes el 2018.",
            f"{quan}: dissabte {DIA_PROVA.day} de {MESOS[DIA_PROVA.month - 1]}, {HORA}.")


def build(places, foto_idx, avui):
    dies = (DIA_PROVA - avui).days
    gran, sota_1, sota_2 = texts(places, dies)

    im = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(im)

    anton = lambda s: _font("anton.ttf", s)
    inter = lambda s: _font("inter-regular.ttf", s)
    inter_m = lambda s: _font("inter-medium.ttf", s)
    inter_b = lambda s: _font("inter-bold.ttf", s)

    # ── Capçalera: escut i on som ──────────────────────────────
    logo = Image.open(ROOT / "logo.png").convert("RGBA")
    logo.thumbnail((92, 92), Image.LANCZOS)
    im.paste(logo, (MARGIN, SEGUR_DALT), logo)
    _tracked(d, (MARGIN + 116, SEGUR_DALT + 14), "CB GRUP BARNA", inter_b(26), INK, 4.2)
    _tracked(d, (MARGIN + 116, SEGUR_DALT + 52), "EL CLOT · BARCELONA", inter(24), MUTED, 3.6)

    y = SEGUR_DALT + 150
    _linia(d, y, MARGIN, W - MARGIN, (226, 222, 216))
    y += 54

    # ── L'etiqueta de la campanya ──────────────────────────────
    _tracked(d, (MARGIN, y), "PORTES OBERTES · ESCOLETA", inter_b(26), RED, 4.6)
    y += 66

    # ── El número, que és de què va la peça ────────────────────
    f = anton(300 if len(gran) <= 2 else 150)
    top, bottom = f.getbbox(gran)[1], f.getbbox(gran)[3]
    d.text((MARGIN - 6, y - top), gran, font=f, fill=RED)
    # Un número sol no diu si és molt o poc: al costat, de quantes són.
    if places > 0 and dies >= 0:
        x = MARGIN - 6 + d.textlength(gran, font=f) + 34
        fg = anton(96)
        gtop = fg.getbbox(f"DE {GRUP}")[1]
        d.text((x, y + (bottom - top) - 96 - gtop + 18), f"DE {GRUP}", font=fg, fill=INK)
    y += bottom - top + 34

    # ── Què vol dir aquell número ──────────────────────────────
    for linia, font, color in ((sota_1, inter_m(44), INK), (sota_2, inter(38), MUTED)):
        for tros in envolta(d, linia, font, W - MARGIN * 2):
            d.text((MARGIN, y), tros, font=font, fill=color)
            y += font.size + 16
        y += 12

    # ── La foto, a sota i retallada des de DALT ────────────────
    ph = Image.open(FOTOS[foto_idx % len(FOTOS)]).convert("RGB")
    pw, phh = ph.size
    escala = W / pw
    ratio = W / FOTO_H
    if pw / phh > ratio:
        nw = int(phh * ratio)
        ph = ph.crop(((pw - nw) // 2, 0, (pw - nw) // 2 + nw, phh))
    else:
        ph = ph.crop((0, 0, pw, int(pw / ratio)))
    ph = ph.resize((W, FOTO_H), Image.LANCZOS)
    im.paste(ph, (0, H - FOTO_H))
    d.rectangle([0, H - FOTO_H - 8, W, H - FOTO_H], fill=RED)

    # ── El peu, sobre la foto i dins de la zona segura ─────────
    peu_h = 150
    d.rectangle([0, H - peu_h, W, H], fill=INK)
    _tracked(d, (MARGIN, H - peu_h + 40), "RESERVA AL WEB", inter_b(28), (255, 255, 255), 4.4)
    _tracked(d, (MARGIN, H - peu_h + 84), "CBGRUPBARNA.INFO", inter(26), (190, 186, 181), 4.0)

    SORTIDA.parent.mkdir(parents=True, exist_ok=True)
    im.save(SORTIDA, "PNG", optimize=True)
    print(f"[story] {SORTIDA.relative_to(ROOT)} · {W}x{H} · "
          f"{SORTIDA.stat().st_size // 1024} KB · {gran} · {dies} dies")
    if escala > 1:
        print("[story] AVÍS: la foto s'està ampliant. Fes servir un original més gran.")


def envolta(d, text, font, ample):
    """Parteix una frase en línies que hi càpiguen."""
    mots, linies, actual = text.split(), [], ""
    for mot in mots:
        prova = (actual + " " + mot).strip()
        if d.textlength(prova, font=font) <= ample:
            actual = prova
        else:
            linies.append(actual)
            actual = mot
    if actual:
        linies.append(actual)
    return linies


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Story del comptador de la campanya")
    ap.add_argument("--places", type=int, default=3, help="places lliures del grup del 2018")
    ap.add_argument("--foto", type=int, default=0, help="quina foto de l'Escoleta (0-4)")
    ap.add_argument("--data", default="", help="data a simular, AAAA-MM-DD (per provar)")
    a = ap.parse_args()
    avui = date.fromisoformat(a.data) if a.data else date.today()
    build(max(0, min(GRUP, a.places)), a.foto, avui)
