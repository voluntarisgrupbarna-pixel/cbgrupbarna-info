#!/usr/bin/env python3
"""
Client HTTP per a basquetcatala.cat · CB Grup Barna (club 24)

Des del setembre de 2026 la FCBQ protegeix el web amb una "Verificació de
seguretat" (reCAPTCHA v3 invisible): la primera petició d'una sessió rep un
302 cap a /security-check, la pàgina executa el reCAPTCHA al navegador i, si
la puntuació és bona, el servidor deixa una galeta `fcbq_rc` (HttpOnly, ~80
minuts) i redirigeix a la pàgina demanada. Un `urllib` pelat es queda a la
porta: 0 partits detectats i el robot no actualitza res.

Aquest mòdul dóna una sola funció, `fetch(url, method="GET")`, que:

  1. prova primer la via directa (urllib), per si la federació relaxa el
     filtre o la IP ja té la galeta;
  2. si rep el 302 a /security-check (o un 403), obre un Chromium headless
     amb Playwright, carrega la pàgina del club, deixa que la verificació
     faci el seu curs i, un cop dins, fa la petició demanada des del mateix
     context (mateixes galetes). El navegador NO es disfressa de res: cap
     bandera anti-detecció, user-agent per defecte de Chromium. Si la
     federació decideix que no (/access-denied), es respecta i es torna una
     cadena buida — mai s'intenta resoldre cap captcha.

Els scripts que el fan servir (update-partits.py, update-resultats.py) ja
són defensius: si `fetch` torna "" no toquen res i la via manual segueix.

Ús des de la línia d'ordres, per depurar:
    python fcbq_client.py https://www.basquetcatala.cat/club/24/resultats POST
"""
import sys
import urllib.error
import urllib.request

BASE = "https://www.basquetcatala.cat"
CLUB_URL = f"{BASE}/club/24"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")
TIMEOUT_NAV_MS = 45_000       # temps màxim perquè el security-check resolgui
_browser_ctx = None           # es reaprofita entre peticions del mateix procés
_pw = None


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def _fetch_direct(url, method):
    """Via ràpida. Torna (html, bloquejat)."""
    req = urllib.request.Request(url, method=method, data=b"" if method == "POST" else None,
                                 headers={"User-Agent": UA, "Accept-Language": "ca,es;q=0.8",
                                          "X-Requested-With": "XMLHttpRequest", "Referer": CLUB_URL})
    opener = urllib.request.build_opener(_NoRedirect)
    try:
        with opener.open(req, timeout=30) as r:
            html = r.read().decode("utf-8", "replace")
            return html, ("security-check" in html[:4000] and "recaptcha" in html)
    except urllib.error.HTTPError as exc:
        loc = exc.headers.get("Location", "") if exc.headers else ""
        if exc.code in (301, 302, 303, 307, 308) and "security-check" in loc:
            return "", True
        if exc.code == 403:
            return "", True
        raise


def _browser_context():
    """Obre (un sol cop) Chromium, passa pel security-check i torna el context."""
    global _browser_ctx, _pw
    if _browser_ctx is not None:
        return _browser_ctx
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("[fcbq] playwright no instal·lat — no es pot passar la verificació de seguretat")
        return None
    _pw = sync_playwright().start()
    browser = _pw.chromium.launch(headless=True)
    ctx = browser.new_context(locale="ca-ES", timezone_id="Europe/Madrid")
    page = ctx.new_page()
    try:
        page.goto(CLUB_URL, wait_until="domcontentloaded", timeout=TIMEOUT_NAV_MS)
        # La pàgina de verificació redirigeix sola quan acaba; s'espera fins
        # que la URL deixi de ser /security-check (o arribi a /access-denied).
        page.wait_for_url(lambda u: "security-check" not in u, timeout=TIMEOUT_NAV_MS)
        page.wait_for_load_state("domcontentloaded", timeout=15_000)
    except Exception as exc:  # timeout o error de xarxa
        print(f"[fcbq] la verificació de seguretat no ha resolt: {exc.__class__.__name__}")
    url = page.url
    if "access-denied" in url or "security-check" in url:
        print(f"[fcbq] la federació no deixa passar el robot ({url}) — no s'insisteix")
        browser.close(); _pw.stop(); _pw = None
        return None
    print(f"[fcbq] verificació superada · sessió a {url}")
    _browser_ctx = ctx
    return ctx


def fetch(url, method="GET"):
    """HTML de `url` (GET o POST buit). Cadena buida si no s'hi pot arribar."""
    try:
        html, bloquejat = _fetch_direct(url, method)
        if not bloquejat:
            return html
        print(f"[fcbq] {url}: security-check — es prova amb navegador")
    except Exception as exc:
        print(f"[fcbq] {url}: via directa ha fallat ({exc}) — es prova amb navegador")
    ctx = _browser_context()
    if ctx is None:
        return ""
    headers = {"X-Requested-With": "XMLHttpRequest", "Referer": CLUB_URL}
    try:
        r = ctx.request.post(url, headers=headers, timeout=30_000) if method == "POST" \
            else ctx.request.get(url, headers=headers, timeout=30_000)
    except Exception as exc:
        print(f"[fcbq] {url}: petició des del navegador ha fallat ({exc})")
        return ""
    if not r.ok or "security-check" in r.url:
        print(f"[fcbq] {url}: resposta {r.status} ({r.url})")
        return ""
    return r.text()


def close():
    """Tanca el navegador si s'ha obert. Cridar-ho al final del script."""
    global _browser_ctx, _pw
    if _browser_ctx is not None:
        try:
            _browser_ctx.browser.close()
        except Exception:
            pass
        _browser_ctx = None
    if _pw is not None:
        try:
            _pw.stop()
        except Exception:
            pass
        _pw = None


if __name__ == "__main__":
    u = sys.argv[1] if len(sys.argv) > 1 else f"{CLUB_URL}/resultats"
    m = sys.argv[2].upper() if len(sys.argv) > 2 else "POST"
    out = fetch(u, m)
    close()
    print(f"--- {len(out)} caràcters")
    print(out[:1500])
