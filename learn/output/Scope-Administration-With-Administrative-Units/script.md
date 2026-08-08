# Scope administration with administrative units

| | |
|---|---|
| Source | `wwl/provision-govern-identities-entra/includes/7-scope-administrative-units.md` (Unit 7) |
| Module | Provision and govern identities in Microsoft Entra (`learn.wwl.provision-govern-identities-entra`) |
| Profile | `unit-video` |
| Voice | `en-US-Vance:DragonHDLatestNeural` (locked input; supersedes the stale `en-US-Ava` in BRIEF.md) |
| Word budget | 435–726 (target 580) |
| Actual words | 593 |
| Est. runtime | ~4:05 content (593 w ÷ 2.42 w/s ≈ 245 s) + 0:11 AI end card |

<!-- Docs grounding (Docs MCP, current learn.microsoft.com, 2026-08-07). No docs-vs-source
     divergence found — the unit is accurate and current. Verifying URLs cited per claim in the
     fidelity ledger below. Cross-checked object types, scoped role assignment, dynamic-membership
     single-object-type constraint, group-scoping gap, and licensing:
       - /entra/identity/role-based-access-control/administrative-units
       - /entra/identity/role-based-access-control/administrative-units#groups
       - /entra/identity/role-based-access-control/admin-units-members-add
       - /entra/identity/role-based-access-control/admin-units-members-dynamic
       - /entra/identity/role-based-access-control/manage-roles-portal#assign-roles-with-administrative-unit-scope
     Restricted-management AUs exist in docs but are NOT taught in this unit — scope kept unchanged.
     Docs nuance not taught by this unit (out of scope, not a contradiction): an AU-scoped
     User Administrator can reset passwords only for NON-admin users in the unit. -->

## Narration

Relecloud just opened an overseas office, and it needs one regional admin to reset passwords and update profiles there — and nowhere else. But hand that person the User Administrator role, and you've handed them every user in the company. So how do you give a role real power over *one slice* of the directory, and none over the rest?

In the next few minutes, you'll see how an administrative unit draws that boundary, how a scoped role stays inside it, and how one tempting shortcut quietly leaves people unprotected. Get it right, and least privilege holds.

Start with what goes wrong. Assign User Administrator at the tenant level, and it resets passwords and edits profiles — but its reach doesn't stop at the new office. That admin can now reach *every* user in the directory, including the executives back at headquarters.

An administrative unit is the boundary that fixes this — a container in Microsoft Entra ID that holds users, groups, or devices. Assign a role scoped to the unit instead of the whole tenant, and its permissions apply only to the objects that unit contains. Scope the User Administrator role to a unit holding just the office's users, and that's exactly who the admin can reach.

So how do you fill the unit? The same two ways a group gets members. Add people one at a time with assigned membership, or write a rule on attributes like office location and let Entra populate it automatically — dynamic membership. With new hires arriving weekly, that saves you adding each one by hand.

But first, a shortcut that looks easier. Relecloud already has a group — New Office, All Staff — holding everyone at the location. Add that group to the unit, and you've seemingly scoped the admin to the whole office in one click. So: can that admin now reset passwords for the people in the group? [[pause:600ms]]

The answer is no. Adding a group brings the group object into scope — not the users inside it. The admin can rename the group or edit its membership, because the group is a direct member. But they can't reset a password for anyone in it: those users are *two steps removed* — members of a group that's a member of the unit, not of the unit itself.

It's the same rule nested groups follow, just relocated: Entra resolves permissions against direct membership only. The shortcut never reaches two levels down. The fix — add the users to the unit directly, or let a dynamic rule do it as each new hire joins.

Dynamic membership has a catch, though. A dynamic unit supports exactly one object type — users, or devices, never both in the same unit. Need the office's accounts *and* their devices? That's two units, not one. And a dynamic unit can't hold a group at all — only individual users or devices.

One last factor: cost. Dynamic rules require a Microsoft Entra ID P1 license for every user or device the rule covers. Assigned membership doesn't — a Free license covers members you add by hand. For an office still ramping up, that's part of deciding whether the convenience is worth it.

So the regional admin's reach is scoped correctly now — to the office's people, and only them. An administrative unit drew the boundary, a scoped assignment held the role inside it, and you know why a group would've quietly left everyone else unprotected.

A hands-on exercise right after this has you build one of these units yourself. To go deeper on group scoping and dynamic rules, follow the administrative units links in the module.

## Chrome copy (on-screen labels — NOT the spoken sentence; Redundancy principle)

**02-title** (`title-hero`)

- kicker: `MICROSOFT LEARN`
- titleLine1: `Scope administration`
- titleLine2: `with administrative units`
- subtitle: `Give a role power over one slice of the directory — not all of it.`

**03-objectives** (`list-steps`, three chips)

1. title: `Scope a role to a boundary` · detail: `Assign the role to an administrative unit, not the whole tenant`
2. title: `Populate the unit` · detail: `Assigned membership by hand, or dynamic membership by rule`
3. title: `Avoid the group trap` · detail: `A group in a unit scopes the group, not its members`

**90-recap** (`title-hero`)

- kicker: `RECAP`
- titleLine1: `One slice,`
- titleLine2: `scoped correctly`
- subtitle: `Boundary drawn, role contained, the group gap avoided.`

**91-cta** (`title-hero`)

- kicker: `NEXT STEP`
- titleLine1: `Build a unit`
- titleLine2: `yourself`
- subtitle: `Do the hands-on exercise, then explore administrative units on Microsoft Learn.`

## Beat plan

Chrome beats (1–3, 14–15) are scaffolded; the body is beats 4–11 (8 body beats). "Shape cue" is a
content-shape hypothesis for the designer (candidate kit block + ground + focal object) — the
designer owns the final selection. Anchor phrases map to `anchors.json`.

| # | Scene | Narration slice | On screen | Shape cue (candidate) | Cue lands on |
|---|---|---|---|---|---|
| 1 | 01-bumper | *(brand sting — no narration)* | Microsoft Learn mark draws | `bumper` · hero-swoosh · the glyph | — |
| 2 | 02-title | "…over *one slice* of the directory, and none over the rest?" | Title + subtitle | `title-hero` · hero-swoosh · the two-line title | `one slice of the directory` |
| 3 | 03-objectives | "…draws that boundary… scoped role stays inside… shortcut leaves people unprotected." | 3 objective chips (labels) | `list-steps` · section-field · the three chips | `draws that boundary` |
| 4 | body — over-privilege | "…reset passwords for *every* user in the directory, including the executives back at headquarters." | Entra Roles blade; User Administrator at **Directory** scope. **capture: Entra admin center → Roles & admins → User Administrator assignment (scope = Directory)** | `media-screenshot` · content-wash · callout box over the scope value | `the executives back at headquarters` |
| 5 | body — the boundary **[spine]** | "An administrative unit is the boundary… permissions apply only to the objects that unit contains." | Tenant ring → administrative-unit ring → the office's users at the core | `diagram-layers` · content-wash · the AU ring closing around the core | `only to the objects that unit contains` |
| 6 | body — populate | "…assigned membership, or… let Entra populate it automatically — dynamic membership." | Two population methods; dynamic lifts for the growing office | `list-select` · content-wash · the *dynamic membership* row lifting | `populate it automatically` |
| 7 | body — the shortcut (PREDICT) | "…can that admin now reset passwords for the people in the group?" | The guiding question card; group being dropped into the unit | `callout-note` (**PREDICT**) · content-wash · the question | `for the people in the group` |
| 8 | body — the reveal **[spine payoff]** | "Adding a group brings the group object into scope — not the users inside it… *two steps removed*." | Unit → group (in scope) → members (out of reach), the two-hop path. **reuse option: module media `7-administrative-unit-group-scoping-gap.png`** | `diagram-flow` · content-wash · the emphasized group node vs. the unreachable members | `the group object into scope` · `two steps removed` |
| 9 | body — the rule + fix | "Entra resolves permissions against direct membership only… add the users to the unit directly…" | Key-point card: direct membership only; the fix | `callout-note` (**KEY POINT**) · content-wash · the term "direct membership" | `direct membership only` · `add the users to the unit directly` |
| 10 | body — dynamic constraint | "…exactly one object type — users, or devices, never both in the same unit… can't hold a group at all." | Constraint rows: object type / both at once / groups | `list-specs` · content-wash · the "one object type" row | `exactly one object type` · `can't hold a group at all` |
| 11 | body — licensing | "Dynamic rules require a Microsoft Entra ID P1 license for every user or device the rule covers. Assigned… a Free license…" | Cost side-by-side: Dynamic = P1 per member; Assigned = Free | `callout-note` (**NOTE**) · content-wash · the P1-vs-Free contrast *(designer may use `list-specs`)* | `every user or device the rule covers` · `a Free license covers members` |
| 12 | 90-recap | "…scoped correctly now — to the office's people, and only them." | Recap payoff card | `title-hero` · hero-swoosh · the payoff line | `scoped correctly now` |
| 13 | 91-cta | "…build one of these units yourself… follow the administrative units links…" | CTA card | `title-hero` · hero-swoosh · the next-step line | `build one of these units yourself` |

## Source-fidelity ledger

Referent / quantifier / modality checked on every row. No claim reached the disqualifier bar.

| Claim in narration | Source / Docs | Verbatim? |
|---|---|---|
| A regional admin should reset passwords and update user properties for one office's employees, and nothing more | Source ¶1 ("resets passwords and updates user properties for that office's employees, and nothing more") | Paraphrase — faithful |
| User Administrator at the tenant level reaches **every** user in the directory, including executives at HQ | Source ¶1; Docs: [administrative-units](https://learn.microsoft.com/entra/identity/role-based-access-control/administrative-units) ("if you assign a role to a user that is not a member of an administrative unit, the scope of the role is the entire tenant") | Quantifier "every" preserved; faithful |
| An administrative unit is a container in Microsoft Entra ID that holds **users, groups, or devices** | Source ¶2 ("holds users, devices, or groups"); Docs: [administrative-units](https://learn.microsoft.com/entra/identity/role-based-access-control/administrative-units) ("can contain only users, groups, or devices") | Same set, order differs — faithful |
| A role scoped to a unit applies **only** to the objects the unit contains | Source ¶2; Docs: [manage-roles-portal](https://learn.microsoft.com/entra/identity/role-based-access-control/manage-roles-portal#assign-roles-with-administrative-unit-scope) ("role permissions apply only when managing members of the administrative unit itself") | Modality "only" preserved; faithful |
| Two ways to populate: assigned membership (one at a time) or dynamic membership (rule on attributes like office location) | Source ¶3; Docs: [admin-units-members-add](https://learn.microsoft.com/entra/identity/role-based-access-control/admin-units-members-add) + [admin-units-members-dynamic](https://learn.microsoft.com/entra/identity/role-based-access-control/admin-units-members-dynamic) | Faithful |
| Adding a group to the unit brings the **group object** into scope, **not** the users inside it | Source ¶5; Docs: [administrative-units#groups](https://learn.microsoft.com/entra/identity/role-based-access-control/administrative-units#groups) ("brings the group itself into the management scope… but **not** the members of the group") | Verbatim intent — faithful |
| The scoped admin **can** rename the group / edit its membership, but **can't** reset a password for members | Source ¶5; Docs: [administrative-units#groups](https://learn.microsoft.com/entra/identity/role-based-access-control/administrative-units#groups) (can manage group name/membership ✅; reset member passwords ❌) | Modality can/can't preserved; faithful |
| Members are **two steps removed** — members of a group that's a member of the unit, not direct members | Source ¶5 ("two steps removed—members of a group that's a member of the unit, not direct members of the unit itself") | Near-verbatim |
| Entra resolves permissions against **direct membership only** | Source ¶6 ("resolves permissions and policies against direct membership only") | Verbatim intent — faithful |
| Fix: add users to the unit directly, or use dynamic membership to do it automatically | Source ¶6 ("add the users to the administrative unit directly, or use dynamic membership…") | Faithful |
| A dynamic unit supports **exactly one** object type — users **or** devices, **never both** in the same unit | Source ¶7; Docs: [admin-units-members-dynamic](https://learn.microsoft.com/entra/identity/role-based-access-control/admin-units-members-dynamic) ("not possible to create an administrative unit with rules for dynamic membership… more than one object type… for users or devices, but not both") | Quantifier "exactly one"/"never both" preserved; faithful |
| Both accounts **and** devices in one auto-populated unit → **two units, not one** | Source ¶7 | Faithful |
| A dynamic unit **can't hold a group at all** | Source ¶7; Docs: [admin-units-members-dynamic](https://learn.microsoft.com/entra/identity/role-based-access-control/admin-units-members-dynamic) ("Administrative units with rules for dynamic membership groups for groups are currently not supported") | Faithful |
| Dynamic membership rules require **Microsoft Entra ID P1** for every user or device the rule covers | Source ¶8; Docs: [administrative-units#groups](https://learn.microsoft.com/entra/identity/role-based-access-control/administrative-units) ("If you are using rules for dynamic membership groups… each administrative unit member requires a Microsoft Entra ID P1 license") + [admin-units-members-dynamic](https://learn.microsoft.com/entra/identity/role-based-access-control/admin-units-members-dynamic) | Faithful |
| Assigned membership needs no such license — a **Free** license is enough for manually added members | Source ¶8; Docs: [admin-units-members-add](https://learn.microsoft.com/entra/identity/role-based-access-control/admin-units-members-add) ("Microsoft Entra ID Free licenses for administrative unit members") | Faithful |
| A hands-on exercise right after this unit has you build such a unit | Source ¶9 ("A hands-on exercise right after this unit has you build exactly this kind of administrative unit yourself") | Faithful |

## Open questions

- **CTA link target.** The unit links to `/entra/identity/role-based-access-control/administrative-units#groups` and `/entra/identity/role-based-access-control/admin-units-members-dynamic`; the CTA narration points to "the administrative units links in the module" rather than a raw URL (paths aren't narrated). Confirm the on-screen CTA should surface these two Learn URLs.
- **Voice mismatch.** BRIEF.md carries `en-US-Ava`; the locked input is `en-US-Vance:DragonHDLatestNeural`. Script uses the locked voice — confirm before the audition/TTS gate. `en-US-Vance` isn't in the narration-doctrine per-voice pace table, so the runtime estimate uses the corpus mean (2.42 w/s); re-measure the actual WAV with `ffprobe` after TTS.
- **`P1` pronunciation.** Left as "P1" (correct product term). Audition the licensing sentence — if Dragon HD mangles it, reword to "P one" in `narration.txt` before locking. Licensing cues deliberately anchor on clean phrases that avoid the `P1` token.
