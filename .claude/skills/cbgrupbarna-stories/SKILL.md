---
name: cbgrupbarna-stories
description: Generate on-brand vertical (9:16) Instagram/TikTok story graphics for CB Grup Barna. Use whenever asked to create a "story", "reel" cover, or vertical social graphic for the club — encodes the club's real colors, typography and two fixed layout rules (logo top-right, red frame on light backgrounds).
---

# CB Grup Barna — Stories

Brand system for vertical (1080×1920) story graphics, reverse-engineered from the
club's real site (`index.html` at the repo root) and its published social pieces —
not invented. Reuse this system for every new story instead of improvising colors
or fonts each time.

A worked reference implementation (style-kit + 3 example stories, fonts inlined as
base64) lives at `.claude/skills/cbgrupbarna-stories/reference.html` — open it to
see the full CSS and copy patterns before generating new pieces.

## Brand tokens

Colors (from `index.html` `:root`, do not substitute other reds/blacks):

| Token | Hex | Use |
|---|---|---|
| `--red` | `#E31E24` | Shield red. Accent word in the headline, divider line, CTA pill, **and the mandatory frame on light backgrounds**. |
| `--black` | `#0A0A0C` | "Declaration" backgrounds (results, confirmations). Never pure `#000` — kept a hair warm so the red doesn't vibrate against it. |
| light bg | `#F2F0EC` | Info/CTA backgrounds (sign-ups, calls to trial). Off-white, never `#FFFFFF` flat. |
| muted | `#6B6F76` | Footer / metadata line only. Always de-emphasized (lower opacity or smaller size). |

Typography (same families the site already loads via Google Fonts — see the
`<link>` in `index.html`):

| Role | Font | Weight | Notes |
|---|---|---|---|
| Headline | Inter | 900 | Big two-line statement, uppercase, tight letter-spacing (`-0.02em`). Second line is the `--red` (or black-on-red) accent word. |
| Eyebrow / footer label | JetBrains Mono | 700 | Tracked uppercase (2–3px letter-spacing), small. This is the club's "meta" voice used site-wide for tags/timestamps. |
| Supporting line / CTA | Inter | 800 | Uppercase, shorter line under the divider. |
| Reserved accent | Bebas Neue | 400 | The club's display face used elsewhere on the site for names/big stat numbers — not used in the 3 reference stories, but available for a stat-forward variant (e.g. a big "34" or "450"). |

## Fixed layout rules (non-negotiable)

1. **Logo always top-right.** `logo.png` (repo root), ~150px wide on a 1080px canvas,
   64px from the top and right edges. Never centered, never top-left — it must
   leave the upper-left corner clear for the headline to breathe.
2. **Light background ⇒ mandatory red frame.** Any story using the light/off-white
   background (`#F2F0EC`) gets a solid `26px` border in `--red` (`#E31E24`) around
   the *entire* canvas, matching the shield's own red trim. A light-background
   story with no border is a bug, not a style choice. Black and red backgrounds do
   not get this frame — they already carry the accent through text/divider.
3. **One accent per piece.** Red marks only the headline's key word, the divider,
   and (if present) the CTA pill — it does not spread through body copy or bullet
   lists.

## Canvas structure

Root class `.story` at `1080×1920`, one background variant per piece:
`bg-black` / `bg-red` / `bg-light`. Inside, in this order:

```
.story.bg-{black|red|light}
├── img.logo            top:64px right:64px width:150px   (rule 1)
├── .content            anchored to bottom third
│   ├── .eyebrow        JetBrains Mono 700, tracked, small
│   ├── .headline       Inter 900, 2 lines, line 2 wrapped in .accent
│   ├── .divider        6px bar, 150px wide
│   ├── .sub            Inter 800, uppercase, supporting line(s)
│   └── .cta            optional — red pill, only on info/CTA pieces
└── .foot               bottom:70px, JetBrains Mono 700, ~60% opacity
```

Color mapping per background (headline/divider/sub base color, with the accent
flipped for contrast):

- `bg-black`: text white, accent word/divider red.
- `bg-red`: text white, accent word/divider black (`#141416`).
- `bg-light` (+ mandatory red frame): text black (`#141416`), accent word red.

## Producing a new story

1. Pick the message and match it to a background variant by intent — a
   result/confirmation reads as `bg-black`, a barri/identity statement as
   `bg-red`, a recruitment/CTA piece as `bg-light` (remember rule 2, the frame).
2. Write two-line headline copy: line 1 neutral, line 2 the punch word/phrase in
   the accent color. Keep it terse — this is a display headline, not a sentence.
3. Copy the markup skeleton above (or lift a `<div class="story ...">` block
   straight out of `reference.html`) and swap in the new eyebrow/headline/sub/cta/
   foot text. Don't restyle — reuse the existing classes so every story stays
   visually consistent with the rest.
4. Fonts:
   - **Delivering as a Claude Artifact**: the Artifact CSP blocks font CDNs, so
     inline Bebas Neue / Inter / JetBrains Mono as base64 `@font-face` data URIs
     (see `reference.html` for the exact `@font-face` blocks — the same base64
     payloads can be reused verbatim, no need to re-fetch).
   - **Delivering as a page inside this repo**: link Google Fonts the same way
     `index.html` already does — `family=Bebas+Neue&family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;700` — no need to inline.
5. Embed `logo.png` from the repo root (or its base64, already captured in
   `reference.html`) — never redraw or substitute the shield.
