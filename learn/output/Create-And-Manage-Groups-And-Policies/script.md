# Create and Manage Groups and Policies

| | |
|---|---|
| Source | `wwl/provision-govern-identities-entra/includes/6-create-manage-groups-policies.md` (Unit 6, *Provision and govern identities in Microsoft Entra*) |
| Profile | `unit-video` (~240s content; budget 435–726, target ~580) |
| Voice | `en-US-Vance:DragonHDLatestNeural` |
| Word budget | 435–726 (target ~580) |
| Actual words | 608 |
| Est. runtime | ~4:11 content + 0:11 AI end card (608 ÷ 2.42 w/s ≈ 251s; **verify against the actual WAV — Vance has no measured corpus rate yet**) |

<!--
Docs-MCP grounding pass (live learn.microsoft.com, 2026-08-07). Every drift-prone claim was
cross-checked; URLs are in the fidelity ledger. Two docs-vs-source divergences were found and
handled in the narration (see ledger rows 5 and 7 and Open questions):
  • Naming policy is scoped to Microsoft 365 groups in current docs — narration says so.
  • Source says Conditional Access "doesn't reach" nested members; current docs say nested groups
    CAN be used for Conditional Access scopes — narration does NOT make the CA claim and anchors
    the nesting payoff on group-based licensing / shared-resource access, which both agree on.
-->

## Narration

*(Scene 01-bumper is the silent Microsoft Learn brand sting — no narration. The voice begins on the title.)*

An admin at Relecloud is standing at a whiteboard, planning access for a new office full of engineers. They need the same policy and the same licenses the existing engineering team already has. Two options go up on the board — and one of them *doesn't* work the way it looks.

Get that choice wrong and the new hires either lose access they need or gain access they shouldn't. So you'll pick the right group type, decide how people become members, and set the policies that keep the group estate from sliding into clutter.

Start with the type — two kinds of group solve two different problems. A security group manages access — apps, files, Conditional Access, licenses — and it can hold users, devices, even service principals. A Microsoft 365 group is for collaboration instead: a shared mailbox, calendar, and site, and it holds only users. Relecloud's job is access, so a security group it is.

Next, how do people get in? With assigned membership, an admin adds and removes each person by hand. With dynamic membership, Entra ID reads user attributes — like office location — and updates the group automatically as people join and leave. For an office that's still hiring, nobody has to remember to add the next starter.

Back to that whiteboard. The tidy option is a small New Office group nested inside All Engineering, so it inherits the parent's licenses and access for free. Before I tell you what happens, take a guess: [[pause:600ms]] do the people inside that nested group actually pick those up?

Most of us expect nesting to work like folders, where everything on the parent flows down to whatever's inside. Groups *don't* behave that way. Nesting makes the child group a member of the parent — but a license or an assigned resource only reaches the parent's direct members. The people inside the nested group are two steps removed, so nothing reaches them.

And this isn't a one-off quirk. Group-based licensing resolves direct members only — a user buried a level down is invisible to it. So whenever something is assigned to a group, ask one question: who are this group's direct members? That's the only population the assignment reaches.

So nesting won't rescue this plan — but structure still matters as Relecloud grows. Once people create their own Microsoft 365 groups, names drift into chaos. A group naming policy fixes that: it enforces a required prefix or suffix on every new name, and it blocks words you don't want in the directory. It needs Microsoft Entra ID P1.

Naming keeps names tidy, but it doesn't stop groups from outliving their purpose. A six-month project group is often still around two years later — owner gone, members unsure why they're there. A group expiration policy gives each Microsoft 365 group a lifetime in days. As it nears the end, Entra ID asks the owners to renew, and a group still in use renews itself automatically. Anything nobody renews gets deleted — but it stays restorable for thirty days.

Three details worth keeping straight: a tenant gets exactly one expiration policy, it covers all your Microsoft 365 groups or a selected subset, and it needs P1 or P2 for the members it covers — the same tier the naming policy relies on.

So, to recap: security groups for access, Microsoft 365 groups for collaboration. Dynamic membership to keep a growing group current. Nesting that reaches direct members only — never a cascade. And naming and expiration policies keeping the estate clean as Relecloud scales.

That handles the groups themselves. Next, see how an administrative unit scopes an admin's reach to just one slice of the directory. Find the full unit on Microsoft Learn.

## Chrome text (supply to the scaffolded chrome scenes)

The narration above carries the title, objectives, recap, and CTA. The on-screen chrome text is
**labels, not the spoken sentence** (Mayer Redundancy). Fill the `__FILL__` CONFIG with:

- **`02-title`** — kicker `MICROSOFT ENTRA ID` · title (2 lines) `Create and Manage` / `Groups and Policies` · subtitle `Provision and govern identities in Microsoft Entra`
- **`03-objectives`** — three one-line objectives (framed as stakes):
  1. `Pick the right group type and membership model`
  2. `Know why nesting doesn't cascade access`
  3. `Govern the estate with naming and expiration policies`
- **`90-recap`** — three recap chips mirroring the objectives:
  1. `Security = access · Microsoft 365 = collaboration`
  2. `Assignments reach direct members only`
  3. `Naming + expiration keep the estate clean`
- **`91-cta`** — CTA line `Explore the full unit on Microsoft Learn` · next-step chip `Next: Scope administration with administrative units`

## Beat plan

Body scenes go in the `scenes.json` `body_slot` (after `03-objectives`, before `90-recap`). Kit
blocks are content-shape hypotheses for the designer, who owns the final selection. Ground is
`content-wash` unless noted. Anchor = the spoken phrase the beat's cue must land on (see
`anchors.json`).

| Scene | Beat — narration slice | On screen (block · focal · reuse/capture) | Shape cue | Anchor phrase |
|---|---|---|---|---|
| `02-title` | **Hook.** Whiteboard; two options; one doesn't work as it looks | `title-hero` · hero-swoosh · title owns the frame; hook lead-in | The video's title over the opening curiosity gap | `Two options go up on the board` |
| `03-objectives` | **Stakes.** Get it wrong → lost or excess access; here's the plan | `title-hero`/objectives chrome · hero-swoosh · 3 objective chips as stakes | Opening objectives, framed as what breaks without this | `pick the right group type` |
| B1 | **Group types.** Security = access (users/devices/service principals); M365 = collaboration (users only); access → security | `list-select` · **Security group** row lifts vs Microsoft 365 group · countLabel "2 group types" | Peer items, one selected — a choose-one for an access problem | `so a security group it is` |
| B2 | **Membership.** Assigned = manual; dynamic = attribute rule, auto-updates; dynamic for a growing office | `list-select` (alt `diagram-flow`) · **Dynamic** row lifts + "attributes → auto" glyph | Two peer models, one chosen; dynamic auto-updates | `reads user attributes` |
| B3 | **Nesting — predict.** New Office nested in All Engineering; does it inherit the parent's licenses/access? *Guess first* | `diagram-layers` · All Engineering (outer) contains New Office (inner); license badge on the parent; **`?` over the boundary — reveal withheld** | Containment/nesting arranged outside-in — the predict beat | `nested inside All Engineering` |
| B4 | **Nesting — reveal.** Child is a *member*; a license/resource reaches direct members only; nested members are two steps removed | `diagram-flow` (alt: **reuse source asset** `media/6-nested-group-non-cascade.png` via `media-screenshot`) · badge halts at the nested boundary; parent's direct members check, nested members do not · **single dark-field candidate** | Branching: reached vs not-reached — the cognitive-conflict payoff | `the parent's direct members` |
| B5 | **The rule.** "Assigned to a group" = direct members only; group-based licensing can't see a nested user | `callout-note` (KEY POINT) · term `DIRECT MEMBERS ONLY` · **dark-field candidate** (this or B4 is the one dramatic beat) | One emphasized takeaway/definition | `Group-based licensing resolves direct members only` |
| B6 | **Naming policy.** Enforces a prefix/suffix on new Microsoft 365 group names + blocks words; needs P1 | `list-specs` · rows `Prefix/Suffix · GRP_[GroupName]_Engineering`, `Blocked words · CEO, Payroll, HR`, `Requires · Entra ID P1` · focal = name assembling with the prefix | Label/value fact sheet of policy fields | `a required prefix or suffix` |
| B7 | **Expiration — lifecycle.** Lifetime in days → owner renew / auto-renew if active → unrenewed deleted → restorable 30 days | `list-steps` · 4 stages; focal opens on `Lifetime in days`, closes on `Restorable 30 days` | Ordered lifecycle procedure | `a lifetime in days` |
| B8 | **Expiration — constraints.** One policy per tenant; All or Selected subset; P1/P2 for covered members | `list-specs` · rows `Policies per tenant · 1`, `Scope · All or Selected`, `License · P1 or P2` · focal = the `1` | Label/value fact sheet; the exam-tested values | `exactly one expiration policy` |
| `90-recap` | **Recap.** Types, dynamic membership, direct-members-only, naming + expiration | recap chrome · hero-swoosh · 3 recap chips | Closing recap of the stated objectives | `security groups for access` |
| `91-cta` | **CTA.** Next: administrative units scope an admin's reach; go to Learn | `title-hero`/CTA chrome · hero-swoosh · Learn CTA + next-unit chip | Closing call to action | `an administrative unit scopes` |

**Capture/reuse notes for the designer & author**

- **Reuse:** the unit ships `media/6-nested-group-non-cascade.png` — "a policy on a parent group
  reaches direct members but not the members of a nested child group." Strong candidate for **B4**
  via `media-screenshot`; an animated `diagram-flow` may teach the halt better — designer chooses.
- **Illustrative values** in B6 (`GRP_[GroupName]_Engineering`, `CEO, Payroll, HR`) are the
  current Microsoft Learn naming-policy examples (see ledger row 7), not invented.
- No portal-capture beats are required for this unit; every teaching beat is conceptual and served
  by invented graphics (Mayer *Image*).

## Source-fidelity ledger

Referent / quantifier / modality checked on every row. "Verbatim?" = faithful to the source claim,
not a quoted phrase.

| # | Claim in narration | Source (Unit 6) + Docs URL | Verbatim? |
|---|---|---|---|
| 1 | Security group manages access (apps, files, Conditional Access, licenses); holds users, devices, service principals | Source ¶"Choose a group type": "A **security group** manages access to shared resources—apps, files, Conditional Access policies, licenses—and it can contain users, devices, and even service principals." · <https://learn.microsoft.com/entra/fundamentals/concept-learn-about-groups#microsoft-entra-groups-overview> | ✅ faithful |
| 2 | Microsoft 365 group = collaboration (shared mailbox, calendar, site); users only | Same source ¶: "A **Microsoft 365 group** provides collaboration surfaces… It contains only users." · same Docs URL ("Members of a Microsoft 365 group can only include users") | ✅ faithful |
| 3 | Assigned membership = admin manually adds/removes | Source ¶"…membership model": "**Assigned membership** means an admin manually adds and removes specific people." · <https://learn.microsoft.com/entra/fundamentals/concept-learn-about-groups#microsoft-entra-groups-overview> | ✅ faithful |
| 4 | Dynamic membership = rule on attributes; auto add/remove as attributes change | Source same ¶: "**Dynamic membership** means Microsoft Entra ID evaluates a rule against user or device attributes… adds or removes members automatically." · <https://learn.microsoft.com/entra/identity/users/groups-create-rule#overview> | ✅ faithful (modality "automatically" preserved) |
| 5 | Nesting: parent's license/assigned resource reaches **direct members only**; nested members two steps removed get nothing | Source ¶"Test the nesting shortcut": "a policy or license assigned to the parent group applies only to the parent's **direct** members… licenses can't be assigned to a nested security group at all." · <https://learn.microsoft.com/entra/fundamentals/how-to-manage-groups#add-a-group-to-another-group> ("only members in the parent group have access to shared resources and applications"; "We currently don't support… Applying licenses to nested security groups") | ⚠️ faithful to the **licensing / shared-resource** claim (docs-confirmed). **Narration omits the source's "Conditional Access policies don't reach them" claim** — current docs say "Nested groups can be used for membership and **Conditional Access scopes**." Preferred docs; see Open questions. |
| 6 | Group-based licensing resolves direct members only; a nested user is invisible to it | Source ¶"This is worth naming…": "**Group-based licensing**, self-service password reset enablement, and authentication-method scoping all resolve direct membership only." · <https://learn.microsoft.com/graph/api/resources/groups-overview#group-based-licensing> + how-to-manage-groups (row 5) | ✅ faithful — narration asserts **only** the group-based-licensing item (docs-confirmed), not the broader list, to avoid over-generalizing |
| 7 | Naming policy enforces a required prefix/suffix on new **Microsoft 365** group names + blocks words; needs P1 | Source ¶"Keep the namespace clean": "A **group naming policy**… enforcing a required prefix or suffix… along with a blocked-word list… This capability requires Microsoft Entra ID P1." · <https://learn.microsoft.com/entra/identity/users/groups-naming-policy#overview> · <https://learn.microsoft.com/microsoft-365/enterprise/groups-naming-policy> | ⚠️ Source says "every self-service group name" (unscoped); current docs scope the Microsoft Entra ID naming policy to **Microsoft 365 groups** — narration scopes it accordingly. P1 requirement ✅ |
| 8 | Expiration policy gives each M365 group a lifetime in days; owners notified to renew; active groups auto-renew; unrenewed deleted; restorable 30 days | Source ¶"Prevent orphaned groups": "a **group expiration policy**… assigning each covered group a lifetime, measured in days… auto-renews… deleted, though it remains restorable for 30 days." · <https://learn.microsoft.com/entra/identity/users/groups-lifecycle#overview> | ✅ faithful (quantifier "restorable for thirty days" = docs "within 30 days"; no specific lifetime number invented) |
| 9 | One expiration policy per tenant; All or Selected subset; requires P1 or P2 for covered members | Source same ¶: "A tenant can have only **one** expiration policy… applies either to **All**… or to a **Selected** subset… requires Microsoft Entra ID P1 or P2 licensing for the members." · <https://learn.microsoft.com/entra/identity/users/groups-lifecycle#overview> ("Currently, you can configure only one expiration policy for all Microsoft 365 groups"; P1 or P2 — possess, not necessarily assign) | ✅ faithful (quantifier "exactly one" = docs "only one"; "P1 or P2" preserved) |

**Not asserted / avoided:** no specific default lifetime value (source states only "measured in
days"; docs give presets/custom ≥ 30 days). No Conditional-Access cascade claim (row 5). No claim
about *who* may create groups beyond "self-service" (source only says self-service creation spreads).

## Open questions

1. **Nesting + Conditional Access.** The unit states Conditional Access policies don't reach nested
   members; current Docs (how-to-manage-groups) say nested groups *can* be used for Conditional
   Access scopes. Narration teaches the licensing/shared-resource cascade failure only (both agree).
   Confirm the intended teaching with the unit SME before a re-record adds the CA claim back.
2. **Naming-policy scope.** Narration scopes the naming policy to Microsoft 365 groups per current
   docs; the source phrasing was broader ("every self-service group name"). Confirm acceptable.
3. **`P1` / `P2` anchoring.** Anchors `naming_p1` and `expire_license` depend on ASR transcribing
   "P1"/"P2" as single tokens. If `transcribe` splits them ("p" "one"), the builder should re-anchor
   on the neighboring words or the narration can spell "P One / P Two". Flagged in `anchors.json`.
4. **Voice pace.** `en-US-Vance` has no measured corpus rate; the 251s estimate uses the 2.42 w/s
   corpus mean. Verify runtime against the rendered WAV before timing scenes (audio is the clock).
