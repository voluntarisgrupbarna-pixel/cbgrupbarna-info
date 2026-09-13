#!/usr/bin/env python3
"""
Finestra horària del robot de partits · CB Grup Barna

GitHub Actions només sap programar en UTC i amb retards de fins a mitja hora,
i no pot saber a quina hora acaba l'últim partit del dia. Per això el
workflow update-partits.yml es dispara sovint (cada 30 minuts els caps de
setmana) i aquest script decideix, en hora de Barcelona i mirant
partits/data.json, si TOCA fer una passada i de quin tipus:

  · complet   → robot diari (hores, pistes, dates, partits nous i resultats).
                Es fa un cop al dia, amb el cron de les 06:00 UTC.
  · resultats → només afegir marcadors (update-resultats.py). Els dies amb
                partit, dues finestres:
                  1. MIGDIA: entre les 13:00 i les 14:00 (els partits del
                     matí ja s'han jugat).
                  2. FINAL DEL DIA: a partir que acaba l'últim partit del dia
                     (hora d'inici + DURADA_PARTIT), i es repeteix cada mitja
                     hora fins que tots els partits del dia tenen resultat o
                     s'acaba el cron. Així "quan acaben els partits" és
                     literal, encara que la federació trigui a penjar-los.
  · fitxer    → algú ha pujat la fitxa de resultats des del navegador
                (/partits/resultats-fcbq/ → partits/fcbq-resultats.html): el
                workflow s'ha disparat pel push i s'apliquen aquells resultats.
  · res       → fora de finestra, o no hi ha partits avui, o ja tenim tots
                els resultats. El workflow acaba sense fer res (uns segons).

Amb workflow_dispatch es pot forçar el mode des de la pestanya Actions.

Escriu `run`, `mode` i `motiu` a $GITHUB_OUTPUT (o els imprimeix si no hi és).
"""
import json
import os
import sys
from datetime import datetime, time, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "partits" / "data.json"
TZ = ZoneInfo("Europe/Madrid")

MIGDIA_INICI = time(13, 0)      # finestra del migdia (hora de Barcelona)
MIGDIA_FI = time(14, 0)
DURADA_PARTIT = timedelta(hours=1, minutes=45)   # partit + temps que la FCBQ tarda a penjar-lo
HORA_UTC_DIARI = 6              # cron del robot complet ("0 6 * * *")


def decideix(ara_local, ara_utc, event, mode_forcat, partits):
    """Torna (run, mode, motiu). Pura, per poder-la provar."""
    if event == "push":
        return True, "fitxer", "fitxa de resultats pujada des del navegador"
    if event == "workflow_dispatch":
        mode = mode_forcat if mode_forcat in ("complet", "resultats") else "complet"
        return True, mode, "llançat a mà"
    if ara_utc.hour == HORA_UTC_DIARI or (ara_utc.hour == HORA_UTC_DIARI + 1 and ara_utc.minute < 30):
        return True, "complet", "robot diari"
    avui = ara_local.date().isoformat()
    d_avui = [p for p in partits if p.get("data") == avui]
    if not d_avui:
        return False, "res", f"cap partit avui ({avui})"
    pendents = [p for p in d_avui if p.get("puntsLocal") is None]
    if not pendents:
        return False, "res", "tots els resultats d'avui ja són a la web"
    hora = ara_local.time()
    if MIGDIA_INICI <= hora < MIGDIA_FI:
        return True, "resultats", f"migdia · {len(pendents)} partits sense resultat"
    ultim = max(d_avui, key=lambda p: p.get("hora") or "00:00")
    h, m = (ultim.get("hora") or "00:00").split(":")
    fi_ultim = ara_local.replace(hour=int(h), minute=int(m), second=0, microsecond=0) + DURADA_PARTIT
    if ara_local >= fi_ultim:
        return True, "resultats", (f"final del dia · l'últim partit ({ultim.get('hora')}) ja ha acabat · "
                                   f"{len(pendents)} sense resultat")
    return False, "res", (f"fora de finestra · migdia {MIGDIA_INICI:%H:%M}-{MIGDIA_FI:%H:%M}, "
                          f"final del dia a partir de {fi_ultim:%H:%M}")


def main():
    ara_utc = datetime.now(ZoneInfo("UTC"))
    ara_local = ara_utc.astimezone(TZ)
    event = os.environ.get("GITHUB_EVENT_NAME", "schedule")
    mode_forcat = os.environ.get("INPUT_MODE", "").strip().lower()
    try:
        partits = json.loads(DATA.read_text(encoding="utf-8")).get("partits", [])
    except Exception as exc:
        print(f"[finestra] no es pot llegir data.json ({exc}) — passada completa per seguretat")
        partits, event = [], "workflow_dispatch"
    run, mode, motiu = decideix(ara_local, ara_utc, event, mode_forcat, partits)
    print(f"[finestra] {ara_local:%A %d/%m %H:%M} Barcelona · run={str(run).lower()} mode={mode} · {motiu}")
    out = os.environ.get("GITHUB_OUTPUT")
    linies = f"run={str(run).lower()}\nmode={mode}\nmotiu={motiu}\n"
    if out:
        with open(out, "a", encoding="utf-8") as f:
            f.write(linies)
    else:
        print(linies, end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
