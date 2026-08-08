<!--
Source verification (Docs MCP, learn.microsoft.com, checked 2026-08-07):
- Eligible vs active assignment types ....... https://learn.microsoft.com/entra/id-governance/privileged-identity-management/pim-configure#terminology
- Activation actions (approval/MFA/justification) https://learn.microsoft.com/entra/id-governance/privileged-identity-management/pim-configure#terminology
- Just-in-time (JIT) access .................. https://learn.microsoft.com/azure/role-based-access-control/pim-integration#pim-functionality
- Activation maximum duration (1-24 h) ....... https://learn.microsoft.com/entra/id-governance/privileged-identity-management/pim-resource-roles-configure-role-settings#role-settings
- Require approval + empty-approver fallback .. https://learn.microsoft.com/entra/id-governance/privileged-identity-management/pim-how-to-change-default-settings#role-settings
- Lockout risk (3 conditions, verbatim) ...... https://learn.microsoft.com/entra/id-governance/privileged-identity-management/pim-how-to-change-default-settings#role-settings
- Emergency access accounts / break-glass GA .. https://learn.microsoft.com/entra/id-governance/privileged-identity-management/pim-deployment-plan#understand-pim
- Custom roles (when a built-in is too broad) . https://learn.microsoft.com/entra/identity/role-based-access-control/custom-overview
- PIM license prerequisite (P2 / Governance) .. https://learn.microsoft.com/entra/id-governance/privileged-identity-management/pim-getting-started#overview  (verified; intentionally NOT taught — unit omits it; see Open questions)
No material docs-vs-source divergence. See fidelity ledger.
-->

# Govern roles with role groups and PIM

| | |
|---|---|
| Source | wwl/provision-govern-identities-entra/includes/9-govern-roles-role-groups-privileged-identity-management.md (Unit 9) |
| Profile | unit-video |
| Voice | en-US-Vance:DragonHDLatestNeural |
| Word budget | 435–726 (target 580) |
| Actual words | 650 |
| Est. runtime | ~4:29 narration (650 ÷ 2.42 w/s ≈ 269s, inside the 180–300s window) + 0:11 AI end card |

## Narration

Here's a problem hiding in a lot of tenants. Your most powerful role, Global Administrator, is switched on permanently for more people than need it — and every one is a standing target, used or not. So what if nobody carried that access by default? What if you could hand someone the role, let it sit dormant until they need it, then expire on its own? That's this unit, and *Microsoft Entra Privileged Identity Management* is how you get there.

You'll see three things: how Entra assigns roles today, and why that leaves access always on; how PIM makes it just-in-time instead; and where one wrong setting can quietly lock your admins out.

Start with how roles get assigned today. Entra ID ships a catalog of built-in roles — well over a hundred — each with a fixed set of permissions. Outside PIM, you grant one with a direct assignment at a scope: the whole tenant, or something narrower, like an administrative unit.

But Entra roles aren't the whole story. Workloads like Exchange, Microsoft Purview, and Microsoft Defender run their own access control, bundling roles into role groups you assign as one unit — so check the workload before you reach for the Entra catalog.

Now the catch. A direct assignment is always on — the moment it's created, the user holds those permissions until someone removes it. That's how a tenant ends up with too many people holding standing access to Global Administrator, just because it was simpler to set up.

PIM replaces always-on with two assignment types. An active assignment works like a direct one — permissions apply immediately. An eligible assignment grants nothing by itself; the user has to activate the role first. Move those standing admins from active to eligible, and nobody carries the access by default.

So what does activating involve? Before the role takes effect, it can require approval, multifactor authentication, or a business justification. Then it's time-boxed: activation maximum duration decides how long — say, four hours — then the permissions expire on their own. That's just-in-time access.

Here's a puzzle. You set a sensitive role to require approval, then leave the approver list empty. So who signs off? You'd expect the request to stall. Instead, PIM falls back to every admin holding an active Privileged Role Administrator or Global Administrator assignment, tenant-wide.

But that fallback only works if at least one of those admins is actually active. If every Privileged Role Administrator and Global Administrator is eligible-only, approval is required, and no approvers are set, there's nobody left to approve. The request sits indefinitely — and depending on the role, that can lock admins out. So keep at least one emergency access account with a permanent, active Global Administrator role, and set explicit approvers.

One more trap. PIM has three duration settings, and two sound almost identical. Activation maximum duration is how long a single activation lasts. Expiration of eligible assignments is how long you can activate the role at all. Expiration of active assignments is how long a standing assignment survives before it's removed. Mix them up, and you answer the wrong question.

Finally, sometimes a built-in role grants more than the job needs, with nothing narrower in the catalog. That's when a custom role is the right call — you pick exactly the permissions the task needs, then assign it at a scope. The real skill is recognizing that moment.

So, back to that standing-access problem. Convert your always-on admins to eligible, and access becomes just-in-time — granted on activation, gated by approval, gone when the time-box expires. The empty-approver puzzle isn't magic; it's a fallback you plan around with an emergency access account. That's the governance model this module builds toward.

Next, you'll configure this exact approval workflow yourself: assign an eligible role, require approval, and see who ends up approving it. To go deeper on role settings and the fallback, follow the Microsoft Learn links in this unit.

## Chrome text (fills the scaffolded `__FILL__` placeholders — labels, not transcript)

**01-bumper** — kicker sub-line: `Provision and govern identities in Microsoft Entra`

**02-title**
- kicker: `Identity governance`
- title (2 lines): `Govern roles with` / `role groups and PIM`
- subtitle: `Turn always-on admin access into just-in-time.`

**03-objectives** (3 chips, framed as stakes)
1. `How Entra assigns roles — and why it's always on`
2. `How PIM makes access just-in-time`
3. `The setting that can lock your admins out`

**90-recap** (3 label lines)
1. `Always-on → eligible = just-in-time access`
2. `Empty approver list → active PRA / GA approve`
3. `Emergency access account prevents lockout`

**91-cta**
- primary: `Next: configure the PIM approval workflow`
- learn-more: `PIM role settings & the approver fallback (links in this unit)`

## Beat plan

Chrome rows (01–03, 90–91) are scaffolded; narration above supplies their text. Body beats B1–B9 fill the `body_slot`. Shape cue = catalog `content_shape` match + the weighted object; the designer owns final block selection.

| # | Scene / beat | Narration slice (opening words) | On screen (label, not transcript) | Kit block + ground | Focal object | Shape cue | Cue → spoken phrase |
|---|---|---|---|---|---|---|---|
| 01 | bumper | *(brand sting, no VO)* | Microsoft Learn mark | `bumper` · hero-swoosh | Learn glyph | mandatory open | — |
| 02 | title | "Here's a problem hiding…" | Title + "always-on → just-in-time" subtitle | `title-hero` · hero-swoosh | 2-line title | one headline owns the frame | `hook_standing_target` → "standing target"; `hook_pim_named` → "Microsoft Entra Privileged Identity Management" |
| 03 | objectives | "You'll see three things…" | 3 stakes chips | *(scaffolded objectives)* · section-field | objective chips | 3 outcomes as stakes | `obj_lockout` → "lock your admins out" |
| B1 | roles today | "Start with how roles get assigned today…" | Built-in catalog; one role picked at a scope | `list-select` · content-wash | selected role chip at tenant scope | choose-one among 100+ peer roles (`avoid_when`: not ordered/nested) · *capture opt: Roles and administrators / Add role assignment* | `b1_direct_assignment` → "a direct assignment at a scope" |
| B2 | role groups | "But Entra roles aren't the whole story…" | DEFINITION: role group = roles bundled as one unit (Exchange / Purview / Defender) | `callout-note` · content-wash | "role group" term card | one definition to emphasize | `b2_role_groups` → "role groups you assign as one unit" |
| B3 | always-on problem | "Now the catch. A direct assignment is always on…" | KEY POINT: a *direct* assignment is always on → standing access | `callout-note` · content-wash | "Always on" state | one takeaway (referent = direct assignment only) | `b3_always_on` → "is always on" |
| B4 | two assignment types | "PIM replaces always-on with two assignment types…" | active (immediate) vs eligible (activate first); eligible lifts | `list-select` · content-wash | eligible row lifting | choose-one between two peers · *reuse: `media/9-privileged-identity-management-active-vs-eligible.png` (ships with module)* | `b4_two_types` → "two assignment types"; `b4_eligible` → "grants nothing by itself" |
| B5 | activation lifecycle | "So what does activating involve?…" | eligible → activate (approval / MFA / justification) → time-box 4h → expire | `list-steps` · content-wash | the 4-hour time-box step | ordered 3–4 step procedure (the JIT spine) · *capture opt: PIM activation blade, max-duration slider* | `b5_activate` → "it can require approval"; `b5_expire` → "expire on their own" |
| B6 | empty-approver puzzle | "Here's a puzzle. You set a sensitive role…" | Approval flow: approver list empty → request approved by fallback (withhold the "who" — predict first) | `console-status` · content-wash | request row flipping pending → approved | checks / approval / pass-fail status · *capture opt: Require approval to activate + empty approver list* | `b6_empty_list` → "leave the approver list empty"; `b6_fallback` → "falls back to every admin" |
| B7 | lockout risk + fix | "But that fallback only works if…" | WARNING: all PRA/GA eligible-only + approval + no approvers → request stuck; fix = emergency access account + explicit approvers | `callout-note` · content-wash *(dark-field candidate — the one dramatic beat, designer's call)* | stuck request / break-glass account | one warning + its mitigation (keep "can", "at least one") | `b7_lockout` → "sits indefinitely"; `b7_emergency` → "at least one emergency access account" |
| B8 | three durations | "One more trap. PIM has three duration settings…" | 3 spec rows: activation max / eligible expiry / active expiry | `list-specs` · content-wash | "Activation maximum duration" row | label/value attributes (disambiguation) | `b8_three_durations` → "three duration settings"; `b8_activation_max` → "how long a single activation lasts" |
| B9 | custom role | "Finally, sometimes a built-in role grants more…" | KEY POINT: built-in too broad → custom role (exact permissions, assign at scope) | `callout-note` · content-wash | "custom role" term card | one takeaway — recognize the moment | `b9_custom_role` → "a custom role is the right call" |
| 90 | recap | "So, back to that standing-access problem…" | 3 recap label lines (answers the opening puzzle) | *(scaffolded recap)* · hero-swoosh | recap lines | payoff of the hook | `recap_activation` → "granted on activation" |
| 91 | cta | "Next, you'll configure this exact approval workflow…" | Next-step + Learn-more label | *(scaffolded cta)* · hero-swoosh | CTA line | call to action | `cta_configure` → "configure this exact approval workflow" |

Body beats: **9** (profile aim ~10; within 5–16). Visual spine: the PIM activation lifecycle (eligible → activate → time-boxed → expire) runs B4 → B5, and the fallback/lockout thread (B6 → B7) pays off the opening puzzle in the recap.

## Source-fidelity ledger

Every factual claim → unit line and/or current Docs URL, with referent (R) / quantifier (Q) / modality (M) checked against the exact source wording.

| # | Claim in narration | Source (Unit 9 + Docs) | R / Q / M check |
|---|---|---|---|
| 1 | "well over a hundred built-in roles, each with a fixed set of permissions" | Unit §Assign roles: "well over 100 today… each with a fixed set of permissions"; [concept-understand-roles](/entra/identity/role-based-access-control/concept-understand-roles) | Q: "well over" kept (not "exactly 100") ✅ |
| 2 | "grant one with a direct assignment at a scope: the whole tenant, or … an administrative unit" | Unit: "creating a direct assignment at a scope: the whole tenant, or a narrower scope such as the administrative unit" | ✅ verbatim |
| 3 | "Exchange, Microsoft Purview, and Microsoft Defender … bundling roles into role groups you assign as one unit" | Unit: "Exchange, Microsoft Purview, and Microsoft Defender each define their own roles and bundle them into role groups—a named collection of roles you assign… as a single unit" | R: role groups belong to the *workloads*, not Entra ✅ |
| 4 | "check the workload before you reach for the Entra catalog" | Unit: "before you reach for the Entra role catalog… confirm the workload doesn't already have its own role group" | M: advisory kept ✅ |
| 5 | "A direct assignment is always on — … until someone removes it" | Unit: "A direct role assignment is always on—the moment it's created, the user holds those permissions until someone removes the assignment" | R: subject = the *direct* assignment (NOT role groups, NOT eligible) ✅ |
| 6 | "too many people holding standing access to Global Administrator, just because it was simpler to set up" | Unit: "too many people hold standing access to the tenant's most powerful role, for no better reason than it was simpler to set up that way" | ✅ |
| 7 | "PIM replaces always-on with two assignment types" | Unit: "PIM replaces 'always on' with two distinct assignment types"; [pim-configure#terminology](/entra/id-governance/privileged-identity-management/pim-configure#terminology) | ✅ |
| 8 | "An active assignment works like a direct one — permissions apply immediately" | Unit: "An active assignment behaves like a direct assignment—permissions apply immediately"; Docs: active = no action needed | ✅ |
| 9 | "An eligible assignment grants nothing by itself; the user has to activate the role first" | Unit (verbatim); Docs: eligible "requires a user to perform one or more actions to use the role" | M: "has to activate" kept ✅ |
| 10 | "activating … can require approval, multifactor authentication, or a business justification" | Unit: "that activation can require approval, multifactor authentication, or a business justification"; Docs terminology (MFA check, business justification, approval) | Term: "business justification" (NOT "written"); M: "can require" ✅ |
| 11 | "activation maximum duration decides how long — say, four hours — then the permissions expire on their own" | Unit guiding question: "activation maximum duration is set to 4 hours"; Unit table: "How long a single activation lasts"; Docs: [max duration 1–24 h](/entra/id-governance/privileged-identity-management/pim-resource-roles-configure-role-settings#role-settings) | "four hours" framed as example ("say, four hours"), not a fixed default ✅ |
| 12 | "That's just-in-time access" | Unit: "the shift from always-on access to just-in-time access"; [pim-integration#pim-functionality](/azure/role-based-access-control/pim-integration#pim-functionality) | ✅ |
| 13 | "leave the approver list empty … PIM falls back to every admin holding an *active* Privileged Role Administrator or Global Administrator assignment, tenant-wide" | Unit: "PIM automatically falls back to every user who currently holds an active assignment to the Privileged Role Administrator or Global Administrator role, tenant-wide"; Docs: "If no specific approvers are selected, active Privileged Role Administrators/Global Administrators become the default approvers" | R: **active** holders; Q: "every … active" kept ✅ |
| 14 | "that fallback only works if at least one of those admins is actually active" | Unit: "that fallback only works if at least one of those admins actually holds an active assignment" | Q: "at least one" kept (a floor, not a ceiling) ✅ |
| 15 | "every PRA and GA is eligible-only, approval is required, and no approvers are set → nobody left to approve; the request sits indefinitely — and depending on the role, that can lock admins out" | Unit §lockout risk; Docs lockout warning (3 conditions verbatim): all PRA/GA eligible not active + approval required + no approvers | Q: "every", "no approvers" kept; M: "can lock", "depending on the role" kept; "sits indefinitely" (NOT "forever") ✅ |
| 16 | "keep at least one emergency access account with a permanent, active Global Administrator role, and set explicit approvers" | Unit: "maintain at least one emergency access account with a permanent active assignment to Global Administrator… configure explicit approvers"; Docs recommend **two** cloud-only break-glass GA accounts | Q: "at least one" kept — docs recommend two (stronger, not contradictory; see divergence note) ✅ |
| 17 | "PIM has three duration settings… Activation maximum duration is how long a single activation lasts" | Unit table row 1: "How long a single activation lasts once approved" | ✅ |
| 18 | "Expiration of eligible assignments is how long you can activate the role at all" | Unit table row 2: "How long the user can activate the role at all; when it expires, they can't activate anymore" | ✅ |
| 19 | "Expiration of active assignments is how long a standing assignment survives before it's removed" | Unit table row 3: "How long a standing active assignment lasts before it's automatically removed" | ✅ |
| 20 | "a custom role … pick exactly the permissions the task needs, then assign it at a scope … recognizing that moment" | Unit §custom role: "select exactly the permissions a task requires… define the role and its permission set, then assign it at a scope… the skill worth carrying forward is recognizing the moment it's the right call"; [custom-overview](/entra/identity/role-based-access-control/custom-overview) | ✅ |

**Docs-vs-source divergence:** none material. Two enrichment notes: (a) the unit says "at least one" emergency access account; Docs ([pim-deployment-plan](/entra/id-governance/privileged-identity-management/pim-deployment-plan#understand-pim)) *recommend two* cloud-only break-glass GA accounts — a stronger recommendation, not a contradiction, so the narration keeps the unit's "at least one". (b) the unit never states PIM's license prerequisite; Docs confirm PIM requires **Entra ID P2 or Entra ID Governance** — verified but intentionally left out of narration to stay in unit scope (see Open questions).

## Open questions

- **License prerequisite omitted by design.** PIM needs Entra ID P2 / Entra ID Governance ([pim-getting-started](/entra/id-governance/privileged-identity-management/pim-getting-started#overview)). The unit doesn't teach it, so the narration doesn't either. If the designer wants a one-line on-screen note ("Requires Entra ID P2 / Governance"), it's factual — but it expands scope beyond the unit.
- **Voice mismatch to reconcile.** `BRIEF.md` lists `en-US-Ava`; the locked batch input is `en-US-Vance:DragonHDLatestNeural`. Script written for Vance per the locked input — flag for the builder before TTS spend.
- **"Four hours" is illustrative,** taken from the unit's guiding question, not a product default (Docs allow 1–24 h). Keep it framed as an example on screen (e.g. "e.g. 4h").
- **Runtime vs target.** 650 words is **within** the 435–726 budget but ~70 over the 580 target — the content is genuinely dense (eligible-vs-active, JIT, approval fallback, lockout, three durations, custom roles). Verify the real WAV with `ffprobe`; if it runs long, cut a sentence rather than pushing `--rate`.
