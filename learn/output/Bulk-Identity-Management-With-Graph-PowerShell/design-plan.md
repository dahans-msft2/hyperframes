# Design plan — Bulk Identity Management with Graph PowerShell

Preset: learn-ilt   Profile: unit-video   Run: bulk-identity-management-graph-202608071310

Spine: **connect → import → loop**, taught in PowerShell. The `code`/`console` family is the
backbone. Two light code reads bracket one dark console payoff — the loop actually *runs* on the
single dark-field beat, which is also the narration's emotional peak ("thirty rows in, thirty
accounts out"). Everything readable is ink; colour is a mark, never body text.

## Per-beat table

| # | Scene id | Component | Kind | Why it fits (+ rejected) | Ground | Config / Elements | Accent use | Asset / capture |
|---|---|---|---|---|---|---|---|---|
| — | `01-bumper` | bumper | block | mandatory brand sting; only kicker varies | **hero-swoosh** | kicker `Provision and govern identities in Microsoft Entra` | ink only | — |
| — | `02-title` | title-hero | block | the title owns the frame — one headline statement | **hero-swoosh** | kicker `MICROSOFT LEARN` · `Bulk Identity Management` / `with Graph PowerShell` · subtitle `Provision hundreds of accounts in a single pass` | ink only (accent rule is a mark) | — |
| — | `03-objectives` | list-steps | block | 3 outcome chips, staggered as named | content-wash | 3 steps (title+detail) from chrome copy; vertical connector | accent number badges (mark) | PowerShell icon (tool anchor) |
| B1 | `04-spine` | list-steps | block | ordered 3-move procedure "Connect · Import · Loop". Rejected `list-select` (nothing is chosen); `diagram-flow` (linear, not branching → its `avoid_when`) | content-wash | steps `Connect` / `Import` / `Loop`, terse one-line gloss each, oversized numerals, final lock-up lights all three | accent numerals (mark) | — |
| B2 | `05-connect` | code-window | block | a short snippet the learner reads — the connect line. Rejected `console-status` (not a status-check panel) | content-wash | filename `provision.ps1` · lang PowerShell · active line = `Connect-MgGraph -Scopes "User.ReadWrite.All"` | blue/purple syntax on **pure #FFFFFF** panel only | PowerShell icon (filename chip) |
| B3 | `06-csv` | list-specs | block | the CSV **column set** as label/value rows. Rejected `list-steps` (columns are unordered attributes, not a sequence); `code-window` (the point is the column set, not `Import-Csv` syntax) | content-wash | rows `DisplayName` · `UserPrincipalName` · `MailNickname` · `TempPassword` (label = column, value = "from the file") | accent underline rules (mark) | — |
| B4 | `07-loop` | **custom** dark PowerShell console | **custom** | the spine payoff — the loop **executes** and account-created lines stream to a count of 30; a terminal is dark by nature, so dark-field is *motivated*, not decorative. Rejected `code-window` (light IDE reader — static, no execution/streaming, can't carry a dark console); `console-status` (a portal status panel flipping one row, not a terminal running a create-loop) | **dark-field** | authored on `_foundation.css`: dark terminal window, prompt, `foreach { New-MgUser … }`, `User created` lines streaming, counter → **30** | white ink (auto-invert); teal-light `#49C5B1` for success lines (7.94 on dark) | PowerShell icon (console title bar) |
| B5 | `08-repeatable` | callout-note | block | one takeaway to emphasize — term "Repeatable". Rejected `stat-count` (no number); `list-specs` (single point, not a spec set) | content-wash | label `KEY POINT` · term `Repeatable` · body: rerun next quarter, no portal blades | positive/teal accent tab (mark) | — |
| B6 | `09-scope-match` | list-select | block | choose-one: two peer scopes, the matched one lifts. Rejected `diagram-flow` (a selection, not branching logic to walk); `list-specs` (one row is *selected*, not just listed) | content-wash | items `User.ReadWrite.All` (selectedIndex 0) · `Directory.ReadWrite.All` (recedes — too broad); kicker, countLabel | accent tab on the lifted row (mark) | — |
| B7 | `10-scope-pattern` | list-specs | block | task→scope **mapping** table. Rejected `list-select` (no single selection — it generalizes a rule); `list-steps` (a mapping, not an ordered sequence) | content-wash | rows: read → `User.Read.All` · group members → `GroupMember.ReadWrite.All` · admin unit → `AdministrativeUnit.ReadWrite.All` | accent underline rules (mark) | Users · Groups · Entra icons (per row / recipient) |
| B8 | `11-update-delete` | code-window | block | same snippet shape, cmdlet swapped — reads as "same shape". Rejected `console-status` (not a status panel) | content-wash | filename `update.ps1` · active line = `Update-MgUser …`; caption: `Remove-MgUser` = identical shape | blue/purple syntax on pure #FFFFFF only | PowerShell icon (filename chip) |
| B9 | `12-contacts` | callout-note | block | one boundary/warning — term "New-MailContact". Rejected `diagram-flow` (a stated boundary, not a walked decision); `list-select` (an exclusion, nothing selected) | content-wash | label `TRAP` · term `New-MailContact` · body: Exchange Online PowerShell, **not** Microsoft Graph | warning/incident accent tab (mark) | Graph/PowerShell ✕ Exchange icons (the boundary) |
| — | `90-recap` | title-hero | block | closing payoff — resolves the Monday-deadline hook | content-wash | kicker `RECAP` · payoff lines · subtitle tied to the hook | ink only | — |
| — | `91-cta` | title-hero | block | closing send-off — **override** to hero-swoosh (see budget) | **hero-swoosh** ⚠ override | kicker `NEXT STEP` · CTA lines · subtitle (exercise + New-MgUser reference) | ink only | — |

`Component` = kit-block id from `blocks/catalog.json` (or `custom`). The builder applies the chosen
`Ground` as `data-ground` on each block's `#root`. **B4 is the only custom scene**; everything else
is a kit block.

## Chrome overrides (deliberate)

- **`91-cta`: content-wash → hero-swoosh.** The scaffold stamps the CTA on the wash; I promote it so
  the video closes on the scarce hero ground. This gives a clean bracket — hero *opens* (bumper +
  title), the wash carries the whole body, and hero *closes* (CTA). Keep display type in the **left
  column** (the swoosh's colour field concentrates upper-right; left col measures 15.6 vs the
  bottom-right 5.95). The builder must set `data-ground="hero-swoosh"` on `91-cta`.
- Everything else kept as scaffolded: `01-bumper` hero, `02-title` hero, `03-objectives` wash,
  `90-recap` wash. `90-recap` stays on the wash deliberately — a calm content-summary that hands off
  into the hero CTA, which keeps hero-swoosh scarce and lets the final beat bloom.

## Frame obligations

Every beat states a ground plane, two depth planes, and an object with weight.

| # | Ground plane | Depth (near / far) | Object with weight |
|---|---|---|---|
| 02 | hero swoosh field | title lock-up (near, soft elevation) / swoosh receding | filled two-line wordmark, not outlined |
| 03 | wash | chip column (near, elevation) / wash | three filled number badges + chips |
| B1 | wash | pipeline stages (near) / wash | three filled stage badges as a lock-up |
| B2 | wash | white IDE window (near, `0 2px 8px rgba(9,31,46,.10)`) / wash | the code panel — a solid slab with an interior |
| B3 | wash | spec rows (near, elevation) / wash | four filled label/value rows |
| B4 | **dark stage** | console window (near, elevation) / dark-field receding | the terminal slab + streaming output + the **30** numeral |
| B5 | wash | key-point card (near, tab + elevation) / wash | filled accent-tab card |
| B6 | wash | lifted row (nearest) / receded peer (far) / wash | the lifted scope row as a solid tile |
| B7 | wash | mapping rows (near) / wash | filled task→scope rows with product icons |
| B8 | wash | white IDE window (near) / wash | the code panel (echoes B2) |
| B9 | wash | trap card (near) / wash | filled warning card + the two boundary icons |
| 90 | wash | recap lock-up (near) / wash | filled payoff wordmark |
| 91 | hero swoosh field | CTA lock-up (near) / swoosh | filled CTA wordmark + link chip |

## Component range

Seven distinct components across the body + chrome — no monotone deck:
`bumper`, `title-hero` (×3: title, recap, cta), `list-steps` (×2: objectives, spine),
`code-window` (×2: connect, update/delete), `list-specs` (×2: csv columns, scope map),
`list-select` (×1: scope match), `callout-note` (×2: key-point, trap), + **1 custom** dark console.

Repeats are all justified by a recurring teaching relationship and are separated in time:
- **code-window ×2** — B2 (setup) and B8 (reprise); B8 deliberately returns to the *quiet light*
  code read so "same shape, now routine" lands — the drama was already spent at B4's dark console.
- **list-specs ×2** — B3 (CSV columns) and B7 (task→scope map); different content shapes, four
  beats apart.
- **callout-note ×2** — B5 (KEY POINT, positive/teal tab) and B9 (TRAP, warning tab); opposite
  semantic accents, four beats apart.

**Twin-list watch:** `03-objectives` and B1 are both `list-steps` and are adjacent. B1 must **not**
read as a carbon copy — objectives are outcome *sentences* with detail sublines that stagger and
hold; B1 is a terse imperative *mnemonic* (Connect / Import / Loop) with oversized numerals whose
final state lights all three at once as a lock-up. Different content, different emphasis, same block.

### Builder shopping list

- **Kit blocks to copy in:** `bumper`, `title-hero`, `list-steps`, `code-window`, `list-specs`,
  `list-select`, `callout-note`.
- **Custom scenes to hand-author on `_foundation.css`:** `07-loop` — the dark PowerShell console
  (dark-field, white ink, monospace, streaming output → count 30).

## Assets — reuse, then capture, then generate

- **Reuse:** the source module's `media/` holds only sibling-unit art
  (`2-soft-delete-timeline`, `6-nested-group…`, `7-administrative-unit…`, `9-privileged-identity…`).
  **None serve Unit 3** — there is nothing here to reuse. Body beats are authored geometry + code +
  product icons.
- **Capture opportunity (offer to author):** this unit teaches PowerShell, not a portal blade, so
  no screen capture is required. One optional enhancement — a **short screen recording of the loop
  running in a real PowerShell terminal** (`media-screen-recording`) could stand in for the B4
  custom console if the author would rather show the genuine article. Offer it; do not fabricate a
  terminal as "real" output. Default plan is the authored console (deterministic, on-brand).
- **Generated:** none. Every beat is schematic (code, lists, a console, callouts) — authored
  geometry animates causally; a raster would not earn its place here.

## Iconography

The named products should appear with their marks, not as bare text. Pull only what each beat needs
(`py tools/icon_index.py add --project . <name>`), prefer SVG:

| Beat | Icon | Library path |
|---|---|---|
| 03 · B1 · B2 · B4 · B8 | **PowerShell** (Graph PowerShell tool mark) | `Azure/general/10825-icon-service-Powershell.svg` |
| B7 | **Users** (read row) | `Azure/identity/10230-icon-service-Users.svg` |
| B7 | **Groups** (group-member row) | `Azure/identity/10223-icon-service-Groups.svg` |
| B7 | **Entra** (recipient — "tells Entra ID what your script may touch") | `Microsoft-Security-product-icons-kit/Entra/SVG/Entra.svg` |
| B9 | **Exchange** (the boundary — Graph ✕ Exchange Online) | `Azure/intune/10339-icon-service-Exchange-Access.svg` |

No dedicated "Microsoft Graph" icon exists in the library — represent Graph PowerShell with the
**PowerShell** mark throughout. One clear icon per concept; icons label meaning, they are not
decoration.

## Signaling — cues tied to spoken words

Each beat has one focal element and reacts *on the word* (the builder anchors these to
`transcript.json` via `word_anchors.py`, never to a guessed offset):

| # | Focal object | Cue → spoken phrase | Reaction |
|---|---|---|---|
| B1 | the 3-move lock-up | `overview_steps` → "Connect, import, loop" | all three stages light simultaneously |
| B2 | the `-Scopes` value | `connect_cmd` → "starts with Connect-MgGraph"; `connect_scope` → "exactly one scope" | line reveal, then highlight **lifts to** `"User.ReadWrite.All"` |
| B3 | the four column rows | `import_csv` → "Import-Csv reads your spreadsheet"; `csv_columns` → "a display name, a user principal name" | rows stagger in as each field is named |
| B4 | the streaming output → **30** | `loop_foreach` → "A foreach walks that list"; `create_newmguser` → "hands each row to New-MgUser" | loop body reveals; each `New-MgUser` line **pulses** as accounts stream; counter punches to 30 |
| B5 | the term **Repeatable** | `repeatable` → "A script is repeatable" | card scale-in with accent-tab wipe |
| B6 | the lifted scope row | `match_scope_question` → "the broader Directory.ReadWrite.All"; `least_privilege` → "match the scope to the task" | `User.ReadWrite.All` **lifts** exactly on `least_privilege`; the broad scope recedes |
| B7 | each task→scope row | `pattern_scales` → "scales to every bulk job"; `read_scope` → "User.Read.All, read-only" | rows populate as each task is named (brisk, 3 rows) |
| B8 | the swapped cmdlet | `update_cmd` → "Update-MgUser runs the very same"; `remove_cmd` → "Remove-MgUser follows the identical shape" | cmdlet name swaps **in place** to read as "same shape" |
| B9 | the boundary | `contacts_trap` → "doesn't manage mail contacts"; `newmailcontact` → "belongs to New-MailContact" | Graph side dims / strikes, Exchange side lights on `newmailcontact` |

## Motion budget

`unit-video` → `max_static_stretch_seconds` **5.0s**. No beat may sit still longer than that. Every
body beat carries a word-anchored carrier motion (reveal, lift, pulse, swap) above, so none idles.
B4's streaming console and the count-to-30 keep the payoff continuously alive — it is the densest
beat by design. `data-reveal-after` pins B4's `New-MgUser` result lines behind the loop start, and
the lifted row in B6 behind its peers, so nothing resolves early.

## Hero-swoosh budget

Spent on beats: **01-bumper, 02-title, 91-cta** (three total; `01-bumper` is the mandatory brand
sting). Each is a brand/title/closing frame — never a content frame:
- **01-bumper** — mandatory opening sting.
- **02-title** — the title card; hero is its home ground.
- **91-cta** — the closing send-off; brand doctrine lists "closing" as a sanctioned hero use, and
  it brackets the open. `90-recap` is intentionally **not** hero (kept on wash) so the CTA stays the
  single scarce close and the gradient does not become wallpaper.

Bottom-right-third rule honoured on both hero beats: display type stays left-anchored.

## Dark-field budget

Spent on **one** beat: **B4 `07-loop`** — the loop-runs console. It is the narration's peak
("thirty rows in, thirty accounts out"), the payoff of the whole spine, and a terminal is dark by
nature, so the ground is motivated rather than decorative. No other beat uses dark-field.

## Contrast declarations

WCAG 2.1, measured against the FRAME tokens. Every readable pixel is ink (or white on dark); no
brand accent carries normal-size text anywhere.

| Text / ground pair | Ratio | Verdict |
|---|---|---|
| ink `#091F2E` on content-wash (all body beats) | **16.02** | AAA — any size |
| ink display on hero-swoosh (01, 02, 91) — left column | 15.6 | AAA (left) |
| ink display on hero-swoosh — worst zone | 5.95 | AA-large ✓ (keep display out of bottom-right third) |
| white ink on dark-field console (B4) | ~17 | AAA |
| success/output line teal-light `#49C5B1` on dark-field (B4) | 7.94 | AAA |
| code body ink on the code-window's **pure #FFFFFF** panel (B2, B8) | ~18 | AAA |
| blue syntax keyword `#0078D4` on pure #FFFFFF (B2, B8) | **4.53** | AA ✓ — **worst readable ratio** |
| text-muted `#33414D` captions on wash (sparingly) | ~9 | AA |

**Worst readable ratio in the plan: 4.53** (blue syntax keyword on pure white). All readable text
clears AA; all body / label / caption text clears AAA at 16.02.

### Contrast risk — the one thing to watch

Coloured PowerShell syntax in the light code-window (B2, B8) clears 4.5 **only on a pure `#FFFFFF`
panel** — on the warm wash, blue drops to **4.31 and fails**. So the builder must keep the
code-window's inner surface pure white (the light-IDE block already does) and never let a coloured
token sit on the wash. Zero-risk fallback: render code as **ink `#091F2E` with weight-only
emphasis** (16.02) and reserve colour for the active-line tint band, which is a non-text mark.

Semantic-accent note for B7: `AdministrativeUnit.ReadWrite.All` is reproduced from the source unit's
scope table (the standalone Docs permissions page wasn't fetched this pass). It is a focal row —
spot-check it against current admin-unit cmdlet docs before render (per the script's open questions).

Re-run after any palette edit:
```
py tools/contrast_gate.py brand/_extract/palette.json --min 3.0
```

## Fonts

Segoe UI / Segoe UI Semibold, embedded from `fonts/`. Monospace code/console: the code-window's
own monospace face on its pure-white panel; the B4 console renders monospace white on dark.
No Space Grotesk / JetBrains Mono / Fraunces — not brand fonts.
