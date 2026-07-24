---
name: cbgrupbarna-stories
description: Generate on-brand vertical (9:16) Instagram/TikTok story and reel-cover graphics for CB Grup Barna. Use whenever asked to create a "story", "portada"/cover, or vertical social graphic for the club — encodes the club's real colors, typography, the unified pill+tag+eyebrow+headline+accent+footer layout, and the two background rules (red frame on white, red/black veil on reel-cover photos).
---

# CB Grup Barna — Stories & portades

Brand system for vertical (1080×1920) story/cover graphics, reverse-engineered
from the club's real site (`index.html` at the repo root) and from actual
published pieces the club uses — not invented. Reuse this system for every new
piece instead of improvising colors, fonts, or layout each time.

**Related club skills** (if present on the machine, prefer them as the
authority and treat this skill as the repo-local fallback):
- `sistema-visual-cbgb` — the club's general design-token skill. Its
  `tokens.conf` is the intended single source of truth for color/type/logo
  values, but at the time this skill was written that file didn't exist yet
  (placeholder only) — so the tokens below are derived directly from
  `index.html` instead. **If `tokens.conf` exists when you read this, use its
  values and treat the table below as out of date.**
- `portada-reels-cbgb` — the club's criteria for reel-cover thumbnails
  specifically (safe zones, grid-cropping, the ≤5-word rule, logo at vertical
  center). This skill's layout was built from direct, repeated user
  instructions that differ from that playbook in one place — see rule ④ below,
  don't silently "fix" it to match the other skill.

A worked reference implementation (style-kit + 5 example pieces, fonts and
photos inlined as base64) lives at
`.claude/skills/cbgrupbarna-stories/reference.html` — open it to see the full
CSS and copy patterns before generating new pieces.

## Brand tokens

Colors (from `index.html` `:root`, do not substitute other reds/blacks):

| Token | Hex | Use |
|---|---|---|
| `--red` | `#E31E24` | Shield red. Hook pill, accent bar, mandatory frame on white backgrounds, mandatory veil on reel-cover photos. |
| `--black` | `#0A0A0C` | Context tag, "declaration" flat background, base tone of the reel-cover veil. Never pure `#000`. |
| white bg | `#FFFFFF` | Flat background for informative/CTA pieces. Pure white, not cream — **always paired with rule ①**. |
| muted | `#6B6F76` / `rgba(255,255,255,.6–.85)` | Eyebrow (on white) and footer line. Always de-emphasized, never protagonist. |

Typography (same families the site already loads via Google Fonts — see the
`<link>` in `index.html`):

| Role | Font | Weight | Notes |
|---|---|---|---|
| Headline | Inter | 900 | Big statement, uppercase, tight letter-spacing (`-0.02em`). |
| Hook pill / tag / kickline / CTA | Inter | 800 | Uppercase, short — the chip and closing-line text. |
| Eyebrow / footer | JetBrains Mono | 700 | Tracked uppercase, small. The club's "meta" voice used site-wide for tags/timestamps. |
| Reserved accent | Bebas Neue | 400 | The club's display face, used elsewhere on the site for names/big stat numbers — not used in the reference pieces, but available for a stat-forward variant. |

## The unified cover block

One layout, used on **every** piece — flat or photo. Top to bottom:

```
.story.bg-{white|red|black|photo}
├── img.photo + .veil     ONLY on bg-photo — full-bleed photo + red/black veil (rule ②)
├── img.logo              top:64px right:64px, ~140px wide          (rule ④)
├── .pill                 top:64px left:64px — the hook, 3–4 words  (rule ③, fixed chip)
├── .tag                  right under .pill — context/series/date   (rule ③, fixed chip)
├── .content              anchored to the lower third
│   ├── .eyebrow          JetBrains Mono 700, tracked, small
│   ├── .headline         Inter 900, the main message
│   └── .kickline         red/black bar + short closing phrase
└── .foot                 bottom:70px, JetBrains Mono 700, reduced opacity
```

Four background variants share this exact block — only the canvas background
and the chip/text color mapping change:

- **`bg-white`** — pure white + mandatory red frame (rule ①). Headline/kickline
  dark (`#141416`), eyebrow/footer muted grey.
- **`bg-red`** — flat `--red`. Headline/kickline white; pill and kickline bar
  flip to black so they don't disappear into the same hue.
- **`bg-black`** — flat `--black`. Headline/kickline white; tag flips to
  white-on-black for the same reason.
- **`bg-photo`** — real club photo, full-bleed, **+ mandatory veil** (rule ②).
  Same white-based palette as `bg-black`.

The pill and tag are brand chips, not page-colored elements: they stay
red/black regardless of the canvas, and only invert when they'd otherwise sit
on their own color. This is what makes them read as the same "stamp" across
every piece in the grid.

## Fixed rules

1. **White background ⇒ mandatory red frame.** Any `bg-white` piece gets a
   solid `26px` border in `--red` around the entire canvas. A white piece with
   no border is a bug.
2. **Reel-cover portada ⇒ mandatory photo + red/black veil.** A reel cover
   never uses a flat background — always a real club photo (from `img/` or
   equivalent) with the veil gradient (red → near-black, see `reference.html`
   `.veil` rule) so the text stays legible. Flat backgrounds (white/red/black)
   are for stories/announcements that aren't reel-cover thumbnails.
3. **Pill/tag are fixed brand chips.** Always red/black, never tinted to match
   the page background — they only invert (see mapping above) when they'd
   otherwise blend into a same-colored canvas.
4. **Logo top-right — confirmed, overrides `portada-reels-cbgb`.** The logo
   always goes top-right, ~140px, 64px from the top and right edges. This was
   flagged as a tension with the club's general reel-cover playbook
   (`portada-reels-cbgb`), which calls for the logo at vertical center to
   survive the profile grid's 3:4/1:1 crop — asked directly, the answer was to
   keep top-right regardless. Treat top-right as final for this system, not an
   open question; don't "fix" it back to center.
5. **One accent per piece.** Red marks only the pill, the kickline bar, and
   (on `bg-white`) the frame — it does not spread through body copy.

## Producing a new piece

1. Decide reel-cover vs. story: reel-cover → `bg-photo` + a real photo (rule
   ②); story/announcement → pick `bg-white` / `bg-red` / `bg-black` by intent
   (result/confirmation → black, barri/identity → red, recruitment/CTA →
   white + frame).
2. Write the copy in this order: **pill** (3–4 word hook) → **tag** (context/
   date/series) → **eyebrow** (who/what this is about) → **headline** (the
   main statement) → **kickline** (one short closing phrase after the bar).
   Keep every field terse — this is a display system, not paragraphs.
3. Copy a `<div class="story ...">` block straight out of `reference.html` and
   swap in the new text/photo. Don't restyle — reuse the existing classes so
   every piece stays visually consistent with the rest.
4. Fonts:
   - **Delivering as a Claude Artifact**: the Artifact CSP blocks font CDNs, so
     inline Bebas Neue / Inter / JetBrains Mono as base64 `@font-face` data
     URIs — reuse the exact payloads already in `reference.html`, no need to
     re-fetch.
   - **Delivering as a page inside this repo**: link Google Fonts the way
     `index.html` already does instead of inlining.
5. Photo (reel-cover only): use a real photo of the actual person/team — never
   stock or generic. `reference.html` currently features 5 real people (Jordi
   Vives, a Sènior femení dorsal-33 player, David Alegre, Carlos Rodríguez de
   la Hera, Nora Serra), sourced from screenshots of the club's own past
   Instagram posts. If the only source is a finished graphic like that (title
   text baked in above the subject, name baked in below), crop tightly to just
   the person — head to torso/waist — excluding those baked-in text bands
   entirely, rather than relying on the veil to hide them; the veil is strong
   at the bottom but light at the top, so top-baked titles will still show
   through if left in. Also crop out any baked-in carousel badges ("1/6") or
   watermark logos sitting in the same top-right corner as this system's own
   escut, to avoid a double-logo look.
   - True background-removal (isolating just the person, no backdrop at all)
     was attempted via the higgsfield MCP's `remove_background`, but the
     sandbox's egress proxy blocks direct uploads to `upload.higgsfield.ai`
     (403 on CONNECT) — not fixable from inside the session. If that path
     opens up later (different environment, or a proxy allowlist change),
     prefer real cutouts over cropped rectangles; until then, tight cropping +
     the veil is the working substitute.
6. Embed `logo.png` from the repo root (or its base64, already captured in
   `reference.html`) — never redraw or substitute the shield.

## Beyond social graphics: office formats

The same tokens (red `#E31E24` / ink `#141416` / muted `#6B6F76`, Arial as the
safe cross-platform stand-in for Inter in tools that can't embed webfonts)
carry into PPTX/DOCX/XLSX deliverables — a renewal or signing doesn't have to
stay a story graphic. `examples/` has one worked sample of each, all built
around David Alegre's real renovació:

- `cbgb-anunci-renovacio.pptx` — 2-slide deck: a dark cover slide reusing the
  pill/tag/eyebrow/headline/kickline block over his photo + veil, then a
  light "fitxa ràpida" facts slide (red-framed per rule ①).
- `cbgb-nota-premsa-renovacio.docx` — a one-page press-release layout:
  logo letterhead, red rule, headline, body, pull-quote, quick-facts table.
- `cbgb-fitxatges-26-27.xlsx` — a fitxatges/renovacions tracking sheet (red
  header row, one row per real person from `reference.html`) with `COUNTA`/
  `COUNTIF` summary formulas and a `Tipus`/`Estat` dropdown so it doubles as a
  fill-in template.

Notes for next time:
- **`pptxgenjs`, `docx`, `openpyxl`, `defusedxml`, `markitdown` were not
  actually preinstalled** in this environment despite the office skills
  saying so — `npm install pptxgenjs` / `npm install docx` / `pip install
  openpyxl pandas defusedxml lxml "markitdown[pptx,docx,xlsx]"` were all
  needed first.
- **LibreOffice (`soffice`) cannot convert anything in this sandbox** — even
  a one-line `.txt` to PDF fails with "source file could not be loaded", and
  `xlsx`'s `recalc.py` times out rather than recalculating. This is
  environment-wide, not a defect in these files. That means: no visual
  render/QA was possible for the pptx/docx here (schema `validate.py` +
  `markitdown` content checks stood in instead), and the xlsx formulas
  (`COUNTA`/`COUNTIF`, both safe pre-2007 functions) are written correctly
  but unverified by recalculation — they should compute normally in real
  Excel/PowerPoint/Word. If `soffice --headless --convert-to pdf` works in a
  future session, use it for real visual QA before trusting layout precisely.
