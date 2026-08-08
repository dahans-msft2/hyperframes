# Manage the User and Contact Lifecycle

| | |
|---|---|
| Source | `wwl/provision-govern-identities-entra/includes/2-manage-user-contact-lifecycle.md` (Unit 2 of `learn.wwl.provision-govern-identities-entra`) |
| Profile | `unit-video` (content 180–300s, target 240s) |
| Voice | `en-US-Vance:DragonHDLatestNeural` (Azure Dragon HD) |
| Word budget | 435–726 (target 580) @ 2.42 w/s |
| Actual words | **651** |
| Est. runtime | ~4:29 content (651 / 2.42 = 269s) + 0:11 end card — inside the 180–300s window; verify against the rendered WAV (Vance's per-voice rate is unmeasured and may pull this toward the 240s target) |

<!--
Docs-MCP grounding pass (live learn.microsoft.com, 2026-08-07) — drift-prone specifics confirmed:
- 30-day restorable soft-delete window; restore returns properties:
  https://learn.microsoft.com/entra/fundamentals/users-restore
- Restore also returns licenses held at deletion:
  https://learn.microsoft.com/powershell/entra-powershell/recover-deleted-data#restore-users
- On-prem-synced accounts can be recreated by the next sync cycle (Entra ID is not source of authority):
  https://learn.microsoft.com/entra/fundamentals/users-restore#overview
- Bulk create (Entra admin center > Entra ID > Users > Bulk create), CSV:
  https://learn.microsoft.com/entra/identity/users/users-bulk-add
- Mail contact via Exchange admin center > Recipients > Contacts; New-MailContact:
  https://learn.microsoft.com/exchange/recipients/mail-contacts
- Hybrid tools (Connect Sync / Cloud Sync — multiple disconnected forests / Connect Health / IdFix):
  https://learn.microsoft.com/entra/identity/hybrid/sync-tools ,
  https://learn.microsoft.com/entra/identity/hybrid/cloud-sync/what-is-cloud-sync
No stated value in the local source was contradicted by current docs. Minor divergences are logged
in the fidelity ledger.
-->

## Narration

Relecloud's directory never stops growing. Every week brings a new hire, a contractor who only needs email, and someone whose last day means their account has to go. But here's what keeps admins up: what happens the moment you delete a user? Delete the wrong one this morning — is it already gone for good?

That question has a reassuring answer — and it's one of several things worth getting right. In this unit, you'll move a user through its whole lifecycle, choose the admin center built for each task, recover a deletion before it's permanent, and tell a real user from a contact who never signs in.

Start with the user itself. A cloud identity moves through a handful of stages, and you move it along: create it, edit its profile as a role changes, add and remove licenses as the job needs, block sign-in when access must stop now, and delete it when someone leaves for good.

Creating one account at a time is fine for a single new hire. But when a batch arrives together, the Microsoft Entra admin center's *Bulk create* feature takes a spreadsheet of display names, user principal names, and initial passwords, and builds every account in one pass.

Two admin centers show you the same user, and each owns a different part of the job. You spend most of your day in the Microsoft 365 admin center — creating users, assigning licenses, blocking sign-in. You open the Microsoft Entra admin center for the identity object underneath, and to restore a deleted account.

That last one is the surprise. Before I answer, picture it: you delete a user by mistake, and catch it five minutes later. Would you expect that account to be gone for good?

It isn't — not right away. Deleting a user moves it into a suspended state for *thirty days*, fully restorable, before Microsoft Entra ID removes it permanently. [[pause:400ms]] Only after those thirty days pass is restoring no longer possible.

During that window, you find the account in the Microsoft Entra admin center under *Deleted users*, select it, and restore it. Restoring brings back the user's properties and the licenses it held before deletion — you're not rebuilding the profile or reassigning every license.

One caveat matters. If the account was synced from an on-premises directory instead of created in the cloud, deleting it in Microsoft Entra ID doesn't settle it. On-premises stays the master record, so the next sync cycle *can* recreate the account you just deleted — and the fix belongs on-premises, not in a cloud portal.

Not everyone in the address book signs in. A vendor's contact might only need to be emailed — that's a mail contact, not a user: a recipient with an external email address that never authenticates. You create one in the Exchange admin center, under *Recipients*, then *Contacts*. The deciding question is simple: does this person sign in? If yes, a user or a guest; if not, a contact.

Finally, not every account started in the cloud — some sync from an on-premises Active Directory. Connect Sync is the classic sync server; Cloud Sync is a lighter, agent-based alternative that supports multiple disconnected forests; Connect Health watches the sync for failures; and IdFix scans on-premises directories for attribute errors before a clean first sync. You won't configure these — recognizing what each does is enough.

So, the account you deleted by mistake this morning? You've got thirty days to bring it back — properties and licenses intact. You can move a user through its lifecycle, match each task to the right admin center, recover a deletion in time, and tell a user from a contact.

Editing accounts one at a time works for a handful of people — but when your overseas office needs dozens before it opens, you'll want to provision at scale without over-granting your own permissions. That's the next unit. To go deeper, follow the *Learn more* links in this module.

## Chrome copy (on-screen text for the scaffolded scenes)

Text only — **labels, not the spoken sentence** (Redundancy). The narration above carries these scenes.

**`02-title` — title-hero**
- kicker: `Provision and govern identities in Microsoft Entra`
- title (2 lines): `Manage the user and` / `contact lifecycle`
- subtitle: `Govern an identity across its whole life`

**`03-objectives` — objectives (3 one-line chips)**
1. `Move a user through its full lifecycle`
2. `Recover a deletion within 30 days`
3. `Tell a user from a mail contact`

**`90-recap` — recap (answers the opening hook)**
- kicker: `Recap`
- `30 days to restore a deleted user — properties + licenses intact`
- `Match each task to the right admin center`
- `Signs in → user or guest · Email only → contact`

**`91-cta` — CTA**
- title: `Next: provision accounts at scale`
- subtitle: `…without over-granting your own permissions`
- link: `Learn more — Provision and govern identities in Microsoft Entra`

## Beat plan

Opening + closing chrome are scaffolded; body beats B1–B9 fill the `body_slot`. `Cue lands on` = the
verbatim phrase in `anchors.json` the visual is anchored to (resolved by `word_anchors.py`).

| # | Beat | Narration slice (first words) | On screen (idea · block · ground) | Focal object / value | Cue lands on |
|---|---|---|---|---|---|
| — | `01-bumper` | *(no VO — 3s sting)* | Learn brand open · `bumper` · hero-swoosh | Microsoft Learn mark | — |
| — | `02-title` | "Relecloud's directory never stops growing…" | Title + curiosity-gap kicker · `title-hero` · hero-swoosh | The delete-by-mistake hook | — |
| — | `03-objectives` | "That question has a reassuring answer…" | 3 objective chips as **stakes** · objectives · content-wash | Lifecycle · admin center · restore · user-vs-contact | — |
| B1 | Lifecycle spine | "Start with the user itself. A cloud identity moves through a handful of stages…" | Five ordered stages: create → edit → license → block → delete · `list-steps` (5-row variant) · content-wash | The five lifecycle stages | `moves through a handful of stages` |
| B2 | Create in bulk | "Creating one account at a time is fine… the *Bulk create* feature takes a spreadsheet…" | Entra admin center Bulk-create upload · `media-screenshot` **capture: Entra ID > Users > Bulk create** (else `list-specs` of CSV columns) · content-wash | CSV **Bulk create** | `Bulk create feature` |
| B3 | Right surface for the task | "Two admin centers show you the same user, and each owns a different part of the job…" | M365 admin center vs Entra admin center — one user, split ownership · `list-select` (two surfaces, lift the task's owner) · content-wash | Match task → admin center | `each owns a different part of the job` |
| B4 | Predict | "That last one is the surprise. Before I answer, picture it…" | Prediction prompt, answer withheld · `callout-note` (label `PREDICT`) · content-wash | "gone for good?" | `expect that account to be gone` |
| B5 | Soft-delete reveal | "It isn't — not right away… a suspended state for *thirty days*, fully restorable…" | Delete → 30-day restorable window → permanent · `media-screenshot` **reuse source asset `media/2-soft-delete-timeline.png`** (else custom timeline) · content-wash | **30 days**, restorable | `suspended state for thirty days` |
| B6 | Restore returns everything | "During that window, you find the account… under *Deleted users*… Restoring brings back the user's properties and the licenses…" | Deleted users → select → restore; properties + licenses return · `console-status` (restore row flips pending→passed) **capture: Entra ID > Users > Deleted users** · content-wash | Properties **and** licenses restored | `brings back the user's properties and the licenses` |
| B7 | On-prem caveat | "One caveat matters. If the account was synced from an on-premises directory…" | Cloud delete vs on-prem master; next sync *can* recreate · `callout-note` (label `CAVEAT`) · content-wash | Synced account **can** return; fix on-prem | `the next sync cycle can recreate` |
| B8 | User or contact? | "Not everyone in the address book signs in… that's a mail contact, not a user… does this person sign in?" | Mail contact object (external email, no sign-in) + the sign-in decision · `diagram-flow` ("Does this person sign in?" → user/guest vs contact) · content-wash | **Mail contact** · Exchange admin center → Recipients > Contacts | `that's a mail contact, not a user` → `does this person sign in` |
| B9 | Where accounts come from | "Finally, not every account started in the cloud… Connect Sync… Cloud Sync… Connect Health… IdFix…" | Four hybrid-sync tools and their one-line role · `list-specs` (tool → what it does) · content-wash | Connect Sync · Cloud Sync · Connect Health · IdFix | `Connect Sync is the classic sync server` |
| — | `90-recap` | "So, the account you deleted by mistake this morning? You've got thirty days…" | Recap that pays off the hook · recap · hero-swoosh | 30-day payoff + the 4 objectives | — |
| — | `91-cta` | "Editing accounts one at a time works for a handful of people…" | Next-unit CTA + Learn more · cta · hero-swoosh | Provision at scale, least privilege | — |

Notes for the designer/author:
- **B4→B5 is a predict-before-reveal pair.** Hold the answer visually on B4; the 30-day timeline (B5) is the reveal. Don't show the timeline while the question is still open.
- **B5 asset reuse:** the module ships `media/2-soft-delete-timeline.png` (delete → 30-day window → permanent). Reuse it rather than inventing a timeline.
- **B2 / B6 capture opportunities:** real Entra admin center screens (Bulk create; Deleted users) teach better than mocks if an author screenshot is available.
- **B1 is 5 stages**, one past `list-steps`' 3–4 comfort zone — if it crowds, split "block sign-in vs delete" into its own callout, or author the stage strip by hand from the foundation.

## Source-fidelity ledger

Every substantive claim → source location and the live Docs URL that confirms it, checked for
**R**eferent / **Q**uantifier / **M**odality drift.

| # | Claim in narration | Source (unit 2) | Docs verification | R/Q/M check | Verbatim? |
|---|---|---|---|---|---|
| 1 | Lifecycle = create, edit profile, add/remove licenses, block sign-in, delete | "Manage a user across its full lifecycle" list | — (matches source) | M: "block sign-in when access **must** stop now" ≈ source "the moment access needs to stop immediately" — same urgency, not overstated | Paraphrase ✅ |
| 2 | **Bulk create** takes a CSV of display names, UPNs, initial passwords in the Entra admin center | "Bulk create feature… spreadsheet of display names, user principal names, and initial passwords" | [users-bulk-add](https://learn.microsoft.com/entra/identity/users/users-bulk-add) | Q: narration lists what you upload, **not** "the only required columns" — so no floor/ceiling error. Docs add *Block sign in* as a 4th required column (see divergences) | ✅ |
| 3 | Two admin centers; M365 for everyday (create/license/block), Entra for the identity object + restore | "Choose the surface that owns each task" | [users-bulk-add](https://learn.microsoft.com/entra/identity/users/users-bulk-add), [users-restore](https://learn.microsoft.com/entra/fundamentals/users-restore) | M: "you spend **most** of your day" is hedged — safe. Source-framed split (both centers can create users) | Source framing ✅ |
| 4 | Guiding question: is a deleted user gone for good if you catch it in 5 minutes? | "Guiding question" callout | — (pedagogical prompt) | — | ✅ |
| 5 | Delete → suspended **30 days**, fully restorable → then permanent | "suspended state for 30 days, fully restorable, before Microsoft Entra ID deletes it permanently… Only after the 30 days pass… restoring… no longer possible" | [users-restore](https://learn.microsoft.com/entra/fundamentals/users-restore) — "remains in a suspended state for 30 days, during which it can be fully restored. Once this 30-day period ends, the account is permanently deleted" | Q: "**Only** after those thirty days pass" preserved (ceiling intact). M: "fully restorable" preserved | ✅ |
| 6 | Under *Deleted users*, select and restore; restore returns **properties and the licenses** held at deletion | "under **Deleted users**… restore it. Restoring brings back the user's properties and the licenses it held before deletion" | Properties: [users-restore](https://learn.microsoft.com/entra/fundamentals/users-restore) "restored, along with all its properties." Licenses: [recover-deleted-data](https://learn.microsoft.com/powershell/entra-powershell/recover-deleted-data#restore-users) "any licenses assigned at the time of deletion are also restored" | R: "the user's properties and the licenses **it** held" → *it* = the restored user, unambiguous | ✅ |
| 7 | A synced (on-prem-mastered) account **can** be recreated by the next sync cycle; fix belongs on-prem | "the next synchronization cycle **can** recreate the account you just deleted… fix… belongs on-premises" | [users-restore#overview](https://learn.microsoft.com/entra/fundamentals/users-restore#overview) — "the sync engine **may** restore the user during the next synchronization cycle" | M: "**can** recreate" preserved — a possibility, not "will" | ✅ |
| 8 | Mail contact = external email, in the address book, never signs in; created in Exchange admin center → *Recipients > Contacts* | "mail contact, not a user: a recipient that carries an external email address… never authenticates… Exchange admin center… **Recipients > Contacts**" | [mail-contacts](https://learn.microsoft.com/exchange/recipients/mail-contacts) — EAC "Recipients > Contacts"; external email address | R: "that never authenticates" → *that* = the mail-contact recipient | ✅ (Graph claim omitted — see below) |
| 9 | Decision: signs in → user/guest; email only → contact | "does this person sign in? If yes… user or a guest. If they only need to be reachable… a contact" | — (matches source) | Q/M: both branches preserved | ✅ |
| 10 | Connect Sync = classic server; Cloud Sync = light, agent-based, multiple disconnected forests; Connect Health = monitors sync failures; IdFix = scans on-prem for attribute errors before first sync | Hybrid-tools table + "This module doesn't deploy or configure any of these" | [sync-tools](https://learn.microsoft.com/entra/identity/hybrid/sync-tools), [cloud-sync](https://learn.microsoft.com/entra/identity/hybrid/cloud-sync/what-is-cloud-sync) "disconnected forest synchronization", [Connect Health](https://learn.microsoft.com/entra/identity/hybrid/connect/whatis-azure-ad-connect#what-is-microsoft-entra-connect-health) | M: "You **won't** configure these — recognizing what each does is enough" matches source scope exactly | ✅ |
| 11 | CTA: next, provision at scale without over-granting your own permissions | Closing line: "provision that many accounts at scale, without granting yourself more permission than the job actually needs" | — (next-unit setup) | M: "without over-granting **your own** permissions" ≈ "granting yourself more permission" | ✅ |

### Divergences (current docs vs local source)

- **Bulk-create required columns.** Current docs list **four** required CSV columns — Name, User principal name, Initial password, **Block sign in (Yes/No)**. The local source names three attributes you upload and omits *Block sign in*. Handled by **not** claiming "the only required columns," so the narration is true under both. No value contradicted.
- **Admin-center path depth.** Current Entra admin center paths are `Entra ID > Users > Deleted users` and `Entra ID > Users > Bulk create`; the local source uses the shorter `Users > Deleted users`. Narration says "under *Deleted users*" and "the Entra admin center's *Bulk create* feature" — surface-level, so it stays correct as the portal IA shifts.

### Unverifiable / omitted

- The local source states "**Microsoft Graph doesn't manage mail contacts at all**." I could not confirm this specific claim via the Docs MCP, so I **omitted it from the narration** rather than assert it. It is a next-unit aside, not core to this unit's objective, so cutting it also serves Coherence.
- `New-MailContact` (Exchange Online PowerShell) is real and confirmed ([New-MailContact](https://learn.microsoft.com/powershell/module/exchangepowershell/new-mailcontact)), but I left the cmdlet out of the spoken line to keep the beat tight — the surface (Exchange admin center → Recipients > Contacts) carries the teaching. Optional to restore if the designer wants a code/callout beat.

## Cue anchors

Written alongside the script in [anchors.json](anchors.json) — a map of cue name → the exact spoken
phrase each visual lands on. Every phrase is a unique contiguous token run, so `word_anchors.py`
resolves each without a `#n` disambiguator. The builder turns these into real audio times against
`transcript.json`; they are not offsets to be estimated.

## Open questions

- **B1 as five stages** exceeds `list-steps`' 3–4 comfort zone. Ship as a 5-row stage strip, or split "block sign-in vs delete" into a separate callout? (Author's call at layout.)
- **B2 / B6:** are author screenshots of the real Entra admin center (Bulk create; Deleted users) available? If yes, prefer them over invented mocks; if not, `list-specs` / `console-status` mocks are the fallbacks cued above.
- **Voice pace:** `en-US-Vance` has no measured per-voice rate in the corpus. 651 words estimates ~4:29 at the 2.42 w/s mean; confirm against the rendered WAV and, if it lands long, trim B8/B9 before reaching for `--rate`.

---

**Word count:** 651 words — inside the 435–726 budget (above the 580 target; ~269s content sits inside the 180–300s window, so no cut is required to stay in bounds).
