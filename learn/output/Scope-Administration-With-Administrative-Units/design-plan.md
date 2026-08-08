# Design plan — Scope administration with administrative units

Preset: learn-ilt   Profile: unit-video   Run: scope-administrative-units-202608071310

The spine made visual: **over-privilege (no boundary) → the AU boundary drawn (dark-field
tentpole) → populate → the group-shortcut leak revealed**. Two matched diagram beats carry it —
beat 5 shows the boundary *solid* on the dark ground (glowing protected core), beat 8 shows the same
boundary *leaking* two levels down on the light ground. Ground contrast reinforces solid-vs-leaky.

## Ground allocation (at a glance)

| Ground | Scenes | Count |
|---|---|---|
| `hero-swoosh` (scarce) | 01-bumper · 02-title · 90-recap · 91-cta — **all chrome, zero body** | 4 |
| `section-field` (segment opener) | 03-objectives | 1 |
| `content-wash` (default) | beats 4, 6, 7, 8, 9, 10, 11 | 7 |
| `dark-field` (the one exception) | beat 5 — the boundary reveal | 1 |
| white (mandatory) | AI end card | 1 |

**Kit vs custom: 12 kit blocks, 1 custom** (beat 4, the over-reach). 13 authored scenes + injected
end card — within the profile's `max_scene_count` 16 (the approved beat plan segments 8 body beats,
each cue-anchored to locked narration, so they are not mergeable).

## Per-beat table

| # | Scene | Component | Kind | Why it fits | Ground | Config / Elements | Accent use | Asset / capture |
|---|---|---|---|---|---|---|---|---|
| 1 | 01-bumper | `bumper` | block | mandatory `opening.bumper` sting | hero-swoosh | kicker (builder fills from series) | ink glyph + accent rule (marks) | — |
| 2 | 02-title | `title-hero` | block | the video's title owns the frame | hero-swoosh | kicker `MICROSOFT LEARN`; title `Scope administration` / `with administrative units`; subtitle | **ink only** (display) | — |
| 3 | 03-objectives | `list-steps` | block | ordered 3-objective roadmap previewed before the body | **section-field ⚑** | 3 chips (script copy) | accent number badges (marks); ink text | — |
| 4 | body — over-privilege | **custom** | custom | no block carries *unbounded* over-reach; it is the "before" that beat 5's layers diagram closes | content-wash | tenant ring flooded by the admin's reach; HQ-exec cluster lit as collateral | `--incident` coral reach + `.strike` (marks) | **capture opt** (optional inset) |
| 5 | body — the boundary **[spine]** | `diagram-layers` | block | containment/trust-boundary around a protected core — the block's exact `best_for` | **dark-field ★** | layers `Tenant (Entra ID)` → `Administrative unit` → core `Office users`; object-type glyphs settle into core | inverted teal-light/purple-light **glow** on core (marks, AAA) | reuse **rejected** |
| 6 | body — populate | `list-select` | block | two peer methods, dynamic emphasized (choose-one) | content-wash | items `Assigned` / `Dynamic`; `selectedIndex` = Dynamic; countLabel | accent tab on the lifted row (mark) | — |
| 7 | body — the shortcut (**PREDICT**) | `callout-note` | block | one held question, answer withheld across the cut | content-wash | label `PREDICT`; term `The group shortcut`; body = the question; `New Office, All Staff` chip drops into an AU glyph | `--see` accent tab (mark); **ink** label/body | — |
| 8 | body — the reveal **[payoff]** | `diagram-flow` | block | walk the two-hop path, hit the wall at step two — `relationships/links matter more than nesting` | content-wash | `Unit` → `Group` (✓ in scope) → `Members` (✗ unreachable); two-hop | `--do` teal ✓ + `--incident` coral ✗/`.strike` (marks/glyphs) | reuse **rejected** |
| 9 | body — the rule + fix (**KEY POINT**) | `callout-note` | block | the single governing principle stated as a definition | content-wash | label `KEY POINT`; term `Direct membership only`; body = rule + the fix | `--teal` accent tab (mark); **ink** text | — |
| 10 | body — dynamic constraint | `list-specs` | block | three hard limits as label/value rows | content-wash | rows `Object type → exactly one`, `Users + devices → two units`, `Group member → not supported`; user/device glyphs | accent underline rules (marks); ink text | — |
| 11 | body — licensing | `list-specs` | block | a cost sheet — the fine-print twin of beat 10 | content-wash | rows `Dynamic → Entra ID P1 (per member)`, `Assigned → Free`; licenses icon | `--incident` (P1) vs `positive` teal (Free) fills (marks); ink text | — |
| 12 | 90-recap | `title-hero` | block | closing payoff owns the frame, bookends the title | **hero-swoosh ⚑** | kicker `RECAP`; title `One slice,` / `scoped correctly`; subtitle | **ink only** | — |
| 13 | 91-cta | `title-hero` | block | next-step card | **hero-swoosh ⚑** | kicker `NEXT STEP`; title `Build a unit` / `yourself`; subtitle | **ink only** | — |
| — | end card | AI disclosure | injected | mandatory `endcard.ai-disclosure` | white | `assets/AI_End_Card.mp4` | — | — |

`⚑` = deliberate chrome override (see **Chrome overrides**). `★` = the one dark-field scene.

## Chrome overrides (flagged for the builder)

The scaffold stamped these three defaults; I am overriding them on purpose — swap the ground, keep
the block:

1. **03-objectives → `section-field`** (scaffold default `content-wash`). The objectives roadmap
   is the video's one segment-opener moment; `section-field` is sanctioned for exactly that, and it
   sets a single cool field between the warm-swoosh title and the warm-wash body. This is the only
   `section-field` spend in the video.
2. **90-recap → `hero-swoosh`** (scaffold default `content-wash`). The closing payoff earns the
   swoosh and makes a symmetric bookend with the title.
3. **91-cta → `hero-swoosh`** (scaffold default `content-wash`). Closing chrome; matches the locked
   input "hero-swoosh for title + CTA."

## Frame obligations

Every body beat names its ground plane, two depth planes, and object with weight. Chrome
`title-hero` / `list-steps` / `bumper` satisfy these natively (elevated cards + accent rule on a
field), so the risk beats are the schematic body beats — especially the one **custom** beat:

- **Beat 4 (custom — over-reach).** Ground plane: the **tenant boundary ring** (Microsoft Entra ID
  directory) as a bounded region — a real floor, not a void. Depth: **near** = the scoped admin as a
  filled, softly elevated role chip (`0 8px 28px rgba(9,31,46,.10)`); **far** = the field of directory
  users, smaller and desaturated, filling the ring, with the HQ-exec cluster distinct. Object with
  weight: the admin token (filled avatar + Entra-role chip) and the reach rendered as a **filled**
  coral wash/arrows flooding to the ring edge — never 1px strokes. This is an honest schematic
  (rings + reach), *not* a fabricated portal blade.
- **Beat 5 (diagram-layers).** Ground plane: the concentric planes themselves on the dark field.
  Depth: outer Tenant ring recessed/desaturated vs the near, elevated AU ring; the core lifts and
  **glows last**. Object with weight: the filled core disc holding the office-user + object-type
  glyphs.
- **Beat 6 (list-select).** Ground plane: the row stack on a tinted card. Depth: the lifted Dynamic
  row rises on soft elevation while the Assigned row recedes. Object with weight: the filled,
  accent-tabbed selected row.
- **Beat 7 (callout-note).** Ground plane: the callout panel. Depth: panel elevated over the wash;
  the `New Office, All Staff` chip drops onto an AU glyph behind it. Object with weight: the filled
  callout card + accent tab.
- **Beat 8 (diagram-flow).** Ground plane: the flow's node lane. Depth: the emphasized Group node
  lifts; the unreachable Members recede and grey. Object with weight: filled nodes (not wireframes),
  the ✓/✗ glyphs, the struck connector.
- **Beat 9 (callout-note).** As beat 7 — elevated definition card, filled accent tab, the term
  `Direct membership only` as the weighted subject.
- **Beats 10 & 11 (list-specs).** Ground plane: the spec sheet on a tinted card. Depth: rows stagger
  in on soft elevation; the emphasized row (10: "exactly one"; 11: the Free/P1 contrast) sits proud.
  Object with weight: filled value chips + the object-type / license glyphs.

## Signaling cues (each tied to a spoken word via `anchors.json`)

The narration names things in sequence; the visual reacts **on the word**. The builder anchors each
via `tools/word_anchors.py` against `transcript.json` — never a guessed offset. Anchor keys are live
in `anchors.json`.

| Beat | Anchor key | Spoken phrase | Cue |
|---|---|---|---|
| 2 | `hook_one_slice` | "one slice of the directory" | title's second line lands |
| 3 | `objectives_boundary` | "draws that boundary" | objective-1 chip lifts |
| 4 | `overprivilege_hq` | "the executives back at headquarters" | reach floods to the ring edge; HQ-exec cluster flashes coral / `.strike` |
| 5 | `au_holds_types` | "holds users, groups, or devices" | the three object-type glyphs settle into the core |
| 5 | `au_scoped_objects` | "only to the objects that unit contains" | the AU ring closes; the core **glows**, reach dims outside it |
| 6 | `populate_dynamic` | "populate it automatically" | the **Dynamic** row lifts with its accent tab |
| 7 | `shortcut_group` | "New Office, All Staff" | the group chip drops into the AU glyph |
| 7 | `predict_question` | "for the people in the group" | the question pulses and **holds** (predict withhold) |
| 8 | `reveal_group_scope` | "the group object into scope" | the Group node lights ✓ (in scope) |
| 8 | `reveal_two_steps` | "two steps removed" | the connector to Members greys/`.strike`; the Members **shake** (unreachable) |
| 9 | `rule_direct_membership` | "direct membership only" | the term punches into the callout |
| 9 | `fix_add_directly` | "add the users to the unit directly" | the fix line reveals |
| 10 | `constraint_object_type` | "exactly one object type" | the "one object type" row highlights |
| 10 | `constraint_no_group` | "can't hold a group at all" | the group row strikes out |
| 11 | `licensing_covers` | "every user or device the rule covers" | the P1 row's per-member cost tallies |
| 11 | `licensing_free` | "a Free license covers members" | the Free row lifts as the low-cost answer |
| 12 | `recap_scoped` | "scoped correctly now" | the payoff line lands |
| 13 | `cta_exercise` | "build one of these units yourself" | the CTA line lands |

A beat where nothing moves with the words is the "could this be a PDF" failure. Every body beat
above has ≥1 word-anchored cue.

## Predict → reveal (engagement — honor the withhold)

Beats 7 and 8 are the video's predict-before-reveal. The withhold is **structural**: scene 7 ends on
the held question (`for the people in the group` + the ~600ms narration pause), scene 8 *opens* with
the answer. Do not preview the answer in scene 7. The reveal (beat 8) is the pedagogical climax and
earns the richest causal motion — the two-hop walk that stops at the wall — carried on the light
ground so it rhymes against beat 5's solid dark boundary.

## Component range

Six distinct components across eight body beats — variation tracks the teaching relationship, not
decoration:

- **custom** (beat 4) — *unbounded over-reach.* No block carries "a role whose reach has no
  boundary." Nearest rejected: `diagram-layers` (`avoid_when`: it asserts containment — the very
  thing missing here; using it would imply a boundary that doesn't exist) and `media-screenshot` (a
  static scope dropdown can't show the reach *spreading*; over-reach is a motion idea). Justified as
  the causal "before" that beat 5's `diagram-layers` completes.
- **`diagram-layers`** (beat 5) — *containment / trust boundary.* Content-shape = nested scopes
  outside-in around a protected core. Rejected `diagram-flow` (`avoid_when`: nesting, not
  links, carries the meaning here).
- **`list-select`** (beat 6) — *choose-one among peers.* Two population methods, Dynamic emphasized.
  Rejected `list-steps` (these are alternatives, not an ordered procedure) and `list-specs` (one
  option is selected/lifted, not a flat attribute sheet).
- **`callout-note`** ×2 (beats 7, 9) — *single emphasized takeaway.* Deliberate **question → rule
  rhyme**: beat 7 poses the PREDICT question, beat 9 (after the climax) crystallizes the KEY POINT
  that answers it. Two beats apart, different label + semantic tab + glyph, so they read as a
  matched pair, not repetition. Beat 9 is the single most callout-appropriate beat in the script.
- **`diagram-flow`** (beat 8) — *a walked path that hits a wall.* Node→connector→emphasis machinery
  walks Unit → Group → Members and stops at step two. Rejected `diagram-layers` (the point is the
  *link* where scope stops, not the nesting) and the module PNG (see Assets).
- **`list-specs`** ×2 (beats 10, 11) — the **"dynamic membership fine print" diptych**: beat 10 =
  what a dynamic unit *can't hold* (constraints), beat 11 = what it *costs* (licensing). Adjacent by
  narration order and deliberately paired; differentiated (10 = 3 constraint rows, 11 = a 2-row
  Free/P1 cost contrast). Rejected `console-status` for beat 10 (its pending→passed flip implies a
  positive resolution — wrong for hard NOs) and `list-select` for beat 11 (a cost trade-off, nothing
  is "selected").

## Builder shopping list

**Kit blocks to copy in** (`templates/blocks/<id>.html` → `scenes/`):
`bumper`, `title-hero` (×3: title, recap, cta), `list-steps`, `list-select`, `callout-note` (×2),
`diagram-flow`, `list-specs` (×2), `diagram-layers`.

**Custom scenes to hand-author** (on `templates/blocks/_foundation.css`, same tokens / type scale /
grounds): **1** — beat 4, the over-reach blast-radius diagram.

**Grounds** already in `assets/grounds/` (content-wash, hero-swoosh, section-field). `dark-field` is
CSS (foundation `#root[data-ground="dark-field"]`) — no PNG. Every field carries the mandatory dither
overlay; judge banding on the rendered MP4, not the preview.

**Icons to pull** (`py tools/icon_index.py add --project . <name>` — icons must live in the project
at render):

| Icon | Source | Beats |
|---|---|---|
| `Entra` (Security kit SVG) | `Microsoft-Security-product-icons-kit/Entra` | 5 (the tenant/Entra ID plane) |
| `Users` | `Azure/identity/10230-icon-service-Users.svg` | 5, 10 (object type) |
| `Groups` | `Azure/identity/10223-icon-service-Groups.svg` | 5, 7, 8, 10 (the group object) |
| `Devices` | `Azure/intune/10332-icon-service-Devices.svg` | 5, 10 (object type) |
| `Entra-Identity-Licenses` | `Azure/identity/02681-icon-service-Entra-Identity-Licenses.svg` | 11 (P1 / Free) |

Prefer SVG. `Groups` is ambiguous in the index (many "group" icons) — pull the Azure/identity
`10223-icon-service-Groups` specifically. Restraint holds: one clear icon per concept.

## Assets — reuse, capture, generate (in that order)

**Source module media — inventoried, reuse rejected with cause.** The unit ships two diagrams:
`media/7-administrative-unit-group-scoping-gap.png` (the beat-8 candidate) and
`media/6-nested-group-non-cascade.png`. Both are **informal hand-drawn doodles** — handwritten
marker font, sketchy strokes, casual whiteboard aesthetic. They are decidedly *off* the ILT frame
(Segoe UI, clean geometry, gradient grounds), and a raster **cannot animate causally**. Beat 8's
entire value is the word-anchored two-hop walk that stops at "two steps removed" — exactly the
causal motion a doodle PNG can't give. **Reject reuse; author beat 8 as `diagram-flow` geometry.**
(The source diagrams remain useful as *reference* for the correct logic, which the fidelity ledger
already confirms — not as shipped art.)

**Capture opportunity (optional, offered to the author).** Beat 4 teaches a real UI: the Entra admin
center → **Roles & administrators → User Administrator** assignment with **scope = Directory**.
The primary beat-4 visual is the custom over-reach schematic (it teaches the *danger*, which a static
blade can't), but a genuine screenshot of that scope value would make a strong corroborating **inset**
("proof the scope really reads Directory"). If the author supplies it, drop it via `media-screenshot`
into a corner of beat 4 with a callout on the scope field. Do **not** fabricate the blade as fact.

**Generated assets: none.** Every body beat is schematic (boundaries, reach, a two-hop path,
constraints, cost) — authored geometry that animates causally beats a raster here. No beat earns a
generated illustration.

## Hero-swoosh budget

Spent on scenes: **01-bumper, 02-title, 90-recap, 91-cta** — 4 scenes, **all opening/closing chrome,
zero body**. This is the ideal use: the swoosh bookends the video (open on the field, all teaching on
the warm wash, close returns to the field). Every spend is sanctioned chrome; none lands on a content
frame.

## Dark-field allocation

Spent on: **beat 5, the boundary reveal** (the one dark scene). Why it earns it: it is the concept
the whole video orbits (the AU boundary = least privilege), and `diagram-layers`' "protected core
that glows last" is the kit's single best block+ground synergy — a glow only reads on a dark field.
It plants the visual tentpole early, so the boundary is burned in before beat 8 shows it leaking.
Runner-up (beat 8, the climax) is deliberately kept on `content-wash`: its drama is the *causal
contradiction* (the boundary we saw solid on dark now leaks on light), not a dark ground. Two
distinct peaks, not one stacked.

## Contrast declarations

Measured with `tools/contrast_gate.py` (WCAG 2.1). **All readable text is ink `#091F2E`** (white,
auto-inverted, on dark-field). **No accent carries normal-size text on any light ground** — every
accent below is a mark, glyph, or display element.

| Text / ground pair | Ratio (worst → best) | Verdict |
|---|---|---|
| ink `#091F2E` on `content-wash` (beats 4,6–11) | 12.27 → 15.91 | **AAA** |
| ink on `section-field` (03-objectives) | 7.91 → 16.13 | **AAA** |
| ink on `hero-swoosh` colour field (01,02,90,91) | **5.95** (doctrine) | **AA** — the video's floor |
| white ink on `dark-field` (beat 5) | 16.84 | **AAA** |
| teal-light `#49C5B1` glow on `dark-field` (mark) | 7.94 | AAA (decorative here) |
| purple-light `#C5B4E3` glow on `dark-field` (mark) | 8.83 | AAA (decorative here) |

**Worst readable-text ratio in the whole video: 5.95:1 (ink on hero-swoosh) — a pass.** Everyday
body text (content-wash) floors at **12.27 (AAA)**.

Guardrails the builder must hold:
- On `hero-swoosh`, keep display type **out of the bottom-right third** (left column 15.6 vs 5.95).
  `title-hero` places the title upper-left — compliant by default.
- **Never** set an accent as normal-size text on a light ground. On `content-wash`, the accents fail
  as text: teal-light 1.39–2.02, purple-light 1.39–1.81, teal 1.55–3.22, blue 2.13–3.30,
  purple 2.18–3.38. They are permitted only as marks/glyphs, or as **display** text (≥24px bold /
  ≥32px regular). `callout-note` labels are small → keep them **ink**, not accent.
- Beat 4 and beat 8 semantic accents (coral reach/✗, teal ✓, `.strike`) are **marks and glyphs**,
  not text — allowed regardless of contrast. The labels beside them stay ink.
- **Semantic accents outrank brand accents** and encode meaning: `positive` teal `#389A91` = reachable
  / Free; `--incident` coral = unreachable / P1 cost; `.strike` = the two-steps-removed break. Retune
  coral for the light ground and re-run `py tools/contrast_gate.py brand/_extract/palette.json
  --min 3.0` if it introduces a new colour. Keep them mutually distinct and distinct from brand chrome.

## Motion budget

Profile `max_static_stretch_seconds = 5.0`. Every body beat carries a word-anchored cue (table
above), so no beat holds still past the budget. The densest beats (5 the boundary, 8 the reveal)
carry the most sustained motion; the predict beat (7) is the one deliberate stillness-before-climax
— it holds the question, but under 5.0s to the cut. Two markers the designer places that compile to
native `check` assertions:
- `data-reveal-after` on beat 8's Members node (it must not appear before the Group node it depends
  on) and on beat 9's fix line (after the rule).
- `data-keep-in-frame` on beat 4's full-frame tenant ring and beat 5's concentric stage (full-frame
  stages that could drift off-canvas).

## Fonts

Segoe UI (body) / Segoe UI Semibold (display), embedded from `fonts/`. No Space Grotesk / JetBrains
Mono / Fraunces. Cloud gate uses the fallback face by design; local render uses real Segoe.
