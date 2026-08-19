#!/usr/bin/env python3
"""Genera un PDF amb tot el contingut del blog de cbgrupbarna.info.

Llegeix els /blog/<slug>/index.html, n'extreu el cos de l'article i en munta
un sol document imprimible (portada + index + articles) que es converteix a
PDF amb Chromium headless.

  python3 scripts/blog-pdf.py            -> documents/blog-cb-grup-barna.pdf
"""
import html
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BLOG = ROOT / "blog"
OUT_HTML = ROOT / "scripts" / ".blog-pdf.html"
OUT_PDF = ROOT / "documents" / "blog-cb-grup-barna.pdf"
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"

MESOS = ["gener", "febrer", "març", "abril", "maig", "juny", "juliol",
         "agost", "setembre", "octubre", "novembre", "desembre"]


def ordre_slugs():
    """Ordre de publicacio segons /blog/index.html (mes nou primer)."""
    idx = (BLOG / "index.html").read_text(encoding="utf-8")
    vistos, slugs = set(), []
    for m in re.finditer(r'href="/blog/([^"/]+)/"', idx):
        s = m.group(1)
        if s not in vistos and (BLOG / s / "index.html").exists():
            vistos.add(s)
            slugs.append(s)
    for p in sorted(BLOG.iterdir()):
        if p.is_dir() and (p / "index.html").exists() and p.name not in vistos:
            slugs.append(p.name)
    return slugs


def un(txt):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", txt)).strip()


def data_llarga(iso):
    try:
        a, m, d = iso.split("-")
        return f"{int(d)} de {MESOS[int(m) - 1]} de {a}"
    except Exception:
        return iso


def absolutitza(frag):
    """/img/... -> file:///.../img/... perque Chromium carregui les imatges."""
    return re.sub(r'(src|href)="/(?!/)', lambda m: f'{m.group(1)}="{ROOT.as_uri()}/', frag)


def faq_a_prosa(frag):
    frag = re.sub(r'<div class="faq">|</div>', "", frag)
    frag = re.sub(r"<details>|</details>", "", frag)
    frag = re.sub(r"<summary>(.*?)</summary>", r"<h3>\1</h3>", frag, flags=re.S)
    return frag


def neteja(frag):
    frag = re.sub(r"<script.*?</script>", "", frag, flags=re.S)
    frag = faq_a_prosa(frag)
    # els enllacos interns no serveixen en paper: es queden com a text
    frag = re.sub(r'<a\s[^>]*href="(?:/|https?://)[^"]*"[^>]*>(.*?)</a>',
                  r'<span class="link">\1</span>', frag, flags=re.S)
    return absolutitza(frag).strip()


def article(slug):
    src = (BLOG / slug / "index.html").read_text(encoding="utf-8")

    def g(pat, d=""):
        m = re.search(pat, src, re.S)
        return m.group(1).strip() if m else d

    cos = g(r'<article class="narrow prose">(.*?)<div style="margin-top:clamp')
    if not cos:
        cos = g(r'<article class="narrow prose">(.*?)</article>')
    hero = g(r'<div class="phead-media"><img src="([^"]+)"')
    return {
        "slug": slug,
        "seccio": un(g(r'<p class="eyebrow red">(.*?)</p>', "Blog")),
        "titol": un(g(r"<h1[^>]*>(.*?)</h1>")),
        "lede": un(g(r'<p class="lede">(.*?)</p>')),
        "data": g(r'<time datetime="([^"]+)"'),
        "hero": (ROOT.as_uri() + hero) if hero.startswith("/") else hero,
        "cos": neteja(cos),
    }


CSS = """
@page { size: A4; margin: 20mm 18mm 18mm; }
@page :first { margin: 0; }
@font-face { font-family:'Anton'; src:url('FONTURI') format('woff2'); }
:root { --ink:#0a0a0a; --ink-2:#46433f; --muted:#8a8681; --line:#e4e1dd;
        --paper-2:#f6f4f1; --red:#E20613; }
* { box-sizing:border-box; margin:0; padding:0; }
body { font-family:'Inter','Helvetica Neue',Helvetica,Arial,sans-serif;
       font-weight:300; font-size:10.5pt; line-height:1.62; color:var(--ink); }
h1,h2,h3 { font-family:'Anton','Arial Narrow',sans-serif; font-weight:400;
           letter-spacing:.02em; text-transform:uppercase; line-height:1.06; }
img { max-width:100%; height:auto; display:block; }
.link { border-bottom:.5pt solid var(--line); }
.eyebrow { font-size:7pt; letter-spacing:.34em; text-transform:uppercase;
           color:var(--muted); }
.eyebrow.red { color:var(--red); }

/* portada */
.cover { position:relative; height:297mm; padding:34mm 24mm; color:#fff;
         background:#0a0a0a; display:flex; flex-direction:column;
         justify-content:space-between; page-break-after:always; }
.cover .bar { width:44mm; height:2.4mm; background:var(--red); }
.cover h1 { font-size:46pt; margin:6mm 0 0; }
.cover .sub { font-size:11pt; font-weight:300; color:#cfcbc6; margin-top:6mm;
              max-width:110mm; }
.cover .peu { font-size:7.5pt; letter-spacing:.3em; text-transform:uppercase;
              color:#8a8681; }
.cover .logo { width:22mm; }

/* index */
.toc { page-break-after:always; }
.toc h2 { font-size:22pt; margin-bottom:2mm; }
.toc .rule { height:.6pt; background:var(--line); margin:5mm 0 7mm; }
.toc ol { list-style:none; counter-reset:t; }
.toc li { counter-increment:t; display:flex; gap:5mm; padding:3mm 0;
          border-bottom:.4pt solid var(--line); page-break-inside:avoid; }
.toc li::before { content:counter(t,decimal-leading-zero);
                  font-family:'Anton',sans-serif; color:var(--red);
                  font-size:10pt; padding-top:1pt; }
.toc .t { font-family:'Anton',sans-serif; text-transform:uppercase;
          font-size:12pt; line-height:1.15; }
.toc .m { font-size:7pt; letter-spacing:.24em; text-transform:uppercase;
          color:var(--muted); margin-top:1.4mm; }

/* article */
article { page-break-before:always; }
.num { font-family:'Anton',sans-serif; font-size:9pt; color:var(--red);
       letter-spacing:.06em; }
article h1 { font-size:26pt; margin:3mm 0 0; }
.meta { font-size:7pt; letter-spacing:.28em; text-transform:uppercase;
        color:var(--muted); margin-top:5mm; }
.lede { font-size:12pt; line-height:1.5; color:var(--ink-2); margin-top:5mm; }
.hero { margin:7mm 0 8mm; }
.prose h2 { font-size:14.5pt; margin:8mm 0 3mm; page-break-after:avoid; }
.prose h3 { font-size:11pt; margin:6mm 0 2mm; page-break-after:avoid; }
.prose p { margin-bottom:3.4mm; }
.prose ul,.prose ol { margin:0 0 4mm 5mm; }
.prose li { margin-bottom:1.8mm; }
.prose blockquote { margin:6mm 0; padding:4mm 0 4mm 6mm;
                    border-left:1.6pt solid var(--red); font-size:12pt;
                    line-height:1.45; color:var(--ink-2); }
.prose table { width:100%; border-collapse:collapse; margin:5mm 0;
               font-size:9pt; }
.prose th,.prose td { border-bottom:.4pt solid var(--line); padding:2mm 2mm;
                      text-align:left; }
.prose figure { margin:6mm 0; }
.prose figcaption,.nota { font-size:8pt; color:var(--muted); margin-top:2mm; }
.prose img { margin:5mm 0; }
.fi { margin-top:9mm; padding-top:4mm; border-top:.4pt solid var(--line);
      font-size:7.5pt; letter-spacing:.2em; text-transform:uppercase;
      color:var(--muted); }
"""


def munta(posts):
    font = (ROOT / "fonts" / "anton-400-1354.woff2").as_uri()
    parts = [
        "<!DOCTYPE html><html lang='ca'><head><meta charset='utf-8'>",
        "<title>Blog · CB Grup Barna</title>",
        "<style>", CSS.replace("FONTURI", font), "</style></head><body>",
        f"""<section class="cover">
  <div><img class="logo" src="{(ROOT / 'logo.png').as_uri()}" alt="CB Grup Barna"></div>
  <div>
    <div class="bar"></div>
    <h1>El blog<br>del Barna</h1>
    <p class="sub">Tot el que hem escrit per a les famílies del barri: guies,
    dades i criteri d'un club de bàsquet de Sant Martí.</p>
  </div>
  <div class="peu">CB Grup Barna · La Nau del Clot · Sant Martí · Barcelona<br>
  {len(posts)} articles · cbgrupbarna.info/blog</div>
</section>""",
        "<section class='toc'><p class='eyebrow red'>Contingut</p>"
        "<h2>Índex d'articles</h2><div class='rule'></div><ol>",
    ]
    for p in posts:
        parts.append(
            f"<li><div><div class='t'>{html.escape(p['titol'])}</div>"
            f"<div class='m'>{html.escape(p['seccio'])} · {data_llarga(p['data'])}</div>"
            f"</div></li>")
    parts.append("</ol></section>")

    for i, p in enumerate(posts, 1):
        hero = f"<div class='hero'><img src='{p['hero']}' alt=''></div>" if p["hero"] else ""
        parts.append(f"""<article>
  <div class="num">{i:02d}</div>
  <p class="eyebrow red" style="margin-top:3mm">{html.escape(p['seccio'])}</p>
  <h1>{html.escape(p['titol'])}</h1>
  <p class="lede">{html.escape(p['lede'])}</p>
  <p class="meta">CB Grup Barna · {data_llarga(p['data'])}</p>
  {hero}
  <div class="prose">{p['cos']}</div>
  <p class="fi">cbgrupbarna.info/blog/{p['slug']}/</p>
</article>""")

    parts.append("</body></html>")
    return "\n".join(parts)


def main():
    posts = [article(s) for s in ordre_slugs()]
    OUT_HTML.write_text(munta(posts), encoding="utf-8")
    OUT_PDF.parent.mkdir(parents=True, exist_ok=True)
    cmd = [CHROME, "--headless", "--disable-gpu", "--no-sandbox",
           "--no-pdf-header-footer", "--virtual-time-budget=20000",
           f"--print-to-pdf={OUT_PDF}", OUT_HTML.as_uri()]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if not OUT_PDF.exists():
        sys.stderr.write(r.stderr)
        return 1
    print(f"{len(posts)} articles -> {OUT_PDF.relative_to(ROOT)} "
          f"({OUT_PDF.stat().st_size / 1024:.0f} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
