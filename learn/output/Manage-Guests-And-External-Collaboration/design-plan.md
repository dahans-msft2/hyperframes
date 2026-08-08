# Design plan — Manage Guests and External Collaboration

Preset: learn-ilt   Profile: unit-video   Run: manage-guests-external-collaboration-202608071310

Target ~240s · 9 body beats (in-band for ~10) · scene target 24s · `max_static_stretch` 5.0s.
Spine: guest **permission levels** + **collaboration-restriction levers**. Hook: *"what can a
guest see by default?"* → predict-before-reveal. The look is a **bookend arc** — open on the hero
swoosh, drop once to the dark field for the hook, run every teaching beat on the warm wash, close
back on the hero swoosh. Text is ink everywhere; accents are marks only.

## Beat table

| Beat | Component | Kind | Why it fits | Ground | Config / Elements | Accent use | Asset / capture |
|---|---|---|---|---|---|---|---|
| `01-bumper` | bumper | block · chrome | mandatory brand open (fixed) | hero-swoosh | kicker `Provision & govern identities · Microsoft Entra` | Learn glyph draw + accent rule wipe (marks) | Learn mark |
| `02-title` | title-hero | block · chrome | the title owns the frame | hero-swoosh | kicker `MICROSOFT LEARN`; title `Manage Guests &` / `External Collaboration`; subtitle `Let partners in — without opening up the directory.` | ink text; accent rule (mark) | — |
| `03-objectives` | list-steps | block · chrome | 3 stakes as ordered chips | content-wash | 3 objective steps (map the levers / delegate least-privilege / know when to move to MTO) | accent number badges + connector (marks) | icon: Entra |
| **B1** `04-scenario` | callout-note | block | pose ONE dramatic question — the curiosity-gap opener | **dark-field** | label `THE SCENARIO`; term **`What can a guest see by default?`**; body Relecloud coordinators ↔ Woodgrove analysts, *one* investigation → *"take a guess"* | white ink (auto-invert); accent tab (mark) | icons: Entra, Users (guest) |
| **B2** `05-lever-map` | list-specs | block | 5 **peer** levers, each a label→what-it-controls pair, nothing selected | content-wash | rows: Invitation flow · Permission levels · Domain lists · Cross-tenant access · Self-service sign-up (+ one-line "controls…" value each) | accent underline rules (marks) | icon: Entra |
| **B3** `06-permission-levels` | list-select | block | 3 peers, **lift the one** that resolves the scenario (the default) | content-wash | items Same as members / **Limited access (default)** / Most restrictive · `selectedIndex=1` · countLabel `3 levels` | lift accent tab (mark) | icon: Users |
| **B4** `07-role-trap` | diagram-flow | block | a decision — "who can invite?" — with the tempting-but-broad answer **flagged** | content-wash | question `Who can invite?` → **User Administrator** (emphasis node, "too broad") vs Guest Inviter; chosen branch toward Guest Inviter | emphasis-node fill + blue connectors (marks) | icons: Roles-and-Administrators, Users |
| **B5** `08-delegate-two-pieces` | list-steps | block | an **ordered, both-required** procedure (2 pieces) | content-wash | step 1 `Assign the Guest Inviter role` · step 2 `Invite setting = "Only users assigned to specific admin roles can invite guest users"` · emphasize **step 2** | accent number badges + connector (marks) | icon: Roles-and-Administrators |
| **B6** `09-invite-redeem` | console-status | block | an **operational status flip** the system performs | content-wash | rows Invitation sent `pass` / Pending redemption `pending→pass` / Guest object created `pass` · `flipIndex=1` | status dot / pill fills (marks) — labels stay ink | icon: Entra |
| **B7** `10-one-object-two-surfaces` | callout-note | block | one **definitional** key point (identity, not a copy) | content-wash | label `KEY POINT`; term **`One guest object · two surfaces`**; body Entra admin center **·** Microsoft 365 Guest users — same record | accent tab + glyph (marks) | icons: Entra, Microsoft 365 wordmark · **capture opportunity** (see Assets) |
| **B8** `11-restriction-levers` | diagram-layers | block | nested boundaries — narration literally says *"a layer deeper"* | content-wash | outer→inner: Domain lists · Cross-tenant access · **core** Partner-tenant trust (MFA claims · apps) | core glow (mark) | icon: Tenant-Properties |
| **B9** `12-when-guests-stop-scaling` | list-select | block | two peer strategies, **lift the resolver** for a standing partnership | content-wash | items Guest-by-guest (fixed group) / **Multitenant Organization** (standing partnership) · `selectedIndex=1` | lift accent tab (mark) | icon: Tenant-Properties |
| `90-recap` | list-specs | block · chrome **(override)** | 4 recap chips that **answer the objectives + the hook** — mirrors `03` | content-wash | rows: Access model → *Levers, not a switch* · What a guest sees → *Limited by default* · Delegation → *Guest Inviter + tenant setting* · When to scale → *Multitenant Organization* | accent underline rules (marks) | — |
| `91-cta` | title-hero | block · chrome **(ground override)** | closing card — the swoosh **bookend** | **hero-swoosh** | kicker `NEXT STEP`; `Configure external collaboration settings` + `Multitenant Organization overview`; action `Try it in your own tenant` | ink text; accent rule (mark) | Learn mark |

`Component` = a kit-block id from `templates/blocks/catalog.json`. Every body beat binds to a kit
block; **zero custom**. `Ground` is applied by the builder as `data-ground` on each block's `#root`.

### Two declared chrome overrides (builder must swap)

1. **`91-cta` ground: content-wash → hero-swoosh.** The brief allocates the scarce swoosh to
   *title + CTA*; doctrine lists "closing" as a valid swoosh use. This bookends the film. Keep the
   title-hero block; only change `data-ground`. **Zone rule:** keep the CTA links/display out of the
   swoosh's **bottom-right third** (that region measures 5.95 vs 15.6 in the left column) — the
   title-hero waterfall is left-anchored, so it complies by default; do not right-justify the links.
2. **`90-recap` block: title-hero → list-specs.** The recap has four parallel takeaways that answer
   the three objectives + the opening hook; a 2-line title would drop three of them. Swapping to a
   4-row `list-specs` mirrors the `03-objectives` chips and lands the Signaling payoff. Ground stays
   content-wash.

## Frame obligations

Every body beat carries a ground plane, two depth planes, and an object with weight (the block
foundations supply these; named here so a sparse beat is caught in the plan, not review).

| Beat | Ground plane | Near / far planes | Object with weight |
|---|---|---|---|
| B1 | navy dark field (dithered) | near: the posed-question card, soft elevation · far: recessed scenario line | the filled question card, not a floating string |
| B2 | wash | near: 5 lifted spec rows · far: the field | 5 filled label/value rows with underline rules |
| B3 | wash | near: the **lifted** default row (elevated tab) · far: the two receded peers | the lifted "Limited access" row as a solid chip |
| B4 | wash | near: emphasised User-Administrator node · far: the muted branch nodes | filled decision nodes + connectors, not wireframes |
| B5 | wash | near: the active step-2 badge · far: the connector spine | two filled numbered step cards |
| B6 | wash | near: the flipping row · far: the settled check rows | a filled portal-style status panel |
| B7 | wash | near: the key-point card (elevation) · far: the two surface labels | the filled callout panel + accent tab |
| B8 | wash | near: the glowing core · far: the outer rings desaturating | filled concentric planes around a solid core |
| B9 | wash | near: the **lifted** MTO row · far: the receded guest-by-guest row | the lifted MTO chip as a solid form |

## Component range

Nine body beats, **seven distinct kit blocks** — strong range with no filler repetition:

- `callout-note` ×2 — B1 (dark-field, a posed *question* / curiosity gap) and B7 (light, a
  *definitional* key point). Same block, genuinely different relationships and grounds.
- `list-select` ×2 — B3 (lift the default permission level) and B9 (lift MTO). Both are the same
  *choose-one-and-lift* relationship; deliberately reused as the video's two decision-lifts and
  well separated (beat 3 vs beat 9). Rhymes the "which one resolves this?" moment.
- `list-specs`, `diagram-flow`, `list-steps`, `console-status`, `diagram-layers` — one each.

Content-shape evidence + nearest rejected block per beat:

| Beat | Chosen (`content_shape`) | Rejected via `avoid_when` |
|---|---|---|
| B1 | callout-note — "one note/definition to emphasize" | **stat-spotlight** (dark-field-native) — needs a *number*; there is none here |
| B2 | list-specs — "attributes as label/value pairs" | **list-select** — nothing is selected (`avoid_when: nothing selected → list-specs`) |
| B3 | list-select — "one selected/emphasized peer" | **list-specs** — a row *does* lift here, so specs is wrong |
| B4 | diagram-flow — "branching decision / walked path" | **list-select** — the meaning is a *rejected* obvious answer, not lifting a winner |
| B5 | list-steps — "ordered 3–4-step procedure" | **list-select** — order/dependency carries it (`avoid_when: order → list-steps`) |
| B6 | console-status — "checks/statuses, pass/pending flip" | **list-steps** — the flip is a *system* status event, not a learner procedure |
| B7 | callout-note — "one takeaway/definition" | **diagram-flow** — no decision; it's a single identity fact |
| B8 | diagram-layers — "nested scopes outside-in around a core" | **list-specs** — these *nest* ("a layer deeper"), they aren't flat attributes |
| B9 | list-select — "choose-one, lift the resolver" | **diagram-flow** — a plain two-peer lift, not a branch walk |

## Shopping list

- **Kit blocks to copy in (body):** `callout-note`, `list-specs`, `list-select`, `diagram-flow`,
  `list-steps`, `console-status`, `diagram-layers`.
- **Chrome blocks (already scaffolded):** `bumper`, `title-hero` (`02`, `91`), `list-steps` (`03`);
  **swap `90-recap` to `list-specs`** and **set `91-cta` `data-ground="hero-swoosh"`** per the two
  declared overrides.
- **Custom scenes:** **none.**

## Assets — reuse first, then capture, then generate

**Source reuse: none available.** The source module ships four media PNGs
(`2-soft-delete-timeline`, `6-nested-group-non-cascade`, `7-administrative-unit-group-scoping-gap`,
`9-privileged-identity-management-active-vs-eligible`) — all belong to **other units** (2/6/7/9).
Unit 5 references **no images**, so there is no Unit-5 source visual to reuse or animate.

**Capture opportunity — B7 (`10-one-object-two-surfaces`).** The strongest teach for *"same record,
two surfaces"* is a real matched pair: the **same guest** in the **Entra admin center → Users →
Guest users** list *and* in the **Microsoft 365 admin center → Users → Guest users** list. If the
author can supply both stills, swap B7 to a **`media-screenshot`** beat (two framed captures with an
accent callout on the identical UPN/`#EXT#` row). Until then the buildable default is the
`callout-note` above — do **not** fabricate the two admin-center UIs as fact.

**Generated assets: none.** Every body beat is schematic (levers, levels, a decision, a status flip,
nested boundaries) — authored geometry that animates causally beats a raster. No beat earns a
generated illustration.

**Icons (pull into `assets/icons/` before render).** Learn videos are chronically under-iconned;
each named product/role gets its official mark, one per concept:

| Icon | Source in library | Serves |
|---|---|---|
| `Entra` (svg) | Microsoft-Security-product-icons-kit | B1, B2, B6, `03` |
| `Users` (svg) | Azure/identity/10230-icon-service-Users | B1 (guest), B3 |
| `Entra-Identity-Roles-and-Administrators` (svg) | Azure/identity/10340 | B4, B5 |
| `Tenant-Properties` (svg) | Azure/identity/02679 | B8, B9 |
| `Microsoft365_logo_horiz_black_rgb` (png) | FY26-M365-and-Office-product-icon-toolkit | B7 (the M365 surface — use the **black** wordmark on the light wash) |

Prefer SVG; use `py tools/icon_index.py add --project . <name>` so each lands in the project.

## Signaling — cues tied to spoken words (builder anchors via `word_anchors.py`)

`anchors.json` already carries these phrases (verbatim, unique runs). No cue is timed to an assumed
words-per-second. Each body beat moves at least once mid-scene, so no dead stretch exceeds the 5.0s
budget on top of the block's native stagger.

| Beat | Cue(s) → spoken word |
|---|---|
| B1 | question card lands → *"how much of your directory can they see by default"*; hold/beat → *"Take a guess before we answer it"* |
| B2 | 5 rows cascade in → *"several levers"* |
| B3 | 3 rows in → *"There are three levels"*; the default row **lifts** → *"that default fits"* |
| B4 | broad node appears → *"User Administrator"*; it's **flagged too-broad** → *"manage licenses across the tenant"* |
| B5 | step 1 badge → *"assign coordinators the Guest Inviter role"*; step 2 badge (the gotcha) → *"set the tenant's invite setting"* |
| B6 | row **flips** to Redeemed → *"redeems it by signing in"*; result row → *"a guest object appears"* |
| B7 | key point reveals → *"shows up in two places"*; lands → *"Same record, two surfaces"* |
| B8 | outer ring settles → *"Allow and deny domain lists"*; core glows last → *"go a layer deeper"* |
| B9 | MTO row **lifts** → *"a Multitenant Organization fits"* |

**Native-check markers to place:**

- `data-reveal-after` — B5 step-2 after step-1; B6 the Redeemed row after the pending row; B4 the
  "too broad" flag after the User-Administrator node appears. **Predict-before-reveal spans B1→B3:**
  B1 poses the question and B3 is its answer — keep B3's "Limited access (default)" lift out of view
  until B3; nothing in B1 may reveal the answer.
- `data-keep-in-frame` — B8's concentric `diagram-layers` stage (it scales outside-in and must stay
  centred); B4's `diagram-flow` stage with its walking cursor.

## Hero-swoosh budget

Spent on beats: **`02-title`, `91-cta`** (plus the fixed `01-bumper` open).
- `02-title` — the title statement owns the frame; the swoosh is the video's identity.
- `91-cta` — the closing card; opening and closing on the swoosh bookends the film and is the one
  sanctioned "closing" use. Recap (`90`) deliberately stays on the wash so the swoosh stays scarce.

## Dark-field budget

Spent on **one** beat: **B1 `04-scenario`** — the curiosity-gap hook (*"what can a guest see by
default? Take a guess"*). This is the single most dramatic beat and the only place the film leaves
the light ground; text auto-inverts to white. No other beat uses dark-field.

## Contrast declarations

All readable text is ink `#091F2E` on light grounds; on the one dark-field beat it auto-inverts to
white. **No accent carries text at any size** — every accent (tabs, badges, connectors, underline
rules, status dots/pills, the core glow) is a non-text **mark**. On B6, the status *word* stays ink;
teal/magenta appear only as dot/pill fills.

| Text / ground pair | Ratio | Verdict |
|---|---|---|
| ink `#091F2E` on content-wash | 16.02 | AAA — any size (B2–B9, `03`, `90`) |
| ink `#091F2E` on hero-swoosh (worst zone) | **5.95** | **AA normal / AAA display** — `02`, `91` (**worst readable pair in the plan**) |
| white `#FFFFFF` on dark-field (lightest stop `#365F7D`) | ≈6.5 | AA normal / AAA display — B1; deeper stops exceed 15 |
| any brand/semantic accent as **text** | — | **not used** — marks only |

**Worst readable pair: ink on hero-swoosh = 5.95 (AA-safe).** No new colours introduced, so the
palette gate result is unchanged; no pair falls below AA-large. `teal-light` / `purple-light` never
carry text.

## Fonts

Segoe UI (body) / Segoe UI Semibold (display), embedded from `fonts/`. No non-brand faces.

## Return

- **Ground allocation:** 10 content-wash (B2–B9 + `03-objectives` + `90-recap`), 3 hero-swoosh
  (`01-bumper` fixed, `02-title`, `91-cta`), 1 dark-field (B1). Hero swoosh spent on title + CTA;
  dark field spent once on the hook.
- **Custom vs kit:** **0 custom / 9 kit** across the body (7 distinct blocks). Two declared chrome
  overrides: `91-cta` → hero-swoosh ground; `90-recap` → `list-specs` block.
- **Contrast risk:** none below AA. Worst readable pair is ink on hero-swoosh at **5.95** (AA-safe);
  watch only the swoosh bottom-right-third zone rule on `02`/`91` (left-anchored, complies by
  default). One thing to police at build: on B6 keep the status word in ink and use the semantic
  colour as a fill, not text.
