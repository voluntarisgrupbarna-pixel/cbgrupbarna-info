#!/usr/bin/env python3
"""Baixa l'informe diari de GA4 i el deixa a admin/analitica/dades.json.

El panell d'analítica d'/admin/analitica/ no parla mai amb Google: llegeix
aquest JSON, que un workflow regenera cada matinada. Així la clau del
service account només viu als secrets de GitHub i el panell és estàtic.

Necessita dos secrets (variables d'entorn):
  GA4_SERVICE_ACCOUNT_JSON  el JSON sencer del service account de Google
                            Cloud amb accés de lector a la propietat GA4
  GA4_PROPERTY_ID           el número de la propietat (Admin → Property
                            settings → Property ID)

Sense els secrets NO falla: diu què falta i surt amb 0, perquè el cron no
quedi en vermell fins que l'Ana els doni d'alta. Amb els secrets, escriu el
JSON i surt amb 0; qualsevol error de l'API sí que surt amb 1.

Com donar d'alta el service account (10 minuts, un sol cop):
  1. https://console.cloud.google.com/ amb voluntarisgrupbarna@gmail.com →
     IAM & Admin → Service accounts → Create (nom: cbgb-analitica).
  2. A la fitxa del service account → Keys → Add key → JSON. Es baixa un
     fitxer .json: aquest fitxer sencer és GA4_SERVICE_ACCOUNT_JSON.
  3. A Google Analytics → Admin → Property access management → afegir el
     correu del service account (cbgb-analitica@...iam.gserviceaccount.com)
     amb el rol «Viewer».
  4. Al repositori de GitHub → Settings → Secrets and variables → Actions →
     crear GA4_SERVICE_ACCOUNT_JSON (el contingut del .json) i
     GA4_PROPERTY_ID (el número).
"""
from __future__ import annotations

import base64
import json
import os
import sys
import time
import urllib.parse
import urllib.request

ARREL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SORTIDA = os.path.join(ARREL, "admin", "analitica", "dades.json")
SCOPE = "https://www.googleapis.com/auth/analytics.readonly"


def b64url(b: bytes) -> str:
    return base64.urlsafe_b64encode(b).rstrip(b"=").decode()


def token_dacces(sa: dict) -> str:
    """OAuth2 de servidor a servidor: un JWT RS256 signat amb la clau del
    service account, bescanviat per un access token."""
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import padding

    ara = int(time.time())
    capcalera = b64url(json.dumps({"alg": "RS256", "typ": "JWT"}).encode())
    cos = b64url(json.dumps({
        "iss": sa["client_email"],
        "scope": SCOPE,
        "aud": "https://oauth2.googleapis.com/token",
        "iat": ara,
        "exp": ara + 3600,
    }).encode())
    per_signar = f"{capcalera}.{cos}".encode()
    clau = serialization.load_pem_private_key(sa["private_key"].encode(), password=None)
    firma = clau.sign(per_signar, padding.PKCS1v15(), hashes.SHA256())
    jwt = f"{capcalera}.{cos}.{b64url(firma)}"

    dades = urllib.parse.urlencode({
        "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
        "assertion": jwt,
    }).encode()
    peticio = urllib.request.Request("https://oauth2.googleapis.com/token", data=dades)
    with urllib.request.urlopen(peticio, timeout=30) as r:
        return json.load(r)["access_token"]


def informe(token: str, prop: str, cos: dict) -> list[dict]:
    peticio = urllib.request.Request(
        f"https://analyticsdata.googleapis.com/v1beta/properties/{prop}:runReport",
        data=json.dumps(cos).encode(),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(peticio, timeout=60) as r:
        resposta = json.load(r)
    files = []
    for fila in resposta.get("rows", []):
        files.append({
            "d": [v["value"] for v in fila.get("dimensionValues", [])],
            "m": [v["value"] for v in fila.get("metricValues", [])],
        })
    return files


def main() -> int:
    sa_json = os.environ.get("GA4_SERVICE_ACCOUNT_JSON", "").strip()
    prop = os.environ.get("GA4_PROPERTY_ID", "").strip()
    if not sa_json or not prop:
        print("Falten GA4_SERVICE_ACCOUNT_JSON i/o GA4_PROPERTY_ID als secrets.")
        print("El panell seguirà dient «esperant credencials». Instruccions a la")
        print("capçalera d'aquest script. No és un error del workflow.")
        return 0

    token = token_dacces(json.loads(sa_json))
    d28 = {"startDate": "28daysAgo", "endDate": "yesterday"}

    dies = informe(token, prop, {
        "dateRanges": [d28],
        "dimensions": [{"name": "date"}],
        "metrics": [{"name": "activeUsers"}, {"name": "sessions"},
                    {"name": "screenPageViews"}],
        "orderBys": [{"dimension": {"dimensionName": "date"}}],
    })
    pagines = informe(token, prop, {
        "dateRanges": [d28],
        "dimensions": [{"name": "pagePath"}],
        "metrics": [{"name": "screenPageViews"}, {"name": "activeUsers"}],
        "orderBys": [{"metric": {"metricName": "screenPageViews"}, "desc": True}],
        "limit": 30,
    })
    fonts = informe(token, prop, {
        "dateRanges": [d28],
        "dimensions": [{"name": "sessionDefaultChannelGroup"}],
        "metrics": [{"name": "sessions"}],
        "orderBys": [{"metric": {"metricName": "sessions"}, "desc": True}],
    })
    events = informe(token, prop, {
        "dateRanges": [d28],
        "dimensions": [{"name": "eventName"}],
        "metrics": [{"name": "eventCount"}],
        "orderBys": [{"metric": {"metricName": "eventCount"}, "desc": True}],
        "limit": 25,
    })
    dispositius = informe(token, prop, {
        "dateRanges": [d28],
        "dimensions": [{"name": "deviceCategory"}],
        "metrics": [{"name": "activeUsers"}],
    })

    os.makedirs(os.path.dirname(SORTIDA), exist_ok=True)
    with open(SORTIDA, "w", encoding="utf-8") as f:
        json.dump({
            "generat": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "periode": "28 dies fins ahir",
            "dies": dies,
            "pagines": pagines,
            "fonts": fonts,
            "events": events,
            "dispositius": dispositius,
        }, f, ensure_ascii=False, indent=1)
    print(f"Escrit {SORTIDA}: {len(dies)} dies, {len(pagines)} pàgines.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
