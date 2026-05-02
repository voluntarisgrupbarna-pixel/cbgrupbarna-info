#!/usr/bin/env python3
"""
Auto-actualitza data.json amb dades reals de JotForm (Campus) i Apps Script (3x3).

Variables d'entorn esperades:
- JOTFORM_API_KEY: clau API de JotForm (GitHub Secret)
- TRES_X_TRES_COUNT_URL (opcional): endpoint d'Apps Script que retorna {"count": N}
"""
import json
import os
import re
import sys
import urllib.request
from datetime import datetime, timezone, timedelta
from pathlib import Path

CAMPUS_FORM_ID = '260962500106347'
DATA_PATH = Path(__file__).resolve().parents[2] / 'data.json'

def jotform_get(path):
    api_key = os.environ.get('JOTFORM_API_KEY', '').strip()
    if not api_key:
        return None
    url = f'https://api.jotform.com/{path}'
    sep = '&' if '?' in url else '?'
    url = f'{url}{sep}apiKey={api_key}'
    req = urllib.request.Request(url, headers={'User-Agent': 'cbgrupbarna-info/1.0'})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.loads(r.read())
    except Exception as e:
        print(f"::warning::JotForm fetch failed for {path}: {e}", file=sys.stderr)
        return None

def get_campus_counts():
    """Retorna dict {1: count, 2: count, 3: count, 4: count, 'total': N} a partir de JotForm."""
    out = {'total': 0, 'weeks': {}}
    # Pull all submissions in pages of 1000 (JotForm max)
    offset = 0
    while True:
        page = jotform_get(f'form/{CAMPUS_FORM_ID}/submissions?limit=1000&offset={offset}')
        if not page or not page.get('content'):
            break
        subs = page['content']
        for sub in subs:
            # Skip non-active submissions
            if sub.get('status') == 'DELETED':
                continue
            out['total'] += 1
            # Detectar setmana en qualsevol resposta
            answers = sub.get('answers', {}) or {}
            weeks_in_sub = set()
            for q in answers.values():
                a = q.get('answer')
                texts = []
                if isinstance(a, list):
                    texts = [str(x) for x in a]
                elif isinstance(a, dict):
                    texts = [str(v) for v in a.values()]
                elif a is not None:
                    texts = [str(a)]
                for t in texts:
                    for m in re.finditer(r'[Ss]etmana\s*(\d)', t):
                        weeks_in_sub.add(int(m.group(1)))
            for w in weeks_in_sub:
                out['weeks'][w] = out['weeks'].get(w, 0) + 1
        if len(subs) < 1000:
            break
        offset += 1000
    return out

def get_3x3_count():
    """Llegeix el comptador del 3x3 d'una variable d'entorn opcional."""
    url = os.environ.get('TRES_X_TRES_COUNT_URL', '').strip()
    if not url:
        return None
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'cbgrupbarna-info/1.0'})
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.loads(r.read())
        # Acceptem {"count": N} o {"filled": N}
        return int(data.get('count') or data.get('filled') or 0)
    except Exception as e:
        print(f"::warning::3x3 count fetch failed: {e}", file=sys.stderr)
        return None

def main():
    if not DATA_PATH.exists():
        print(f"::error::data.json not found at {DATA_PATH}", file=sys.stderr)
        sys.exit(1)

    config = json.loads(DATA_PATH.read_text())
    changed = False

    # ---- Campus
    campus = get_campus_counts()
    if campus is not None:
        weeks = config.get('campus', {}).get('weeks', [])
        for w in weeks:
            wid = w.get('id')
            new_filled = campus['weeks'].get(wid)
            if new_filled is not None and new_filled != w.get('filled'):
                print(f"Campus week {wid}: {w.get('filled')} -> {new_filled}")
                w['filled'] = new_filled
                changed = True
        # Total per a referència (no es mostra per setmana)
        config['campus']['totalSubmissions'] = campus['total']
        changed = True  # always bump lastUpdate when JotForm responds

    # ---- 3x3
    n3 = get_3x3_count()
    if n3 is not None:
        if config.get('tres_x_tres', {}).get('filled') != n3:
            print(f"3x3 filled: {config['tres_x_tres'].get('filled')} -> {n3}")
            config['tres_x_tres']['filled'] = n3
            changed = True

    # Update timestamp si alguna cosa ha canviat
    if changed:
        # Hora local Madrid (UTC+2 a estiu)
        now = datetime.now(timezone(timedelta(hours=2)))
        config['lastUpdate'] = now.replace(microsecond=0).isoformat()
        DATA_PATH.write_text(json.dumps(config, indent=2, ensure_ascii=False) + '\n')
        print(f"data.json updated at {config['lastUpdate']}")
    else:
        print("No changes")

if __name__ == '__main__':
    main()
