# Design plan — Call queue routing methods

Preset: **learn-ilt**   Profile: **unit-video** (~240s · aim ~10 scenes, ceiling ~21 · max static 5.0s)
Run: `call-queue-routing-methods-202608071230`   ·   Source: MS-721 Unit 8, *Interpret call queue routing methods*

The script + beat plan are **approved**. This plan decides the *look*: ground per scene, kit block
(or `custom`) per beat, the weighted focal object each beat owns, and where the scarce hero / the one
dark-field are spent. Structure of the stamped chrome is respected; two chrome fills are deliberately
overridden (recap block, CTA ground) — both flagged and justified below.

**Visual spine.** The four routing methods + the timeout math are the spine. The four methods are
authored as a **coherent peer set** — one shared vocabulary (a bounded queue panel = ground plane;
filled agent-avatar tiles = the weighted objects; one filled *call token* pill = the carrier element
that travels beat-to-beat) and a consistent `Routing method · N of 4` header chip — while **each
method beat owns a different focal motion** (fan-out / step-down / level-up / idle-lift). Peer
coherence comes from the shared vocabulary and framing; distinction comes from motion, never from
recoloring the labels (labels stay ink; accent is reserved for the *selection* / *recommended* marks).

---

## Per-beat table

| # | Component | Kind | Why it fits | Ground | Config / Elements | Accent use | Asset / capture |
|---|---|---|---|---|---|---|---|
| 1 · Bumper *(chrome)* | `bumper` | block | mandatory Learn open | **hero-swoosh** | kicker: "TEAMS PHONE · CONFIGURE AUTO ATTENDANTS & CALL QUEUES" | brand rule wipe (mark) · ink kicker | Teams product icon (chrome mark) |
| 2 · Title *(chrome)* | `title-hero` | block | one headline owns the frame | **hero-swoosh** *(hero spend)* | kicker "MICROSOFT LEARN"; title "Call queue routing / methods"; subtitle "Teams Phone" | accent rule (mark) · ink title | — |
| 3 · Objectives *(chrome)* | `list-steps` | block | three stakes as an ordered set | content-wash | 3 rows: "Who the queue rings" · "Callback vs. hold" · "The timeout trap" | ink badges/connector; amber mark on row 3 | — |
| 4 · The mystery *(hook)* | `callout-note` | block | one withheld question | content-wash | label QUESTION; a caller tile + a free agent tile; a **struck `↩ callback` badge** | `.strike` mark (magenta, non-text) · ink body | — |
| 5 · Four methods | `list-select` | block | a small peer set, choose-one — the routing-method control | content-wash | kicker "ROUTING METHOD"; 4 peer rows (Attendant · Serial · Round robin · Longest idle); countLabel "4 methods"; **no row lifted** (establishing) | accent tab reserved (unused here) · ink labels | reuse `call-queue-routing-method.png` as label/fidelity ref + optional authenticity inset |
| 6 · Attendant | **custom** *(nearest `diagram-flow`)* | custom | simultaneous one-to-many broadcast, not a branch walk | content-wash | one call token **fans out to ALL agent tiles at once**; "Default" tag; first-to-answer wins | ring pulse (mark) · ink labels | — |
| 7 · Serial | `list-steps` | block | ordered, one-at-a-time, top-to-bottom | content-wash | agents 1→2→3→4; call token **advances down the list** until answered / timeout | accent step badges (mark) · ink labels | — |
| 8 · Round robin | **custom** *(nearest `chart-bar`)* | custom | counters **equalize/balance over rounds** — a leveling motion, not grow-to-fixed-value | content-wash | per-agent call counters tick up and **level to equal**; "inbound sales" tag | bar fills (mark) · ink labels | — |
| 9 · Longest idle | `list-select` | block | peer set with **one lifted** = the choose gesture (spine resolves) | content-wash | same 4 rows; **lift the longest-idle** (selectedIndex) with idle timers; +overlay: presence toggle **snaps On**; +overlay: "Recommended" ribbon on Round robin & Longest idle | accent tab on lifted row (mark); teal-light ribbon fill w/ **ink** text | — |
| 10 · Two-agent catch | `callout-note` | block | one qualifying NOTE | content-wash | label NOTE; "Fewer calls than agents → only the first **2** idle-longest are offered" | emphasis on "2" (ink, display) | — |
| 11 · Callback intro | **custom** *(nearest `diagram-flow`)* | custom | a two-actor causal handoff path, not a decision tree | content-wash | a waiting caller **drops off hold**; a **`↩ we'll call you back` path draws** to a freed agent; "no hold" chip | callback path stroke (teal mark) · ink labels | — |
| 12 · Eligibility | `list-specs` | block | a set of trigger attributes, staggered | content-wash | 3 OR-rows: Wait time · Calls in queue · Calls-to-agent ratio + an **ANY ONE** brace; footnote row: "publicly dialable · non-premium · E.164 · not ringing an agent" | accent underline rules (mark) · ink rows | — |
| 13 · Predict | `callout-note` | block | predict-before-reveal — hold the question | content-wash | label QUESTION; config card held: "Callback ON · Eligible @ 60s · Timeout 120s · Music: Default"; **answer withheld** | ink card; no accent text | — |
| 14 · The reveal *(spine climax)* | **custom** timeline *(nearest `stat-spotlight`)* | custom | the timeout math on a horizontal time axis — the WOW | **dark-field** *(the one dark scene)* | a **clock bar**: eligible marker @ **60s**, music bar running to **120s**, **timeout gate @ 120s fires FIRST**; "offer never plays" stamp | **white** text (auto-invert); eligible = teal-light (AAA on dark); timeout/villain = magenta **mark**; stamp = white display on magenta chip | — |
| 15 · The rule | `callout-note` | block | the single KEY POINT takeaway | content-wash | label KEY POINT; "Call timeout **>** eligible + music + reach agent"; inline resolved mini-clock: **timeout bar extended past music**, success tick | success tick (teal mark) · ink body | — |
| 16 · Recap *(chrome — OVERRIDE)* | `list-select` | block | approved narration is a **three-part** recap answering the three objectives; title-hero can't carry three signaled straps | content-wash | 3 straps: "4 methods (RR + Longest idle ✓)" · "Callback for waiters" · "Timeout ≥ the whole sequence"; **lift the timeout strap** (core takeaway) | accent tab on lifted strap (mark) · ink straps | — |
| 17 · CTA *(chrome — OVERRIDE ground)* | `title-hero` | block | closing bookend belongs on the hero | **hero-swoosh** *(hero spend)* | kicker "NEXT STEP"; title "Create a / call queue"; subtitle "Walk routing & callback end to end on Microsoft Learn" | accent rule (mark) · ink title | — |
| 18 · End card | — | fixed asset | mandatory AI disclosure | (video) | `assets/AI_End_Card.mp4`, 10.667s (injected at build) | n/a | — |

`Component` = a kit-block id from `templates/blocks/catalog.json`, or `custom` for a bespoke layout
no block carries. For a `custom` beat the nearest kit block is named; the builder authors it on
`templates/blocks/_foundation.css` (same tokens, cqw type scale, grounds, primitives). `Ground` is
applied by the builder as `data-ground` on the block's `#root`.

### Chrome overrides (explicit — the builder must swap)

- **Beat 16 Recap:** block `title-hero` → **`list-select`** (three straps, timeout strap lifted).
  Driven by the approved three-part recap narration + per-strap signaling (each strap lands on its
  spoken phrase); a single title-hero headline cannot carry three signaled recap points. Ground
  stays content-wash, seam stays `cut-up`.
- **Beat 17 CTA:** ground `content-wash` → **`hero-swoosh`**. Sanctioned scarce-hero spend (title +
  CTA); closes the video on the same hero the opening used, bookending the piece. Block stays
  `title-hero`, seam stays `cut-left`.

All other chrome (bumper, title, objectives) is used as stamped — fills only.

---

## Frame obligations

Every beat answers ground plane · two depth planes · object with weight. The spine + reveal beats:

| Beat | Ground plane | Depth (near / far) | Object with weight |
|---|---|---|---|
| 4 · mystery | bounded queue card | struck callback badge lifted over caller/agent tiles (near) · panel (far) | filled caller tile + free-agent tile |
| 5 · four methods | bounded routing-method panel | rows elevated over panel (near) · wash (far) | four filled peer rows + "4 methods" count chip |
| 6 · Attendant | queue panel with a header line | call token + ringing tiles (near) · panel (far) | filled call-token pill fanning to filled avatar tiles |
| 7 · Serial | numbered ordered list rail | active step lifted (near) · dimmed later steps (far) | call-token pill descending the rail |
| 8 · Round robin | counter baseline / floor | growing bars (near) · gridlines (far) | filled per-agent counter bars leveling |
| 9 · Longest idle | routing-method panel (same as 5) | lifted longest-idle row + snapped toggle (near) · receded peers (far) | lifted row card + presence toggle + ribbon |
| 11 · callback | hold lane → agent lane, a floor line | drawn callback path (near) · lanes (far) | caller pill leaving hold + freed agent tile + path stroke |
| 14 · reveal | dark stage with a horizontal time axis | markers/gate on the axis (near) · axis + labels (far) | filled clock bar; the 120s timeout gate as a heavy slamming mark |
| 15 · rule | callout panel w/ an inline mini-axis | extended timeout bar clearing the music (near) · panel (far) | filled resolved timeline + success tick |

Callout beats (10, 13) sit on the universal tinted card (`card-tinted`, soft elevation
`0 2px 8px rgba(9,31,46,.10)`) — that card is the ground plane + near plane; the emphasized
term/figure is the weighted object.

---

## Component range

Nine distinct kit blocks + 4 custom across 17 authored scenes — the expression varies beat to beat
while the system (palette/type/contrast/chrome) stays invariant.

- **`callout-note` ×4** (4 mystery, 10 catch, 13 predict, 15 rule) — the recurring "one emphasized
  fact/question" idiom; each a different label (QUESTION / NOTE / QUESTION / KEY POINT) so they read
  as beats, not repeats.
- **`list-select` ×3** (5 establish the peer set, 9 resolve it by lifting longest-idle, 16 recap) —
  the choose-one-of-N idiom that *is* the routing-method control; it carries the spine's peer
  coherence. Rejected `list-specs` for beat 5 (methods are peers to choose among, not label/value
  attributes) and rejected `media-screenshot` of the real dropdown (authoritative but static —
  Ken-Burns + one callout can't cascade the four peers or lift one per later beat, breaking the
  spine's shared-vocabulary motion; kept instead as the fidelity reference / optional inset).
- **`list-steps` ×2** (3 objectives, 7 Serial) — ordered top-to-bottom; objectives↔recap symmetry.
- **`list-specs` ×1** (12 eligibility) — three OR-triggers as staggered spec rows under an ANY-ONE
  brace. Rejected `diagram-flow`: there is no branch to walk, only three parallel triggers — a tree
  would over-structure a flat "any of these three."
- **`title-hero` ×2** (2 title, 17 CTA) · **`bumper` ×1** — the hero bookends.
- **custom ×4** (6 Attendant fan-out, 8 Round-robin leveling, 11 callback path, 14 timeout clock) —
  each rejects its nearest block for a specific reason (below).

### Rejected-block ledger (the four custom beats)

| Beat | Nearest kit | Why rejected → custom |
|---|---|---|
| 6 Attendant | `diagram-flow` | its gesture is sequential node→connector down a *branching tree*; the teaching point is a **simultaneous** one-to-many broadcast ("rings at once") — a synchronized fan-out the block can't express. |
| 8 Round robin | `chart-bar` | chart-bar grows bars to fixed category values with a trend line; the teaching is bars **equalizing/balancing over rounds** (converging to equal) — a leveling motion, not grow-to-value. |
| 11 Callback intro | `diagram-flow` | not a decision tree — a **two-actor causal handoff** over time (caller leaves hold → agent frees → callback path draws). |
| 14 The reveal | `stat-spotlight` | shares the dark-field WOW, but stat-spotlight is a single count-up numeral; the beat needs a **multi-marker horizontal time axis** (60s / music / 120s gate) — a bespoke timeline. |

---

## Builder shopping list

- **Kit blocks to copy in:** `bumper`, `title-hero`, `list-steps`, `list-select`, `list-specs`,
  `callout-note`.
  *(chrome recap swaps to `list-select`; chrome CTA reuses `title-hero` on hero-swoosh.)*
- **Custom scenes to hand-author** on `_foundation.css` (shared spine vocabulary — queue panel,
  agent-avatar tile, call-token pill): **06-attendant** (fan-out), **08-roundrobin** (leveling
  counters), **11-callback** (causal path), **14-reveal** (dark-field timeout clock).

---

## Assets — reuse the source's own first, then flag captures

The source module (`configure-auto-attendants-call-queues/media/`) ships on-brand, authoritative
visuals. Reuse-first:

- **`call-queue-routing-method.png`** — the *real* Teams admin-center radio group showing exactly
  Attendant routing · Serial routing · Round robin · Longest idle. **Use it for beat 5** as the
  label/fidelity source (the four labels are verbatim from this control) and as an **optional
  authenticity inset** the author may drop beside the animated `list-select` rows. Copy into
  `assets/media/` if used.
- **`caller-call-queue.png`** — the Teams incoming-call card ("Call for Contoso Main Line"). Useful
  as a caller-motif reference for beats 4/11; not required (the caller is authored geometry).

### Capture opportunities to offer the author (real UI teaches better than a mock)

- **Beat 5 / 9 — routing-method control in the Teams admin center.** A fresh screenshot (or a short
  screen-recording of selecting *Longest idle* and watching *Presence-based routing* auto-enable)
  would make beat 9's toggle gotcha authoritative. Offer via `media-screenshot` / `media-screen-recording`;
  lands as the inset on beat 5 or a cut-in on beat 9. **Do not fabricate the toggle behaviour** — flag
  for capture; the animated `list-select` overlay is the fallback.

### Generated assets

**None.** Every body beat is schematic (fan-out, ordered list, leveling counters, causal path,
time axis) — authored geometry that animates causally beats a raster. No beat is carrying the
video's identity that isn't already a hero chrome frame. Per brand asset policy, no generation.

### Icons

- Pull the **Teams** product icon into the project: `py tools/icon_index.py add --project . Teams`
  → lands in `assets/icons/`. Use as the chrome mark (bumper kicker / title / CTA). Restraint: one
  product icon; agent tiles stay authored avatar geometry, not scattered glyphs.

---

## Hero-swoosh budget

Spent on beats: **1 (bumper) · 2 (title) · 17 (CTA)** — opening bookend pair + closing bookend. No
content body beat touches the hero. This is the sanctioned "title · opening · closing" spend; the
everyday ground is content-wash. Zone rule honoured: display type stays in the **left/upper** two
thirds of the swoosh (title-hero already does) — the bottom-right third measures ink 5.95 (AA, the
weakest zone) vs 15.64 top-left.

## Dark-field allocation

**Beat 14 only** (the timeout reveal — the WOW). No other beat may claim it. Confirmed against the
script's open question. On dark-field the ink auto-inverts to **white**; accents invert too
(teal-light 7.94 AAA, purple-light 8.83 AAA) so the eligible marker may read as a teal-light display
mark, while the timeout villain stays a magenta **mark** (never normal-size text).

---

## Contrast declarations (measured — `tools/contrast_gate.py`, WCAG 2.1)

**GATE PASS: 13 declared text pairings ≥ 4.5, worst 5.95.** All readable text is ink on light /
white on dark; every accent is a non-text mark or display-only.

| Surface | Text/pair | Ratio | Verdict |
|---|---|---|---|
| content-wash (beats 3–13,15,16) | ink `#091F2E` | 16.0 | AAA — any size |
| hero-swoosh (1,2,17), left/upper | ink `#091F2E` | 15.6 | AAA |
| hero-swoosh, bottom-right third | ink `#091F2E` | **5.95** | AA — keep display type out of this zone |
| dark-field (14) | white text | 7.4–20+ | AA–AAA (ink auto-inverts to white) |
| dark-field (14) | teal-light eligible mark | 7.94 | AAA (display/mark) |
| dark-field (14) | purple-light | 8.83 | AAA (display/mark) |
| ribbon (9) | ink on teal-light fill | high (dark-on-light) | AA/AAA — ribbon uses **ink** text |

### Contrast-law risks flagged

1. **Magenta villain on dark-field (beat 14).** Magenta is not AA as normal text on any ground.
   Keep the timeout gate + "offer never plays" as **marks / display-only** — the stamp is white
   display text on a magenta chip (clears AA-large), never normal-size magenta text.
2. **hero-swoosh bottom-right third (beats 1/2/17).** Weakest zone (5.95). Keep all display type
   left/upper — title-hero's layout already complies; the builder must not push the CTA line into
   the bottom-right.
3. **Four-method color-coding temptation (beats 5–9).** Method **labels stay ink**; the accent tab /
   ribbon / lifted-row mark is the only color. Do **not** recolor a method's label to differentiate
   it — differentiation is by focal motion, not by accent text (which would fail).
4. **Recommended ribbon (beat 9).** Ribbon fill is a light accent (teal-light) carrying **ink**
   text, not white-on-teal (which is only 3.2). Verified dark-on-light = AA+.

No text-bearing surface uses an accent below AA. Re-run after any palette edit:
`py tools/contrast_gate.py brand/_extract/palette.json --min 4.5 --zones`.

---

## Scene-density note

17 authored scenes (5 chrome + 12 body) is above the ~10 aim but within the ~21 ceiling. The beat
plan is **approved**; coherence holds because the four method beats and the two clock beats (14/15)
share one visual vocabulary and one traveling carrier (the call-token pill / the time axis), so the
body reads as one continuous walk through the queue rather than 17 independent slides. The shortest
callouts (10, 13) may re-time under the 14s floor against real word anchors — if so, the builder
should let them ride the adjacent beat's ground with a held focal rather than hard-cutting a thin
scene. All body durations are re-timed to `transcript.json` word anchors (`anchors.json` is written);
never to an assumed words-per-second.

## Fonts

Segoe UI / Segoe UI Semibold, embedded from `fonts/`. No Space Grotesk / JetBrains Mono / Fraunces.

## Motion note (hand-off, not owned here)

Motion belongs to motion-doctrine. Two markers the designer places that become native `check`
assertions: (a) beat 14's music/timeout markers depend on the eligible marker — the builder pins
the reveal ordering so the answer can't appear before the predict beat (13) resolves; the reveal
scene must not pre-state the answer. (b) Any full-frame stage (6 fan-out, 14 clock) carries
`data-keep-in-frame`. The traveling **call-token pill** is the film's carrier element across the
method spine (6→7→8→9) — the builder keeps its exit/entry vector continuous.
