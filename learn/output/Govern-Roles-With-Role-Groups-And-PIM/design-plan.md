# Design plan — Govern roles with role groups and PIM

Preset: learn-ilt   Profile: unit-video   Run: govern-roles-pim-202608071310

Spine: the PIM activation lifecycle (eligible → activate → time-boxed → expire). The video's
thesis — **always-on → just-in-time** — has two poles, and I give each pole a distinct home:
B3 is the *always-on* pole (standing access), B5 is the *just-in-time* pole (the lifecycle).
The empty-approver → lockout thread (B6 → B7) is the danger climax and pays off in the recap.

| Beat | Component | Kind | Why it fits | Ground | Config / Elements | Accent use | Asset / capture |
|---|---|---|---|---|---|---|---|
| 01 bumper | bumper | block | mandatory brand open | hero-swoosh | kicker: `Provision and govern identities in Microsoft Entra` | ink only (accent rule = mark) | — |
| 02 title | title-hero | block | one headline owns the frame (curiosity-gap hook) | hero-swoosh | kicker + 2-line title + subtitle; mass kept upper-left | ink only | — |
| 03 objectives | list-steps | block | 3 stakes as a roadmap, not an agenda | content-wash *(chrome default)* | 3 stake chips; accent number badges | ink text; badge fills non-text | — |
| B1 roles today | list-select | block | choose-one among 100+ peer roles | content-wash | kicker `Built-in roles`, ~5 role rows, `selectedIndex` = Global Administrator, `countLabel` "100+ built-in roles" · **Entra** icon | accent tab on lifted row (non-text) | reuse: Entra icon · capture opt: *Roles and administrators → Add role assignment* |
| B2 role groups | callout-note | block | one DEFINITION + advisory | content-wash | label `DEFINITION`, term "Role group", body: roles bundled as one unit; check the workload first · **Exchange · Purview · Defender** icons | accent tab + glyph (non-text) | icons: Exchange, Purview, Defender |
| B3 always-on | **custom** | custom | the standing-access image no block carries | content-wash | authored on `_foundation.css`: a tenant frame holding N admin tokens that light and **stay lit** (standing), one labeled Global Administrator · `data-keep-in-frame` on the stage · **admin/shield** icon | `--incident` fill on lit tokens (mark, not text) | icon: Global Administrator (shield) |
| B4 two types | list-select | block | choose between two peers, eligible lifts | content-wash | kicker `Assignment type`, 2 rows Active / Eligible, `selectedIndex` = Eligible, detail "grants nothing until activated" | accent tab on Eligible (non-text) | adapt (if present) source `active-vs-eligible` diagram → rebuild as animated list-select |
| B5 activation lifecycle | list-steps | block | ordered 4-step JIT spine | content-wash | steps 1 Eligible · 2 Activate (approval / MFA / justification) · 3 Time-box **e.g. 4h** · 4 Expire; `data-reveal-after` gates step 4 behind step 3 · **PIM / clock** icon | accent number badges + connector (non-text) | icon: Entra/PIM clock · capture opt: *PIM activation blade, max-duration slider* |
| B6 empty-approver puzzle | console-status | block | approval flow, request flips pending → approved | content-wash | title "Activation request", rows: Approval required = yes, Approver list = **empty**, MFA = pass; `flipIndex` on the fallback approver, held by `data-reveal-after` (predict first) | status pills (non-text) | capture opt: *Require approval to activate + empty approver list* |
| B7 lockout risk + fix | callout-note | block | one WARNING + its mitigation — the one dramatic beat | **dark-field** | label `WARNING`, term "Lockout risk", body: all PRA/GA eligible-only + approval + no approvers → request sits indefinitely; fix = keep ≥1 emergency access account (permanent active GA) + explicit approvers; `data-reveal-after` reveals the fix after the risk · **key / break-glass** icon | white ink (auto-inverted); `--incident` mark; teal-/purple-light legal as display on dark | icon: key/break-glass · capture opt: *role-settings lockout warning* |
| B8 three durations | list-specs | block | label/value disambiguation | content-wash | rows: Activation maximum duration → "how long one activation lasts"; Expiration of eligible → "how long you can activate at all"; Expiration of active → "how long a standing assignment survives" | accent underline rules (non-text) | — |
| B9 custom role | callout-note | block | one KEY POINT — recognize the moment | content-wash | label `KEY POINT`, term "Custom role", body: built-in too broad → pick exact permissions → assign at a scope | accent tab + glyph (non-text) | — |
| 90 recap | title-hero | block | payoff of the hook (three answer lines) | content-wash *(chrome default)* | kicker `RECAP` + 2-line payoff + subtitle | ink only | — |
| 91 cta | title-hero | block | closing send-off | hero-swoosh *(**override** from chrome default content-wash — see budget)* | kicker `NEXT STEP` + 2-line CTA + subtitle; mass kept upper-left | ink only | — |

`Component` is a kit-block id from `blocks/catalog.json`, or `custom`. `Kind` is `block` / `custom`.
For a `block`, `Config / Elements` names the CONFIG values the builder must set; the chosen `Ground`
is applied by the builder as `data-ground` on the block's `#root`. On `dark-field`, tokens **stay
ink** and the ground auto-inverts them to white — never hardcode white.

## Chrome overrides (touch chrome only deliberately)

Only one chrome scene departs from its stamped default:

- **91-cta → hero-swoosh** (default was `content-wash`). The swoosh returns for the closing
  send-off, closing the loop opened by the title. Builder: set `data-ground="hero-swoosh"` on
  91-cta's `#root`.

All other chrome scenes keep their stamped grounds: **03-objectives stays content-wash** (the
script author floated `section-field`; I decline — there is no act break to open, and a cool-blue
field between two hero scenes and the content would spend a scarce ground on a roadmap). **90-recap
stays content-wash** — it is a content payoff (three answer lines) that reads calmest as ink on
wash, reserving the swoosh's warmth for the final CTA.

## Frame obligations

Every content beat: **ground plane** = the content-wash field with a `card-tinted` panel
(`card-bg`, `border`, soft `elevation`) as the bounded surface; **two depth planes** = the elevated
near panel over the receded wash (separated by elevation + scale, not colour); **object with weight**
= a filled focal form with an interior, never a 1px wireframe.

| Beat | Ground plane | Near / far planes | Object with weight |
|---|---|---|---|
| B1 | wash + role-list panel | lifted GA row (near) over receded peer rows (far) | filled GA row chip with accent tab |
| B2 | wash + definition card | tab + glyph (near) over card body (far) | the filled "Role group" term card |
| B3 | wash + tenant frame (`data-keep-in-frame`) | lit admin tokens (near) over the tenant boundary (far) | the cluster of filled, standing admin tokens |
| B4 | wash + type-list panel | lifted Eligible row (near) over Active row (far) | filled Eligible row with accent tab |
| B5 | wash + step column | active step badge (near) over the connector spine (far) | the filled 4h time-box step badge |
| B6 | wash + console panel | the flipping request row (near) over the check rows (far) | the filled request row (pending→approved pill) |
| B7 | **dark-field** + warning panel | elevated warning card (near) over the navy field (far) | the filled `--incident` warning glyph + stuck-request token |
| B8 | wash + spec sheet | active spec row underline (near) over the rows (far) | the filled "Activation maximum duration" row |
| B9 | wash + key-point card | tab + glyph (near) over card body (far) | the filled "Custom role" term card |

## Component range

Seven distinct kit blocks + one custom across 14 scenes — expression varies with the teaching
relationship, not for its own sake:

- **list-select ×2** (B1, B4). B1 is a long cascade of 100+ peers narrowing to one; B4 is a binary
  toggle. Same shape (choose-one, one lifts), deliberately different scale, three beats apart.
  *Rejected `list-specs`* — its `avoid_when` sends "peers being chosen among" to a select archetype;
  nothing here is a label/value pair and one row is selected.
- **callout-note ×3** (B2 definition, B7 warning, B9 key-point). Each is well-separated, and B7 sits
  on `dark-field` so it reads as a different object entirely. Learn content legitimately carries
  several single-emphasis beats; they are never adjacent. *Rejected for B7: `console-status`* — its
  `avoid_when` is "the beat is conceptual"; B7 teaches severity + mitigation, and repeating a status
  panel right after B6 would flatten the escalation.
- **list-steps ×1** (B5) — the JIT spine. *Rejected `diagram-flow`* — the lifecycle is a linear
  sequence, not a branch; `diagram-flow.avoid_when` = "a linear sequence (use list-steps)".
- **console-status ×1** (B6) — the approval flow with a pending→approved flip. *Rejected
  `callout-note`* — the puzzle needs an operational status row that *flips*, not a static card.
- **list-specs ×1** (B8) — three label/value rows to disambiguate. *Rejected `list-steps`* — the
  three durations are attributes, not ordered steps; `list-specs.avoid_when` names exactly this.
- **custom ×1** (B3) — see below.

Builder shopping list:

- **Kit blocks to copy into `scenes/`** (body): `list-select` (B1, B4), `list-steps` (B5),
  `callout-note` (B2, B7, B9), `console-status` (B6), `list-specs` (B8). *(bumper / title-hero /
  list-steps chrome are already stamped; B5 still needs its own `list-steps` copy.)*
- **Custom scene to hand-author** on `templates/blocks/_foundation.css`: B3 (standing access).

### The one custom — justified (B3, always-on)

B3 is the *always-on* pole of the thesis and the hook's central image ("standing target"), which
the recap explicitly pays off ("back to that standing-access problem"). No kit block carries it: the
nearest, `list-select`, animates **one row lifting while the rest recede** — the exact inverse of
what this beat needs, where **all** holders light and *remain* lit to read as "always on". It is
authored geometry (tokens that turn on and stay on animate the "always-on" idea causally, which a
raster cannot), on the same tokens / type scale / grounds as the kit. One custom in nine body beats;
every other beat is reframed to fit a block.

## Assets — reuse first, then flag captures, generate nothing

- **Reuse (source module):** the script cites `media/9-…active-vs-eligible.png`. It is not reachable
  from this workspace, so B4 is authored as an animated `list-select` regardless (doctrine: rebuild
  and animate the eligible lift, don't drop a flat PNG). If the author has the source diagram, it is
  a structural reference only.
- **Icons (ship the brand library into the project):** `py tools/icon_index.py add --project . Entra
  Exchange Purview Defender` — Entra (B1/B4/B5/B6/B7), Exchange · Purview · Defender (B2), plus a
  Global-Administrator shield (B3) and a key/break-glass (B7) from the Security set. Prefer SVG. One
  icon per concept — a named product appears with its mark, not as bare text.
- **Capture opportunities to offer the author** (real UI teaches better than a mock — flagged, not
  fabricated): B1 *Roles and administrators → Add role assignment*; B5 *PIM activation blade +
  max-duration slider*; B6 *Require approval to activate + empty approver list*; B7 *role-settings
  lockout warning*. Each lands as a `media-screenshot` inset over its authored beat if supplied.
- **Generated assets: none.** Every beat is schematic (lists, a console, spec rows, a warning, a
  scope frame) — better as authored geometry that animates causally. The title rides typography on
  the swoosh; no hero illustration is needed. An empty-looking beat here is a composition job, not an
  illustration slot.

## Signaling — every cue tied to a spoken word

The narration names things in sequence; the visual reacts at the word. Anchor every cue to the
transcript with `word_anchors.py`, never to an assumed offset.

| Beat | Cue (type) → spoken phrase |
|---|---|
| 02 | title lifts (pulse) → "standing target"; PIM lockup settles → "Microsoft Entra Privileged Identity Management" |
| 03 | third chip highlights (lift) → "lock your admins out" |
| B1 | GA row lifts + scope pill sets (highlight) → "a direct assignment at a scope" |
| B2 | term card pops (pulse) → "role groups you assign as one unit" |
| B3 | admin tokens light and **stay lit** (pulse-and-hold) → "is always on"; GA token flags (highlight) → "standing access to Global Administrator" |
| B4 | Eligible row lifts, Active recedes (lift/slide) → "two assignment types"; Eligible dims to empty (highlight) → "grants nothing by itself" |
| B5 | Activate gates reveal (pop) → "it can require approval"; time-box fills to 4h then **drains** and step 4 reveals (fill→empty) → "expire on their own" |
| B6 | approver-list row reads **empty** (highlight); fallback approver reveals — **held until the predict lands** (`data-reveal-after`, pop) → "falls back to every admin" |
| B7 | request row jams (shake/strike) → "sits indefinitely"; break-glass account lights (highlight, revealed after the risk) → "at least one emergency access account" |
| B8 | "Activation maximum duration" row underlines (highlight) → "how long a single activation lasts" |
| B9 | term card pops (pulse) → "a custom role is the right call" |
| 90 | payoff lines cascade (waterfall) → "granted on activation" |
| 91 | CTA settles on the swoosh → "configure this exact approval workflow" |

**Engagement moves honoured:** curiosity-gap opener = the title hook on the swoosh (never a bulleted
agenda); **predict-before-reveal** = B6 withholds "who approves?" behind `data-reveal-after`;
**show-the-failure** = B3 keeps the standing admins lit and B7 keeps the jammed request visible while
the fix contradicts it in place.

## Motion budget — max static hold 5.0s (native `keepsMoving` assertion)

Every beat carries a motion within the 5.0s dead-zone budget: cascade/lift (B1, B4), card pop
(B2, B9), token light-up (B3), staged badges + draining time-box (B5), status flip (B6), shake +
reveal (B7), staggered underlines (B8), waterfall (90). Two markers compile to native `check`
gates and are placed deliberately: `data-reveal-after` on B5 (step 4 after step 3), B6 (fallback
after the puzzle) and B7 (fix after the risk); `data-keep-in-frame` on B3's full-frame tenant stage.

## Hero-swoosh budget

Spent on beats: **01 bumper · 02 title · 91 cta** — three scenes, the scarce allowance.

- **01 bumper** — the mandatory branded open; hero-swoosh is its stamped default.
- **02 title** — the title owns the frame and opens the curiosity gap; the swoosh is the video's
  identity frame. Keep display mass upper-left (zone rule below).
- **91 cta** — deliberate override from the chrome default; the swoosh **returns** for the send-off,
  closing the loop from the title. Keep display mass upper-left.

Deliberately **not** spent: 90-recap (content payoff, calmer as ink-on-wash) and 03-objectives (no
act break). `section-field` is **unused** — a single-arc unit has no segment divider to open.

## Contrast declarations (measured — `contrast_gate.py`, WCAG 2.1)

| Text | Ground | Ratio | Verdict |
|---|---|---|---|
| ink `#091F2E` | content-wash | 12.27 worst / 15.91 best | AAA |
| ink `#091F2E` | hero-swoosh | 5.95 worst | AA (keep display out of bottom-right third) |
| white (auto-inverted ink) | dark-field | 16.02 | AAA |
| teal-light / purple-light (display accents only) | dark-field | 7.94 / 8.83 | AAA — B7 only, non-body |
| any brand/semantic accent | any light ground | ≤ 4.41 | **decorative / mark only — never readable text** |

Worst readable-text pair anywhere in the video: **ink on the hero-swoosh colour field, 5.95:1 (AA)**
— clears the 4.5 bar. No accent carries readable text on any ground. On light grounds all text is
ink; on `dark-field` (B7) the ground auto-inverts ink to white (16.02, AAA) and only there may
teal-/purple-light appear as *display* accents. Semantic `--incident` (B3 tokens, B7 mark) is a
mark, never body text. No new colour introduced, so no re-gate required.

**Zone rule:** on hero-swoosh (02, 91) keep display type out of the bottom-right third — the safe-zone
map bottoms at the swoosh's colour field; hold the title mass upper-left where ink measures 15.6.

## Fonts

Segoe UI (body) / Segoe UI Semibold (display), embedded via `@font-face` from `fonts/`. No Space
Grotesk / JetBrains Mono / Fraunces.

## Don't-list compliance

No accent body text · no `teal-light`/`purple-light` text on a light ground · no gradient field
behind body copy (content sits on the wash; text on cards) · no invented grounds (`#463668`
retired) · soft elevation only, no hard decorative drop shadows · no non-brand fonts · dark-field
spent exactly once.

---

## Return summary

- **Ground allocation:** hero-swoosh ×3 (01 bumper, 02 title, 91 cta — scarce, opening + title +
  closing); content-wash ×10 (03 + B1 B2 B3 B4 B5 B6 B8 B9 + 90); **dark-field ×1** (B7, the
  lockout climax); section-field ×0 (no act break). One deliberate chrome override: 91-cta → swoosh.
- **Custom vs kit:** **1 custom** (B3 standing-access) + **13 blocks** across 7 distinct kit blocks
  (bumper, title-hero, list-steps, list-select, callout-note, console-status, list-specs).
- **Contrast risk:** none. Worst readable pair is ink on hero-swoosh, 5.95:1 (AA). Only watch item is
  the hero-swoosh bottom-right-third zone rule — mitigated by holding title/CTA mass upper-left.
