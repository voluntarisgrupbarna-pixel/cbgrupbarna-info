"""Qui juga contra qui, amb l'escut de cadascú.

Resol el nom d'un rival tal com el escriu el calendari de la FCBQ
(«C.B. SANTFELIUENC B», «KIDS&US MANRESA U13») cap al seu escut de
partits/logos/clubs/. El fan servir el generador de fitxes d'equip i
qualsevol altra peça que hagi de pintar un partit.

L'ordre de resolució és el mateix que el de l'app de /partits/:

  1. map.json — excepcions manuals, rival exacte → escut. Mana sempre.
  2. alias.json — l'inventari d'àlies del calendari FCBQ → escut.
  3. Emparellament automàtic pel nom de fitxer, en dues passades:
     el nom compactat del fitxer dins del nom del rival, i si no,
     els tokens significatius del fitxer dins dels del rival.

A cada pas es prova també el nom del rival SENSE els sufixos d'equip
(«B», «1A», «U13», «2012»...): el club és el mateix i l'escut també.

Qui no resol, torna None: el que pinta decideix el substitut (les
inicials, mai l'escut d'un altre).
"""
from __future__ import annotations

import json
import os
import re
import unicodedata
from pathlib import Path

ARREL = Path(__file__).resolve().parent.parent
LOGOS = ARREL / "partits" / "logos"

# Paraules que no distingeixen un club d'un altre: no valen com a prova
# d'emparellament a la passada de tokens.
_BUIDES = {"CLUB", "BASQUET", "BASKET", "CB", "CBF", "AE", "UE", "AB", "BC",
           "A", "B", "C", "E", "U"}

_SUFIX = re.compile(r"[A-Z]|\d[A-Z]?|[A-Z]?\d{1,4}|U\d{2}")


def _norm(s: str) -> str:
    s = unicodedata.normalize("NFD", s or "")
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^A-Z0-9]+", " ", s.upper()).strip()


def _compacta(s: str) -> str:
    return _norm(s).replace(" ", "")


class Escuts:
    def __init__(self) -> None:
        def llegeix(nom):
            f = LOGOS / nom
            return json.loads(f.read_text(encoding="utf-8")) if f.exists() else {}

        excepcions = {k: v for k, v in llegeix("map.json").items() if not k.startswith("_")}
        alias = llegeix("alias.json").get("alias", {})
        fitxers = llegeix("index.json").get("fitxers", [])

        self._excepcions = {_compacta(k): v for k, v in excepcions.items()}
        self._alias = {_compacta(k): v for k, v in alias.items()}
        self._fitxers = []
        for f in fitxers:
            base = os.path.splitext(os.path.basename(f))[0].replace("_", " ")
            self._fitxers.append((f, _compacta(base),
                                  set(_norm(base).split()) - _BUIDES))
        self._cache: dict[str, str | None] = {}

    def _variants(self, nom: str) -> list[str]:
        n = _norm(nom)
        vs = [n]
        toks = n.split()
        while toks and _SUFIX.fullmatch(toks[-1]):
            toks = toks[:-1]
            if toks:
                vs.append(" ".join(toks))
        return vs

    def escut(self, rival: str) -> str | None:
        """Ruta de l'escut relativa a /partits/ (p. ex.
        'logos/clubs/cb_boet_mataro.png'), o None si no n'hi ha."""
        if rival in self._cache:
            return self._cache[rival]
        res = None
        variants = self._variants(rival)
        for v in variants:
            c = _compacta(v)
            if c in self._excepcions:
                res = self._excepcions[c]; break
            if c in self._alias:
                res = self._alias[c]; break
        if res is None:
            for v in variants:
                c = _compacta(v)
                millors = [(f, fc) for f, fc, _ in self._fitxers if fc and fc in c]
                if millors:
                    res = max(millors, key=lambda x: len(x[1]))[0]; break
        if res is None:
            n_toks = set(_norm(rival).split())
            millors = [(f, len(ft)) for f, _, ft in self._fitxers if ft and ft <= n_toks]
            if millors:
                res = max(millors, key=lambda x: x[1])[0]
        self._cache[rival] = res
        return res


def inicials(nom: str) -> str:
    """Dues lletres per al substitut quan no hi ha escut."""
    toks = [t for t in _norm(nom).split() if t not in _BUIDES and not t.isdigit()]
    if not toks:
        toks = _norm(nom).split() or ["?"]
    if len(toks) == 1:
        return toks[0][:2]
    return toks[0][0] + toks[1][0]


if __name__ == "__main__":
    import sys
    e = Escuts()
    data = json.loads((ARREL / "partits" / "data.json").read_text(encoding="utf-8"))
    rivals = sorted({(p["visitant"] if p["casa"] else p["local"]) for p in data["partits"]})
    sense = 0
    for r in rivals:
        f = e.escut(r)
        if not f:
            sense += 1
            print(f"  sense escut: {r}  (aniria amb «{inicials(r)}»)")
        elif "-v" in sys.argv:
            print(f"  {r} → {f}")
    print(f"{len(rivals) - sense}/{len(rivals)} rivals amb escut")
