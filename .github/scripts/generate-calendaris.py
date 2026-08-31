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

# L'escut de cada partit: el del Barna i el del rival, com a les fitxes
# d'equip del web. El resolutor és el mateix (scripts/escuts_partits.py).
import importlib.util as _ilu
_spec = _ilu.spec_from_file_location("escuts_partits", ROOT / "scripts" / "escuts_partits.py")
_escuts_mod = _ilu.module_from_spec(_spec)
_spec.loader.exec_module(_escuts_mod)
ESCUTS = _escuts_mod.Escuts()
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


# Es carreguen un cop i es reencaixen per mida quan calen: la fitxa en
# dibuixa centenars i obrir el PNG a cada fila seria llençar el temps.
_ESCUT_CACHE = {}


def _escut_img(ruta_abs, mida):
    clau = (str(ruta_abs), mida)
    if clau not in _ESCUT_CACHE:
        img = Image.open(ruta_abs).convert("RGBA")
        # Encaix "contain": l'escut sencer dins del quadrat, mai retallat.
        img.thumbnail((mida, mida), Image.LANCZOS)
        _ESCUT_CACHE[clau] = img
    return _ESCUT_CACHE[clau]


# L'escut oficial en alta (683x908, el mateix que el welcome pack de
# l'Ana): a la fitxa impresa es nota respecte del logo petit del web.
_ESCUT_BARNA = ROOT / "assets" / "marca" / "club" / "escut_transp.png"


def dibuixa_escut(im, dr, nom, es_barna, x, cy, mida):
    """Enganxa l'escut d'un equip centrat verticalment a cy. Qui no en té,
    duu un cercle amb les inicials — mai l'escut d'un altre i mai un forat.
    Retorna l'amplada ocupada."""
    ruta = _ESCUT_BARNA if es_barna else None
    if not es_barna:
        rel = ESCUTS.escut(nom)
        if rel:
            ruta = ROOT / "partits" / rel
    if ruta and ruta.exists():
        img = _escut_img(ruta, mida)
        im.paste(img, (round(x + (mida - img.width) / 2),
                       round(cy - img.height / 2)), img)
    else:
        r = mida / 2
        dr.ellipse([x + 1, cy - r + 1, x + mida - 1, cy + r - 1],
                   fill=CREAM, outline=(210, 205, 198), width=2)
        ini = _escuts_mod.inicials(nom)
        f_ini = font(F_BOLD, max(11, round(mida * 0.34)))
        iw = text_w(dr, ini, f_ini)
        dr.text((x + (mida - iw) / 2, cy - mida * 0.21), ini, font=f_ini, fill=MUTED)
    return mida


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
    row_h = min(row_h, 92)
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

        # Els dos escuts, amb el local primer: a casa el Barna obre la
        # fila, a fora l'obre el rival. La barra vermella/tinta de
        # l'esquerra ja diu casa o fora; els escuts ho fan llegible d'un
        # cop d'ull a la fitxa impresa.
        mida_e = min(70, round(row_h) - 14)
        cy = ry + (row_h - 6) / 2
        ex = MARGIN + jw
        parells = [("barna", True), (rival(p), False)] if p["casa"]             else [(rival(p), False), ("barna", True)]
        for nom_e, es_barna in parells:
            dibuixa_escut(im, dr, nom_e, es_barna, ex, cy, mida_e)
            ex += mida_e + 8
        tx = ex + 6

        dt = f'{fmt_data(p["data"])} · {p["hora"]}'
        dr.text((tx, ry + 8), dt, font=f_dt, fill=MUTED)
        rv = truncate(dr, rival(p), f_rv, W - MARGIN - tx - 130)
        dr.text((tx, ry + 27), rv, font=f_rv, fill=INK)

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


MESOS_CAT = ["gener", "febrer", "març", "abril", "maig", "juny", "juliol",
             "agost", "setembre", "octubre", "novembre", "desembre"]
DIES_CAT = ["Dilluns", "Dimarts", "Dimecres", "Dijous", "Divendres",
            "Dissabte", "Diumenge"]


def dia_llarg(iso):
    d = date.fromisoformat(iso)
    return f"{DIES_CAT[d.weekday()]} {d.day} de {MESOS_CAT[d.month - 1]}"


JORNADA_MAX = 19  # files (partits + capçaleres de dia) per pàgina del cartell


def pagina_jornada(etiqueta, files, equips_nom, pag_idx, n_pags, temporada):
    """El cartell d'una jornada sencera: tots els partits del club aquell
    cap de setmana, en format post (1080x1350), amb l'escut de cada equip.
    `files` barreja capçaleres de dia ("dia", iso) i partits ("partit", p)."""
    im = Image.new("RGB", (W, H), PAPER)
    dr = ImageDraw.Draw(im)

    dr.rectangle([MARGIN, 74, MARGIN + 70, 80], fill=RED)
    y = 96
    dr.text((MARGIN, y), f"TEMPORADA {temporada} · TOTS ELS EQUIPS".upper(),
            font=font(F_BOLD, 20), fill=MUTED)
    y += 40
    dr.text((MARGIN, y), "LA JORNADA", font=font(F_ANTON, 50), fill=INK)
    y += 58
    dr.text((MARGIN, y), etiqueta.upper(), font=font(F_ANTON, 50), fill=RED)
    y += 70
    n_partits = sum(1 for t, _ in files if t == "partit")
    label = f"{n_pags > 1 and f'PÀGINA {pag_idx + 1}/{n_pags} · ' or ''}{n_partits} PARTITS"
    f_pill = font(F_BOLD, 22)
    pw = text_w(dr, label, f_pill) + 46
    dr.rounded_rectangle([MARGIN, y, MARGIN + pw, y + 46], radius=23, fill=INK)
    dr.text((MARGIN + 23, y + 11), label, font=f_pill, fill=PAPER)
    y += 74

    row_h = min(112.0, (H - y - 130) / max(1, len(files)))
    f_h = font(F_ANTON, 22)
    f_eq = font(F_BOLD, 19)
    f_rv = font(F_MED, 18)
    f_tag = font(F_BOLD, 14)
    f_dia = font(F_BOLD, 17)

    i = 0
    for tipus, dada in files:
        ry = y + i * row_h
        if tipus == "dia":
            dr.text((MARGIN, ry + row_h / 2 - 10), dia_llarg(dada).upper(),
                    font=f_dia, fill=RED_INK)
            dr.line([MARGIN, ry + row_h - 8, W - MARGIN, ry + row_h - 8],
                    fill=(220, 216, 210), width=2)
            i += 1
            continue
        p = dada
        if i % 2 == 1:
            dr.rectangle([MARGIN - 14, ry, W - MARGIN + 14, ry + row_h - 5], fill=ROW_ALT)
        dr.rectangle([MARGIN - 14, ry, MARGIN - 8, ry + row_h - 5],
                     fill=RED if p["casa"] else INK)
        cy = ry + (row_h - 5) / 2
        dr.text((MARGIN, cy - 12), p["hora"], font=f_h, fill=INK)
        modificat = bool(p.get("avis")) and p["avis"].get("expira", "") >= avui_iso()

        mida_e = min(64, round(row_h) - 14)
        ex = MARGIN + 92
        parells = [("barna", True), (rival(p), False)] if p["casa"]             else [(rival(p), False), ("barna", True)]
        for nom_e, es_barna in parells:
            dibuixa_escut(im, dr, nom_e, es_barna, ex, cy, mida_e)
            ex += mida_e + 7
        tx = ex + 8

        nom_eq = (equips_nom.get(p["equipId"]) or p["equipId"]).upper()
        amplada_text = W - MARGIN - tx - 92
        dr.text((tx, cy - 19), truncate(dr, nom_eq, f_eq, amplada_text),
                font=f_eq, fill=INK)
        dr.text((tx, cy + 2), truncate(dr, rival(p), f_rv, amplada_text),
                font=f_rv, fill=MUTED)

        tag = "MODIFICAT" if modificat else ("CASA" if p["casa"] else "FORA")
        tw = text_w(dr, tag, f_tag)
        if modificat:
            dr.rectangle([W - MARGIN - tw - 10, cy - 13, W - MARGIN + 4, cy + 11], fill=RED)
            dr.text((W - MARGIN - tw, cy - 8), tag, font=f_tag, fill=PAPER)
        else:
            dr.text((W - MARGIN - tw, cy - 8), tag, font=f_tag,
                    fill=RED_INK if p["casa"] else MUTED)
        i += 1

    fy = H - 96
    dr.line([MARGIN, fy, W - MARGIN, fy], fill=(220, 216, 210), width=2)
    dr.text((MARGIN, fy + 18), "CLUB BÀSQUET GRUP BARNA · Nau Parc Clot, El Clot",
            font=font(F_BOLD, 16), fill=INK)
    handle = "@cbgrupbarna"
    hw = text_w(dr, handle, font(F_BOLD, 16))
    dr.text((W - MARGIN - hw, fy + 18), handle, font=font(F_BOLD, 16), fill=RED_INK)
    return im


def avui_iso():
    return date.today().isoformat()


def genera_jornades(data, temporada):
    """Un cartell per DIA amb partits — dissabte i diumenge, per separat.
    Cada un és el seu propi post 4:5, perquè es puguin descarregar i
    compartir l'un sense l'altre. Retorna el bloc per al manifest
    ("_jornades")."""
    equips_nom = {e["id"]: e.get("nom") or e.get("curt") or e["id"]
                  for e in data.get("equips", [])}
    per_dia = {}
    for p in data.get("partits", []):
        per_dia.setdefault(p["data"], []).append(p)

    (OUT_DL / "jornades").mkdir(exist_ok=True)
    (OUT_IMG / "jornades").mkdir(exist_ok=True)
    sortida = []
    for iso in sorted(per_dia):
        partits = sorted(per_dia[iso], key=lambda p: p["hora"])
        etiqueta = dia_llarg(iso)
        files = [("partit", p) for p in partits]
        n_pags = -(-len(files) // JORNADA_MAX)
        per_pag = -(-len(files) // n_pags)
        pags = [files[i:i + per_pag] for i in range(0, len(files), per_pag)]
        images = [pagina_jornada(etiqueta, pag, equips_nom, i, len(pags), temporada)
                  for i, pag in enumerate(pags)]

        slug = f"jornada-{iso}"
        thumb = images[0].resize((700, round(700 * H / W)), Image.LANCZOS)
        thumb.save(OUT_IMG / "jornades" / f"{slug}.webp", "WEBP", quality=84, method=6)
        for old in (OUT_DL / "jornades" / f"{slug}.png", OUT_DL / "jornades" / f"{slug}.pdf"):
            old.unlink(missing_ok=True)
        if len(images) == 1:
            images[0].save(OUT_DL / "jornades" / f"{slug}.png", "PNG", optimize=True)
            tipus = "png"
        else:
            images[0].save(OUT_DL / "jornades" / f"{slug}.pdf", "PDF",
                           save_all=True, append_images=images[1:])
            tipus = "pdf"
        sortida.append({"clau": iso, "etiqueta": etiqueta, "tipus": tipus,
                        "partits": len(partits), "dates": [iso]})
    print(f"[jornades] {len(sortida)} cartells, un per dia")
    return sortida


def hash_equip(equip, partits, temporada):
    """Empremta estable de tot el que pot canviar l'aspecte de la fitxa,
    perquè es pugui saltar la regeneració (i el PDF no determinista de
    Pillow) quan la FCBQ no ha canviat res per a aquest equip."""
    partits = sorted(partits, key=lambda p: (p["data"], p["hora"]))
    payload = {
        # Puja quan canvia el DIBUIX de la fitxa (no les dades), perquè
        # les fitxes velles no es quedin publicades amb l'aspecte antic.
        "disseny": 5,
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
    # El cartell de cada jornada (tots els equips d'un cap de setmana),
    # amb la seva pròpia empremta perquè només es redibuixin les que
    # canvien de debò.
    try:
        h_j = hashlib.sha1(json.dumps(
            {"disseny": 7, "temporada": temporada,
             "partits": [{"data": p["data"], "hora": p["hora"], "casa": p["casa"],
                          "local": p["local"], "visitant": p["visitant"],
                          "equipId": p["equipId"]} for p in
                         sorted(d["partits"], key=lambda x: (x["data"], x["hora"]))]},
            sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()
        antic_j = manifest_antic.get("_jornades") or {}
        if antic_j.get("hash") == h_j and (OUT_DL / "jornades").exists():
            manifest["_jornades"] = antic_j
            print("[jornades] sense canvis")
        else:
            manifest["_jornades"] = {"hash": h_j,
                                     "actualitzat": date.today().isoformat(),
                                     "llista": genera_jornades(d, temporada)}
    except Exception as exc:
        print(f"[jornades] ✗ {exc}")


    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[calendaris] {fets} fitxes regenerades, {reutilitzats} sense canvis, "
          f"de {len(d['equips'])} equips")


if __name__ == "__main__":
    main()
