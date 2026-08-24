#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comprova que un canvi toca les tres versions d'una pàgina, no només una.

Per què existeix: la web viu en català, castellà i anglès, i cada traducció és
un fitxer independent. Fins ara res no impedia pujar un canvi que arreglés la
pàgina catalana i deixés les altres dues dient una altra cosa. El lint ho
detectava, però dies després i mirant dates de commit. Això ho detecta ABANS
de fusionar, mirant què toca el canvi.

La regla és senzilla: si toques una pàgina que té traduccions declarades a
i18n/routes.yml, has de tocar les tres. Si n'esborres una, has d'esborrar les
tres.

  python3 scripts/i18n-paritat.py --des origin/main --fins HEAD
  python3 scripts/i18n-paritat.py --fitxers a.html b.html
  python3 scripts/i18n-paritat.py --tot        # audita el repositori sencer

Torna 1 si troba parelles trencades, 0 si tot va junt.

Excepcions legítimes: hi ha canvis que només toquen un idioma amb tota la raó
—corregir una falta d'ortografia que només hi ha en castellà, per exemple. Per
a aquests casos, posa el motiu a i18n/excepcions-paritat.yml. No hi ha manera
de saltar-se-ho sense deixar escrit per què.
"""
import argparse, os, re, subprocess, sys

try:
    import yaml
except ImportError:
    sys.exit("Cal pyyaml: pip install pyyaml")

ARREL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDIOMES = ("ca", "es", "en")

RE_REDIR = re.compile(r'http-equiv=["\']refresh', re.I)


def ruta_de_fitxer(f):
    """De 'es/blog/x/index.html' a '/es/blog/x/'."""
    u = "/" + f.replace(os.sep, "/")
    return u[: -len("index.html")] if u.endswith("/index.html") else u


def fitxer_de_ruta(u):
    """De '/es/blog/x/' a 'es/blog/x/index.html'."""
    p = u.lstrip("/")
    return p if p.endswith(".html") else os.path.join(p, "index.html")


def carrega_mapa():
    with open(os.path.join(ARREL, "i18n", "routes.yml"), encoding="utf-8") as fh:
        m = yaml.safe_load(fh)
    trios, de_ruta = [], {}
    for r in m.get("rutes", []):
        trio = {i: r.get(i) for i in IDIOMES}
        if not trio["ca"]:
            continue
        trios.append(trio)
        for i in IDIOMES:
            if trio[i]:
                de_ruta[trio[i]] = trio
    return trios, de_ruta


def carrega_excepcions():
    p = os.path.join(ARREL, "i18n", "excepcions-paritat.yml")
    if not os.path.exists(p):
        return {}
    with open(p, encoding="utf-8") as fh:
        d = yaml.safe_load(fh) or {}
    return {e["ruta"]: e.get("motiu", "") for e in (d.get("nomes_un_idioma") or [])}


def git(*args):
    return subprocess.run(["git", *args], cwd=ARREL, capture_output=True,
                          text=True, check=False).stdout.splitlines()


def es_redireccio(f):
    p = os.path.join(ARREL, f)
    if not os.path.exists(p):
        return False
    with open(p, encoding="utf-8", errors="replace") as fh:
        return bool(RE_REDIR.search(fh.read(4000)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--des")
    ap.add_argument("--fins", default="HEAD")
    ap.add_argument("--fitxers", nargs="*")
    ap.add_argument("--tot", action="store_true")
    args = ap.parse_args()

    trios, de_ruta = carrega_mapa()
    excepcions = carrega_excepcions()

    if args.tot:
        return audita_tot(trios, excepcions)

    if args.fitxers:
        tocats = [f for f in args.fitxers if f.endswith(".html")]
    elif args.des:
        tocats = [f for f in git("diff", "--name-only", "--diff-filter=AMD",
                                 args.des, args.fins, "--", "*.html")]
    else:
        sys.exit("Cal --des, --fitxers o --tot.")

    # De fitxer tocat a trio afectat, amb quins idiomes s'han tocat.
    afectats = {}
    for f in tocats:
        u = ruta_de_fitxer(f)
        trio = de_ruta.get(u)
        if not trio:
            continue                      # no és una pàgina amb traduccions
        if es_redireccio(f):
            continue                      # els reenviaments no porten text
        clau = trio["ca"]
        afectats.setdefault(clau, {"trio": trio, "tocats": set()})
        for i in IDIOMES:
            if trio[i] == u:
                afectats[clau]["tocats"].add(i)

    problemes = []
    for clau, d in sorted(afectats.items()):
        trio, tocats_idi = d["trio"], d["tocats"]
        falten = [i for i in IDIOMES if trio[i] and i not in tocats_idi]
        if not falten:
            continue
        if clau in excepcions:
            print(f"  ✓ {clau} · només {'+'.join(sorted(tocats_idi))} · "
                  f"excepció escrita: {excepcions[clau]}")
            continue
        problemes.append((clau, trio, sorted(tocats_idi), falten))

    if not problemes:
        print(f"Paritat correcta · {len(afectats)} pàgines tocades, "
              "totes en els tres idiomes.")
        return 0

    print(f"PARITAT TRENCADA · {len(problemes)} pàgines tocades en un idioma "
          "i no en els altres\n")
    for clau, trio, tocats_idi, falten in problemes:
        print(f"  {clau}")
        print(f"    s'ha tocat:  {', '.join(tocats_idi)}")
        for i in falten:
            print(f"    falta:       {i} → {trio[i]}")
        print()

    print("Com es tanca:")
    print("  python3 scripts/i18n-extreu.py <ruta-catalana> es en")
    print("  # omplir i18n/feina/{es,en}/<pàgina>.json")
    print("  python3 scripts/i18n-munta.py <ruta-catalana> es")
    print("  python3 scripts/i18n-munta.py <ruta-catalana> en")
    print("  python3 scripts/i18n-hreflang.py && python3 scripts/build-sitemap.py")
    print()
    print("Si el canvi només ha de ser en un idioma, escriu el motiu a")
    print("i18n/excepcions-paritat.yml i torna-ho a provar.")
    return 1


def audita_tot(trios, excepcions):
    """Mira tot el repositori: quina versió és més vella que el seu original."""
    def data(u):
        f = fitxer_de_ruta(u)
        if not os.path.exists(os.path.join(ARREL, f)):
            return None
        s = git("log", "-1", "--format=%ct", "--no-renames", "--", f)
        return int(s[0]) if s else None

    endarrerides = []
    for trio in trios:
        d_ca = data(trio["ca"])
        if d_ca is None:
            continue
        for i in ("es", "en"):
            if not trio[i]:
                continue
            d = data(trio[i])
            if d is None:
                endarrerides.append((trio["ca"], i, trio[i], "no existeix"))
            elif d < d_ca:
                dies = (d_ca - d) // 86400
                if dies >= 1:
                    endarrerides.append((trio["ca"], i, trio[i], f"{dies} dies més vella"))

    if not endarrerides:
        print(f"Tot al dia · {len(trios)} pàgines, cap traducció endarrerida.")
        return 0

    print(f"TRADUCCIONS ENDARRERIDES · {len(endarrerides)}\n")
    for ca, i, d, per_que in endarrerides:
        marca = "  ✓" if ca in excepcions else "   "
        print(f"{marca} {ca} → {i}: {d} · {per_que}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
