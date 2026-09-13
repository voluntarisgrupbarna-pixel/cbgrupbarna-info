#!/usr/bin/env python3
"""
Robot de RESULTATS · CB Grup Barna (club 24)

Complement del robot diari (update-partits.py). Aquest només fa una cosa:
recollir els marcadors de la fitxa "Resultats de l'última setmana" de la
pàgina del club a la FCBQ (https://www.basquetcatala.cat/club/24 → botó
Resultats, que crida POST /club/24/resultats) i AFEGIR-LOS als partits que
ja hi ha a partits/data.json.

No toca res més: ni hores, ni pistes, ni dates, ni afegeix partits nous, ni
marca cap "MODIFICAT". La fitxa de calendari de cada equip
(partits/calendaris/) es reaprofita tal com està i només s'hi omplen els
resultats — el generador la torna a dibuixar només per als equips que han
rebut un marcador nou. Els canvis de calendari els segueix portant el robot
diari al matí.

Es llança els caps de setmana al migdia i quan acaba l'últim partit del dia
(vegeu finestra-partits.py i update-partits.yml). Si la federació encara no
ha penjat un resultat, simplement no hi ha res nou i no es fa cap commit.

També accepta la fitxa de resultats ENGANXADA des del navegador d'Ana:
    python update-resultats.py --fitxer partits/fcbq-resultats.html
Aquest fitxer el puja la pàgina /partits/resultats-fcbq/ (via el marcador
"Resultats → web" des de basquetcatala.cat), perquè el reCAPTCHA de la FCBQ
no deixa passar navegadors automatitzats però sí el d'una persona.

Defensiu com el diari: si no s'hi pot arribar o el format canvia, surt amb
codi 0 sense tocar res.
"""
import html as htmlmod
import json
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fcbq_client  # noqa: E402

CLUB_ID = 24
ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "partits" / "data.json"
CANVIS = ROOT / "partits" / "canvis.json"
URL_RESULTATS = f"https://www.basquetcatala.cat/club/{CLUB_ID}/resultats"

FILA_RE = re.compile(r'<div id="fila">(.*?)(?=<div id="fila">|<div class="col-md-12" id="lineSpace">|$)', re.S)
EQUIP_RE = re.compile(r'class="teamNameLink"[^>]*>(.*?)</a>', re.S)
HORA_RE = re.compile(r'class="time2"[^>]*>\s*(\d{2})-(\d{2})-(\d{4})\s+(\d{2}:\d{2})\s*<')
SCORE_RE = re.compile(r'class="score">\s*([^<]*?)\s*<', re.S)
CAT_RE = re.compile(r'class="fs-12">(.*?)</div>', re.S)


def _net(s):
    return re.sub(r"\s+", " ", htmlmod.unescape(s)).strip()


def parse_resultats(html):
    """Llista de dicts {data, hora, local, visitant, categoria, puntsLocal, puntsVisitant}.
    puntsLocal/puntsVisitant són None si el partit encara no té marcador ("-")."""
    out = []
    for m in FILA_RE.finditer(html):
        bloc = m.group(1)
        equips = [_net(e) for e in EQUIP_RE.findall(bloc)]
        hm = HORA_RE.search(bloc)
        cm = CAT_RE.search(bloc)
        scores = SCORE_RE.findall(bloc)
        if len(equips) < 2 or not hm or not cm:
            continue
        dd, mm, yyyy, hora = hm.groups()
        punts = [None, None]
        if len(scores) >= 2:
            for i in range(2):
                s = _net(scores[i])
                punts[i] = int(s) if s.isdigit() else None
        out.append({"data": f"{yyyy}-{mm}-{dd}", "hora": hora, "local": equips[0], "visitant": equips[1],
                    "categoria": _net(cm.group(1)), "puntsLocal": punts[0], "puntsVisitant": punts[1]})
    return out


def _norm(s):
    return re.sub(r"[\s.,]+", "", (s or "").upper())


def aplica_resultats(data, resultats):
    """Escriu els marcadors nous dins data (in place). Torna la llista d'aplicats."""
    by_cat = {(e.get("competicio") or "").upper(): e for e in data["equips"]}
    index = {p["id"]: p for p in data["partits"]}
    aplicats = []
    for r in resultats:
        if r["puntsLocal"] is None or r["puntsVisitant"] is None:
            continue  # encara sense marcador
        eq = by_cat.get(r["categoria"].upper())
        if not eq:
            print(f"    · sense equip per a «{r['categoria']}» — s'omet")
            continue
        p = index.get(f"{eq['id']}_{r['data']}")
        if not p:
            # el partit s'ha pogut moure de dia: busca'l pel rival dins la mateixa setmana
            cands = [q for q in data["partits"] if q["equipId"] == eq["id"] and q.get("puntsLocal") is None
                     and _norm(q["local"]) == _norm(r["local"]) and _norm(q["visitant"]) == _norm(r["visitant"])]
            p = cands[0] if len(cands) == 1 else None
        if not p:
            print(f"    · {eq['nom']} {r['data']}: partit no trobat a data.json — s'omet (el robot diari l'afegirà)")
            continue
        if p.get("puntsLocal") is not None:
            continue  # ja el teníem
        # comprova que local/visitant coincideixen amb el que tenim; si estan
        # girats (la FCBQ ha canviat la pista), gira els punts perquè el
        # marcador quedi ben posat respecte de local/visitant de data.json
        pl, pv = r["puntsLocal"], r["puntsVisitant"]
        if _norm(p["local"]) != _norm(r["local"]) and _norm(p["local"]) == _norm(r["visitant"]):
            pl, pv = pv, pl
        p["puntsLocal"], p["puntsVisitant"], p["estat"] = pl, pv, "jugat"
        aplicats.append((eq["nom"], p))
    return aplicats


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    avui = date.today().isoformat()
    if len(argv) >= 2 and argv[0] == "--fitxer":
        fitxer = ROOT / argv[1]
        html = fitxer.read_text(encoding="utf-8", errors="replace") if fitxer.exists() else ""
        print(f"[resultats] fitxa enganxada des del navegador: {argv[1]} ({len(html)} caràcters)")
    else:
        html = fcbq_client.fetch(URL_RESULTATS, "POST")
        fcbq_client.close()
    if not html:
        print("[resultats] sense resposta de la FCBQ — no es toca res")
        _marca_comprovacio(avui, contactat=False)
        return 0
    resultats = parse_resultats(html)
    print(f"[resultats] {len(resultats)} partits a la fitxa de la setmana, "
          f"{sum(1 for r in resultats if r['puntsLocal'] is not None)} amb marcador")
    if not resultats:
        print("[resultats] format no reconegut — no es toca res")
        _marca_comprovacio(avui, contactat=False)
        return 0
    data = json.loads(DATA.read_text(encoding="utf-8"))
    aplicats = aplica_resultats(data, resultats)
    _marca_comprovacio(avui, contactat=True)
    if not aplicats:
        print("[resultats] cap marcador nou — no es fa commit")
        return 0
    data["lastUpdate"] = avui
    DATA.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[resultats] OK → {len(aplicats)} resultats nous")
    for nom, p in aplicats:
        print(f"    · {nom}: {p['local']} {p['puntsLocal']}-{p['puntsVisitant']} {p['visitant']} ({p['data']})")
    return 0


def _marca_comprovacio(avui, contactat):
    """Només actualitza la data de l'última comprovació a canvis.json (l'historial no es toca)."""
    hist = {"ultimaComprovacio": avui, "connexioOk": contactat, "canvis": []}
    if CANVIS.exists():
        try:
            hist["canvis"] = json.loads(CANVIS.read_text(encoding="utf-8")).get("canvis", [])
        except Exception:
            pass
    CANVIS.write_text(json.dumps(hist, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())
