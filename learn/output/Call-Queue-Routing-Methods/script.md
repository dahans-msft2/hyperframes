<!--
  SOURCE (primary, read in full):
    C:\learn-pr\learn-m365-pr\learn-m365-pr\wwl\configure-auto-attendants-call-queues\includes\8-interpret-call-queue-routing-methods.md
    Module: "Configure auto attendants and call queues" (MS-721 / Teams Phone), Unit 8.

  DOCS-MCP GROUNDING (live learn.microsoft.com, 2026-08-07 — server microsoft_docs_mcp):
    - Routing methods, presence-based routing, callback, timeout worked example:
        https://learn.microsoft.com/microsoftteams/aa-cq-setup-call-queue
    - Attendant = Default; Longest Idle & Round Robin = Recommended; "Selecting Longest Idle
      automatically enables Presence based routing":
        https://learn.microsoft.com/microsoftteams/aa-cq-reference-limits-supported-configurations
    - Default music-on-hold behaviour:
        https://learn.microsoft.com/microsoftteams/music-on-hold
    - CTA target ("Learn more" — Create a call queue):
        https://learn.microsoft.com/microsoftteams/aa-cq-setup-call-queue

  VERIFICATION: Current docs AGREE with the local unit on every substantive claim, including the
    60s-eligible / 120s-timeout / 2-min-music worked example (verbatim). No claim required
    preferring the docs over the local source. Two non-contradicting ENRICHMENTS noted in the
    ledger (an extra "…and the agent answers the callback" condition; a North-America number-prefix
    restriction) were left OUT to stay scoped to what this unit teaches. Terminology note: current
    setup UI now says "representative"; this unit (and this script) use "agent" to match MS-721.
  RUN_ID: call-queue-routing-methods-202608071230
-->

# Why your call-queue callback never fires

| | |
|---|---|
| Source | 8-interpret-call-queue-routing-methods.md (Configure auto attendants and call queues, Unit 8) |
| Profile | unit-video (~4 min) |
| Frame preset | learn-ilt |
| Voice | en-US-Ava:DragonHDLatestNeural (LOCKED) |
| Word budget | 435–726 (target 580) |
| Actual words | 602 |
| Est. runtime | ~4:09 content (602 ÷ 2.42 w/s) + 0:11 end card ≈ 4:20 total |

## Narration

Here's a call queue setup that looks completely correct — and quietly fails.

This is how call queue routing works in Microsoft Teams Phone, and how to keep it from tripping you up.

By the end, you'll know three things: how the four routing methods hand out calls, and which two Microsoft recommends; how callback offers a waiting caller a call back instead of hold music; and the timing trap that stops callback from ever being offered.

Picture that broken setup. Callback is on, a caller is clearly waiting, an agent is clearly free — and the callback never comes. Nothing's misconfigured. To see why, you first need to see how a call queue handles a call. It starts with one decision: who to ring.

That decision is the routing method — and you get four of them. Each hands out calls differently, so your choice decides how the work is shared across agents.

The default on every queue, new or existing, is Attendant routing. A call comes in, every agent's phone rings at once, and whoever answers first gets it. Fast — but it leans on the same quick hands.

Serial rings agents one at a time, in the exact order you list them. If one dismisses the call or doesn't answer, it moves to the next, and keeps going until someone picks up or the call times out.

Round robin evens things out, so every agent gets the same number of calls. That's the one for inbound sales, where each rep should get an equal shot at the next lead.

Longest idle sends the next call to whoever's been free the longest — and free means their presence is set to *Available*. Choosing it flips presence-based routing on automatically, even when that toggle looks off. These two — Round robin and Longest idle — are the ones Microsoft recommends.

One catch: when fewer calls are waiting than there are available agents, only the first two longest-idle agents get offered calls.

So that's who the queue rings. Callback handles the people still waiting: turn it on, and an eligible caller can hang up and get called back the moment an agent frees up — instead of sitting on hold.

A caller becomes eligible the moment any one of three conditions comes true: they wait past your set time, the queue grows past a set number of calls, or the calls-to-agent ratio crosses your limit. Their number just has to be publicly dialable, non-premium, and in standard E one six four format.

So — back to our mystery. Callback's on, eligibility's set to sixty seconds, everything looks right. Will this caller ever get offered a callback? [[pause:800ms]]

Watch the clock. At sixty seconds, the caller becomes eligible — but the default hold music runs a full two minutes, and the timeout is set to one hundred and twenty seconds. The timeout fires before the music ends, so the offer never plays. Callback wasn't broken — the timeout just never gave it *room*.

So here's the rule to keep: your Call timeout has to outlast the whole sequence — time to become eligible, time for the music to finish, and time for the callback to reach a free agent. Get that one value right, and callback finally works.

So, four routing methods deciding who rings: Attendant, Serial, Round robin, and Longest idle — the last two recommended. Callback for the callers still on hold. And one timing rule tying it together: set the timeout long enough, or callback never gets its turn.

Want to set one up yourself? Head to the call queue setup guide on Microsoft Learn and walk through routing and callback end to end.

## Beat plan

Chrome beats (bumper / title / objectives / recap / cta) are already scaffolded — narration above
supplies their text. Body beats 4–15 are authored between them. `On screen` names a candidate kit
block + ground; the designer owns the final selection. The **four methods** and the **timeout math**
are the visual spine.

| # | Beat | Narration slice | On screen (block · ground) | Shape cue | Signaling → lands on |
|---|---|---|---|---|---|
| 1 | Bumper *(chrome)* | "Here's a call queue setup that looks completely correct — and quietly fails." | Learn **bumper** on **hero-swoosh**. Kicker: "Teams Phone · Configure auto attendants & call queues". | `bumper` — mandatory open. | Brand sting settles on **"quietly fails"** — the itch is planted. |
| 2 | Title *(chrome)* | "This is how call queue routing works in Microsoft Teams Phone…" | **title-hero** on **hero-swoosh** (scarce hero ground, spent here). Title "Call queue routing / methods"; subtitle "Teams Phone". | `title-hero` — one headline owns the frame. | Title waterfalls on **"call queue routing"**. |
| 3 | Objectives *(chrome)* | "By the end, you'll know three things: … the four routing methods … callback … the timing trap…" | **objectives** on **content-wash** — 3 stakes chips: "Who the queue rings" · "Callback vs. hold" · "The timeout trap". *(Redundancy: chips are labels, not the sentence.)* | `list-select` / objectives chips. | Chip 1 on **"four routing methods"**; chip 2 on **"callback"**; chip 3 (amber) on **"timing trap"**. |
| 4 | The mystery *(hook)* | "Picture that broken setup … the callback never comes. Nothing's misconfigured … It starts with one decision: who to ring." | **callout-note** (question) on **content-wash** — a queue motif: waiting caller + free agent, a struck-through "↩ callback" badge. Pivot chip "First: who rings?" | `callout-note` (open mystery) → hands to routing. | "callback" badge strikes on **"the callback never comes"**; pivot chip on **"who to ring"**. |
| 5 | Four methods | "That decision is the routing method — and you get four of them. Each hands out calls differently…" | **list-select** on **content-wash** — four peer rows: Attendant · Serial · Round robin · Longest idle; count "4 methods". *(Reuse the unit's `call-queue-routing-method.png` as reference; capture: routing-method dropdown in Teams admin center.)* | `list-select` — peers, one chosen per beat. | Rows cascade on **"four of them"**; count reads on **"hand out calls differently"**. |
| 6 | Attendant | "The default on every queue … every agent's phone rings at once … leans on the same quick hands." | **custom** on **content-wash** — one call fans out to ALL agent tiles at once; "Default" tag. *(nearest kit: `diagram-flow` one-to-many.)* | `custom` (nearest `diagram-flow`) — simultaneous fan-out. | All tiles ring on **"rings at once"**; "Default" tag on **"The default on every queue"**. |
| 7 | Serial | "Serial rings agents one at a time, in the exact order you list them … until someone picks up or the call times out." | **list-steps** on **content-wash** — ordered agent 1→2→3, the call advancing down the list. | `list-steps` — ordered, top-to-bottom. | Call steps down the list on **"one at a time"**; advance on **"moves to the next"**. |
| 8 | Round robin | "Round robin evens things out … each rep should get an equal shot at the next lead." | **custom** on **content-wash** — per-agent call counters level to equal heights. *(nearest kit: `chart-bar` — equal bars.)* | `custom` (nearest `chart-bar`) — counts equalize. | Counters level on **"the same number of calls"**; "inbound sales" tag on **"inbound sales"**. |
| 9 | Longest idle | "Longest idle sends the next call to whoever's been free the longest … presence set to Available … flips presence-based routing on automatically … These two … Microsoft recommends." | **list-select** on **content-wash** — agents with idle timers; the longest-idle lifts (accent tab). A **presence-based routing** toggle snaps On (was greyed). "Recommended" ribbon on Round robin + Longest idle. | `list-select` (pick idle-longest) + toggle gotcha. | Idle-longest lifts on **"free the longest"**; toggle snaps On on **"flips presence-based routing on automatically"**; ribbon on **"Microsoft recommends"**. |
| 10 | The two-agent catch | "One catch: when fewer calls are waiting than there are available agents, only the first two longest-idle agents get offered calls." | **callout-note** (NOTE) on **content-wash** — "Fewer calls than agents → only the first 2 idle-longest are offered." | `callout-note` — one qualifying NOTE. | "2" emphasises on **"only the first two longest-idle agents"**. |
| 11 | Callback intro | "So that's who the queue rings. Callback handles the people still waiting … get called back the moment an agent frees up — instead of sitting on hold." | **custom** on **content-wash** — a waiting caller drops off hold; a "↩ we'll call you back" path draws to a freed agent. *(nearest kit: `diagram-flow`.)* | `custom` (nearest `diagram-flow`) — hold → callback path. | Callback path draws on **"get called back"**; "no hold" chip on **"instead of sitting on hold"**. |
| 12 | Eligibility | "A caller becomes eligible the moment any one of three conditions comes true: … wait time … number of calls … calls-to-agent ratio. Their number … publicly dialable, non-premium … E one six four format." | **list-specs** on **content-wash** — 3 OR-conditions (Wait time · Calls in queue · Calls-to-agent ratio), any-one-true; small footnote row: "publicly dialable · non-premium · E.164 · not ringing an agent". *(alt: `diagram-flow` any-one-true.)* | `list-specs` (3 trigger conditions, OR) + footnote. | Row 1 on **"they wait past your set time"**; row 2 on **"the queue grows past a set number of calls"**; row 3 on **"the calls-to-agent ratio crosses your limit"**; footnote on **"standard E one six four format"**. |
| 13 | Predict | "So — back to our mystery. Callback's on, eligibility's set to sixty seconds … Will this caller ever get offered a callback?" `[[pause:800ms]]` | **callout-note** (question) on **content-wash** — the config held: "Callback ON · Eligible @ 60s · Timeout 120s · Music: Default". *Withhold the answer.* | `callout-note` — predict-before-reveal; hold on the question. | Config card holds through **"ever get offered a callback"** → `[[pause:800ms]]` (no answer yet). |
| 14 | The reveal *(spine climax)* | "Watch the clock … eligible at sixty seconds — but the default hold music runs a full two minutes, and the timeout is set to one hundred and twenty seconds. The timeout fires before the music ends, so the offer never plays. Callback wasn't broken…" | **custom** timeline on **dark-field** *(the one dramatic dark scene, spent here)* — a clock bar: eligible marker at **60s**, music bar running to **120s**, timeout marker at **120s** firing FIRST; "offer never plays" stamps. | `custom` timeline — the timeout math; dark-field WOW. | Eligible marker on **"the caller becomes eligible"**; music bar on **"runs a full two minutes"**; timeout marker on **"one hundred and twenty seconds"**; it fires on **"fires before the music ends"**; stamp on **"the offer never plays"**. |
| 15 | The rule | "So here's the rule to keep: your Call timeout has to outlast the whole sequence — eligible + music + reach a free agent. Get that one value right…" | **callout-note** (KEY POINT) on **content-wash** — "Call timeout > eligible + music + reach agent". A timeout bar visibly extended past the music bar; callback now succeeds. | `callout-note` — the single takeaway. | Rule inequality on **"has to outlast the whole sequence"**; success tick on **"callback finally works"**. |
| 16 | Recap *(chrome)* | "So, four routing methods deciding who rings … the last two recommended. Callback for the callers still on hold. And one timing rule tying it together…" | **recap** on **content-wash** — three recap straps: "4 methods (RR + Longest idle ✓)" · "Callback for waiters" · "Timeout ≥ the whole sequence". | recap — objectives answered. | Strap 1 on **"four routing methods"**; strap 2 on **"Callback for the callers"**; strap 3 on **"set the timeout long enough"**. |
| 17 | CTA *(chrome)* | "Want to set one up yourself? Head to the call queue setup guide on Microsoft Learn…" | **cta** on **hero-swoosh** — "Learn more → Create a call queue" (Teams docs). | cta — Learn more. | CTA chip lands on **"call queue setup guide on Microsoft Learn"**. |
| 18 | End card | *(no narration)* | Mandatory **AI-disclosure** end card + Microsoft logo — `assets/AI_End_Card.mp4`, 10.667s (appended at build). | n/a — fixed asset. | n/a |

## Source-fidelity ledger

Every row checked for **referent · quantifier · modality**, not just quote presence. Local `.md` =
the Unit 8 include; Docs = live learn.microsoft.com (2026-08-07).

| Claim in narration | Source of the claim | Verbatim / grounded? |
|---|---|---|
| "four routing methods" — Attendant, Serial, Round robin, Longest idle | Local: "choice of routing methods … Attendant, Serial, Longest idle, or Round Robin." Docs (`aa-cq-setup-call-queue`). | Verbatim (set of four). |
| "The default on every queue, new or existing, is Attendant routing" | Local: "All new and existing call queues have attendant routing selected by default." Docs reference table: Attendant = *Default*. | Verbatim; quantifier "new and existing" preserved. |
| "every agent's phone rings at once, and whoever answers first gets it" | Local: "rings all call agents at the same time. The first call agent to pick up … gets the call." | Grounded paraphrase. |
| "Serial rings agents one at a time, in the exact order you list them … moves to the next … until someone picks up or the call times out" | Local: "rings all call agents one by one, in the order specified … tries all agents until the call is answered or times out." | Verbatim/grounded. |
| "Round robin … every agent gets the same number of calls … inbound sales … equal opportunity" | Local: "balances … so each call agent gets the same number of calls … desirable in an inbound sales environment to assure equal opportunity." | Verbatim/grounded. |
| "Longest idle sends the next call to whoever's been free the longest — free means their presence is set to Available" | Local: "routes the next available call to the agent who has been idle the longest. An agent is considered idle when their presence state is set to Available." | Verbatim; "Available" preserved. |
| "flips presence-based routing on automatically, even when that toggle looks off" | Local: "presence-based routing is automatically enabled — even if the toggle appears off." Docs footnote 4: "Selecting Longest Idle … automatically enables Presence based routing." | Verbatim; modality (automatic, despite toggle) preserved. |
| "These two — Round robin and Longest idle — are the ones Microsoft recommends" | Local TIP: "Setting Routing Method to Round robin or Longest idle is the recommended setting." Docs reference: both marked *Recommended*. | Verbatim; the pair, not a single method. |
| "when fewer calls are waiting than there are available agents, only the first two longest-idle agents get offered calls" | Local NOTE: "When there are fewer calls in the queue than available agents, only the first two longest idle agents are presented with calls." | Verbatim; quantifier "first two" preserved. |
| "eligible caller can hang up and get called back … the moment an agent frees up" | Local: "Callback allows eligible callers waiting in a call queue to receive a callback to the number they're calling from when an agent becomes available." | Grounded; modality "eligible" preserved. |
| "eligible the moment any one of three conditions comes true: wait time / number of calls / calls-to-agent ratio" | Local: "becomes eligible … based on any one of the following configured conditions coming true: Wait time in queue; Number of calls in queue; Calls to agent ratio." Docs (`aa-cq-setup-call-queue`, Step 5). | Verbatim; "any one" (OR, not AND) preserved. |
| "publicly dialable, non-premium, and in standard E one six four format" (+ not ringing an agent, on-screen) | Local: "its inbound phone number must be a publicly dialable, nonpremium phone number in E.164 format, and it must not be presenting to an agent." | Verbatim. |
| Worked example: "eligible at sixty seconds … default music runs a full two minutes … timeout one hundred and twenty seconds … timeout fires first, callback isn't offered" | Local: "Call back wait time 60s; Call Queue Timeout 120s; Music Default … default music is two minutes long, the call queue timeout occurs first, and callback isn't offered." Docs (`aa-cq-setup-call-queue`) — **verbatim match**. | Verbatim; all three values + the ordering preserved. |
| "Call timeout has to outlast the whole sequence — eligible + music + reach a free agent" | Local: "the Call timeout value must be set high enough to allow the call to become eligible … and for the music to finish … For a callback to work: timeout long enough for the call to become eligible; the music to stop; the caller to request a callback; the callback to wait until an agent is available." | Grounded; conditions compressed faithfully (see enrichment note). |
| "call queue setup guide on Microsoft Learn" (CTA) | Docs CTA target: Create a call queue — https://learn.microsoft.com/microsoftteams/aa-cq-setup-call-queue | Grounded CTA; exact link confirmed at build. |

### Enrichments in current docs (left out to stay in scope — not contradictions)

| Current-docs detail | Why not in the narration |
|---|---|
| Docs list a fifth "for a callback to work" condition: "…and for the agent to answer the callback." | The local unit lists four; the fifth is an obvious extension of "reach a free agent." Kept the unit's framing; no accuracy loss. |
| Docs add a North-America inbound number-prefix restriction table. | Out of scope for this unit (regional edge case); the E.164 / non-premium rule already carries the teaching point. |
| Setup UI now says "representative"; reference tables still say "Agent Routing Methods". | Used "agent" to match this MS-721 unit's language. Terminology only — no behavioural change. |

## Cue anchors

Written to `anchors.json` beside this file — each cue → the exact spoken phrase it must land on
(verbatim substrings of the narration). The builder resolves them to real times with
`tools/word_anchors.py` against `transcript.json`. Written here because this is where the word each
visual is *about* is known.

## Required-elements check

| Element | Present | Where |
|---|---|---|
| opening.bumper | ✅ | Beat 1 |
| opening.title | ✅ | Beat 2 |
| opening.objectives | ✅ | Beat 3 (framed as stakes: who rings · callback vs hold · the trap) |
| closing.recap | ✅ | Beat 16 (three straps answer the three objectives) |
| closing.cta | ✅ | Beat 17 (Create a call queue) |
| endcard.ai-disclosure | ✅ | Beat 18 |

## Open questions

- **Word count 602 vs target 580** (+3.8%) — inside the 435–726 budget and the 180–300s unit-video
  content window (≈249s). If Ava's audition runs long, the cheapest trims are Beat 8's "inbound
  sales" clause (~10 words) or Beat 10's two-agent catch (~21 words, a source NOTE, not core).
- **Voice not yet auditioned.** Hardest line for Ava is Beat 12/14: "standard E one six four format"
  and "one hundred and twenty seconds." Audition those before TTS spend; if "E one six four" reads
  poorly, drop the term to narration and keep "E.164" on-screen only.
- **dark-field is spent on the reveal (Beat 14).** That is the one dramatic dark scene for this
  video — no other beat may claim it.
- **CTA link** (`aa-cq-setup-call-queue`) is the Docs-confirmed target; re-confirm the exact
  learner-facing URL at build.
