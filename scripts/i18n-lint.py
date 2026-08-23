#!/usr/bin/env python3
"""
Revisa la salut del multiidioma de cbgrupbarna.info. No toca cap fitxer.

    python3 scripts/i18n-lint.py                    # informe complet
    python3 scripts/i18n-lint.py --nomes-errors     # només el que atura la CI
    python3 scripts/i18n-lint.py --actualitza-base  # accepta l'estat d'avui

Per què existeix. El problema del multiidioma d'aquesta web no és traduir:
és que res avisa quan una traducció es queda enrere. Si toques la pàgina
catalana i no la castellana, no passa res —fins que algú se n'adona mesos
després. Aquest script és el que se n'adona el mateix dia.

Comprova nou coses, en dos nivells de gravetat:

  ERRORS (aturen la CI: són contradiccions, no feina pendent)
    · L'atribut lang de l'<html> no coincideix amb el directori.
    · Un hreflang apunta a una pàgina que no existeix.
    · Un hreflang no és recíproc: A diu que B és la seva traducció i B no ho diu.
    · Un enllaç fa servir un sinònim que el vocabulari del club dona per
      prohibit —«Team calendars» en comptes de «Match days by team».

  PENDENTS (informen, no aturen res: és feina, i la feina es prioritza)
    · Pàgines sense versió castellana o anglesa.
    · Pàgines amb traducció al mapa però sense hreflang que ho digui.
    · Pàgines sense x-default.
    · Slugs sense traduir sota /es/ i /en/ (amb les excepcions escrites a
      i18n/excepcions.yml: noms propis i paraules iguals en els tres idiomes).
    · Traduccions més velles que el seu original.
    · Pàgines en castellà o anglès sense parella catalana.
    · Enllaços que semblen una etiqueta i no fan servir el nom canònic. Aquí
      no és un error perquè la frontera entre etiqueta i prosa no es pot
      endevinar sempre: ho ha de mirar una persona.

La CI no falla per l'estat que ja hi havia. i18n/baseline.txt guarda els
errors coneguts del dia que es va posar en marxa, i el lint només es queixa
del que sigui NOU. Així es pot activar avui sense haver d'arreglar-ho tot
primer, i alhora ningú n'hi pot afegir de nous sense adonar-se'n.
"""
import argparse
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://cbgrupbarna.info"
MAPA = ROOT / "i18n" / "routes.yml"
ETIQUETES = ROOT / "i18n" / "etiquetes.yml"
EXCEPCIONS = ROOT / "i18n" / "excepcions.yml"
BASE = ROOT / "i18n" / "baseline.txt"

# Quants dies de marge abans de considerar una traducció endarrerida. Un dia
# o dos són el ritme normal de treball; una setmana ja és oblit.
DIES_DE_MARGE = 7

RE_HTML_LANG = re.compile(r'<html[^>]*\blang=["\']([^"\']+)["\']', re.I)
RE_ALTERNATE = re.compile(
    r'<link[^>]+rel=["\']alternate["\'][^>]*hreflang=["\']([^"\']+)["\'][^>]*href=["\']([^"\']+)["\']',
    re.I,
)
RE_ENLLAC = re.compile(r'<a\b[^>]*\bhref=["\']([^"\']+)["\'][^>]*>(.*?)</a>', re.I | re.S)
RE_ETIQUETA = re.compile(r"<[^>]+>")
RE_NOINDEX = re.compile(r'<meta[^>]+name=["\']robots["\'][^>]*content=["\'][^"\']*noindex', re.I)


def fitxer_de(url):
    resta = url.lstrip("/")
    return ROOT / (resta + "index.html" if url.endswith("/") else resta)


def idioma_de(url):
    return "es" if url.startswith("/es/") else "en" if url.startswith("/en/") else "ca"


def dates_git():
    """Data de l'últim commit que va tocar cada fitxer, en una sola passada.

    Fer un `git log` per fitxer serien 300 processos; amb l'historial sencer
    llegit d'un cop n'hi ha prou i es nota.

    Dos detalls que costen molt si es descuiden. Sense `--no-renames`, git es
    posa a buscar renoms i l'historial d'aquest repositori en té prou (tandes
    de centenars de fotos en un sol commit) perquè no acabi mai. I filtrant
    per '*.html' es descarta d'entrada tot el que aquí no mirem, que és la
    major part del que hi ha.
    """
    dates = {}
    sortida = subprocess.run(
        ["git", "log", "--no-renames", "--format=%x00%cs", "--name-only", "--", "*.html"],
        cwd=ROOT, capture_output=True, text=True, timeout=90,
    ).stdout
    data = None
    for linia in sortida.splitlines():
        if linia.startswith("\0"):
            data = linia[1:].strip()
        elif linia.strip() and data:
            dates.setdefault(linia.strip(), data)
    return dates


def carrega():
    mapa = yaml.safe_load(MAPA.read_text(encoding="utf-8")) or {}
    etiquetes = yaml.safe_load(ETIQUETES.read_text(encoding="utf-8")) or {}
    excepcions = yaml.safe_load(EXCEPCIONS.read_text(encoding="utf-8")) or {}
    return mapa, etiquetes, excepcions


def slug_exempt(ca, idioma, excepcions):
    """Un slug igual en dos idiomes que no és cap descuit.

    N'hi ha de tres menes: rutes senceres amb nom propi a dins —les fitxes de
    cada empresa patrocinadora—, paraules que ja s'escriuen igual en els tres
    idiomes, com «blog» o «3x3», o que són vocabulari del club, com
    «Escoleta», i les seccions de navegació que s'ha decidit deixar amb el nom
    català perquè ningú les busca pel nom i canviar-les trencaria enllaços
    publicats. El motiu de cada decisió és a i18n/excepcions.yml.
    """
    for llista in ("rutes_exemptes", "rutes_exemptes_de_renom"):
        for regla in excepcions.get(llista, []):
            if ca.startswith(regla["ruta"]):
                return True
    ultim = ca.strip("/").split("/")[-1]
    return ultim in (excepcions.get("segments_exempts", {}).get(idioma) or [])


def revisa():
    mapa, etiquetes, excepcions = carrega()
    rutes = mapa.get("rutes", [])
    orfes = mapa.get("orfes", {})
    dates = dates_git()
    errors, pendents = [], []

    # Índex de totes les pàgines del mapa, per no llegir dues vegades el mateix.
    urls = set()
    for r in rutes:
        for idioma in ("ca", "es", "en"):
            if r.get(idioma):
                urls.add(r[idioma])
    contingut = {}
    for url in urls:
        f = fitxer_de(url)
        contingut[url] = f.read_text(encoding="utf-8", errors="ignore") if f.exists() else None

    # ── lang de l'<html> ────────────────────────────────────────────────────
    for url, text in sorted(contingut.items()):
        if text is None:
            continue
        trobat = RE_HTML_LANG.search(text)
        esperat = idioma_de(url)
        if not trobat:
            errors.append(f"lang-absent · {url} · l'<html> no diu en quin idioma està")
        elif trobat.group(1).split("-")[0].lower() != esperat:
            errors.append(f"lang-erroni · {url} · l'<html> diu «{trobat.group(1)}» i és a /{esperat}/")

    # ── hreflang: existència, reciprocitat i x-default ──────────────────────
    declarats = {}
    for url, text in contingut.items():
        if text is None:
            continue
        trobats = {}
        for codi, href in RE_ALTERNATE.findall(text):
            trobats[codi.lower()] = href.replace(SITE, "") or "/"
        declarats[url] = trobats

    for url, trobats in sorted(declarats.items()):
        for codi, desti in sorted(trobats.items()):
            if codi == "x-default":
                continue
            if not fitxer_de(desti).exists():
                errors.append(f"hreflang-trencat · {url} · diu que la versió {codi} és {desti}, que no existeix")
                continue
            tornada = declarats.get(desti, {})
            if tornada and tornada.get(idioma_de(url)) not in (url, None):
                errors.append(f"hreflang-no-reciproc · {url} ↔ {desti} · no s'apunten l'un a l'altre")

    for r in rutes:
        germanes = [r.get(i) for i in ("es", "en") if r.get(i)]
        if not germanes:
            continue
        # Si la pàgina catalana és noindex, no se li demanen hreflang: declarar
        # com a versió principal una pàgina que hem tret de l'índex és pitjor
        # que no declarar res. scripts/i18n-hreflang.py salta aquests grups
        # pel mateix motiu i els diu pel nom quan s'executa.
        if RE_NOINDEX.search(contingut.get(r["ca"]) or ""):
            continue
        for url in [r["ca"], *germanes]:
            trobats = declarats.get(url, {})
            if not trobats:
                pendents.append(f"sense-hreflang · {url} · té traducció al mapa i no ho declara")
            elif "x-default" not in trobats:
                pendents.append(f"sense-x-default · {url} · cap versió marcada com a per defecte")

    # ── traduccions que falten, slugs sense traduir i desfasament ───────────
    for r in rutes:
        ca = r["ca"]
        for idioma in ("es", "en"):
            desti = r.get(idioma)
            if desti is None:
                if r.get("nota"):
                    continue
                pendents.append(f"sense-traduccio · {ca} · falta la versió {idioma}")
                continue
            if desti == f"/{idioma}{ca}" and ca.strip("/") \
                    and not slug_exempt(ca, idioma, excepcions):
                pendents.append(f"slug-sense-traduir · {desti} · manté la ruta catalana")
            f_ca, f_tr = fitxer_de(ca), fitxer_de(desti)
            d_ca = dates.get(str(f_ca.relative_to(ROOT)))
            d_tr = dates.get(str(f_tr.relative_to(ROOT)))
            if d_ca and d_tr and d_ca > d_tr:
                from datetime import date
                dies = (date.fromisoformat(d_ca) - date.fromisoformat(d_tr)).days
                if dies >= DIES_DE_MARGE:
                    pendents.append(f"desfasada · {desti} · {dies} dies més vella que {ca}")

    for idioma, llista in (orfes or {}).items():
        for url in llista:
            pendents.append(f"orfe · {url} · cap pàgina catalana n'és l'original")

    # ── vocabulari dels enllaços ────────────────────────────────────────────
    permeses = etiquetes.get("enllacos", {})
    excepcions = etiquetes.get("excepcions_de_text", [])
    for url, text in sorted(contingut.items()):
        if text is None:
            continue
        idioma = idioma_de(url)
        for desti, etiqueta in RE_ENLLAC.findall(text):
            desti = desti.replace(SITE, "").split("#")[0].split("?")[0]
            desti = re.sub(r"^/(es|en)/", "/", desti)
            regla = permeses.get(desti)
            if not regla:
                continue
            net = RE_ETIQUETA.sub(" ", etiqueta)   # amb espai: un enllaç de
            # dues línies («títol» + «subtítol» en dos <span>) ha de quedar com
            # dues frases, no com una paraula inventada que les enganxa.
            net = " ".join(net.split())
            if not net or any(e in net for e in excepcions):
                continue
            bones = regla.get(idioma, [])
            dolentes = (regla.get("prohibides") or {}).get(idioma, [])
            if net in bones:
                continue
            if net in dolentes:
                errors.append(f"vocabulari · {url} → {desti} · es diu «{net}» i s'ha de dir «{bones[0]}»")
                continue
            # Dins d'un text seguit, un enllaç pot dir el que li convingui:
            # «podeu consultar el calendari del vostre equip» és una frase, no
            # una etiqueta, i obligar-la a dir «Dies de partit» faria una
            # prosa absurda. La regla només val per al que fa d'etiqueta:
            # curt, sense puntuació de frase i començat en majúscula.
            paraules = net.split()
            es_etiqueta = (len(paraules) <= 5 and net[:1].isupper()
                           and not any(c in net for c in ".,;:!?"))
            if es_etiqueta:
                pendents.append(f"etiqueta-a-revisar · {url} → {desti} · es diu «{net}»")

    # --- Preguntes freqüents (i18n/faq.yml) ---------------------------------
    # Des del 23/08/2026 les preguntes freqüents no viuen a l'HTML sinó a la
    # seva font única, i per tant tampoc les veia aquest lint. Una pregunta
    # publicada en català i no traduïda és exactament la mateixa mena de
    # deute que una pàgina sense traduir.
    faq = ROOT / "i18n" / "faq.yml"
    if faq.exists():
        per_ruta = {r["ca"]: r for r in rutes if r.get("ca")}
        dades = yaml.safe_load(faq.read_text(encoding="utf-8")) or {}
        for e in dades.get("preguntes", []):
            ident = e.get("id", "?")
            if e.get("pendent"):
                pendents.append(
                    f"faq-sense-resposta · {ident} · espera: {e['pendent'].strip().splitlines()[0][:70]}")
                continue
            # Només compta com a deute si la pàgina existeix en aquell
            # idioma: si no, la feina és traduir la pàgina, no la pregunta,
            # i ja surt com a `sense-traduccio` més amunt.
            parella = per_ruta.get(e.get("pagina")) or {}
            for idioma in ("ca", "es", "en"):
                if idioma != "ca" and not parella.get(idioma):
                    continue
                tros = e.get(idioma) or {}
                if not (tros.get("q") and tros.get("r")):
                    pendents.append(
                        f"faq-sense-traduccio · {ident} · falta la versió {idioma}")

    return sorted(set(errors)), sorted(set(pendents))


def clau(linia):
    """La part estable d'un avís: el tipus i on és, sense el detall.

    El detall en queda fora a posta —la xifra de dies d'una traducció
    endarrerida canvia cada dia— però la pàgina i, quan cal, l'enllaç
    concret, hi són: així un error nou en una pàgina que ja en tenia un
    altre no passa desapercebut.
    """
    parts = linia.split(" · ")
    return " · ".join(parts[:2])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--nomes-errors", action="store_true")
    ap.add_argument("--actualitza-base", action="store_true",
                    help="desa els errors d'ara com a coneguts")
    args = ap.parse_args()

    errors, pendents = revisa()

    if args.actualitza_base:
        BASE.write_text(
            "# Errors que ja hi havia el dia que es va activar el lint.\n"
            "# La CI no s'atura per aquests; sí per qualsevol de nou.\n"
            "# Cada línia que s'arregli, s'esborra d'aquí.\n"
            + "".join(f"{clau(e)}\n" for e in errors), encoding="utf-8")
        print(f"{len(errors)} errors desats com a coneguts a {BASE.relative_to(ROOT)}")
        return 0

    coneguts = set()
    if BASE.exists():
        coneguts = {l.strip() for l in BASE.read_text(encoding="utf-8").splitlines()
                    if l.strip() and not l.startswith("#")}
    nous = [e for e in errors if clau(e) not in coneguts]

    def bloc(titol, linies):
        if not linies:
            return
        print(f"\n{titol} ({len(linies)})")
        per_tipus = defaultdict(list)
        for l in linies:
            per_tipus[l.split(" · ")[0]].append(l)
        for tipus, grup in sorted(per_tipus.items(), key=lambda kv: -len(kv[1])):
            print(f"\n  {tipus} — {len(grup)}")
            for l in grup[:15]:
                print("    " + l.split(" · ", 1)[1])
            if len(grup) > 15:
                print(f"    … i {len(grup) - 15} més")

    bloc("ERRORS NOUS", nous)
    if not args.nomes_errors:
        bloc("PENDENTS", pendents)
        if errors and not nous:
            print(f"\nErrors ja coneguts: {len(errors)} (a i18n/baseline.txt)")

    print(f"\n{'─' * 60}")
    print(f"errors nous: {len(nous)} · errors coneguts: {len(errors) - len(nous)} · pendents: {len(pendents)}")
    return 1 if nous else 0


if __name__ == "__main__":
    sys.exit(main())
