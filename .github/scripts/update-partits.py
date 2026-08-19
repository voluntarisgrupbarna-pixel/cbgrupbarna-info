#!/usr/bin/env python3
"""
Robot FCBQ · CB Grup Barna (club 24)
Cada dia baixa el calendari global del club de basquetcatala.cat, el compara
amb el que ja teníem i actualitza partits/data.json amb els canvis: hora,
pista, data o resultat. Cada canvi es marca al propi partit (camp "avis")
perquè la app mostri un rètol "MODIFICAT" durant uns dies, i queda registrat
a partits/canvis.json com a historial per a l'avís diari.

Disseny defensiu: si la federació no respon, bloqueja el robot o el format
canvia i no es troba cap partit, surt amb codi 0 SENSE tocar res — la via
manual (pujar el PDF a /partits/ → Gestió) sempre segueix funcionant.
"""
import json, re, sys, unicodedata, urllib.request
from datetime import date, timedelta
from pathlib import Path

CLUB_ID = 24
ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "partits" / "data.json"
CANVIS = ROOT / "partits" / "canvis.json"
CLUB_RE = re.compile(r"(?:[A-Z0-9]+-)?C[.,]?\s*B[.,]?\s*GRUP\s*BARNA(?:\s+[A-Z0-9]{1,3})?", re.I)
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")
DIES_AVIS = 7          # quants dies es manté el rètol "MODIFICAT" a la fitxa

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "ca,es;q=0.8"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")

def strip_tags(html):
    html = re.sub(r"<script.*?</script>|<style.*?</style>", " ", html, flags=re.S | re.I)
    html = re.sub(r"<br\s*/?>|</(td|th|tr|div|p|li|h\d)>", "\n", html, flags=re.I)
    html = re.sub(r"<[^>]+>", " ", html)
    html = html.replace("&nbsp;", " ").replace("&amp;", "&")
    return [re.sub(r"\s+", " ", l).strip() for l in html.splitlines() if l.strip()]

DATE_RE = re.compile(r"(\d{2})[-/](\d{2})[-/](\d{4})\s+(\d{2}:\d{2})")
SCORE_RE = re.compile(r"(\d{1,3})\s*[-–]\s*(\d{1,3})")

def parse_lines(lines):
    """Mateixa lògica que el parser del PDF: data+hora → partit → categoria → pista."""
    out = []
    for i, line in enumerate(lines):
        dm = DATE_RE.search(line)
        if not dm:
            continue
        window = lines[i:i + 6]
        partit = categoria = pista = adreca = ""
        punts = None
        for cand in window[0:4]:
            c = cand[dm.end():].strip() if cand is line else cand
            if CLUB_RE.search(c) and " - " in c and not c.lower().startswith("instal"):
                partit = c
                break
        if not partit:
            continue
        for cand in window:
            if cand.lower().startswith("instal"):
                inst = cand.split(":", 1)[-1].strip()
                k = inst.find(" (")
                pista, adreca = (inst[:k].strip(), inst[k + 2:].rstrip(")").strip()) if k > 0 else (inst, "")
            elif re.search(r"COPA|LLIGA|CAMPIONAT|NIVELL|PREFERENT|INTERTERRITORIAL", cand, re.I) and cand != partit:
                categoria = categoria or cand
        sm = SCORE_RE.search(partit)
        if sm and not CLUB_RE.search(sm.group(0)):
            punts = (int(sm.group(1)), int(sm.group(2)))
            partit = partit[:sm.start()].strip(" -")
        mh = re.match(rf"^({CLUB_RE.pattern})\s+-\s+(.+)$", partit, re.I)
        ma = re.match(rf"^(.+?)\s+-\s+({CLUB_RE.pattern})$", partit, re.I)
        if mh:
            local, visitant, casa = mh.group(1), mh.group(2), True
        elif ma:
            local, visitant, casa = ma.group(1), ma.group(2), False
        else:
            continue
        dd, mm, yyyy, hora = dm.groups()
        out.append({
            "clubNom": (local if casa else visitant).strip(),
            "data": f"{yyyy}-{mm}-{dd}", "hora": hora, "local": local.strip(),
            "visitant": visitant.strip(), "casa": casa, "categoria": categoria,
            "pista": pista, "adreca": adreca,
            "puntsLocal": punts[0] if punts else None,
            "puntsVisitant": punts[1] if punts else None,
        })
    return out

def slugify(s):
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")

CAMPS_SEGUITS = [("data", "Data"), ("hora", "Hora"), ("pista", "Pista")]

def main():
    urls = [f"https://www.basquetcatala.cat/partits/calendari_club_global/{CLUB_ID}",
            f"https://www.basquetcatala.cat/partits/calendari_club_mensual/{CLUB_ID}"]
    scraped = []
    for url in urls:
        try:
            html = fetch(url)
        except Exception as exc:
            print(f"[robot] no s'ha pogut baixar {url}: {exc}")
            continue
        found = parse_lines(strip_tags(html))
        print(f"[robot] {url}: {len(found)} partits detectats")
        scraped += found
    avui = date.today().isoformat()
    if not scraped:
        print("[robot] cap partit trobat — no es toca data.json (via PDF segueix activa)")
        _actualitza_canvis([], avui, contactat=False)
        return 0

    data = json.loads(DATA.read_text(encoding="utf-8"))
    by_cat = {(e.get("competicio") or "").upper(): e for e in data["equips"]}
    by_club = {(e.get("clubNom") or "").upper(): e for e in data["equips"] if e.get("clubNom")}
    index = {p["id"]: p for p in data["partits"]}
    added = updated = results = 0
    canvis_avui = []

    for s in scraped:
        # la categoria (competicio) es unica per equip; clubNom ("C.B GRUP
        # BARNA A"/"B") es comparteix entre fins a 8 equips diferents (un
        # per genere/categoria amb la mateixa lletra), aixi que NO pot anar
        # primer o assigna partits a l'equip equivocat en silenci.
        eq = by_cat.get(s["categoria"].upper()) or by_club.get(s.get("clubNom", "").upper())
        if not eq:
            if not s["categoria"]:
                continue
            eq = {"id": slugify(s["categoria"] + " " + s.get("clubNom", "")[-1:]),
                  "nom": s["categoria"].title(), "curt": s["categoria"][:14], "emoji": "🏀",
                  "competicio": s["categoria"], "clubNom": s.get("clubNom", ""),
                  "posicio": None, "equipsGrup": None, "notaLliga": ""}
            data["equips"].append(eq)
            by_cat[s["categoria"].upper()] = eq
            if eq["clubNom"]:
                by_club[eq["clubNom"].upper()] = eq
        pid = f"{eq['id']}_{s['data']}"
        if pid in index:
            p = index[pid]
            canviats = [(label, p.get(camp), s[camp]) for camp, label in CAMPS_SEGUITS
                        if s.get(camp) and p.get(camp) != s[camp]]
            if canviats:
                for label, abans, despres in canviats:
                    canvis_avui.append({"equip": eq["nom"], "rival": s["visitant"] if s["casa"] else s["local"],
                                         "camp": label, "abans": abans, "despres": despres, "partitId": pid})
                p["data"], p["hora"], p["pista"], p["adreca"] = s["data"], s["hora"], s["pista"], s["adreca"]
                p["avis"] = {"detectat": avui, "expira": (date.today() + timedelta(days=DIES_AVIS)).isoformat(),
                             "resum": " · ".join(f"{l}: {a or 'sense confirmar'} → {d}" for l, a, d in canviats)}
                updated += 1
            if s["puntsLocal"] is not None and p.get("puntsLocal") is None:
                p["puntsLocal"], p["puntsVisitant"], p["estat"] = s["puntsLocal"], s["puntsVisitant"], "jugat"
                results += 1
        else:
            s.update({"id": pid, "equipId": eq["id"], "estat": "pendent"})
            data["partits"].append(s)
            index[pid] = s
            added += 1
            canvis_avui.append({"equip": eq["nom"], "rival": s["visitant"] if s["casa"] else s["local"],
                                 "camp": "Nou partit", "abans": "—", "despres": f"{s['data']} {s['hora']}", "partitId": pid})

    # neteja els avisos caducats perquè el fitxer no creixi indefinidament
    for p in data["partits"]:
        if p.get("avis") and p["avis"]["expira"] < avui:
            del p["avis"]

    _actualitza_canvis(canvis_avui, avui, contactat=True)

    if not (added or updated or results):
        print("[robot] res de nou — no es fa commit")
        return 0
    data["partits"].sort(key=lambda p: (p["data"], p["hora"]))
    data["lastUpdate"] = avui
    DATA.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[robot] OK → {added} nous, {updated} actualitzats, {results} resultats")
    for c in canvis_avui:
        print(f"    · {c['equip']} vs {c['rival']}: {c['camp']} {c['abans']} → {c['despres']}")
    return 0

def _actualitza_canvis(canvis_avui, avui, contactat):
    """Manté un historial curt (30 dies) dels canvis detectats, per a la app i l'avís diari."""
    hist = {"ultimaComprovacio": avui, "connexioOk": contactat, "canvis": []}
    if CANVIS.exists():
        try:
            hist_previ = json.loads(CANVIS.read_text(encoding="utf-8"))
            hist["canvis"] = hist_previ.get("canvis", [])
        except Exception:
            pass
    if canvis_avui:
        hist["canvis"].append({"data": avui, "items": canvis_avui})
    fa_30_dies = (date.today() - timedelta(days=30)).isoformat()
    hist["canvis"] = [c for c in hist["canvis"] if c["data"] >= fa_30_dies]
    CANVIS.write_text(json.dumps(hist, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

if __name__ == "__main__":
    sys.exit(main())
