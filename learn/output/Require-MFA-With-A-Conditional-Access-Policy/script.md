<!--
  Grounded live against Microsoft Learn (Docs MCP), 2026-08-06:
  https://learn.microsoft.com/entra/identity/authentication/tutorial-enable-azure-mfa
  Every portal path, menu, and control label below is quoted from that page.
-->

# Require MFA with a Conditional Access policy

| | |
|---|---|
| Source | https://learn.microsoft.com/entra/identity/authentication/tutorial-enable-azure-mfa |
| Profile | demo-walkthrough (tight low-end cut) |
| Voice | en-US-Ava:DragonHDLatestNeural (~153 wpm) |
| Word budget | profile 217–2178; **tight target ~430** (~180 s content @ ~153 wpm) |
| Actual words | 433 |
| Est. runtime | 2:50 + 0:11 end card |

## Narration

A stolen password shouldn't be enough to get into your tenant. With a single Conditional Access policy, every sign-in you choose has to prove it's really the user — before it's let near your resources. Here's how you build that in a few minutes.

You'll do four things. Create a Conditional Access policy, point it at a test group of users, require multifactor authentication, and switch it on. So let's open the Microsoft Entra admin center.

First, what Conditional Access is. Think of it as an *if-then* rule that sits on the sign-in. If a sign-in matches the conditions you set — these users, this app — then Entra steps in and asks for more proof before it grants access. That's why it's the recommended way to require MFA: you decide who gets prompted, and when.

So let's build one. In the admin center, browse to Entra ID, then Conditional Access, and select New policy. Give it a clear name, like M F A Pilot. Now the *who*: under Assignments, open Users, choose your test group, and select it. The policy targets just those users, so no one else is affected while you test.

Next, the *what* — which sign-ins trigger the rule. Under Cloud apps or actions, choose Select resources. For this walkthrough, pick the Windows Azure Service Management API, then choose Select. That scopes the policy to sign-ins for Azure management. With the who and the what set, there's one thing left: the requirement itself.

This is the part that matters. Under Access controls, open Grant, and select Grant access. Then check *Require multifactor authentication*, and choose Select. You've just told Entra that for these users, on this app, a password alone isn't enough — they also have to pass a second factor.

The policy is built, but it isn't live yet. Scroll to Enable policy and flip it to On. You could set it to Report-only first to preview the impact, but for a small test group, turn it straight on. Then select Create, [[pause:600ms]] and the policy is active.

So, four steps: you created a Conditional Access policy, aimed it at a test group, required multifactor authentication, and turned it on. Now, when those users sign in to that app, a password only gets them partway — then Entra asks for the second factor before it lets them through.

Try it with a test user, and watch the MFA prompt appear on the next sign-in. When you're ready to go further, the next tutorial builds a *risk-based* Conditional Access policy — one that asks for MFA only when a sign-in looks risky. Find it on Microsoft Learn.

## Beat plan

| # | Narration line | On screen | Shape cue | Motion / screenshot note |
|---|---|---|---|---|
| 1 · bumper *(chrome)* | *(silent brand sting — no VO)* | Microsoft Learn mark; kicker sub-line **"Microsoft Entra ID · Identity & access"** | `bumper` (brand, hero-swoosh) — scaffolded `scenes/01-bumper.html` | Fill the `kicker` config only; ~3 s, no narration. |
| 2 · title + hook *(chrome)* | "A stolen password shouldn't be enough…" | Title (≤2 lines): **"Require MFA with a / Conditional Access policy"**; kicker **"Microsoft Entra ID"**; subtitle **"A step-by-step portal walkthrough"** | `title-hero` (hero-swoosh) — scaffolded `scenes/02-title.html` | Hook frames the stakes; on-screen is the title, *not* the spoken line (Redundancy). |
| 3 · objectives *(chrome)* | "You'll do four things…" | Four outcome chips: **"Create the policy" · "Target your users" · "Require MFA" · "Turn it on"** | objectives chrome — scaffolded `scenes/03-objectives.html` (list-steps style) | Chips reveal as each is named (Temporal Contiguity). Chips are labels, not the sentence. |
| 4 · concept | "First, what Conditional Access is…" | `ca-overview.png` — the Conditional Access overview diagram; one callout on the *if → then* flow (conditions → grant) | `media-screenshot` (content-wash), callout region over the sign-in → access path | Slow Ken Burns push; callout lands on `cue.conceptIfThen` ("asks for more proof…"). Portal-capture ⇒ dead-zone exempt, holding is correct. |
| 5 · new policy + assign group | "So let's build one…" | `ca-new-policy.png` — the Conditional Access page → **New policy**; sequential callouts on **New policy**, then **Assignments / Users** | `media-screenshot` (content-wash), two-step callout | `cue.newPolicy` → `cue.policyName` → `cue.assignGroup`. **Capture opportunity:** the name-and-assign-group blade isn't in the 5 stills — an author still or short recording would teach it cleaner. |
| 6 · select app | "Next, the *what*…" | `ca-select-apps.png` — resource picker; callout on the **Windows Azure Service Management API** row | `media-screenshot` (content-wash), callout over the selected app row | Callout lands on `cue.selectApp`. |
| 7 · grant / require MFA | "This is the part that matters…" | `ca-require-mfa.png` — the **Grant** panel; callout on **Require multifactor authentication** (checked) | `media-screenshot` (content-wash), callout over the checked control | `cue.grantAccess` → `cue.requireMfa`. This is the climax beat — let the callout hold. |
| 8 · enable on + create | "The policy is built…" | `ca-enable-on.png` — **Enable policy** toggle set to **On**; callout on the On toggle, then **Create** | `media-screenshot` (content-wash), callout over the On toggle | `cue.enableOn` → `cue.createPolicy`. **Capture opportunity (flagged):** an author `media-screen-recording` of the live test sign-in (test user → "More information required" MFA prompt) would land the payoff in motion — optional bonus beat after this one, or feed it into the CTA. |
| 9 · recap *(chrome)* | "So, four steps…" | Four-step recap: **Create · Target · Require MFA · Turn it on**; badge **"Policy live"** | recap chrome — scaffolded `scenes/90-recap.html` (list-steps) | Pays off the opening hook — a password now only gets them partway. |
| 10 · cta *(chrome)* | "Try it with a test user…" | CTA line: **"Try it, then build a risk-based policy"**; link label **"Microsoft Learn"** | cta chrome — scaffolded `scenes/91-cta.html` (title-hero) | Next step = the risk-based Conditional Access tutorial in the same series. |
| 11 · end card *(appended)* | *(no VO)* | AI disclosure + Microsoft logo | pipeline endcard (`assets/AI_End_Card.mp4`) | 10.667 s, appended by the pipeline; not part of the word budget. |

## Source-fidelity ledger

All rows verified against the live tutorial page (fetched 2026-08-06):
`https://learn.microsoft.com/entra/identity/authentication/tutorial-enable-azure-mfa`

| Claim in narration | Where it comes from in the source (section) | Verbatim label? |
|---|---|---|
| Conditional Access is the recommended way to require MFA | "Create a Conditional Access policy": *"The recommended way to enable and use Microsoft Entra multifactor authentication is with Conditional Access policies."* | ✅ paraphrase, faithful |
| It's an if/then rule that reacts to sign-in events before granting access | "Create a Conditional Access policy": *"policies that react to sign-in events and that request additional actions before a user is granted access"* | ✅ paraphrase, faithful |
| Open the Microsoft Entra admin center | Step 1: *"Sign in to the Microsoft Entra admin center"* (entra.microsoft.com) | ✅ verbatim |
| Browse to Entra ID → Conditional Access → select New policy | Step 2: *"Browse to **Entra ID** > **Conditional Access** > Overview, select **+ Create new policy**"* | ⚠ label is **"+ Create new policy"** on the **Overview** page (narration says "New policy") |
| Name it, e.g. M F A Pilot | *"Enter a name for the policy, such as MFA Pilot"* | ✅ verbatim |
| Under Assignments, open Users, choose your test group, Select | Assignments steps: *"Users or workload identities" → "Users and groups" → "Select users and groups" → select group → "Select"* | ⚠ full label chain is "Users or workload identities"; narration compresses to "Users" |
| Under Cloud apps or actions, choose Select resources | "Configure which apps require MFA": *"Select the current value under **Cloud apps or actions** … Under **Include**, choose **Select resources**"* | ✅ verbatim |
| Pick the Windows Azure Service Management API, then Select | *"select **Windows Azure Service Management API** … Then choose **Select**"* | ✅ verbatim |
| Under Access controls, Grant → Grant access | "Configure multifactor authentication for access": *"Under **Access controls**, select the current value under **Grant**, and then select **Grant access**"* | ✅ verbatim |
| Check Require multifactor authentication, then Select | *"Select **Require multifactor authentication**, and then choose **Select**"* | ✅ verbatim (one screenshot alt-text hyphenates "multi-factor"; body form used) |
| Enable policy → On (Report-only previews impact) → Create | "Activate the policy": *"Under **Enable policy**, select **On** … select **Create**"*; Report-only/Off noted | ✅ verbatim |
| Test: sign in as a test user, get the MFA prompt | "Test Microsoft Entra multifactor authentication": *"you're prompted to use Microsoft Entra multifactor authentication or to configure a method"* | ✅ paraphrase, faithful |
| Next tutorial = risk-based Conditional Access policy | *"In a later tutorial in this series, we configure Microsoft Entra multifactor authentication by using a risk-based Conditional Access policy."* | ✅ verbatim |

## Cue anchors

Written to `anchors.json` beside this file — cue name → the exact spoken phrase the callout
must land on. All phrases are hyphen-free so they resolve against ASR word tokens (the transcript
splits `if-then` into `if` + `then`). The builder turns them into real times with
`tools/word_anchors.py transcript.json --spec anchors.json`.

## Open questions

- **On-screen names must match the stills.** Doc examples are policy **"MFA Pilot"** and group **"MFA-Test-Group"**. Confirm the recorded screenshots show the same names; if they differ, align the callout labels to whatever the stills actually show.
- **Missing screen among the 5 stills.** There's no capture of the name + assign-group blade (only `ca-new-policy.png` shows the Conditional Access page). Decide: fold naming/assignment into the `ca-new-policy` callouts, or have the author capture that blade.
- **Optional payoff recording (flagged on beat 8).** Include an author `media-screen-recording` of the live test sign-in (MFA prompt) as a bonus beat, or leave the payoff to the CTA? Adds ~10–15 s if included.
