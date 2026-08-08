# Bulk Identity Management with Graph PowerShell

<!--
Docs-MCP grounding pass (learn.microsoft.com, 2026-08-07) — drift-prone specifics verified:
- New-MgUser · module Microsoft.Graph.Users · least-privileged delegated scope User.ReadWrite.All
  https://learn.microsoft.com/powershell/module/microsoft.graph.users/new-mguser
- Connect-MgGraph -Scopes "User.ReadWrite.All" (documented bulk-create connect flow)
  https://learn.microsoft.com/microsoft-365/enterprise/create-user-accounts-with-microsoft-365-powershell
- Get-MgUser (read) · User.Read.All  https://learn.microsoft.com/powershell/module/microsoft.graph.users/get-mguser
- New-MgGroupMemberByRef · module Microsoft.Graph.Groups · -OdataId into directoryObjects
  https://learn.microsoft.com/powershell/module/microsoft.graph.groups/new-mggroupmemberbyref
- New-MailContact · Exchange Online PowerShell (module "Exchange PowerShell"), NOT Graph
  https://learn.microsoft.com/exchange/recipients-in-exchange-online/manage-mail-contacts
No cmdlet/scope-name divergence between the source unit and current docs. One immaterial casing
difference only (docs example writes -MailNickName; source writes -MailNickname — PowerShell
parameter names are case-insensitive, so both bind identically). Prefer source spelling on screen.
-->

| | |
|---|---|
| Source | `wwl/provision-govern-identities-entra/includes/3-bulk-identity-management-graph.md` (Unit 3) |
| Module | Provision and govern identities in Microsoft Entra (`learn.wwl.provision-govern-identities-entra`) |
| Profile | `unit-video` |
| Voice | `en-US-Vance:DragonHDLatestNeural` |
| Word budget | 435–726 (target 580) |
| Actual words | 595 |
| Est. runtime | 4:06 content (595 ÷ 2.42 w/s ≈ 246s) + 0:11 AI end card |

## Narration

Relecloud's overseas office opens Monday, and the stack of new-hire names on your desk keeps growing. Thirty accounts, clicked in one at a time in the portal, won't be ready before the doors open. So here's the question this unit answers: how do you create every one of those accounts in a single pass, and run it again the next time a batch of hires lands?

Microsoft Graph PowerShell is the way, and by the end you'll be able to do three things with it. Connect with the right permission scope. Pull your new hires from a spreadsheet. And let one command create the whole list.

The whole thing is really just three moves, and they never change. First, you connect and request a scope. Next, you import a CSV of your users. Then you loop over that list and create each account. Connect, import, loop.

Every Graph PowerShell session starts with Connect-MgGraph, and the scope you request right there decides what the rest of the script is allowed to do. To create accounts, you ask for exactly one scope: *User.ReadWrite.All*. Ask for less, and the create step simply fails.

Then Import-Csv reads your spreadsheet into a collection of objects, one for every new hire. Each row carries the same fields you'd type into the portal's bulk-create sheet: a display name, a user principal name, a mail nickname, and a temporary password. Same columns, just driven from a file.

Now the loop does the work. A foreach walks that list and hands each row to New-MgUser, one at a time. That single cmdlet creates the account, switches it on, and forces a password reset at first sign-in. Thirty rows in, thirty accounts out.

Here's why that beats clicking through a browser. A script is *repeatable*. Run it again next quarter, when the next wave of hires arrives, and you don't reopen a single blade. You point it at a new file and go.

Now, one small detail is doing more than it looks. Why *User.ReadWrite.All*, and not the broader Directory.ReadWrite.All? Both of them would work. But the broad one grants far more than user management alone, and that's the decision actually being tested. You match the scope to the task, not to whatever also happens to work.

And that same rule scales to every bulk job. Reading users for an audit? That's User.Read.All, read-only, no changes. Adding people to a group? GroupMember.ReadWrite.All. Building an administrative unit? AdministrativeUnit.ReadWrite.All. None of them stand in for each other. Each scope tells Entra ID exactly what your script may touch.

Creating accounts isn't the only bulk task, either. A department change, a manager swap: Update-MgUser runs the very same CSV-and-loop pattern, under that same *User.ReadWrite.All* scope. And when an account has to go, Remove-MgUser follows the identical shape. Learn the pattern once, reuse it everywhere.

One trap, though, before you reach for this out of habit. Microsoft Graph doesn't manage mail contacts at all. Scripting a vendor contact with New-MgUser just won't work, because that contact was never a user object. That job belongs to New-MailContact, over in Exchange Online PowerShell, not Graph.

So the overseas office is covered. You connected with a scope, imported a CSV, and let New-MgUser build the whole roster in one pass. Then you reused that same loop to update and to delete, matching every scope to its task along the way. One pattern for the entire directory.

Ready to run it yourself? The next exercise takes you through bulk-provisioning with Graph PowerShell, hands-on. For the parameters, open the New-MgUser reference on Microsoft Learn.

## Chrome copy (fill the scaffolded scenes)

**`opening.bumper`** — kicker sub-line: `Provision and govern identities in Microsoft Entra`

**`opening.title`** — title (2 lines) + subtitle:
- Title: `Bulk Identity Management` / `with Graph PowerShell`
- Subtitle: `Provision hundreds of accounts in a single pass`

**`opening.objectives`** — three one-line chips (labels, not the spoken sentences):
1. `Connect with the least-privileged scope`
2. `Import your users from a CSV`
3. `Create every account with one cmdlet`

**`closing.recap`** — three recap chips (answers the opening hook):
1. `Connect · Import · Loop — one repeatable pattern`
2. `Match the scope to the task, not the broadest`
3. `Create, update, delete — same CSV-and-loop shape`

**`closing.cta`** — call to action:
- Primary: `Try it: Exercise — Bulk provision with Graph PowerShell`
- Learn more: `New-MgUser reference · learn.microsoft.com`

## Beat plan

Chrome scenes `01-bumper`, `02-title`, `03-objectives`, `90-recap`, `91-cta` are scaffolded; body
scenes below are authored into the `body_slot`. Kit blocks are candidates — the designer owns final
selection. `Cue → phrase` names match `anchors.json`; the builder resolves them to real word times.

| # | Scene id | Narration slice | On screen (focal object) | Kit block · ground | Cue → spoken phrase | Motion note |
|---|---|---|---|---|---|---|
| — | `01-bumper` | *(silent)* | Microsoft Learn mark + kicker | `bumper` · hero-swoosh | — | Scaffolded open, no VO. |
| — | `02-title` | "…how do you create every one of those accounts in a single pass…" | Title lines + subtitle; the **hook question** is the beat | `title-hero` · hero-swoosh | `hook_question` → "how do you create every one of those accounts" | Waterfall title; hold on the question, don't answer it yet. |
| — | `03-objectives` | "Connect with the right permission scope. Pull your new hires… let one command create the whole list." | 3 objective chips (short labels) | `objectives` (scaffolded) · content-wash | `objectives_scope` → "the right permission scope" | Chips stagger in as each is named (temporal contiguity). |
| B1 | `04-spine` | "…just three moves… First, you connect… Next, you import a CSV… Then you loop… Connect, import, loop." | 3 numbered steps: **Connect → Import → Loop** | `list-steps` · content-wash | `overview_steps` → "Connect, import, loop" | Steps reveal top-to-bottom as each is spoken; final "Connect, import, loop" lands all three lit. |
| B2 | `05-connect` | "Every Graph PowerShell session starts with **Connect-MgGraph**… you ask for exactly one scope: **User.ReadWrite.All**." | Code: `Connect-MgGraph -Scopes "User.ReadWrite.All"` — active line = the Connect line; **`-Scopes` value** is the focus | `code-window` · content-wash | `connect_cmd` → "starts with Connect-MgGraph"; `connect_scope` → "exactly one scope" | Line reveal; highlight lifts to the scope string on `connect_scope`. |
| B3 | `06-csv` | "**Import-Csv** reads your spreadsheet… a display name, a user principal name, a mail nickname, and a temporary password. Same columns…" | Spec rows = CSV columns: `DisplayName`, `UserPrincipalName`, `MailNickname`, `TempPassword` | `list-specs` · content-wash | `import_csv` → "Import-Csv reads your spreadsheet"; `csv_columns` → "a display name, a user principal name" | Rows stagger as the four fields are named; label ≠ spoken sentence. |
| B4 | `07-loop` | "A **foreach** walks that list and hands each row to **New-MgUser**… creates the account, switches it on, and forces a password reset… Thirty rows in, thirty accounts out." | Code: the `foreach { New-MgUser … -AccountEnabled -PasswordProfile … }` loop — active line = `New-MgUser` | `code-window` · content-wash | `loop_foreach` → "A foreach walks that list"; `create_newmguser` → "hands each row to New-MgUser" | Reveal loop body; pulse the `New-MgUser` line on `create_newmguser` (this is the payoff of the spine). |
| B5 | `08-repeatable` | "A script is *repeatable*. Run it again next quarter… you don't reopen a single blade." | KEY POINT card — term **Repeatable**, body: rerun on next batch, no portal blades | `callout-note` · content-wash | `repeatable` → "A script is repeatable" | Panel scale-in with accent-tab wipe; single emphasized takeaway. |
| B6 | `09-scope-match` | "Why *User.ReadWrite.All*, and not the broader **Directory.ReadWrite.All**?… match the scope to the task, not to whatever also happens to work." | Two peer scope rows; **`User.ReadWrite.All` lifts** with accent tab, `Directory.ReadWrite.All` recedes (too broad) | `list-select` (selectedIndex = the matched scope) · content-wash | `match_scope_question` → "the broader Directory.ReadWrite.All"; `least_privilege` → "match the scope to the task" | The chosen row lifts exactly on `least_privilege`; this is the decision being tested. |
| B7 | `10-scope-pattern` | "Reading users… User.Read.All… Adding people to a group? GroupMember.ReadWrite.All. Building an administrative unit? AdministrativeUnit.ReadWrite.All… what your script may touch." | Task → scope spec rows: read → `User.Read.All`; group members → `GroupMember.ReadWrite.All`; admin unit → `AdministrativeUnit.ReadWrite.All` | `list-specs` · content-wash | `pattern_scales` → "scales to every bulk job"; `read_scope` → "User.Read.All, read-only" | Rows populate as each task is named; the rule generalizes — keep the reveal brisk (3 rows). |
| B8 | `11-update-delete` | "**Update-MgUser** runs the very same CSV-and-loop pattern, under that same *User.ReadWrite.All* scope… **Remove-MgUser** follows the identical shape." | Code: the `foreach { Update-MgUser … }` loop; caption notes `Remove-MgUser` = same shape | `code-window` · content-wash | `update_cmd` → "Update-MgUser runs the very same"; `remove_cmd` → "Remove-MgUser follows the identical shape" | Echo B4's layout so the "same shape" reads visually; swap the cmdlet name in place. |
| B9 | `12-contacts` | "Microsoft Graph doesn't manage mail contacts… **New-MgUser** just won't work… That job belongs to **New-MailContact**… Exchange Online PowerShell, not Graph." | TRAP card — term **New-MailContact**, body: Exchange Online PowerShell, not Microsoft Graph | `callout-note` · content-wash | `contacts_trap` → "doesn't manage mail contacts"; `newmailcontact` → "belongs to New-MailContact" | Single warning beat; the boundary (Graph vs Exchange Online) is the point. |
| — | `90-recap` | "You connected with a scope, imported a CSV, and let **New-MgUser** build the whole roster in one pass… matching every scope to its task… One pattern for the entire directory." | Recap chips (answers the opening hook) | `90-recap` (scaffolded) · hero-swoosh | `recap_one_pass` → "the whole roster in one pass" | Chips resolve the three objectives; pays off the Monday-deadline hook. |
| — | `91-cta` | "The next exercise takes you through bulk-provisioning with Graph PowerShell… open the New-MgUser reference on Microsoft Learn." | CTA: next exercise + Learn more link | `91-cta` (scaffolded) · hero-swoosh | `cta_exercise` → "The next exercise takes you" | Hand off to Unit 4 exercise. |

## Source-fidelity ledger

Every claim → source line and/or Docs URL. Referent / quantifier / modality checked against the
source before ✅.

| Claim in narration | Where it comes from | Verified |
|---|---|---|
| Overseas office opens Monday; ~thirty new hires; one-at-a-time in the portal won't be ready in time | Source ¶1: "Relecloud's overseas office opens Monday… Creating each account one at a time in the portal doesn't get thirty people set up before the doors open" | ✅ verbatim scenario; quantifier "thirty" preserved |
| Graph PowerShell path = connect with a scope → loop over a CSV → one cmdlet creates every account | Source ¶1: "connect with the right scope, loop over a spreadsheet of names, and let a single cmdlet create every account in the list" | ✅ |
| Every session starts with `Connect-MgGraph`; the requested scope decides what the script may do | Source §"Connect with a scope": "Every Graph PowerShell session starts with `Connect-MgGraph`, and the scope you request there determines what the rest of the script is allowed to do" · Docs: create-user-accounts-with-microsoft-365-powershell (`Connect-MgGraph -Scopes "User.ReadWrite.All"`) | ✅ |
| To create accounts the scope is `User.ReadWrite.All`; a narrower scope doesn't cover creation ("ask for less, and the create step fails") | Source: "For creating accounts, that scope is `User.ReadWrite.All`" + "the least-privileged delegated scope documented for creating and updating users… no narrower built-in scope covers user creation" · Docs: New-MgUser permissions list least-privileged = User.ReadWrite.All | ✅ modality checked — "no narrower scope covers creation" → a lesser scope won't authorize the create |
| `Import-Csv` reads the spreadsheet into a collection of objects | Source §"Connect with a scope": "`Import-Csv` reads the spreadsheet into a collection of objects" | ✅ |
| CSV columns = display name, user principal name, mail nickname, temporary password; same fields as the portal Bulk create sheet | Source code block (`-DisplayName $hire.DisplayName -UserPrincipalName … -MailNickname … PasswordProfile @{ Password = $hire.TempPassword …}`) + "the same display name, user principal name, and initial password columns you'd upload through the portal's **Bulk create** feature" | ✅ referent = portal Bulk create |
| `foreach` hands each row to `New-MgUser` one at a time; it enables the account and forces a password change at first sign-in | Source: "the `foreach` loop hands each row to `New-MgUser` one at a time" + code `-AccountEnabled` and `ForceChangePasswordNextSignIn = $true` | ✅ "switches it on" = `-AccountEnabled`; "password reset at first sign-in" = `ForceChangePasswordNextSignIn` |
| A script is repeatable; rerun next quarter for the next batch without reopening a blade | Source: "a script is repeatable. Run it again next quarter when the next batch of hires arrives, and you don't reopen a single blade" | ✅ near-verbatim |
| `Directory.ReadWrite.All` also works but grants far more; match the scope to the task, not the one that also happens to work | Source §"Match the scope…": "easy to reach for `Directory.ReadWrite.All`… since it also works, but it grants far more than user management alone… picking the one that matches the operation—not the one that happens to also work" | ✅ modality "would work" = source "also works" |
| The rule scales: read/export → `User.Read.All`; add/remove members → `GroupMember.ReadWrite.All`; admin units → `AdministrativeUnit.ReadWrite.All`; none substitute for each other; the scope tells Entra ID what the script may touch | Source scope table + "None of these four scopes substitute for one another" + "The scope you request tells Microsoft Entra ID exactly what the script is allowed to touch" · Docs: New-MgGroupMemberByRef (Microsoft.Graph.Groups); Get-MgUser read scope User.Read.All | ✅ `AdministrativeUnit.ReadWrite.All` cited from source table (Docs page not separately fetched; consistent with the Graph least-privilege model) |
| `Update-MgUser` uses the same CSV-and-loop pattern under the same `User.ReadWrite.All`; `Remove-MgUser` follows the same shape | Source §"Update and delete…": "`Update-MgUser` still runs under `User.ReadWrite.All`, the same scope that created the accounts… and `Remove-MgUser` follows the same shape again" | ✅ |
| Microsoft Graph doesn't manage mail contacts; `New-MgUser` won't create one; use `New-MailContact` in Exchange Online PowerShell, not Graph | Source §"Contacts stay off this toolkit": "Microsoft Graph doesn't manage mail contacts at all… The cmdlet that belongs to that job is `New-MailContact`, and it runs in Exchange Online PowerShell, not Microsoft Graph PowerShell" · Docs: Manage mail contacts in Exchange Online → `New-MailContact` (Exchange PowerShell) | ✅ |
| CTA: next unit is a hands-on bulk-provision exercise; New-MgUser reference on Learn | Module TOC: Unit 4 `4-exercise-bulk-provision-graph-powershell.md` · Source link `/powershell/module/microsoft.graph.users/new-mguser` | ✅ |

## Open questions

- **Audition the cmdlet/scope reads before final render.** The teaching content is literal cmdlet
  and scope tokens (`Connect-MgGraph`, `New-MgUser`, `New-MailContact`, `User.ReadWrite.All`,
  `Directory.ReadWrite.All`). Run `tools/audition_voices.py --from-script script.md` on the Vance
  voice; if the hyphen or dots read unnaturally, prefer an SSML `say-as`/reword fix over `--rate`.
- **`AdministrativeUnit.ReadWrite.All` (B7)** is reproduced from the source unit's scope table; the
  standalone Docs permissions page wasn't fetched this pass. If the designer surfaces it as a
  focal row, spot-check it against current admin-unit cmdlet docs before render.
- On-screen code uses the source's `-MailNickname` spelling (docs example casing `-MailNickName` is
  equivalent — PowerShell parameter names are case-insensitive).
