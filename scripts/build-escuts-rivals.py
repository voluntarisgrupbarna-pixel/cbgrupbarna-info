#!/usr/bin/env python3
"""Escriu partits/logos/rivals.json: cada rival de data.json -> el seu escut.

La pagina /partits/ pinta el cap de setmana amb JavaScript i necessita
saber l'escut de cada rival sense reimplementar el resolutor: aquest
script el precalcula amb scripts/escuts_partits.py (el mateix de les
fitxes d'equip i de calendari) i deixa el resultat com a JSON.

El crida update-partits.yml cada dia, just despres de refrescar
data.json: un rival nou al calendari surt aqui a la seguent passada.

Format:  { "CB BOET MATARO 2012": "logos/clubs/cb_boet_mataro.png",
           "CB MOLLET B": null, ... }
Un null vol dir "sense escut a l'inventari": la pagina hi pinta les
inicials, mai l'escut d'un altre.
"""
import importlib.util
import json
from pathlib import Path

ARREL = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("escuts_partits", ARREL / "scripts" / "escuts_partits.py")
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)

data = json.loads((ARREL / "partits" / "data.json").read_text(encoding="utf-8"))
escuts = _mod.Escuts()
rivals = {}
for p in data.get("partits", []):
    nom = p["visitant"] if p["casa"] else p["local"]
    if nom not in rivals:
        rivals[nom] = escuts.escut(nom)

sortida = ARREL / "partits" / "logos" / "rivals.json"
sortida.write_text(json.dumps(dict(sorted(rivals.items())), ensure_ascii=False, indent=1) + "\n",
                   encoding="utf-8")
amb = sum(1 for v in rivals.values() if v)
print(f"[rivals] {amb}/{len(rivals)} rivals amb escut → {sortida.relative_to(ARREL)}")
