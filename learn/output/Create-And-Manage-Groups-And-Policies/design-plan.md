# Design plan — Create and Manage Groups and Policies

Preset: learn-ilt   Profile: unit-video (~240s · ~10 scenes · max static 5.0s)

Spine: **types → membership → nesting (predict → reveal) → naming → expiration.** The design
gives the wrong-prior ("nesting cascades like folders") its own two-beat arc and spends the single
`dark-field` on the moment that prior is contradicted. Everything else stays on the everyday wash;
the swoosh is reserved for the opening/closing bookend.

## Per-beat table

| Beat | Component | Kind | Why it fits | Ground | Config / Elements | Accent use | Asset / capture |
|---|---|---|---|---|---|---|---|
| `01-bumper` | bumper | block | mandatory brand open (chrome, as stamped) | hero-swoosh | kicker `MICROSOFT ENTRA ID` | ink; rule wipe is a graphic | — |
| `02-title` | title-hero | block | the title owns the frame over the curiosity-gap hook | hero-swoosh | kicker + 2-line title + subtitle (chrome) | ink only (accent rule = graphic) | — |
| `03-objectives` | list-steps | block | three stakes as a numbered ladder (chrome, as stamped) | content-wash | 3 objective steps framed as stakes | ink; accent number badges (graphic) | — |
| B1 | list-select | block | two group *types*, choose the one that fits an access problem | content-wash | kicker `GROUP TYPES` · items[Security group / Microsoft 365 group] · selectedIndex 0 · countLabel `2 group types` · icons: Entra ID on Security row, Microsoft 365 on M365 row | ink text; selected-row accent tab (graphic) | — |
| B2 | list-select | block | two *membership models*, choose one — the matched second half of the same decision framework | content-wash | kicker `MEMBERSHIP` · items[Assigned / Dynamic] · selectedIndex 1 · countLabel `2 membership models` · "attributes → auto" glyph on the Dynamic row | ink text; selected-row accent tab (graphic) | — |
| B3 | diagram-layers | block | nesting shown as **containment** (parent contains child) — the folders mental model, reveal withheld | content-wash | layers outer→inner [`All Engineering (parent)`, `New Office (nested)`] · core `Members?` · license badge on the parent plane · **`?` over the boundary, answer gated off** (`data-reveal-after`) · `data-keep-in-frame` | ink text; license badge + ring = graphics | — |
| B4 | diagram-flow | block | reframes containment → **membership graph**: badge reaches direct members, halts at the nested boundary — the reached-vs-not payoff | **dark-field** | nodes: Parent group → license/resource badge → direct members (**reached ✓**); nested child group → its members (**not reached ✕**) · emphasized decision = the halt · chosen branch `direct members only` · not-reached gated after reached (`data-reveal-after`) · `data-keep-in-frame` | white ink (auto-inverted); semantic teal ✓ / magenta ✕ marks + blue connectors = graphics | reuse fallback: `media/6-nested-group-non-cascade.png` (author's option) |
| B5 | callout-note | block | one emphasized rule generalizes the reveal — a KEY POINT card, not a list | content-wash | label `KEY POINT` · term `DIRECT MEMBERS ONLY` · body "Group-based licensing resolves direct membership only — a user a level down is invisible to it." | ink text; accent tab + glyph (graphics) | — |
| B6 | list-specs | block | naming policy is a set of **fields** (label/value fact sheet) | content-wash | rows: `Prefix / suffix · GRP_[GroupName]_Engineering`, `Blocked words · CEO, Payroll, HR`, `Requires · Microsoft Entra ID P1` · focal = name assembling with the prefix · Entra ID icon on the Requires row | ink text; accent underline rules (graphics) | — |
| B7 | list-steps | block | expiration is an **ordered lifecycle** of 4 stages | content-wash | steps: `Lifetime in days` → `Owners renew (active groups auto-renew)` → `Unrenewed deleted` → `Restorable 30 days` · focal opens on step 1, closes on step 4 | ink text; accent number badges + connector (graphics) | — |
| B8 | list-specs | block | the exam-tested constraints are **label/value** facts | content-wash | rows: `Policies per tenant · 1`, `Scope · All or Selected subset`, `License · P1 or P2 for covered members` · focal = the `1` | ink text; accent underline rules (graphics) | — |
| `90-recap` | title-hero | block | three recap chips mirror the objectives (chrome, as stamped) | content-wash | kicker `RECAP` + payoff line + subtitle | ink only | — |
| `91-cta` | title-hero | block | closing call to action — **override to hero-swoosh** to bookend the title | **hero-swoosh** (override) | kicker `NEXT STEP` + CTA line + Learn subtitle + next-unit chip | ink only (accent rule = graphic) | — |

`Component` is a kit-block id from `blocks/catalog.json` (or `custom`). `Kind` is `block`/`custom`.
For blocks, `Config / Elements` names the CONFIG the builder sets; the `Ground` is applied by the
builder as `data-ground` on the block's `#root`.

**Chrome override (builder action):** swap `91-cta` `data-ground` from the scaffolded
`content-wash` to `hero-swoosh`. This is the only chrome change; every other chrome scene stays as
stamped by `new_project.py` / `chrome.json`. Reason: the CTA is the closing frame, and doctrine
lists "closing" as a sanctioned swoosh use — lifting it back to the swoosh bookends the video's
identity with `02-title`.

## Frame obligations

Every beat states its **ground plane · two depth planes · object with weight**. The kit blocks
supply all three by construction (elevated `.ilt-panel` on the ground = near/far planes; filled
nodes/badges/rows = weighted objects) — no beat is a wireframe on a void.

| Beat | Ground plane | Near / far planes | Object with weight |
|---|---|---|---|
| B1 / B2 | the wash + row rail | elevated selected row (near) vs receded peers (far) | the filled, tabbed selected row |
| B3 | the wash | inner `New Office` plane (near) inside the `All Engineering` plane (far) | the license badge sitting on the parent plane |
| B4 | dark navy field | reached direct-members cluster (near, lit) vs nested members (far, dimmed) | the license/resource badge that visibly halts at the boundary |
| B5 | the wash | elevated key-point panel (near) over the wash (far) | the filled callout card with its accent tab |
| B6 / B8 | the wash | elevated spec sheet (near) over the wash (far) | the assembling `GRP_…` name / the punched `1` |
| B7 | the wash | connector-linked step badges (near) over the wash (far) | the four filled number badges on the connector |

## Component range

Six distinct block types carry eight body beats — the video does **not** share one layout:

- **list-select ×2** (B1, B2) — deliberate matched pair. B1 and B2 are the two halves of one
  decision framework ("first the type, then the membership"); presenting them in the same
  choose-one form is the pedagogy, not laziness. Distinguished by kicker, selectedIndex, and cue
  (B1 lifts row 0 on the verdict; B2 lifts row 1 with an attributes→auto glyph). Closest rejected:
  `list-specs` — its `avoid_when` names "peers being chosen among" and points at exactly this
  archetype; here one row **is** selected, so `list-select` wins.
- **diagram-layers** (B3) — containment/inheritance arranged outside-in; the folders mental model.
  Closest rejected: `list-select` (its `avoid_when`: "containment… use diagram-layers").
- **diagram-flow** (B4) — branching *reached vs not-reached*, the cognitive-conflict payoff.
  Closest rejected: `media-screenshot` reusing `6-nested-group-non-cascade.png` — rejected because
  authored geometry animates the badge **halting** causally on the narrated word ("two steps
  removed"), which a Ken Burns push on a static PNG can't; the reuse asset stays on offer to the
  author.
- **callout-note** (B5) — one emphasized definition. Closest rejected: `list-specs` (its
  `avoid_when`: "a single emphasized fact… use callout-note").
- **list-specs ×2** (B6, B8) — both are genuine label/value fact sheets (policy fields; exam-tested
  constraints). Closest rejected for each: `list-steps` — rejected because neither is an ordered
  procedure (B6 fields are unordered; B8 constraints are unordered).
- **list-steps** (B7) — the one genuinely ordered lifecycle. Closest rejected: `diagram-flow`
  (list-steps `avoid_when`: "a branching decision"); the lifecycle is linear, not branching.

**Custom vs kit:** 8 body beats, **0 custom, 8 blocks.** No beat needed a bespoke layout — the kit
carries every teaching relationship in this unit.

## Builder shopping list

- **Kit blocks to copy in (body):** `list-select`, `diagram-layers`, `diagram-flow`,
  `callout-note`, `list-specs`, `list-steps`. (Chrome blocks `bumper`, `title-hero`, `list-steps`
  are already stamped.)
- **Custom scenes to hand-author:** none.
- **Grounds:** `content-wash` and `hero-swoosh` PNGs are already in the project; `dark-field` is
  CSS-only (the foundation paints it from `#root[data-ground="dark-field"]`) — nothing to copy for B4.
- **Icons to pull** (`py tools/icon_index.py add --project . …`): Microsoft Entra ID (B1, B2, B6),
  Microsoft 365 (B1). Prefer SVG; wire on the row each labels.

## Assets — reuse first, then capture, then generate

**Reuse (source module media):** `provision-govern-identities-entra/media/6-nested-group-non-cascade.png`
("a policy on a parent group reaches direct members but not the members of a nested child group")
is the authoritative artwork for the nesting non-cascade. It is offered to the author as the **B4
fallback**; the primary B4 is an authored `diagram-flow` because the halt must animate on the
narrated word, which the static PNG cannot.

**Capture opportunities:** none. Per the script's beat plan, every teaching beat in this unit is
conceptual and served by invented graphics (Mayer *Image*) — no portal step, setting, report, or
dashboard is taught, so no screenshot/recording is warranted. Do not fabricate a portal UI.

**Generated assets:** none. Every beat is schematic (choices, containment, a membership graph, fact
sheets, a lifecycle) and is better as authored geometry that animates causally than as a raster.

## Signaling — cues anchored to spoken words

Each beat has one focal element that **reacts on the word**; anchor via `word_anchors.py` against
`transcript.json`, never a guessed offset. Anchor names are from `anchors.json`.

| Beat | Cue | Anchor phrase (cue name) |
|---|---|---|
| B1 | Security row lifts + tab | `so a security group it is` (`types_verdict`) |
| B2 | Dynamic row lifts; attributes→auto glyph pulses | `reads user attributes` (`member_dynamic`) |
| B3 | license badge pulses on parent; `?` appears and **holds** (reveal withheld) | `nested inside All Engineering` (`nest_structure`) → `take a guess` (`nest_predict`) |
| B4 | badge **reaches** direct members (✓) then **halts** at the nested boundary (✕) | `the parent's direct members` (`nest_direct`) → `two steps removed` (`nest_removed`) |
| B5 | term `DIRECT MEMBERS ONLY` pops | `Group-based licensing resolves direct members only` (`rule_licensing`) |
| B6 | name assembles with the prefix; blocked words strike; P1 chip lands | `a required prefix or suffix` (`naming_prefix`) → `Microsoft Entra ID P1` (`naming_p1`) |
| B7 | steps stagger; step 1 opens, step 4 (`Restorable 30 days`) highlights | `a lifetime in days` (`expire_lifetime`) → `restorable for thirty days` (`expire_restore`) |
| B8 | the `1` punches in | `exactly one expiration policy` (`expire_one`) |

**Native-check markers** (become `check` assertions — place deliberately):

- `data-reveal-after` on B3's answer (kept off through the predict) and on B4's not-reached mark
  (appears only after the reached mark) — the predict→reveal cannot resolve early.
- `data-keep-in-frame` on the B3 and B4 full-frame diagram stages.
- Motion budget: `max_static_stretch_seconds` = **5.0**. Every ~20s body scene carries the block's
  staggered reveal plus its named cue, so no dead zone exceeds 5s.

## Hero-swoosh budget

Spent on beats: **`01-bumper`, `02-title`, `91-cta` (override)** — three frames, all in the
opening/closing bookend; **zero body beats.**

- `01-bumper` / `02-title` — the branded open and the title card own the swoosh (as stamped).
- `91-cta` — deliberate override from `content-wash`: the closing frame lifts back to the swoosh to
  bookend the title and give the "go to Learn" beat brand weight. Doctrine sanctions the swoosh for
  "closing." Keep display type out of the swoosh's **bottom-right third** (the CTA title/chip sit
  left/upper).

`90-recap` and `03-objectives` stay on `content-wash` (as stamped) — they are content-dense chip
frames; holding the swoosh to the bookend is what keeps it scarce.

## dark-field budget

Spent on **exactly one beat: B4 (nesting reveal).** It is the video's dramatic peak — the moment
the "nesting cascades like folders" prior is contradicted. B3 sets it up calmly on the wash; B4
lands the contradiction on the navy field. B5 (the rule) deliberately does **not** take dark-field —
it is the calmer generalization and belongs on the wash. The foundation auto-inverts text to white
and swaps `--paper` to translucent glass on `dark-field`, so `diagram-flow` composes correctly
there.

> **Builder verification for B4:** confirm the `diagram-flow` emphasis node, the "You" cursor, and
> the connectors read on `dark-field` (they were tuned for the light default). If the halt is not
> legible, the fallback is to hand-author B4 as `custom` on `_foundation.css` for the dark ground,
> or reuse `6-nested-group-non-cascade.png` via `media-screenshot`. Do **not** move dark-field off
> the reveal.

## Contrast declarations

All readable text is ink; no accent carries text at any size. Accents appear **only as graphics**
(row tabs, underline rules, number badges, connectors, the license badge, semantic ✓/✕ marks).

| Text / ground pair | Ratio | Verdict |
|---|---|---|
| ink `#091F2E` on `content-wash` (B1, B2, B3, B5, B6, B7, B8; objectives, recap) | 16.02 | AAA — any size |
| white `#FFFFFF` on `dark-field` (B4) | ~17 | AAA — any size |
| ink `#091F2E` on `hero-swoosh`, left/upper (01-bumper, 02-title, 91-cta) | 15.6 | AAA |
| ink `#091F2E` on `hero-swoosh`, worst colour field | 5.95 | AA — keep display out of bottom-right third |
| any brand accent (purple/blue/teal/magenta) as **text** | — | **not used as text anywhere** |
| teal-light `#49C5B1` / purple-light `#C5B4E3` | — | not used (decorative-only tokens avoided) |

**Worst readable-text ratio in the video: 5.95** — ink on the `hero-swoosh` colour field (chrome
title/CTA only), which clears AA. Every body beat is 16.02 (wash) or ~17 (dark-field white). No
contrast risk: no design relies on an accent at text size, so nothing needs the pure-`#FFFFFF`
escape hatch.

## Fonts

Segoe UI / Segoe UI Semibold, embedded from `fonts/`.
