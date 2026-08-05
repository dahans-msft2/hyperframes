---
version: alpha
name: Learn ILT — Frame (video / frame layer)
description: >
  Microsoft Learn / WWL ILT brand for companion videos. A LIGHT system: warm paper
  ground, deep navy ink, gradient fields (never flat fills), a frosted glass band, and a
  measured contrast law where body text is ALWAYS ink. Tokens are extracted from the ILT
  master template (theme1.xml + pixel-sampled slide exports), not invented. Motion is NOT
  governed here — motion belongs to motion-doctrine / cut-the-curve.
unit: the frame — 1920x1080 primary
principle: light is the brand · text is ink · the hero swoosh is scarce · every field is dithered

# NORMATIVE TOKENS (machine-readable). Prose below is context.
colors:
  # grounds (gradient FIELDS — apply as background on a full-bleed CHILD of the root, never the root)
  wash: "#FFF9F5"          # content-wash — the everyday ground, near-white warm
  paper: "#FFF8F3"         # lt2 — nominal warm paper
  ink: "#091F2E"           # dk2 — the one text colour. Always.
  text: "#091F2E"
  text-muted: "#33414D"    # dark slate — still AA on wash; use sparingly
  # brand accents — DISPLAY TEXT ONLY (>=24px bold / >=32px regular) OR non-text marks
  primary: "#8661C5"       # purple — strongest; 4.41 on paper (display only)
  magenta: "#BF3AC4"       # accent4 (corrected; NOT #C03BC4)
  blue: "#0078D4"
  teal: "#389A91"
  # decorative ONLY — never carry text
  teal-light: "#49C5B1"
  purple-light: "#C5B4E3"
  # surfaces
  border: "rgba(9,31,46,0.14)"
  glass-bg: "rgba(255,255,255,0.42)"
  card-bg: "rgba(255,255,255,0.55)"
  elevation: "0 2px 8px rgba(9,31,46,0.10)"
  positive: "#389A91"
  negative: "#BF3AC4"

grounds:
  content-wash: { use: "default — every content frame", css: "radial-gradient(120% 120% at 12% 4%, #FFFCFA 0%, #FFF9F5 46%, #F7F2F9 100%)" }
  hero-swoosh:  { use: "title · opening · closing · dividers (SCARCE)", css: "radial-gradient(90% 120% at 92% 8%, #CE88DF 0%, #86A0EB 22%, #78A6ED 40%, #B1DBDE 56%, #FCEBE6 74%, #FDF5F1 100%)" }
  section-field:{ use: "segment openers", css: "linear-gradient(105deg, #FEF9F5 0%, #C7DAEC 42%, #9BB5E2 66%, #BCB3E5 84%, #CED7E8 100%)" }
  dark-field:   { use: "the deliberate exception (white ink inverts here)", css: "radial-gradient(90% 120% at 6% 4%, #365F7D 0%, #121F42 38%, #0A142D 66%, #050D1A 100%)" }

radii:
  pill: "100px"
  card-lg: "16px"
  bar: "6px"
  circle: "50%"

typography:
  body:      { fontFamily: "Segoe UI", cqw: 0.94, weight: 400, lineHeight: 1.5, color: "text" }
  kicker:    { fontFamily: "Segoe UI Semibold", cqw: 0.73, weight: 600, tracking: "0.10em", upper: true, color: "ink" }
  h1:        { fontFamily: "Segoe UI Semibold", cqw: 3.75, weight: 600, lineHeight: 1.05, tracking: "-0.01em", color: "ink" }
  h2:        { fontFamily: "Segoe UI Semibold", cqw: 2.2, weight: 600, lineHeight: 1.1, color: "ink" }
  stat-num:  { fontFamily: "Segoe UI Semibold", cqw: 2.6, weight: 600, lineHeight: 1.0, color: "ink" }
  label:     { fontFamily: "Segoe UI", cqw: 0.68, weight: 600, color: "ink" }

spacing:
  pad-x: "6cqw"
  gap: "1.4cqw"

components:
  ground-field:
    description: "Full-bleed position:absolute inset:0 CHILD of the root/clip. Carries a ground gradient AND the mandatory dither overlay. Never put a full-bleed fill on the root itself (renders black)."
    dither: "::after feTurbulence noise, opacity 0.035, mix-blend-mode overlay, static seed — MANDATORY on every field or H.264 bands it"
  glass-band:
    backgroundColor: "{colors.glass-bg}"
    backdrop: "blur(28px) saturate(1.25)"
    rounded: "right end only"
    description: "Translucent blurred band on a gradient field, runs off the left edge, carries a title in ink. Upstream liquid-glass-* blocks implement this idiom."
  card-tinted:
    backgroundColor: "{colors.card-bg}"
    border: "1.5px solid {colors.border}"
    rounded: "{radii.card-lg}"
    shadow: "{colors.elevation}"
    description: "Universal content card. Soft elevation for depth is encouraged; a hard decorative drop shadow is not."
---

# Learn ILT frame

A **light system**. Warm paper, deep navy ink, gradient fields. This SUPERSEDES upstream
palette and typography. It does not touch motion.

## The contrast law — non-negotiable

**Body, caption, label and kicker text is `#091F2E` ink. Always.** No brand accent is AA-safe
for normal text on the near-white ground (purple, the strongest, reaches only 4.41 vs the 4.5
requirement). Accents are for **display text** (>=24px bold / >=32px regular) or **non-text
marks** (a chart line, a bar fill) — never body copy. On an image ground the rule is stricter
still: no accent passes anywhere; text is ink, full stop. Escape hatch: to use an accent at
normal text size, switch that surface to pure `#FFFFFF`.

Roles INVERT on `dark-field`: purple-light 8.83 (AAA), teal-light 7.94 (AAA) while primary
drops to 3.63. Re-derive any dark-ground role; never carry it across.

## Grounds

Four grounds, only four. `content-wash` is the everyday ground and is almost white — content
sits directly on it, no card required. The **hero swoosh is scarce**: title, section, closing,
dividers — nothing else. Spending it on a content frame is what makes a deck look cheap.
`dark-field` is the deliberate exception. Every field carries the mandatory dither overlay —
it looks flawless in preview and bands in the MP4 without it.

## Depth — the frame must have somewhere to stand

Every content frame owes the viewer three things: a **ground plane** (a surface, not a void),
**depth** (two planes, near/far, distinguished by more than colour — soft elevation is
encouraged), and **an object with weight** (a filled form, not a 1px wireframe).

## Typography

**Segoe UI Semibold** (display) and **Segoe UI** (body). Embed via `@font-face` from `fonts/`
for deterministic render — a system-font lookup drifts between machines. Space Grotesk /
JetBrains Mono / Fraunces are NOT brand fonts.

## Motion

Not here. Seams ride `cut-the-curve` in the film's current (default LEFT); the seam law is
`motion-doctrine`. This preset only fixes the look.
