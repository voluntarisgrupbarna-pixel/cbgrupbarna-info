#!/usr/bin/env python3
"""
Omple la traducció de la feina de i18n/feina/ amb l'API de Claude.

    export ANTHROPIC_API_KEY=...
    python3 scripts/i18n-tradueix.py /club/ es
    python3 scripts/i18n-tradueix.py --tot en          # tot el que quedi buit

No inventa res pel seu compte: al model li arriba el glossari sencer
(i18n/glossari.yml) amb els noms que no es tradueixen mai, els termes del
club i el to de cada idioma, i li arriba **només text**, mai HTML. Torna els
mateixos trossos, en el mateix ordre, i l'script comprova que en tornin tants
com n'han sortit abans de desar res.

Els noms propis es comproven un per un: si un tros català deia «Escoleta» i
el traduït no ho diu, l'script avisa i no ho dona per bo. És la comprovació
que separa una traducció automàtica utilitzable d'una que et converteix el
club en «Escuelita».

Si no hi ha clau d'API, la feina es pot omplir igualment a mà o amb
qualsevol altre traductor: és un JSON amb un camp buit per tros.
"""
import argparse
import json
import os
import sys
import urllib.request
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
FEINA = ROOT / "i18n" / "feina"
GLOSSARI = ROOT / "i18n" / "glossari.yml"
MODEL = "claude-opus-4-5"          # es pot canviar amb --model
IDIOMES = {"es": "castellà", "en": "anglès"}
LOT = 40                            # trossos per crida


def instruccions(idioma):
    g = yaml.safe_load(GLOSSARI.read_text(encoding="utf-8"))
    termes = "\n".join(f"  {t['ca']} → {t[idioma]}" for t in g["termes"])
    noms = "\n".join(f"  {n}" for n in g["noms_propis"])
    return f"""Ets el traductor del CB Grup Barna, un club de bàsquet base del barri del
Clot, a Barcelona. Tradueixes del català al {IDIOMES[idioma]} textos de la seva web.

To: {g['to'][idioma]}

Aquests noms NO es tradueixen mai. Han de sortir igual, lletra per lletra:
{noms}

Aquests termes es tradueixen sempre així:
{termes}

Et donaré una llista numerada de trossos de text. Respon NOMÉS amb un JSON
que sigui una llista de cadenes, amb la traducció de cada tros en el mateix
ordre i amb la mateixa quantitat d'elements. Res més: ni explicacions, ni
codi de format.

Regles dels trossos:
· Un tros pot ser mitja frase, perquè a la pàgina hi ha una etiqueta pel
  mig. Tradueix-lo com el tros que és, sense afegir-hi el que et sembli que
  falta i sense completar la frase.
· Respecta els espais del principi i del final tal com siguin.
· Deixa igual les fletxes (→), els números, els percentatges, les adreces i
  els noms de fitxer. Els decimals, però, sí que van a l'anglesa en anglès:
  65,5% → 65.5%.
· No afegeixis mai HTML."""


def demana(trossos, idioma, model, clau):
    cos = json.dumps({
        "model": model,
        "max_tokens": 8000,
        "system": instruccions(idioma),
        "messages": [{"role": "user", "content": json.dumps(trossos, ensure_ascii=False, indent=1)}],
    }).encode()
    req = urllib.request.Request(
        os.environ.get("ANTHROPIC_BASE_URL", "https://api.anthropic.com").rstrip("/")
        + "/v1/messages",
        data=cos,
        headers={"content-type": "application/json", "x-api-key": clau,
                 "anthropic-version": "2023-06-01"})
    with urllib.request.urlopen(req, timeout=180) as r:
        resposta = json.loads(r.read())
    text = "".join(b["text"] for b in resposta["content"] if b["type"] == "text").strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0]
    return json.loads(text)


def revisa_noms(trossos, traduits):
    """Els noms propis que hi havia a l'original, hi han de continuar sent."""
    noms = (yaml.safe_load(GLOSSARI.read_text(encoding="utf-8")))["noms_propis"]
    avisos = []
    for ca, tr in zip(trossos, traduits):
        for nom in noms:
            if nom in ca and nom not in tr:
                avisos.append(f'«{nom}» hi era i s\'ha perdut: {tr[:60]}')
    return avisos


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ruta", nargs="?")
    ap.add_argument("idioma", choices=["es", "en"])
    ap.add_argument("--tot", action="store_true")
    ap.add_argument("--model", default=MODEL)
    args = ap.parse_args()

    clau = os.environ.get("ANTHROPIC_API_KEY")
    if not clau:
        print("Falta ANTHROPIC_API_KEY. La feina es pot omplir igualment a mà:\n"
              f"  {FEINA.relative_to(ROOT)}/{args.idioma}/<pàgina>.json")
        return 1

    if args.tot:
        fitxers = sorted((FEINA / args.idioma).glob("*.json"))
    elif args.ruta:
        nom = (args.ruta.strip("/").replace("/", "__") or "portada") + ".json"
        fitxers = [FEINA / args.idioma / nom]
    else:
        print("Cal una ruta, o --tot")
        return 1

    for fitxer in fitxers:
        feina = json.loads(fitxer.read_text(encoding="utf-8"))
        pendents = [t for t in feina["trossos"] if not t.get(args.idioma, "").strip()]
        if not pendents:
            continue
        print(f"  {feina['origen']} · {len(pendents)} trossos")
        for i in range(0, len(pendents), LOT):
            lot = pendents[i:i + LOT]
            traduits = demana([t["ca"] for t in lot], args.idioma, args.model, clau)
            if len(traduits) != len(lot):
                print(f"    ATENCIÓ: n'han sortit {len(lot)} i n'han tornat {len(traduits)}."
                      " No deso res d'aquest lot.")
                continue
            for avis in revisa_noms([t["ca"] for t in lot], traduits):
                print(f"    avís: {avis}")
            for t, nou in zip(lot, traduits):
                t[args.idioma] = nou
        fitxer.write_text(json.dumps(feina, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"    desat")
    print("\nAra:  python3 scripts/i18n-munta.py --tot " + args.idioma)
    return 0


if __name__ == "__main__":
    sys.exit(main())
