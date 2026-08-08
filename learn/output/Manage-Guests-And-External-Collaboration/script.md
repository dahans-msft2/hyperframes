# Manage Guests and External Collaboration

<!--
Source-grounding pass (Docs MCP, live learn.microsoft.com, 2026-08-07):
- Guest permission levels ......... https://learn.microsoft.com/entra/identity/users/users-restrict-guest-permissions
- External collaboration settings . https://learn.microsoft.com/entra/external-id/external-collaboration-settings-configure
- Default user permissions ........ https://learn.microsoft.com/entra/fundamentals/users-default-permissions
- Guest Inviter role .............. https://learn.microsoft.com/entra/identity/role-based-access-control/permissions-reference#guest-inviter
- Guests in M365 admin center ..... https://learn.microsoft.com/microsoft-365/admin/add-users/about-guest-users
- Cross-tenant / B2B governance ... https://learn.microsoft.com/entra/architecture/5-secure-access-b2b
- Multitenant Organization ........ https://learn.microsoft.com/microsoft-365/enterprise/plan-multi-tenant-org-overview
-->

| | |
|---|---|
| Source | `wwl/provision-govern-identities-entra/includes/5-manage-guests-external-collaboration.md` (Unit 5) |
| Profile | `unit-video` (~240s content target; 435–726 words) |
| Voice | `en-US-Vance:DragonHDLatestNeural` |
| Word budget | 435–726 (target 580) |
| Actual words | **626** |
| Est. runtime | ~4:19 content @ 2.42 w/s + 0:11 end card |

## Narration

Managing guests and external collaboration in Microsoft Entra ID. Let outside partners in — without handing them the run of your directory.

In this unit, you'll map the levers of external access, invite a partner with the least privilege that does the job, and spot when one-by-one invitations stop scaling. Leave a lever loose, and a guest you invited for one project can see far more than they should.

Start with the scenario. Relecloud's coordinators need Woodgrove Bank's fraud analysts inside one investigation — and *only* that. So here's the real question: the moment you invite one of them as a guest, how much of your directory can they see by default? [[pause:500ms]] Take a guess before we answer it.

Here's the catch: guest access isn't one switch. It's several levers, each answering a different question — how a guest gets in, how much they see, which domains you'll invite, how far you trust a partner tenant. None of them replaces another; together they define what "let this analyst in" really means.

Back to what a guest can see. There are three levels. Same access as members is the most inclusive. The default — limited access — stops a guest from browsing your users and groups. The *most restrictive* level narrows them to their own profile: no other users, no groups, not even their own memberships. For analysts here for one project, that default fits.

So who pulls these levers? Coordinators need to invite analysts themselves, without a ticket to IT. The obvious move is User Administrator — it can invite. But it can also reset passwords, edit profiles, and manage licenses across the tenant. That's far more than "invite one analyst" needs.

The least-privileged path takes *two* pieces, not one. First, assign coordinators the Guest Inviter role — its only power is sending invitations. Second, set the tenant's invite setting to "only users assigned to specific admin roles can invite guest users." Skip that second piece, and everyone can still invite — so the role changes nothing.

With that set, inviting is simple. A coordinator sends an invitation to an external email address. The analyst redeems it by signing in with their own account — and a guest object appears in your directory, no Relecloud identity to create or maintain.

Here's a point that trips people up. That one guest object shows up in two places: beside your members in the Microsoft Entra admin center, and in the Guest users list in the Microsoft 365 admin center. Same record, two surfaces — not a *copy*, not a second account to reconcile.

Two more levers tighten the outer edges. Allow and deny domain lists act before any invitation is sent — permit a partner's domain, block consumer email outright. Cross-tenant access settings go a layer deeper, governing trust with one specific partner tenant: which multifactor claims you trust from them, and which of your apps their users can reach.

One last judgment call. Inviting analysts one project at a time works for a fixed group. But if this becomes a standing partnership — hundreds of people, changing constantly — those individual invitations become a maintenance burden. That's when a Multitenant Organization fits: it synchronizes users as members, not guests you invite one by one. Spotting that shift is the skill; configuring it is a separate job.

So that's the shape of it. External collaboration is a set of levers, not a switch. Permission levels decide what a guest sees — limited by default, tighter when you need it. Guest Inviter plus the right tenant setting delegates invitations without over-granting. And when guests stop scaling, a Multitenant Organization is your next move.

Want to go deeper? Open the Microsoft Learn docs on configuring external collaboration settings, and on how a Multitenant Organization differs from one-off invitations. Then try it in your own tenant.

## Beat plan

Chrome scenes (`01`–`03`, `90`–`91`) are scaffolded; narration above supplies their text (filled below).
Body scenes `04`–`12` go in the `body_slot`. On-screen carries **labels, not the spoken sentence** (Redundancy).

| # | Scene | Narration slice | On screen (label, not transcript) | Shape cue (block · ground) | Focal object | Lands on phrase |
|---|---|---|---|---|---|---|
| — | `01-bumper` | *(no VO)* | Microsoft Learn brand sting | `bumper` · hero-swoosh | Learn mark | — |
| — | `02-title` | "Managing guests and external collaboration…" | Title (2 lines) + subtitle | `title-hero` · hero-swoosh | Title line | "external collaboration in Microsoft Entra ID" |
| — | `03-objectives` | "…map the levers… least privilege… stop scaling." | 3 objective chips (framed as stakes) | *(scaffolded objectives)* | Objective chips | "map the levers of external access" |
| B1 | `04-scenario` | "…how much of your directory can they see by default? Take a guess…" | Relecloud → Woodgrove; **"What can a guest see by default?"** | `callout-note` · **dark-field** *(the one dark scene — the hook)* | The question term | "how much of your directory can they see by default"; predict → "Take a guess before we answer it" |
| B2 | `05-lever-map` | "…several levers, each answering a different question…" | 5 lever labels + one-line "controls" each (Invitation flow · Permission levels · Domain lists · Cross-tenant access · Self-service sign-up) | `list-specs` · content-wash | The 5-row stack | reveal → "several levers" |
| B3 | `06-permission-levels` | "There are three levels… that default fits." | 3 level chips: Same as members / **Limited access (default)** / Most restrictive | `list-select` · content-wash *(selectedIndex = Limited)* | Lifted "Limited access (default)" row | reveal → "There are three levels"; lift → "that default fits" |
| B4 | `07-role-trap` | "The obvious move is User Administrator… far more than 'invite one analyst' needs." | Decision: who can invite? → **User Administrator (too broad)** vs Guest Inviter | `diagram-flow` · content-wash | User Administrator node flagged | show broad role → "User Administrator"; flag → "manage licenses across the tenant" |
| B5 | `08-delegate-two-pieces` | "…two pieces, not one. First… Second… so the role changes nothing." | 2 steps: **1** Assign Guest Inviter · **2** Invite setting = "Only users assigned to specific admin roles can invite guest users" | `list-steps` · content-wash | Step **2** badge | step 1 → "assign coordinators the Guest Inviter role"; step 2 → "set the tenant's invite setting" |
| B6 | `09-invite-redeem` | "A coordinator sends an invitation… redeems it… a guest object appears…" | Status: Invitation sent → Pending → **Redeemed** (row flips) | `console-status` · content-wash *(flipIndex = redemption)* | The flipping row | flip → "redeems it by signing in"; result → "a guest object appears" |
| B7 | `10-one-object-two-surfaces` | "…shows up in two places… Same record, two surfaces…" | KEY POINT: **One guest object · two surfaces** (Entra admin center · Microsoft 365 Guest users). `capture:` same guest in both admin centers would beat the mock | `callout-note` · content-wash | Term "One guest object" | reveal → "shows up in two places"; land → "Same record, two surfaces" |
| B8 | `11-restriction-levers` | "Allow and deny domain lists… Cross-tenant access settings go a layer deeper…" | Concentric: **Domain lists** (outer) → Cross-tenant access → **Partner-tenant trust** (core: MFA claims · apps) | `diagram-layers` · content-wash | The core (partner-tenant trust) | outer → "Allow and deny domain lists"; settle to core → "go a layer deeper" |
| B9 | `12-when-guests-stop-scaling` | "…a Multitenant Organization fits… Spotting that shift is the skill…" | Guest-by-guest (fixed group) vs **Multitenant Organization** (standing partnership) | `list-select` · content-wash *(selectedIndex = MTO)* | Lifted "Multitenant Organization" | lift → "a Multitenant Organization fits" |
| — | `90-recap` | "…limited by default… Multitenant Organization is your next move." | 4 recap chips (answers the opening hook) | *(scaffolded recap)* | Recap chips | answer → "limited by default" |
| — | `91-cta` | "Open the Microsoft Learn docs…" | 2 "Learn more" links + "Try it in your tenant" | *(scaffolded cta)* | Primary link | "configuring external collaboration settings" |

## Chrome text (fill for scaffolded scenes)

**`02-title`**
- kicker: `Provision and govern identities in Microsoft Entra`
- title (2 lines): `Manage Guests &` / `External Collaboration`
- subtitle: `Let partners in — without opening up the directory.`

**`03-objectives`** (framed as stakes, ~3 one-liners)
1. `Map the levers that control external access`
2. `Delegate invitations with least privilege`
3. `Know when to move from guests to a Multitenant Organization`

**`90-recap`** (answers the objectives)
1. `Levers, not a single switch`
2. `Guests see limited access by default`
3. `Guest Inviter + the tenant invite setting`
4. `A Multitenant Organization when guests stop scaling`

**`91-cta`**
- primary: `Configure external collaboration settings` → `learn.microsoft.com/entra/external-id/external-collaboration-settings-configure`
- secondary: `Multitenant Organization overview` → `learn.microsoft.com/entra/identity/multi-tenant-organizations/overview`
- action: `Try it in your own tenant`

## Cue anchors

Written to `anchors.json` (cue name → exact spoken phrase). The builder resolves them to real
audio times with `python ../../tools/word_anchors.py transcript.json --spec anchors.json`. Every
phrase is a verbatim, unique run in the narration above (checked against the "far more than"
collision in the objectives beat — the B4 cue uses `manage licenses across the tenant` instead).

## Source-fidelity ledger

Claim checked (not just quoted): **referent** · **quantifier** · **modality**. Local source =
Unit 5 include; Docs = live learn.microsoft.com (verified 2026-08-07).

| Claim in narration | Source in Unit 5 | Docs verification (URL) | Verified? |
|---|---|---|---|
| External collaboration is several distinct levers, none replacing another (invitation flow, permission levels, domain lists, cross-tenant access, self-service sign-up) | §"Map the external-collaboration surface" + lever table | external-collaboration-settings-configure; architecture/5-secure-access-b2b#control-collaboration | ✅ |
| Three guest permission levels: same-as-members, **limited (default)**, most restrictive | §"Map" | users-restrict-guest-permissions#overview (Same as member / Limited (default) / Restricted); external-collaboration-settings-configure | ✅ quantifier "three" + default = limited preserved |
| Most restrictive = own profile only; no other users, no groups, **not even their own memberships** | §"Map" ("most restrictive… only their own profile") | users-restrict-guest-permissions ("can't see membership of any groups… view only their own user profile… restricts seeing membership of groups they're in") | ✅ |
| Limited (default) "stops a guest from browsing your users and groups" | §"Map" ("keeps a guest from enumerating other users, groups, and properties") | external-collaboration-settings-configure ("blocks… enumerating users, groups… **Guests can see membership of all non-hidden groups**") | ⚠️ FLAG — "limited" blocks *enumeration* but still shows non-hidden group membership. Narration puts group-membership hiding on the **most-restrictive** level (docs-correct) and keeps "browsing users and groups" for limited. Faithful; nuance noted. |
| B2B flow: invite external email → guest redeems with own account → guest object appears, no managed identity | §"Map" / §"One guest object…" | add-users-administrator (invite external user; UPN `#EXT#`); architecture/5-secure-access-b2b#control-external-user-access (redemption) | ✅ |
| Guest Inviter role = sending invitations only | §"Delegate…" ("grants exactly one capability: sending B2B invitations") | permissions-reference#guest-inviter ("manage B2B guest user invitations… **does not include any other permissions**") | ⚠️ FLAG — role also holds directory *read* actions; "only power is sending invitations" is a faithful plain-language simplification of the docs' own "no other permissions" statement. |
| User Administrator can also reset passwords, edit profiles, manage licenses — far more than inviting | §"Delegate…" (verbatim) | permissions-reference#user-administrator | ✅ modality "can" preserved |
| Tenant setting label "Only users assigned to specific admin roles can invite guest users"; Guest Inviter works when it's selected | §"Delegate…" (verbatim label) | external-collaboration-settings-configure#configure-settings-in-the-portal; #assign-the-guest-inviter-role-to-a-user | ✅ verbatim |
| Without the restrictive setting, "everyone can still invite" and the role adds nothing | §"Delegate…" ("the tenant setting might still allow **every member**…") | external-collaboration-settings-configure ("By default, all users… can invite") | ⚠️ FLAG — source says "might still allow every member"; narration says "everyone can still invite." Accurate to the *default* (all users incl. guests), slight strengthening of the modal — noted. |
| One guest object surfaces in the Entra admin center **and** the Guest users list in the Microsoft 365 admin center — same record | §"One guest object, two surfaces" (calls it the "Guests" list) | about-guest-users ("**Guest users** list… Users > Guest users"; "the user also appears on the **Guest users** page") | ⚠️ FLAG — source label "Guests list" → current portal label is **"Guest users"**. Followed docs. |
| Allow/deny domain lists control invitations at the domain level, before any invite | §"Map" | external-collaboration-settings-configure (Collaboration restrictions: allow any / deny specified / allow only specified) | ✅ |
| Cross-tenant access settings = trust with one specific partner tenant (which MFA claims you trust, which apps their users reach) | §"Map" (source pairs inbound MFA trust with **outbound** app access) | architecture/5-secure-access-b2b#control-collaboration ("control application access by guests… (inbound)… (outbound)"); cross-tenant access supports trusting partner MFA | ⚠️ FLAG — reframed both as **inbound** trust (MFA claims *from* them; *your* apps *their* users reach) for coherence; docs support inbound guest-app access. Source's app example was outbound — deliberate simplification to avoid a referent flip. |
| Self-service sign-up = external users request app access on their own, no invitation | §"Map" | external-collaboration-settings-configure#to-configure-guest-self-service-sign-up | ✅ |
| MTO synchronizes users **as members, not guests**; recognizing the shift is the skill, configuring MTO is separate | §"Awareness: when guest-by-guest stops scaling" | plan-multi-tenant-org-overview ("user type of **member** rather than guest"); multi-tenant-organization-microsoft-365#b2b-member-users | ✅ modality preserved (existing guests don't auto-convert — not claimed) |

## Open questions

- **Voice mismatch in BRIEF.md.** BRIEF still lists `en-US-Ava`; locked input is
  `en-US-Vance:DragonHDLatestNeural`. Confirm Vance is provisioned and audition the hardest
  sentence — B8: "…which multifactor claims you trust from them, and which of your apps their
  users can reach." — before any full render.
- **B7 capture opportunity.** If an author can supply matched screenshots of the same guest in
  the Entra admin center Users list *and* the Microsoft 365 admin center Guest users list, a
  `media-screenshot` beat would teach the "one record, two surfaces" point better than the
  invented `callout-note`. Designer's call.
- **"Microsoft 365" read.** Kept as the brand token (Dragon HD reads "three sixty-five"). If the
  audition mangles it, spell "Microsoft three sixty-five" in `narration.txt` only.
