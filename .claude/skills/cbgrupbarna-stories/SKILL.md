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
4. **Logo top-right — known tension with `portada-reels-cbgb`.** This series
   fixes the logo at top-right, ~140px, 64px from the edges, per direct and
   repeated user instruction. The club's reel-cover playbook (`portada-reels-cbgb`)
   instead calls for the logo at **vertical center, never a corner**, because
   the profile grid (3:4/1:1 crop) eats the corners. If a piece from this
   system is actually uploaded as a reel's custom cover (not just posted as a
   story), re-check this against the grid crop before a big rollout — don't
   silently resolve the conflict one way or the other.
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
5. Photo (reel-cover only): pull a real club photo (e.g. `img/hero-player.webp`,
   `img/team-action.webp`, or a new upload) — never a stock or generic image —
   and apply the `.veil` gradient from `reference.html` verbatim.
6. Embed `logo.png` from the repo root (or its base64, already captured in
   `reference.html`) — never redraw or substitute the shield.
