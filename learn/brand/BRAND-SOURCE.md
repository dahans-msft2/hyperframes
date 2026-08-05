# Brand source of truth — extracted, not transcribed

Extracted 2026-08-03 by `tools/extract_brand.py`. Raw output: `_extract/ilt-theme.json`.

**Source**: `MD-102-Refresh-Working/md102-companion-videos/_source/ilt-templates/ILT-Course-Content-Neutral-Template.potx`
**Master**: `Microsoft ILT Course Content Neutral` · 49 layouts · 13.333 × 7.5 in (16:9, = 1920×1080)

The authoritative theme part is **`ppt/theme/theme1.xml`, named "Light Mode"**. The deck also
carries `theme2`/`theme3`, which are stock Office themes — ignore them.

---

## Color scheme (all 12 OOXML slots, verbatim)

| Slot | Hex | Role |
|---|---|---|
| `dk1` | `#000000` | text ink |
| `lt1` | `#FFFFFF` | pure white |
| `dk2` | `#091F2E` | **deep navy ink** — was missing from the old spec |
| `lt2` | `#FFF8F3` | **warm paper ground** — was missing from the old spec |
| `accent1` | `#8661C5` | purple |
| `accent2` | `#389A91` | teal |
| `accent3` | `#0078D4` | Microsoft blue |
| `accent4` | `#BF3AC4` | magenta |
| `accent5` | `#49C5B1` | light teal |
| `accent6` | `#C5B4E3` | light purple |
| `hlink` | `#0078D4` | link |
| `folHlink` | `#0078D4` | followed link |

## Font scheme

| Role | Typeface |
|---|---|
| major (headings) | **Segoe UI Semibold** |
| minor (body) | **Segoe UI** |

---

## Delta vs. the previous hand-transcribed spec

The old `templates/brand-spec.md` + `_engine/render_enhancements.py` carried 7 tokens
transcribed by hand from a slide. Reconciliation:

| Old token | Old value | Theme value | Verdict |
|---|---|---|---|
| `ACC_PURPLE` | `#8661C5` | `accent1 #8661C5` | ✅ exact |
| `ACC_EXP_TEAL` | `#389A91` | `accent2 #389A91` | ✅ exact |
| `ACC_BLUE` | `#0078D4` | `accent3 #0078D4` | ✅ exact |
| `ACC_TEAL` | `#49C5B1` | `accent5 #49C5B1` | ✅ exact |
| `ACC_LIGHT_PURPLE` | `#C5B4E3` | `accent6 #C5B4E3` | ✅ exact |
| `ACC_MAGENTA` | `#C03BC4` | `accent4 #BF3AC4` | ❌ **WRONG** — transcription error |
| `DARK_PURPLE` | `#463668` | *not in theme* | ⚠️ **invented** for the video system |

**Missing from the old spec entirely** — and both are load-bearing for the retheme:
- `dk2 #091F2E` — the brand's real dark ink (a deep navy, not a purple)
- `lt2 #FFF8F3` — the brand's warm paper ground

Also never captured: the brand's actual typefaces are **Segoe UI / Segoe UI Semibold**. The
44 shipped videos used Space Grotesk + JetBrains Mono + Fraunces — none of which are brand fonts.

---

## Finding: the brand is a LIGHT system

Three independent confirmations that the ground inversion is a **return** to brand, not a
departure from it:

1. The theme part is literally named **"Light Mode"**.
2. The palette ships a warm paper ground (`lt2 #FFF8F3`) and a deep navy ink (`dk2 #091F2E`) —
   a light-ground pairing. It ships no dark ground at all.
3. The mandatory AI disclosure end card is **white with black text** (verified by frame
   extraction — see below).

The MD-102 videos went dark-dominant (24 of 44) against the brand, and the invented
`DARK_PURPLE #463668` ground has no basis in the theme. Every dark video today therefore ends
on an unmotivated hard cut to a white end card. **Going light removes an existing clash.**

---

## AI disclosure end card — verified specs

`ffprobe`, 2026-08-03. The `normalized` column is a **historical** measurement — that file was
deleted when the ffmpeg-concat flow was retired. It is recorded here only to document why a
second, much smaller copy of the card is not something to go looking for.

| | `AI_End_Card.mp4` (ships) | `AI_End_Card_normalized.mp4` (deleted) |
|---|---|---|
| Resolution | 1920×1080 | 1920×1080 |
| Frame rate | 30 fps | 30 fps |
| Duration | 10.666667 s | 10.666667 s |
| Video | h264 | h264 |
| Audio | **none** | aac 48 kHz stereo (silent) |
| Size | 8,885,320 B | 525,712 B |

Content: white ground, black `Segoe UI`-style text — *"This video was created by humans using
AI tools"* — with `humans` and `AI` in a purple→blue gradient (reads as `accent1 #8661C5` →
`accent3 #0078D4`). Frame: `_extract/endcard-frame.png`.

**Use the ORIGINAL, not `_normalized`.** `_normalized` was prepared for ffmpeg concat: it adds a
silent audio track and re-encodes at ~394 kbps (a 17× size reduction, so visibly degraded).
Authoring the card into the composition means HyperFrames re-encodes anyway — feeding it the
already-compressed copy would double-compress it. The original's lack of an audio stream is an
advantage, not a problem: no silent track to fight the narration mix.

Resolution matches the **composition** (1920×1080), not the 1280×720 deliverable, so it drops
in natively.

---

## Open: two brand authorities

Playbook slide 24 ("Brand Guidance and Visuals") directs illustrations, icons, glyphs and
diagrams to the **Microsoft Learn primary color palette**, citing the Microsoft Learn Style
Guide, Microsoft Learn illustrations, a **Microsoft Learn Figma file**, and WWL Learning Lab
icons/diagrams. That is a different authority from this deck's theme.

The two appear consistent (both are the purple/teal/blue family), but the Learn palette has not
been extracted and reconciled. Until it is, this theme is the authority for **chrome and
ground**; the Learn palette governs **illustrations and icons**.

The referenced Figma file is a hook for the upstream `figma` skill (`hyperframes figma tokens`).

---

## Ground artwork — exported from the deck, 2026-08-04

Three grounds are now the deck's own exported PNGs rather than CSS reconstructions, in
`assets/grounds/`. All are 1920×1080 so they map 1:1 to output pixels with no render-time
rescale.

| Ships as | Exported as | Role |
|---|---|---|
| `ground-content-wash.png` | `background-gradient-light.png` | everyday content ground |
| `ground-section-field.png` | `background-gradient-dark.png` | segment openers |
| `ground-hero-swoosh.png` | `background-swoosh.png` | title / divider / closing |

Named by role, not by export filename: "dark" is misleading for what is a pale blue wash, and
it is *not* the near-black `dark-field`, which has no equivalent in the deck and stays CSS.

Four findings worth not rediscovering:

- **`background-gradient-medium.png` is a duplicate of `light`.** Full-resolution comparison:
  71.5% of pixels differ, but the maximum difference is **2/255** — dithering noise, not
  content. The 134 KB vs 300 KB file-size gap is encoder settings. Only one is installed.
- **The swoosh PNG is a 2× upscale of a 960×540 source**, not a native 1920 render (arc
  transition measures 5px). This is fine and better than the original: pre-resampling to the
  exact output size removes render-time rescaling, which was the actual moiré risk. The dot
  halftone survived at ~95% of its original energy.
- **A CSS gradient cannot replace these.** A 7-stop simulation fitted to the real pixels gives
  worst-case error 14.87/255 on the wash and 37.45/255 on the section field — visible bands.
  An earlier fit that appeared to pass was measuring residual against its own bucket means,
  which is circular.
- **The exports are NOT dithered.** `ground-content-wash.png` carries only 16 distinct
  luminance levels with a median flat run of 49px (longest 810px). The mandatory noise layer
  applies to image grounds exactly as it does to CSS ones — see `learn-brand-doctrine`.

The SVG export route is a dead end: PowerPoint wraps a raster rather than emitting vectors
(960×540 viewport, one base64 `<image>` at 1024×577, zero gradient defs).
