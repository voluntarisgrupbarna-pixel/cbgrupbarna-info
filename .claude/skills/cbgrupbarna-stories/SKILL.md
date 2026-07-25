---
name: cbgrupbarna-stories
description: Generate on-brand vertical (9:16) Instagram/TikTok story and reel-cover graphics for CB Grup Barna, aligned with the club's official brand manual. Use whenever asked to create a "story", "portada"/cover, "cartell", or vertical social graphic for the club — encodes the official colors, typography (Bebas Neue + Montserrat), the two logo placements (top-right for sèrie/editorial, centered for institucional), and the plate-vs-veil photo rule.
---

# CB Grup Barna — Stories & portades

Brand system for vertical (1080×1920) story/cover graphics. **Built directly
on the club's official brand manual** —
`.claude/skills/cbgrupbarna-stories/manual/CB_Grup_Barna_Identitat_Visual_2026_v1.1.pdf`
(14 pages, July 2026) — not reverse-engineered guesswork. Where anything below
conflicts with a newer version of that PDF, the PDF wins; update this file to
match.

A worked reference implementation (style-kit + 9 example pieces, fonts and
photos inlined as base64) lives at
`.claude/skills/cbgrupbarna-stories/reference.html` — open it to see the full
CSS and copy patterns before generating new pieces.

> **If the user shares a finished, real piece the club already published or
> designed (a post, story, or reel cover) — do not regenerate, redesign, or
> "correct" it against this system.** This skill is for producing *new*
> pieces from scratch. A real piece the user shares is already correct by
> definition; the only acceptable action is to use it as-is (crop out phone/
> app chrome if it's a screenshot, nothing else) or to study it as a reference
> for a *new* piece's composition. Rebuilding it in this skill's template and
> handing that back is a mistake this skill has made before — e.g. the
> Supercopa Femenina/Masculina posts and reels are real official pieces;
> deliver those files themselves, never a recreation.

**Related club skills** (if present on the machine, prefer them for anything
this skill doesn't cover):
- `sistema-visual-cbgb` — general design-token skill; superseded by the PDF
  manual above for anything the two disagree on.
- `portada-reels-cbgb` — reel-cover-thumbnail criteria (safe zones,
  grid-cropping, ≤5-word rule). Still relevant for pure reel-cover thumbnails;
  this skill's two logo placements (below) come from the brand manual, not
  from that skill.
- `aparador-perfil-cbgb` — real conversion data and the **3 pins** strategy
  (see `reference.html` §04), plus a real failure directly relevant here: the
  flat red/black + epic-text "institucional" register got **748 views vs.
  3K–12K elsewhere** when overused — "l'èpica en estàtic es mor." Cap that
  register at 3–4 Feed pieces max (see rule ⑦ below).

## Brand tokens (manual §04–05)

| Token | Hex | Use | Target share |
|---|---|---|---|
| `--red` | `#E31E24` | Roig Barna. Identity, not decoration — one accent per piece. | 30% |
| `--black` | `#0A0A0C` | Contrast, premium. The **dominant** color of the system, not red. | 55% |
| white | `#FFFFFF` | Pure white — clarity, breathing room. Light bg ⇒ mandatory red frame. | 15% |
| muted | `#6B6F76` | Metadata / secondary text only. Never protagonist, doesn't count in the ratio. | — |

Typography — **exactly two families, per the manual**:

| Role | Font | Notes |
|---|---|---|
| Titulars, noms, xifres | **Bebas Neue** | Display only. 1–2 lines max, never a paragraph. No outlines/shadows/gratuitous italic tilt. |
| Text, informació, CTA | **Montserrat** (600/700/800/900) | Body, eyebrows, tags, buttons, captions. |

`reference.html` also keeps JetBrains Mono for small tracked metadata
(chapter tags, footers) as a house convention from before the manual was
available — **not** an official third family; don't add a real third
typeface to a piece.

## Two logo placements — not one (manual §02–03, §10)

The escut is always the *official* file (never redrawn/approximated/recreated
with AI), intact, isolated by a protection zone `x` = 20% of the shield's own
width, minimum height 18mm print / 64px digital.

1. **Editorial / sèrie pieces (has a photo)** → escut **top-right**, ~150px
   wide on a 1080px canvas, 64px from the top and right edges.
2. **Institucional pieces (flat bg, no photo — grans anuncis)** → escut
   **centered** at the top. This is the one earlier versions of this skill
   got wrong by defaulting every piece to top-right — the manual is explicit
   that institutional covers (ascensos, campanyes de pertinença,
   presentacions de temporada) center the shield instead.

Don't guess which applies — it's decided by which of the two templates below
the piece is.

## Template A — Portades de sèrie (editorial, escut top-right)

For fitxatges, renovacions, and recurring content series (tips, POV,
"cap. XX" chapters). Real photo, required. Anatomy, top to bottom:

```
.story.bg-photo
├── img.photo + .plate OR .veil   (rule below — not interchangeable)
├── img.logo                      top-right, ~150px                (two-placements rule)
├── .pill                         top-left — series name, 3–4 words, fixed red/black chip
├── .tag1                         under .pill — "Cap. XX" or context, fixed chip
├── .content                      lower third
│   ├── .eyebrow                  Montserrat 700, tracked, small — who/what
│   ├── .headline                 Bebas Neue — the statement, 1–2 lines
│   └── .kickline                 red/black bar + short Montserrat 800 closing phrase
└── .foot                         "CB Grup Barna · El Clot", small, reduced opacity
```

**Plate vs. veil (not optional, pick correctly):**
- **`.plate`** — solid `--black`, bottom ~36% of the canvas only, short fade
  at its top edge. Use for a **single person's announcement** (a specific
  fitxatge/renovació cover) — the photo stays completely clean above it: face,
  jersey, everything undimmed.
- **`.veil`** — red→black gradient wash over the **entire** photo. Use only
  for a **recurring content-series** episode (a "cap. XX" chapter that isn't
  about one specific signing). Never apply the veil to an individual
  player/coach cover, and never leave a series episode without it.

Manual requirements for this template specifically: series name and chapter
number always visible, hook is one idea (not a summary), real photo with
treatment (plate/veil count), fixed signature. Don't turn every chapter into
a new sub-brand — same pill/tag/type system every time.

## Template B — Portades institucionals (grans anuncis, escut centrat)

For ascensos, campanyes de pertinença, presentacions de temporada, fites del
club. **No photo. No pill/tag chips.** The typographic message is the
protagonist. Anatomy:

```
.story.inst.bg-{white|red|black}
├── img.logo          centered top                          (two-placements rule)
├── .ieyebrow          Montserrat 700, tracked, centered — brief context
├── .ititle            Bebas Neue, huge, centered, 1–2 lines — one word/line in .acc (the one accent)
├── .isecondary        Montserrat 700, centered, max 2–3 lines
├── .icta               optional red pill button (only when there's a real CTA)
└── .foot               centered, fixed signature
```

Rules specific to this template: flat background only (white/red/black), one
accent color block in the titular (not scattered through the piece), secondary
text capped at 2–3 lines, constant bottom signature. **Don't mix the two
templates in one piece** — no pill/tag chip on an institutional cover, no
centered logo on a sèrie cover.

## Fixed rules

1. **White background ⇒ mandatory red frame.** Any `bg-white` piece (either
   template) gets a solid `26px` border in `--red` around the entire canvas.
2. **Plate for one person, veil for a series — see Template A above.** Getting
   this backwards is the most common mistake with this system.
3. **Pill/tag are fixed brand chips** (Template A only). Always red/black,
   never tinted to the page background — they only invert when they'd
   otherwise sit on their own color (e.g. pill flips black on `bg-red`).
4. **Logo placement follows the template, not habit** — top-right for
   Template A, centered for Template B. See "Two logo placements" above.
5. **One accent per piece.** Red marks the pill/kickline bar (Template A) or
   the one accent word in `.ititle` (Template B) and, on white bg, the frame
   — it never spreads through body copy.
6. **Never redraw, recolor, rotate, stretch, shadow, or AI-recreate the
   escut.** Always the official file. (Manual §12, "Usos incorrectes.")
7. **Don't overuse Template B.** Real data (`aparador-perfil-cbgb`) shows this
   exact register cratered to 748 views vs. 3K–12K elsewhere when it was
   nearly every piece — repetition fatigue. Cap it at 3–4 Feed pieces at a
   time; lean on Template A or an actual video for anything more frequent.

## Producing a new piece

1. **Pick the template first** — it decides the logo position and whether
   there's a photo:
   - One person's fitxatge/renovació → **Template A**, `.plate`.
   - A recurring series episode → **Template A**, `.veil`.
   - A club-wide announcement with no specific person → **Template B**.
2. Write copy in order: (A) pill → tag → eyebrow → headline → kickline, or
   (B) ieyebrow → ititle (with one accent word) → isecondary → optional CTA.
   Keep every field terse — this is a display system, not paragraphs.
3. Copy a `<div class="story ...">` block straight out of `reference.html`
   and swap in the new text/photo. Don't restyle — reuse the existing classes.
4. Fonts: reuse the exact base64 `@font-face` payloads already in
   `reference.html` (Bebas Neue + Montserrat + JetBrains Mono) for a Claude
   Artifact (CSP blocks font CDNs); link Google Fonts instead for a page
   inside this repo, the way `index.html` already does.
5. Photo (Template A only): a real photo of the actual person/team, never
   stock. If the only source is a finished graphic (title text baked in
   above, name baked in below), crop tightly to just the person — head to
   torso/waist — excluding those baked-in bands entirely; on `.plate` pieces
   especially, a top-baked title has nothing hiding it (the plate only covers
   the bottom ~36%). Also crop out baked-in carousel badges ("1/6") or
   watermark logos sharing the top-right corner with this system's escut.
   - True background-removal was attempted via the higgsfield MCP's
     `remove_background` but the sandbox's egress proxy blocks uploads to
     `upload.higgsfield.ai` (403 on CONNECT) — not fixable from inside the
     session. Prefer a real cutout over a cropped rectangle if that path
     opens up later; until then, tight cropping + plate/veil is the working
     substitute.
6. Embed `logo.png` from the repo root (or its base64, already in
   `reference.html`) — never redraw or substitute the shield.

## Beyond social graphics: office formats

The same tokens carry into PPTX/DOCX/XLSX deliverables — a renewal or signing
doesn't have to stay a story graphic. `examples/` has one worked sample of
each, built around David Alegre's real renovació, from before this skill
adopted Bebas Neue/Montserrat — **they still use Inter/Arial for the
headline font**, which is now off-manual. Re-export with Bebas Neue (or
Arial Black as the closer safe-list fallback for PPTX, since Bebas Neue isn't
on the office-skill's font-metric-safe list) before treating them as current
references:

- `cbgb-anunci-renovacio.pptx` — 2-slide deck: a dark cover slide over his
  photo with a scrim approximating `.plate`, then a light "fitxa ràpida"
  facts slide (red-framed per rule ①).
- `cbgb-nota-premsa-renovacio.docx` — a one-page press-release layout: logo
  letterhead, red rule, headline, body, pull-quote, quick-facts table.
- `cbgb-fitxatges-26-27.xlsx` — a fitxatges/renovacions tracking sheet (red
  header row) with `COUNTA`/`COUNTIF` summary formulas and a `Tipus`/`Estat`
  dropdown so it doubles as a fill-in template.

Notes for next time:
- **`pptxgenjs`, `docx`, `openpyxl`, `defusedxml`, `markitdown`, and
  `poppler-utils` (`pdftoppm`) were not actually preinstalled** in this
  environment despite the office/PDF skills saying so — `npm install
  pptxgenjs` / `npm install docx` / `pip install openpyxl pandas defusedxml
  lxml "markitdown[pptx,docx,xlsx]"` / `apt-get install poppler-utils` were
  all needed first. `poppler-utils` did install cleanly (unlike the next
  point) — use it (`pdftoppm`) for PDF page rendering.
- **LibreOffice (`soffice`) cannot convert anything in this sandbox** — even
  a one-line `.txt` to PDF fails with "source file could not be loaded", and
  `xlsx`'s `recalc.py` times out rather than recalculating. This is
  environment-wide, not a defect in the files. No visual render/QA was
  possible for the pptx/docx here (schema `validate.py` + `markitdown`
  content checks stood in instead), and the xlsx formulas are written
  correctly but unverified by recalculation. If `soffice --headless
  --convert-to pdf` works in a future session, use it for real visual QA.
