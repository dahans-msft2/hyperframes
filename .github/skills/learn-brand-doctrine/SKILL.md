---
name: learn-brand-doctrine
description: "Microsoft Learn / WWL ILT visual brand law for companion videos — grounds, gradient fields, the frosted glass band, ink and accent roles, typography, and the measured contrast rules that decide what colour may carry text. Use when choosing colours, backgrounds, or type for a Learn video; when authoring or reviewing a composition's look; when porting an old MD-102 template; or when someone asks whether something is on brand. These rules SUPERSEDE generic and upstream palette, typography, and house-style guidance. They do NOT govern motion — motion belongs to motion-doctrine."
---

# Learn Brand Doctrine

Supersedes upstream palette / typography / house-style. **Does not touch motion.**

Source of truth: `learn/brand/BRAND-SOURCE.md` and the frame preset at
`learn/frame-presets/learn-ilt/FRAME.md`. Everything here is
**extracted** from the ILT master template — theme tokens from `theme1.xml`, gradient stops
pixel-sampled from the deck's own rendered slides. Nothing is invented.

## The thesis: this is a light system

The theme part is named, literally, **"Light Mode"**. It ships a warm paper ground and a deep
navy ink and **no dark ground at all**. The mandatory AI end card is white.

The predecessor MD-102 video system ran dark-dominant — 24 of 44 videos on an invented
`#463668` gradient that appears nowhere in the theme — which meant every video ended on an
unmotivated hard cut to a white card. **Light is a return to brand, not a departure.**

## Grounds

The brand is **gradient fields, not flat fills**. Four grounds, and only four. Three are now
the deck's own exported artwork rather than a CSS reconstruction:

| Ground | Source | Use |
|---|---|---|
| `content-wash` | `assets/grounds/ground-content-wash.png` | **default** — every content frame |
| `hero-swoosh` | `assets/grounds/ground-hero-swoosh.png` | title · opening · closing · dividers |
| `section-field` | `assets/grounds/ground-section-field.png` | segment openers |
| `dark-field` | CSS `radial-gradient(90% 120% at 6% 4%, #365F7D, #121F42 38%, #0A142D 66%, #050D1A)` | the deliberate exception |

Copy the PNGs into the project at `assets/grounds/` the same way the end card is copied, and
reference them relatively. Each is 1920×1080 so it maps 1:1 to output pixels with no
render-time rescale.

`dark-field` stays CSS because nothing in the deck matches it. The deck's export named
"background-gradient-dark" is a pale blue wash — that is `section-field`, not this near-black
field. White ink fails on all three image grounds (best 2.69), so none of them substitutes.

**The hero swoosh is scarce.** Title, section, closing — nothing else. Spending it on a content
frame is exactly what makes a deck look cheap. The wash is the everyday ground and it is
almost white; content sits directly on it with no card required.

### On an image ground, text is ink — measured, not preference

Every pixel of all three image grounds was measured. Dark ink `#091F2E` passes AA everywhere
(worst 5.95, on the swoosh's colour field). **No accent passes anywhere** — purple peaks at
4.50 and bottoms at 1.64, teal bottoms at 1.20.

This is stricter than the solid-token table, where purple is permitted as display text on `bg`
at 4.41. **That permission does not travel to an image ground.** A purple stat number on the
swoosh is invisible, and the old gate could not see it because it reduced each ground to a
single representative hex.

One zone rule: on `hero-swoosh`, keep display type out of the **bottom-right third**. The left
column measures 15.6 against 5.95 there — still AA, but it is the one place where a thin weight
will struggle.

Verify with:

```
py tools/contrast_gate.py brand/_extract/palette.json --min 4.5 --zones
```

### Every gradient field carries a dither layer — mandatory

A wide, smooth, low-contrast ramp is the worst case for 8-bit H.264. `section-field` moves
through roughly 40 RGB levels across 1920px — about 48px per step. That posterizes into
visible vertical bands. **It will look flawless in `hyperframes preview` and banded in the
MP4**, because the browser dithers the CSS gradient and the encoder does not.

The fix is a low-opacity noise layer over the gradient, *under* the content. Noise breaks the
flat step boundaries so the encoder cannot align a band edge to them:

```css
.gradient-field::after {
  content: "";
  position: absolute;
  inset: 0;
  pointer-events: none;
  opacity: 0.035;                    /* 3–4%. Above 5% it reads as grain. */
  mix-blend-mode: overlay;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='3'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
}
```

`baseFrequency` must stay high (≈0.8) so the noise is per-pixel. A low frequency produces
visible clouds, which is a different artefact and a worse one.

Rules:

- Applies to **all four grounds — including the image ones**. Switching from CSS to the deck's
  own PNGs does *not* solve banding; the exports are smooth, not dithered. Measured flat-run
  width along the gradient axis: `content-wash` carries only **16 distinct levels** with a
  median flat run of **49px** (longest 810px), `section-field` 64 levels at 17px, `hero-swoosh`
  75 levels at 4px. The wash is the worst offender precisely because it looks the most
  innocuous. `dark-field` bands worst of the CSS grounds — dark ramps have the fewest levels.
- The seed is static. `feTurbulence` without an animated seed is deterministic, so it survives
  the render contract. Never animate it; per-frame noise reads as video compression failure
  and destroys the encoder's temporal prediction.
- Judge banding on the **rendered MP4**, never on the preview. If a field still bands after
  dithering, reduce the gradient's spatial extent rather than raising noise opacity.

## The two signature devices

**The bloom + arc.** A luminous teal → blue → periwinkle → orchid field sweeping in from one
corner into warm paper, separated by a ~2px white arc, with a fine white dot matrix
(≈3px pitch, `rgba(255,255,255,.28)`) over the dense area. Never a flat fill, never a hard edge.

**The glass band.** A translucent blurred band floating on a gradient field, running off the
left edge, rounded on the right end only, carrying a title in ink.
`rgba(255,255,255,.42)` + `backdrop-filter: blur(28px) saturate(1.25)`.
Upstream `liquid-glass-*` / `ios26-liquid-glass` blocks implement this idiom — install, don't rebuild.

## The contrast law — non-negotiable

Measured with `tools/contrast_gate.py` (WCAG 2.1). Contrast failure is a rubric **disqualifier**,
and this palette fails quietly: mid-saturation accents on a near-white ground.

**Body, caption, label and kicker text is `#091F2E` ink. Always. No exceptions.**
No accent is AA-safe at normal size on the paper ground — purple, the strongest, reaches 4.41
against the 4.5 requirement.

| Token | On paper | Verdict |
|---|---|---|
| ink `#091F2E` | 16.02 | AAA — any size |
| primary `#8661C5` | 4.41 | display text only (≥24px bold / ≥32px regular) |
| magenta `#BF3AC4` | 4.33 | display text only |
| blue `#0078D4` | 4.31 | display text only |
| teal `#389A91` | 3.22 | display text only |
| teal-light `#49C5B1` | 2.02 | **decorative only — never text** |
| purple-light `#C5B4E3` | 1.81 | **decorative only — never text** |

**The roles invert on dark.** On `dark-field`, purple-light is 8.83 (AAA) and teal-light 7.94
(AAA) while primary drops to 3.63. Any token role from the old dark system must be
**re-derived, not carried across** — including the 8-dot spine, whose old 0.5/0.32 opacities
were tuned for a dark ground.

**Escape hatch:** if a design genuinely needs an accent at normal text size, switch that surface
to pure `#FFFFFF` — purple 4.64, magenta 4.55, blue 4.53 all clear AA there. That is the only
sanctioned reason to leave the warm ground.

Re-run after any palette edit:
```
py tools/contrast_gate.py brand/_extract/palette.json --min 3.0
```

## Typography

**Segoe UI Semibold** (display) and **Segoe UI** (body) are the brand faces. Embed via
`@font-face` from `fonts/` — a system-font lookup is not deterministic and drifts between
render machines.

Space Grotesk, JetBrains Mono and Fraunces are **not** brand fonts. They were used across all
44 predecessor videos; they do not carry forward.

## Semantic accents outrank brand accents

Scene-level semantic variables (`--do`, `--see`, `--teal`, `--coral`, `--incident`, `.strike`)
encode **meaning**. Meaning wins. They get new values tuned for the light ground but keep their
semantic role, stay mutually distinguishable, and stay distinguishable from brand chrome.
Never collapse them into the accent family.

## Corrections to the old spec

The previous hand-transcribed brand spec had real errors. Do not trust it:

- `ACC_MAGENTA #C03BC4` was **wrong** — the real `accent4` is `#BF3AC4`
- `DARK_PURPLE #463668` is **not in the theme** — invented; retired
- `dk2 #091F2E` (the real ink) and `lt2 #FFF8F3` (the real paper) were **missing entirely**

## Do — the frame must have somewhere to stand

This doctrine used to be only prohibitions. A rule set that answers *"what gets me
disqualified?"* and never *"what makes this frame good?"* produces the minimum legal frame:
outline shapes floating on a flat wash. That is a doctrine bug, not a taste failure.

**Every content frame owes the viewer three things.** A frame missing all three is sparse by
construction and should not pass review.

| | What it means | Cheapest honest version |
|---|---|---|
| **Ground plane** | The content sits *somewhere*. There is a floor, a surface, a bounded region — not a void. | A bounded panel with an edge, or a horizon/table line |
| **Depth** | At least two planes, near and far, distinguishable by more than colour. | Soft elevation on the near plane; scale + desaturation on the far |
| **An object with weight** | The subject reads as a thing, not a wireframe. | A filled form with an interior, not a 1px stroke |

**Elevation is allowed and encouraged.** A previous version of this file said *"No shadows,
anywhere."* That rule was **invented** — it appears nowhere in the extracted brand source, and it
single-handedly removed layering from the system. Use soft, low-contrast elevation
(`0 2px 8px rgba(9,31,46,.10)` and up) to separate planes. What is banned is a *hard drop
shadow used as decoration*, not depth itself.

**Ambient light is allowed** where it builds a place rather than decorates a corner. The old
"no ambient glows" line was reasoning from a dark-ground device; the underlying rule is *no
glow that carries no meaning*, which is a motion/composition rule, not a colour ban.

## Illustration, icons and glyphs — use the system, don't hand-draw

The playbook is explicit: **"Use the Microsoft Learn primary color palette for illustrations,
icons, glyphs, and diagrams,"** and names four sanctioned sources:

- Microsoft Learn illustrations
- WWL Learning Lab icons
- Microsoft IconCloud
- Fluent Icon Collections

### Reuse the source's own visuals before inventing new ones

The learning content you are adapting already ships its own **on-brand, authoritative** visuals —
screenshots, diagrams, and illustrations in the source module's `media/` folder. **Reuse them
first.** A diagram from the module is already correct, already approved, and already on palette;
re-drawing it from scratch risks drift and wastes effort. Break a source diagram into its parts and
**animate** it — each element revealing on its narrated beat — rather than dropping the flat PNG:
that earns the motion a raster can't give while keeping the source's own authority. Inventory the
source module's media at planning time and map each reusable asset to the beat it serves.

### Offer the author a capture, don't silently mock one

Where a beat teaches something that lives in a **real UI** — a portal step, an admin-center
setting, a report, a dashboard — a genuine **screenshot or screen recording** teaches it better
than an invented mock, and a fabricated UI risks being subtly wrong. When planning such a beat,
**flag it as a capture opportunity** and offer the author the chance to supply the real asset
(the `media-screenshot` / `media-screen-recording` blocks are built for exactly this). Give a
concrete suggestion — *what* to capture and *where* it lands — so the author can drop it in. Never
fabricate a portal UI as fact when a real capture was there for the asking.

**Hand-drawn SVG primitives are a legitimate choice, not the only one.** If a beat needs a
device, a cloud, a person, or a service mark and a real icon or illustration would carry it
better, use one — on the Learn palette. A 1px outline rectangle standing in for "a device" is a
placeholder, and placeholders should not ship.

**Generated assets are opt-in, not mandatory.** Generate one when it earns its place:

- the beat's subject is a *thing* the viewer should recognise (a device, a person, a place)
- the frame needs a foreground object with real weight that geometry can't supply
- a hero or closing frame is carrying the video's identity
- the user asked for one

Do **not** generate an asset because a beat looks empty. An empty beat is usually a composition
problem, and an illustration dropped into it is decoration. Schematic beats — flows, boundaries,
comparisons, narrowing — are frequently *better* as authored geometry, because geometry can
animate causally and a raster illustration cannot.

Freeze anything generated into the project's `assets/` so the render stays deterministic. The
predecessor pipeline did this (`hero-cloud.png`, `hero-bridge.png`, `hero-devices.png`) — worth
knowing the pattern exists, not worth copying wholesale.

## Don't

- No accent-coloured body text, ever *(contrast-derived)*
- No `teal-light` / `purple-light` text on a light ground *(measured)*
- No gradient field behind body copy *(contrast-derived)*
- No invented grounds
- No hard drop shadows as decoration — soft elevation for depth is fine, see **Do** above

## Open: two brand authorities

The ILT theme governs **ground and chrome**. Playbook slide 24 points illustrations, icons,
glyphs and diagrams at the **Microsoft Learn primary colour palette**, citing the Learn Style
Guide and a Microsoft Learn **Figma file**. They appear consistent (both purple/teal/blue) but
have not been formally reconciled. Until they are, use this doctrine for ground and chrome and
the Learn palette for illustration. The Figma reference is a hook for the upstream `figma`
skill (`hyperframes figma tokens`).
