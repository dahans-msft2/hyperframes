# Design plan — Require MFA with a Conditional Access policy

Preset: learn-ilt   Profile: demo-walkthrough (~10 scenes · max static 12s · **portal-capture dead-zone exempt**)

Scope: the **5 BODY beats only** (4–8). Chrome (bumper · title · objectives · recap · cta) is
already stamped from the kit and is **not re-decided here** — with one explicitly-flagged optional
override on the recap (see *Hero-swoosh / dark-field budget*). The AI end card is appended by the
pipeline.

All five body beats are `media-screenshot` over the real portal stills already in
`assets/media/`. The block's motion — a slow Ken Burns push plus the callout reveal(s) landed on the
narrated word — is the carrier; portal-capture is dead-zone exempt, so a held still is *correct*
here, not a defect.

---

## Per-beat table

| Beat | Ground | Block | Screenshot src | Fit | Callout region(s) `{x,y,w,h}` % of the 16:9 window | Cue anchor(s) | Focal control |
|---|---|---|---|---|---|---|---|
| 4 · concept | content-wash | media-screenshot | `assets/media/ca-overview.png` | **contain** | C1 `{54,43,15,29}` | `conceptIfThen` | The **Require MFA** node in the "Verify every access attempt" column (the *then*) |
| 5 · new policy + assign | content-wash | media-screenshot *(+ 2 authored chips)* | `assets/media/ca-new-policy.png` | **contain** | C1 `{30,50,17,8}` over **+ Create new policy**; chip A + chip B in the lower letterbox | `newPolicy` → `policyName` → `assignGroup` | **+ Create new policy** button (name + assign-group carried as authored chips — blade not captured) |
| 6 · select app | content-wash | media-screenshot | `assets/media/ca-select-apps.png` | **contain** | C1 `{51,40,27,13}` | `selectApp` | The checked **Microsoft Azure Management** app row |
| 7 · grant / require MFA *(climax)* | content-wash | media-screenshot | `assets/media/ca-require-mfa.png` | **contain** | C1 `{43,13,8,6}` over **Grant access**; C2 `{43,19,15,10}` over **Require multifactor authentication** | `grantAccess` → `requireMfa` | **Require multifactor authentication** checkbox (checked) — let C2 hold |
| 8 · enable on + create | content-wash | media-screenshot | `assets/media/ca-enable-on.png` | **contain** | C1 `{44,35,16,17}` over **On**; C2 `{3,62,23,22}` over **Create** | `enableOn` → `createPolicy` | **On** toggle → **Create** |

Cue anchors are the names in `anchors.json`; the builder resolves each to a real time with
`tools/word_anchors.py transcript.json --spec anchors.json` and fires that callout's reveal on it.
Never guess an offset.

### Callout regions are computed for `object-fit: contain` — this is a REQUIRED builder change

The shipped block uses `object-fit: cover`. These stills are **nowhere near 16:9**, so `cover`
crops the exact control the beat is about:

| Still | px | ratio | Under `cover` (the default) | Under `contain` (required) |
|---|---|---|---|---|
| ca-require-mfa | 258×900 | **0.29:1** | shows only the center **16%** of height — the Require-MFA checkbox is **cropped off**; you'd see "Require device to be compliant" instead | full panel, as a centered ribbon (image = center 16% of width) |
| ca-select-apps | 603×582 | 1.04:1 | center 58% of height — the **Select** button at the bottom is **cropped off** | full panel (image = center 59% of width) |
| ca-new-policy | 1200×224 | **5.36:1** | center 33% of width — left nav gone, **+ Create new policy** clipped at the edge | full toolbar strip (image = center 33% of height) |
| ca-overview | 875×353 | 2.48:1 | center 72% of width (survives, but inconsistent) | full diagram (image = center 72% of height) |
| ca-enable-on | 258×124 | 2.08:1 | center 85% of height (survives) | full toggle (image = center 86% of height) |

**Action for the builder:** set the media `<img>` to `object-fit: contain` on all five body
beats. My regions above are measured against the *contained* placement of each image inside the
16:9 window (control fraction → screen fraction, accounting for the letterbox), so they only land
if `contain` is used. To make the letterbox invisible, set `.mf-screen` background to `#FFFFFF` —
the portal chrome is white, so white bars read as the page's own canvas rather than as bars.

For the two extreme ratios (require-mfa 0.29:1, new-policy 5.36:1) the contained image is a thin
ribbon. That is fine — the ribbon is fully legible and the empty letterbox is *used* (beat 5 chips
below; beat 7 the climax ribbon is spotlit). If a tighter frame is wanted, an **optional media
crop** is the cleaner fix: crop `ca-require-mfa.png` to the *Grant heading → Require MFA* region
(~258×280, ≈0.92:1) — it still holds both C1 and C2 controls and nearly fills the height. If the
still is cropped, re-measure C1/C2 against the crop.

### The stills already carry baked-in red highlight boxes — the callout is the spotlight, not a second box

Every one of the five stills ships a **red rectangle already drawn on the target control**
(Create new policy, the MA row, Require MFA, the On segment, plus the Select buttons). Do **not**
add a competing hard box. Size each block callout ~1–2% larger than the baked red box so its job is
the **vignette spotlight** (the callout's `box-shadow: 0 0 0 100vmax rgba(9,31,46,.06)` dims
everything outside the region) + the **animated ring reveal** timed to the narrated word + the
**Ken Burns** push — the three things a static PNG can't do. Keep the block ring at the default
`--accent-2` blue `#0078D4` (a graphic, contrast-law-exempt); blue reads as *ours* and stays
distinct from the source's red control marker.

---

## Frame obligations (ground plane · depth · object with weight)

Every body beat satisfies all three through the block, so none is sparse by construction:

- **Ground plane** — `content-wash` (dithered) + the browser-window card (`.mf-window`, soft
  elevation `0 18px 60px rgba(9,31,46,.18)`). The window is the surface the screenshot sits on.
- **Depth** — near plane: the window card + the callout ring + (beat 5) the annotation chips, all
  elevated over — far plane: the wash ground with its mandatory noise dither. Two planes,
  distinguished by elevation and blur, not just colour.
- **Object with weight** — the framed real portal UI is the filled object with interior weight (a
  genuine screen, never a 1px wireframe). Beat 7's climax ribbon is spotlit as the object.

---

## Beat 5 — the un-captured blade, handled honestly (no invented screen)

`ca-new-policy.png` shows the Conditional Access **Overview** page and its **+ Create new policy**
button — it does **not** show the name/Assignments blade. Per the brief and doctrine, I do **not**
fabricate that UI. Instead:

- **C1** is the one real callout, on **+ Create new policy** (`newPolicy`).
- Naming and group assignment ride as **two authored ink-on-paper annotation chips** in the
  generous lower letterbox (the contained toolbar strip fills only the center ~33% of height, so
  the bottom third is free space):
  - **Chip A** (fires on `policyName`): `Name it — “MFA Pilot”`
  - **Chip B** (fires on `assignGroup`): `Assignments → Users → your test group`
  These are labels the narration *says next*, not a mocked blade — honest, and they turn dead
  letterbox into teaching.
- **Capture opportunity (flag to author):** `capture: the New Conditional Access policy blade
  showing the Name field ("MFA Pilot") and Assignments → Users and groups → the test group
  selected`. If supplied, beat 5 upgrades to real UI + real callouts and the chips retire.

This means the shipped single-callout block CONFIG is **extended** on beats 5, 7 and 8 to a
sequential-callout list (each callout carries its own cue), exactly as the brief anticipates
("sequence multiple callouts … beat 5 … beat 8"). Beat 5 additionally needs the two chips.
See the builder note.

---

## Component range

One block across all five body beats — `media-screenshot` — and that is **correct, not
monotony**: the profile is a demo-walkthrough whose teaching *is* a sequence of real portal
screens. The variety lives where it should: a different real screen, a different focal control, and
a different callout choreography per beat (single reveal on 4 and 6; two-step on 7 and 8;
callout + two authored chips on 5). The nearest rejected alternative was `media-screen-recording`
for the beats (rejected: we have stills, not clips — a recording is the *optional* payoff on beat
8, below), and `diagram-flow` for the beat-4 concept (rejected: the source ships an authoritative
if→then diagram already — reuse the real asset over re-drawing it).

### Builder shopping list

- **Kit blocks to copy in:** `media-screenshot` × 5 (one instance per body beat 4–8), each on the
  foundation, `data-ground="content-wash"`.
- **Block extension (beats 5, 7, 8):** promote `CONFIG.callout` from a single object to an ordered
  list, each entry `{x,y,w,h, cue}`; reveal entry *n* on its resolved cue time (stagger the
  `back.out(1.6)` ring-in used for the single callout). Keep the vignette on the *active* callout.
- **Beat 5 chips:** two ink-on-paper annotation chips in the lower letterbox, revealed on
  `policyName` and `assignGroup`.
- **Custom scenes to hand-author:** none. All body beats are the media-screenshot block (extended).

---

## Assets — reuse first, then flag captures

- **Reused source stills (5/5):** every body beat uses a real portal capture already in
  `assets/media/`. No generated asset is warranted — these are authoritative UI; an invented mock
  would risk being subtly wrong and would fail the reuse-first rule.
- **Capture opportunities to offer the author (2):**
  1. Beat 5 — `capture: the name + Assignments/Users blade` (above). Cleanest single upgrade.
  2. Beat 8 — `capture: a media-screen-recording of a test user sign-in hitting the "More
     information required" MFA prompt`. Optional bonus payoff beat after 8, or fed into the CTA;
     adds ~10–15s and lands the result in motion. Not required for a ship.
- **Optional icon:** the Entra ID product icon on the beat-4 caption chip
  (`py tools/icon_index.py add --project . Entra`) — restraint applies; the screens already carry
  product context, so this is a nicety, not a requirement.

---

## Hero-swoosh / dark-field budget

Spent on body beats: **none.** All five are `content-wash`. Screenshots earn no scarce ground, and
`dark-field` would fight bright white portal UI (and auto-invert authored text to white). The
`hero-swoosh` stays where the chrome already spends it (title / cta).

**One optional chrome override, flagged not forced (designer-mode requires I name it):** the
`90-recap` chrome is the video's single legitimate candidate for the dramatic ground — it pays off
the opening hook ("a password now only gets them partway") with a "Policy live" badge. Promoting it
to `dark-field` would give the piece exactly one dark, cinematic payoff beat and spend the
exception deliberately. Default is to **leave the recap as stamped**; take this override only if the
team wants the single dramatic beat. If taken, keep recap text on ink tokens and let `dark-field`
auto-invert to white — never hardcode white.

---

## Contrast declarations (authored text only)

Callout **boxes / rings / chips-borders are graphics** — accent (`#0078D4`) is permitted and the
contrast law does not apply to them. Only authored **text** is bound by the law, and all of it is
ink:

| Authored surface | Text token | Background | Ratio | Verdict |
|---|---|---|---|---|
| Callout label chips (beat 5 chips A/B; any per-callout label) | ink `#091F2E` | opaque **`#FFFFFF`** chip | **~16.8:1** | AAA |
| Descriptive caption (block default, under the window) | ink-soft `#59636e` | wash `#FFF9F5` | **~5.85:1** | AA (normal text) |
| Any callout label if placed over the still | ink `#091F2E` | its own `#FFFFFF` chip (never bare portal UI) | **16.02:1** on wash | AAA |

**Legibility verdict for callout labels over screenshots:** ✅ safe. No authored label sits
directly on the busy portal UI — each rides an **opaque white (`#FFFFFF`) ink-on-paper chip**
(ink `#091F2E` = 16.02:1 on paper, ~16.8:1 on pure white, AAA at any size). No brand accent carries
text at any size on the light ground (purple, the strongest, is only 4.41:1). The blue callout ring
is a non-text graphic and is exempt. Re-run `py tools/contrast_gate.py brand/_extract/palette.json
--min 3.0` if any authored colour is introduced.

---

## Fonts

Segoe UI / Segoe UI Semibold, embedded from `fonts/` (`segoeui-regular.woff2`,
`segoeui-semibold.woff2`) per `scenes.json`. No non-brand faces.
