# Design plan — Manage the user and contact lifecycle

Preset: learn-ilt   Profile: unit-video   Run: manage-user-contact-lifecycle-202608071300

The script is approved. This plan decides the **look** only — ground per scene, kit block per beat,
focal object, accent discipline, and where the two scarce grounds (hero-swoosh, the single
dark-field) are spent. Every body beat maps to a kit block; **custom count = 0**. Two chrome
defaults are deliberately overridden (91-cta → hero-swoosh; B5 spends the dark-field) — both flagged
below so the builder swaps them.

## Per-beat table

| Beat | Component | Kind | Why it fits | Ground | Config / Elements | Accent use | Asset / capture |
|---|---|---|---|---|---|---|---|
| `01-bumper` | bumper | block | mandatory Learn brand open | hero-swoosh | kicker `PROVISION AND GOVERN IDENTITIES IN MICROSOFT ENTRA` | brand accent rule wipe (non-text) | — |
| `02-title` | title-hero | block | the video's title owns the frame | hero-swoosh | kicker + title `Manage the user and` / `contact lifecycle` + subtitle | ink display + accent rule (left-anchored) | — |
| `03-objectives` | list-steps | block | three objectives as the stakes of the unit | content-wash | 3 chips: lifecycle · recover in 30 days · user vs contact | number badges (non-text) | — |
| B1 · Lifecycle spine | list-steps | block | five **ordered** stages a user moves through — the connector line *is* the spine | content-wash | 5 steps: Create → Edit profile → Add/remove licenses → Block sign-in → Delete; `connector:true`; Users glyph at spine head | number badges + connector line (non-text) | authored geometry |
| B2 · Create in bulk | media-screenshot *(fallback list-specs)* | block | a real Bulk-create blade teaches better than a mock; CSV→accounts | content-wash | `src assets/media/bulk-create.png`, url `entra.microsoft.com`, caption "one CSV, every account", callout over the Bulk-create button; **fallback** list-specs rows Display name / User principal name / Initial password | callout box border (non-text) | **capture: Entra ID > Users > Bulk create** (else list-specs CSV mock) |
| B3 · Right surface | list-specs | block | two surfaces, **split ownership** of one user — label→owned-tasks | content-wash | 2 rows: `Microsoft 365 admin center → create · license · block sign-in`, `Microsoft Entra admin center → the identity object · restore`; shared Users glyph; Entra.svg on the Entra row | label underline rules (non-text) | authored (icons) |
| B4 · Predict | callout-note | block | one withheld question, emphasized — answer held back | content-wash | label `PREDICT`, term "Delete the wrong user — gone for good?", body "You catch it five minutes later." | accent tab + glyph (non-text) | — |
| **B5 · Soft-delete reveal** | **stat-spotlight** | block | the single most dramatic beat — **30** is the hook payoff, the WOW number | **dark-field** | value `30`, suffix ` DAYS`, label `FULLY RESTORABLE`, caption "suspended, restorable — until day 30 makes it permanent" | white ink (auto-inverted) + accent underline + glow (non-text) | authored — **no external PNG needed** |
| B6 · Restore returns all | console-status | block | a portal operation resolving pass/fail — the licenses row is the surprise | content-wash | title "Restore deleted user"; rows Locate under *Deleted users* · Select · Restore properties · **Licenses restored**; `flipIndex` = licenses row; Entra.svg chrome | status pips (positive teal / pending amber, non-text) | **capture: Entra ID > Users > Deleted users** (else console-status mock) |
| B7 · On-prem caveat | callout-note | block | one emphasized caveat — synced accounts can come back | content-wash | label `CAVEAT`, term "Synced from on-premises?", body "On-prem stays master — the next sync can recreate it. Fix it on-prem." | semantic caution tab (non-text) | authored (Entra Connect Sync icon) |
| B8 · User or contact? | diagram-flow | block | a **branching decision** — does this person sign in? | content-wash | root "Does this person sign in?" → YES `User / guest` · NO `Mail contact` (emphasized); "You" cursor walks the NO branch; Exchange icon on contact node | blue connectors + emphasis-node fill (non-text) | authored (icons) |
| B9 · Where accounts come from | list-specs | block | four peer tools → one-line role — a calm reference sheet | content-wash | 4 rows: Connect Sync · Cloud Sync · Connect Health · IdFix → their roles; Entra Connect Sync icon on the sync rows | label underline rules (non-text) | authored (icons) |
| `90-recap` | title-hero | block | pays off the hook — 30 days, intact | content-wash *(kept — see scarcity note)* | kicker `RECAP`, title "30 days to restore —" / "properties + licenses intact", subtitle condenses admin-center + user-vs-contact | ink display + accent rule | — |
| `91-cta` | title-hero | block | closing send-off to the next unit | **hero-swoosh** *(override — see below)* | kicker `NEXT STEP`, title "Next: provision" / "accounts at scale", subtitle "…without over-granting your own permissions" (left-anchored) | ink display + accent rule | — |
| End card | AI disclosure MP4 | — | mandatory AI disclosure; injected from `scenes.json.endcard` | n/a (white video) | `assets/AI_End_Card.mp4` | — | frozen (do not author) |

`Component` = kit-block id from `blocks/catalog.json`, or `custom`. `Kind` = `block` / `custom`.
Ground is applied by the builder as `data-ground` on each block's `#root`.

## Overrides to the scaffold (builder must swap)

1. **B5 spends the dark-field.** The script beat plan proposed B5 on `content-wash` with a
   `media-screenshot` reuse of `media/2-soft-delete-timeline.png`. I override that: B5 is
   `stat-spotlight` on `dark-field`. The soft-delete reveal is the payoff of the curiosity-gap
   hook, and **"30 days" is the single dramatic number** the whole video turns on — exactly what
   `stat-spotlight` / `dark-field` exist for. A flat source PNG on the everyday ground under-sells
   the climax; the reveal earns the one dark-field. The warm→dark **ground cut** from B4 (predict)
   to B5 (reveal) *is* the drama. No external asset is needed, which also removes B5's only
   asset-availability risk.
2. **91-cta → hero-swoosh.** `chrome.json` stamps `91-cta` on `content-wash`; I promote it to
   `hero-swoosh` per the brief ("scarce hero-swoosh for title + CTA") and title-hero's own default
   ground — the warm closing send-off.

**90-recap is deliberately kept on `content-wash`** (its chrome default), *not* promoted to
hero-swoosh, to honor "scarce hero-swoosh for **title + CTA**." The recap consolidates on the
everyday ground; the CTA then lifts to the warm swoosh for the final send-off. If maximal
bookend symmetry is later preferred, recap can move to hero-swoosh — but scarcity wins here.

## Frame obligations (ground plane · two depth planes · object with weight)

Every beat answers all three; the kit blocks supply them (bounded cards, soft elevation,
filled forms). Called out per beat:

- **B1** — ground: the wash + connector spine as a floor line. depth: elevated numbered badges over
  a receded connector. object: filled stage badges + the Users glyph (not a wireframe).
- **B2** — ground: the browser-window chrome of media-screenshot. depth: the screenshot plane behind
  a raised accent callout box. object: the captured blade (or filled list-specs rows).
- **B3** — ground: two tinted spec cards on the wash. depth: elevated cards over the ground; the
  lifted Entra row nearer. object: the shared Users glyph + Entra.svg mark.
- **B4** — ground: the callout panel. depth: accent tab + glyph raised off the card. object: the
  filled note card.
- **B5** — ground: the dark-field itself (a place, not a void). depth: the glowing number plane over
  a receded accent underline. object: the huge filled "30" with weight and glow.
- **B6** — ground: the console panel. depth: status rows over the panel; the flipping row lifts.
  object: filled status pips + row fills.
- **B7** — ground: the caveat card. depth: the caution tab + sync icon raised. object: the filled
  card + Entra Connect Sync mark.
- **B8** — ground: the flow's implied plane. depth: white nodes over blue connectors; the emphasized
  contact node nearer. object: filled decision nodes + the "You" cursor.
- **B9** — ground: four spec rows on the wash. depth: elevated rows; sync-icon marks raised. object:
  filled rows + icons.

Two beats carry a thin-risk: **B1** (5 rows, one past list-steps' 3–4 comfort — tighten `rowGap`; if
it still crowds, split "block sign-in vs delete" into its own callout) and **B9** (four calm
reference rows — keep low emphasis so it reads as a fact sheet, not four competing beats).

## Component range

Nine **distinct** kit blocks carry fourteen scenes — the expression varies beat to beat while the
system (palette, type, chrome, four grounds) stays invariant:

- `bumper`, `title-hero` — chrome (title-hero also carries recap + cta).
- `list-steps` — used twice for genuinely different *ordered* content: the objectives stakes and
  the B1 lifecycle spine (the connector line reads as the spine metaphor).
- `media-screenshot` — B2 (real Bulk-create blade), the only capture-led beat.
- `list-specs` — twice, five beats apart, for two different label→value fact sheets: B3
  (surface → owned tasks) and B9 (tool → role). Evidence: both are unordered attribute sets, not
  procedures.
- `callout-note` — twice, deliberately: B4 `PREDICT` and B7 `CAVEAT` are both *single emphasized
  notes* (the block's exact best_for), far apart, with distinct labels and tone (predict vs
  caution). This is the honest block for each; not repetition for its own sake.
- `stat-spotlight` — once, the dark-field WOW (B5).
- `console-status` — once, the restore operation (B6).
- `diagram-flow` — once, the sign-in decision (B8).

### Rejected blocks (and the `avoid_when` that applies)

- **B1** rejected `diagram-flow` — the lifecycle is a *linear* sequence, not a branch
  (`avoid_when`: a linear sequence → use list-steps).
- **B2** rejected `list-select` — nothing is chosen among peers; it's CSV → accounts.
- **B3** rejected `list-select` (the script's proposal) — **nothing is selected**; both surfaces are
  kept, each owns tasks (`avoid_when`: nothing is selected → use list-specs). This is a division of
  labor, not a choose-one.
- **B5** rejected `stat-count` (number is dramatic enough to carry the whole beat → use
  stat-spotlight) and rejected the script's `media-screenshot`-on-content-wash (under-sells the
  climax; see override 1).
- **B6** rejected `diagram-flow` — a restore is an operation with pass/fail states, not branching
  logic.
- **B7** rejected `list-specs` — one emphasized caveat, not a set of facts.
- **B8** rejected `list-select` — a branching decision, not a peer selection
  (`avoid_when`: a branching decision → use diagram-flow).
- **B9** rejected `list-steps` — four *unordered* peer tools, not an ordered procedure
  (`avoid_when`: unordered attributes → use list-specs).

## Builder shopping list

- **Kit blocks to copy into `scenes/`** (chrome `bumper` + `title-hero` are already stamped):
  `list-steps` (B1), `media-screenshot` (B2), `list-specs` (B3, B9), `callout-note` (B4, B7),
  `stat-spotlight` (B5), `console-status` (B6), `diagram-flow` (B8).
- **Custom scenes to hand-author:** **none.** 100% kit coverage.
- **Icons to pull** (`py tools/icon_index.py add --project . <name>`): `Entra` (B3/B6),
  `Users` (B1/B2/B3/B8), `Entra-Connect-Sync` (B7/B9). Exchange rides
  `10339-icon-service-Exchange-Access` (B8). No dedicated Microsoft 365 / Cloud Sync / Connect
  Health / IdFix marks exist — those ride **text labels**, not an invented logo.

## Signaling — every cue tied to a spoken word

One clear focal element per beat; the visual reacts on the narrated word (anchors resolved by
`word_anchors.py` against `transcript.json` — never a guessed offset). Cue keys are from
`anchors.json`:

| Beat | Cue | Lands on (anchor) |
|---|---|---|
| B1 | stage badges highlight/cascade down the spine | `lifecycle_stages` — "moves through a handful of stages" |
| B2 | accent callout box pops over the Bulk-create button | `bulk_create` — "Bulk create feature" |
| B3 | the Entra row's underline draws / lifts (it owns restore, setting up B5–B6) | `two_surfaces` — "each owns a different part of the job" |
| B4 | the PREDICT card scales in, tab wipes — **answer withheld** | `predict_delete` — "expect that account to be gone" |
| B5 | the "30" count-up slams up **as the ground cuts warm→dark** | `soft_delete_30` — "suspended state for thirty days" |
| B6 | the **licenses** row flips pending→passed | `restore_props_licenses` — "brings back the user's properties and the licenses" |
| B7 | a return-arrow / "can recreate" emphasis on the caveat | `onprem_caveat` — "the next sync cycle can recreate" |
| B8 | the mail-contact node emphasizes; the "You" cursor walks the NO branch | `mail_contact` — "that's a mail contact, not a user" → `signin_decision` — "does this person sign in" |
| B9 | rows stagger in | `hybrid_tools` — "Connect Sync is the classic sync server" |

**Engagement — predict-before-reveal (B4→B5).** Hold the answer on B4; do **not** show the 30-day
number while the question is open. Mechanically enforce it: pin B5's number/caption with
`data-reveal-after` so the payoff cannot appear early, and let the withholding B4 card carry the
prediction. The warm→dark ground cut is the reveal.

**Native check markers to place** (they compile into `check` assertions):

- `data-reveal-after` on B5's caption (reveals after the "30" establishes) and on B6's flip row
  (licenses reveal after the properties row).
- `data-keep-in-frame` on B5's full-frame stat stage and B8's diagram stage (full-frame stages that
  could shift off-canvas).

## Motion budget

Profile `max_static_stretch_seconds = 5.0s` — every beat needs a carrier motion inside 5s. The kit
blocks all ship staggered reveals; the load-bearing carriers here are B1's cascade down the spine,
B5's ground cut + count-up, B6's row flip, B8's cursor walk, and the row staggers on B3/B9. No beat
holds static past the 5s budget.

## Hero-swoosh budget

Spent on beats: **01-bumper, 02-title, 91-cta** — and nowhere else. Justification:

- `01-bumper` — the mandatory Learn brand sting (fixed ground, not a design spend).
- `02-title` — the opening title; the swoosh's canonical use.
- `91-cta` — the closing send-off (override from the chrome content-wash default). The warm sweep
  bookends the video against the opening title.

**Zero content beats touch the swoosh.** `90-recap` is held on `content-wash` to keep the swoosh
scarce (see the scarcity note above). Display type on all three swoosh scenes stays **left-anchored,
out of the bottom-right third** (the one swoosh zone where thin ink drops to 5.95).

## Dark-field budget

Spent on **B5 only** — the soft-delete reveal, the payoff of the curiosity-gap hook, the WOW
"30 DAYS" number. This is the single sanctioned dark-field exception; no other scene uses it. White
ink auto-inverts here.

## Contrast declarations

Every readable text surface is ink `#091F2E` (auto-inverted to white on `dark-field`). No brand
accent carries normal-size text on any light ground.

| Surface | Text token | Ratio | Verdict |
|---|---|---|---|
| content-wash — body / caption / label / kicker (all content beats + objectives + recap) | ink `#091F2E` | **16.02** | AAA — any size |
| content-wash — display (h1 / stat-num) | ink `#091F2E` | **16.02** | AAA |
| hero-swoosh — display (title / kicker / cta), left-anchored | ink `#091F2E` | **5.95 – 15.6** | AA-pass (worst 5.95, colour field; keep out of bottom-right third) |
| dark-field B5 — number + label + caption | white ink (auto-invert) | **≈15+** | AAA |
| dark-field B5 — any accent display (underline/glow are non-text) | teal-light `#49C5B1` / purple-light `#C5B4E3` | 7.94 / 8.83 | AAA if used as display; here they are non-text marks |
| **any light ground — brand accent as normal-size text** | purple `#8661C5` (strongest) | 4.41 | **FORBIDDEN** — never used; all accents here are non-text marks or display-only |

**Worst readable-text ratio across the whole video = 5.95** (ink on the hero-swoosh colour field) —
**AA-pass.** No AA-large failure anywhere. Every accent in the plan is a non-text mark (number
badges, connector lines, callout tabs, label underlines, status pips, the B5 underline/glow) or
display-only — **no contrast risk.**

Re-run if any colour is introduced:
`py tools/contrast_gate.py brand/_extract/palette.json --min 3.0`

## Fonts

Segoe UI / Segoe UI Semibold, embedded from `fonts/` (already scaffolded). No non-brand faces.
