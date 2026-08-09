#!/usr/bin/env python3
"""
Generador de fitxes de calendari · CB Grup Barna

Llegeix partits/data.json i, per a cada equip amb partits carregats, dibuixa
la "fitxa de partits" (imatge PNG, o PDF de diverses pàgines si no hi caben
totes les jornades) i la desa a partits/calendaris/. També escriu
partits/calendaris/manifest.json amb les dades que la pàgina
/partits/calendaris/ necessita per mostrar-les (tipus de fitxer, pàgines,
data de generació).

Es crida automàticament cada dia des de update-partits.yml, després
d'actualitzar partits/data.json amb el robot de la FCBQ: si un equip és nou,
si canvia una jornada o si es publica el calendari d'un equip de promoció,
la fitxa descarregable es torna a generar sola, sense intervenció manual.

Disseny defensiu: si un equip no té partits, se salta (surt a "Encara sense
calendari" a la pàgina). Si falla la generació d'un equip concret, s'avisa
per consola i es continua amb la resta — mai talla tot el procés.
"""
import hashlib
import json
from datetime import date
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "partits" / "data.json"
OUT_IMG = ROOT / "partits" / "calendaris" / "img"
OUT_DL = ROOT / "partits" / "calendaris" / "descarrega"
MANIFEST = ROOT / "partits" / "calendaris" / "manifest.json"
FONTS = Path(__file__).parent / "fonts"

# ── Sistema visual CB Grup Barna (mateixos tokens que partits/index.html) ──
RED = (230, 51, 41)
RED_INK = (183, 35, 27)
INK = (14, 17, 22)
CREAM = (244, 241, 236)
PAPER = (255, 255, 255)
MUTED = (107, 101, 96)
BORDER = (14, 17, 22, 18)
ROW_ALT = (244, 241, 236)

W, H = 1080, 1350
MARGIN = 62
ROWS_MAX = 14  # coincideix amb el criteri que ja feia servir el club a mà


def font(name, size):
    return ImageFont.truetype(str(FONTS / name), size)


F_ANTON = "anton.ttf"
F_BOLD = "inter-bold.ttf"
F_MED = "inter-medium.ttf"


def text_w(draw, txt, f):
    b = draw.textbbox((0, 0), txt, font=f)
    return b[2] - b[0]


def truncate(draw, txt, f, max_w):
    if text_w(draw, txt, f) <= max_w:
        return txt
    while txt and text_w(draw, txt + "…", f) > max_w:
        txt = txt[:-1]
    return txt + "…"


DIES = ["dg.", "dl.", "dt.", "dc.", "dj.", "dv.", "ds."]
MESOS = ["gen", "feb", "mar", "abr", "mai", "jun", "jul", "ago", "set", "oct", "nov", "des"]


def fmt_data(iso):
    y, m, d = iso.split("-")
    return f"{d}/{m}"


def rival(p):
    return p["visitant"] if p["casa"] else p["local"]


def pagina(equip, partits, pag_idx, n_pags, temporada):
    im = Image.new("RGB", (W, H), PAPER)
    dr = ImageDraw.Draw(im)

    # filet superior
    dr.rectangle([MARGIN, 74, MARGIN + 70, 80], fill=RED)

    y = 96
    dr.text((MARGIN, y), f"TEMPORADA {temporada}".upper(), font=font(F_BOLD, 20), fill=MUTED)
    y += 40
    dr.text((MARGIN, y), "FITXA DE PARTITS", font=font(F_ANTON, 50), fill=INK)
    y += 58
    nom = equip["nom"].upper()
    dr.text((MARGIN, y), nom, font=font(F_ANTON, 50), fill=RED)
    y += 62
    comp = equip.get("competicio") or ""
    if comp:
        comp_txt = truncate(dr, comp, font(F_BOLD, 21), W - 2 * MARGIN)
        dr.text((MARGIN, y), comp_txt, font=font(F_BOLD, 21), fill=INK)
        y += 34

    # píndola equip · N jornades (o pàgina X/Y si n'hi ha més d'una)
    y += 14
    label = f"{n_pags > 1 and f'PÀGINA {pag_idx + 1}/{n_pags} · ' or ''}{len(partits)} JORNADES"
    f_pill = font(F_BOLD, 22)
    pw = text_w(dr, label, f_pill) + 46
    dr.rounded_rectangle([MARGIN, y, MARGIN + pw, y + 46], radius=23, fill=INK)
    dr.text((MARGIN + 23, y + 11), label, font=f_pill, fill=PAPER)
    y += 70

    # ── files ──
    row_h = (H - y - 150) / ROWS_MAX
    row_h = min(row_h, 78)
    f_j = font(F_ANTON, 24)
    f_dt = font(F_MED, 17)
    f_rv = font(F_BOLD, 22)
    f_tag = font(F_BOLD, 15)

    for i, p in enumerate(partits):
        ry = y + i * row_h
        if i % 2 == 1:
            dr.rectangle([MARGIN - 14, ry, W - MARGIN + 14, ry + row_h - 6], fill=ROW_ALT)
        bar = RED if p["casa"] else INK
        dr.rectangle([MARGIN - 14, ry, MARGIN - 8, ry + row_h - 6], fill=bar)

        jx = f"J{i + 1}"
        dr.text((MARGIN, ry + row_h / 2 - 16), jx, font=f_j, fill=INK)
        jw = 62

        dt = f'{fmt_data(p["data"])} · {p["hora"]}'
        dr.text((MARGIN + jw, ry + 8), dt, font=f_dt, fill=MUTED)
        rv = truncate(dr, rival(p), f_rv, W - 2 * MARGIN - jw - 150)
        dr.text((MARGIN + jw, ry + 27), rv, font=f_rv, fill=INK)

        tag = "CASA" if p["casa"] else "FORA"
        tw = text_w(dr, tag, f_tag)
        dr.text((W - MARGIN - tw, ry + row_h / 2 - 9), tag,
                 font=f_tag, fill=RED_INK if p["casa"] else MUTED)

    # ── peu ──
    fy = H - 96
    dr.line([MARGIN, fy, W - MARGIN, fy], fill=(220, 216, 210), width=2)
    dr.text((MARGIN, fy + 18), "CLUB BÀSQUET GRUP BARNA · Nau Parc Clot, El Clot",
             font=font(F_BOLD, 16), fill=INK)
    handle = "@cbgrupbarna"
    hw = text_w(dr, handle, font(F_BOLD, 16))
    dr.text((W - MARGIN - hw, fy + 18), handle, font=font(F_BOLD, 16), fill=RED_INK)

    return im


def hash_equip(equip, partits, temporada):
    """Empremta estable de tot el que pot canviar l'aspecte de la fitxa,
    perquè es pugui saltar la regeneració (i el PDF no determinista de
    Pillow) quan la FCBQ no ha canviat res per a aquest equip."""
    partits = sorted(partits, key=lambda p: (p["data"], p["hora"]))
    payload = {
        "temporada": temporada,
        "nom": equip["nom"],
        "competicio": equip.get("competicio") or "",
        "partits": [
            {"data": p["data"], "hora": p["hora"], "casa": p["casa"],
             "local": p["local"], "visitant": p["visitant"]}
            for p in partits
        ],
    }
    raw = json.dumps(payload, sort_keys=True, ensure_ascii=False)
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()


def genera_equip(equip, partits, temporada):
    partits = sorted(partits, key=lambda p: (p["data"], p["hora"]))
    n = len(partits)
    if n == 0:
        return None
    n_pags = -(-n // ROWS_MAX)  # ceil
    per_pag = -(-n // n_pags)   # repartit de manera equilibrada
    pags = [partits[i:i + per_pag] for i in range(0, n, per_pag)]

    images = [pagina(equip, pag, i, len(pags), temporada) for i, pag in enumerate(pags)]

    slug = equip["id"]
    thumb = images[0].resize((700, round(700 * H / W)), Image.LANCZOS)
    thumb.save(OUT_IMG / f"{slug}.webp", "WEBP", quality=84, method=6)

    for old in (OUT_DL / f"{slug}.png", OUT_DL / f"{slug}.pdf"):
        old.unlink(missing_ok=True)

    if len(images) == 1:
        images[0].save(OUT_DL / f"{slug}.png", "PNG", optimize=True)
        return {"tipus": "png", "pagines": 1, "jornades": n}
    else:
        images[0].save(OUT_DL / f"{slug}.pdf", "PDF", save_all=True, append_images=images[1:])
        return {"tipus": "pdf", "pagines": len(images), "jornades": n}


def main():
    OUT_IMG.mkdir(parents=True, exist_ok=True)
    OUT_DL.mkdir(parents=True, exist_ok=True)

    manifest_antic = {}
    if MANIFEST.exists():
        try:
            manifest_antic = json.loads(MANIFEST.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            manifest_antic = {}

    d = json.loads(DATA.read_text(encoding="utf-8"))
    temporada = d.get("temporada", "").replace("-", " · ") or "2026 · 2027"
    partits_per_equip = {}
    for p in d["partits"]:
        partits_per_equip.setdefault(p["equipId"], []).append(p)

    manifest = {}
    fets = 0
    reutilitzats = 0
    for equip in d["equips"]:
        ps = partits_per_equip.get(equip["id"], [])
        if not ps:
            continue

        h = hash_equip(equip, ps, temporada)
        anterior = manifest_antic.get(equip["id"])
        slug = equip["id"]
        fitxer_existent = (OUT_DL / f"{slug}.png").exists() or (OUT_DL / f"{slug}.pdf").exists()

        if anterior and anterior.get("hash") == h and fitxer_existent:
            # Cap canvi real de la FCBQ per a aquest equip: es manté la
            # fitxa tal com estava (mateixa data d'actualització) i no es
            # torna a escriure el PNG/PDF, per no generar soroll al commit.
            manifest[equip["id"]] = anterior
            reutilitzats += 1
            continue

        try:
            info = genera_equip(equip, ps, temporada)
        except Exception as exc:
            print(f"[calendaris] ✗ {equip['id']}: {exc}")
            continue
        if info:
            info["nom"] = equip["nom"]
            info["hash"] = h
            info["actualitzat"] = date.today().isoformat()
            manifest[equip["id"]] = info
            fets += 1

    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[calendaris] {fets} fitxes regenerades, {reutilitzats} sense canvis, "
          f"de {len(d['equips'])} equips")


if __name__ == "__main__":
    main()
