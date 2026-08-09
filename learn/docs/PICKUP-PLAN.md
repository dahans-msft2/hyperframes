# Pick-up plan — Learn video pipeline

**Written:** 8 Aug 2026, end of session, ahead of vacation.
**Status when you left:** Highway 12 shipped. Everything below is exploration, nothing is committed to.

---

## 1. Where things actually stand

| Thing | State |
|---|---|
| Highway 12 video | **Shipped.** [Release v2](https://github.com/dahans-msft2/hyperframes/releases/tag/Highway-12-Lewis-And-Clark-v2) — 6:27, real cartography, road-aligned routes |
| Gallery | Live at https://dahans-msft2.github.io/hyperframes/ — was silently broken for *every* release; fixed on `main` (`82730b92`) |
| Working branch | `highway-12-cloud-v2` (pushed) — the enhanced cloud build |
| Superseded | v1 release still listed in the gallery; left in place pending your call |
| Foundry white paper | `learn/docs/HyperFrames-Learn-Pipeline-to-Azure-Foundry-Technical-Overview.docx` — v0.2, 7 Aug. Read and incorporated below |

---

## 2. The finding that changes the ordering

The four tracks aren't independent. **Track 1 (private repo) silently triggers the render-cost question in Track 2.**

The white paper (§6.3) lists four triggers for migrating render to Azure. One is:

> *"The repository becomes private, changing hosted-runner economics."*

That trigger fires the moment Track 1 lands. Measured today:

- **Cloud render = 59.6 min of compute** (setup is only ~2 min — see §4)
- GitHub Actions is **free on public repos**. On private repos it's metered, and **Windows runners bill at 2× minutes**
- So one video ≈ **120 billed minutes**

Against a typical included allowance of ~3,000 minutes/month, that's roughly **25 videos/month before overage** — and Learn work is bursty, so a module drop could blow through it in a day.

> **Do not treat "go private" as a pure repo-hygiene move.** It converts render from free to metered and makes the render-plane decision urgent. Verify current GitHub billing rates before committing — the 2× Windows multiplier is the part people miss.

**Consequence for ordering:** get the font-licensing answer moving *before* or *alongside* the repo split, not after. It has organisational lead time and it selects the entire render architecture.

---

## 3. Track 1 — Private repo extraction

**Verdict: very feasible. The coupling is already near zero.**

Audited today:

| Measure | Value |
|---|---|
| Tracked files under `learn/` (excl. `output/`) | **94 files, ~10.9 MB** |
| Imports from `packages/` or `registry/` | **None.** One prose mention in a docstring |
| How the CLI is obtained | `npx hyperframes@<pinned>` — published npm, version pinned in `learn/config.json` → `cli.published_version` (`0.7.77`) |
| Learn-specific workflows | 6: `video-ci`, `render-video`, `render-batch`, `build-ci-image`, `deploy-gallery`, `copilot-setup-steps` |

You were right — nothing from the hyperframes source tree is needed. The fork linkage is historical, not functional.

**What to carry over:** `learn/{tools,templates,brand,profiles,frame-presets,assets,config.json}`, the 6 workflows, `.github/skills/learn-*`, `.github/agents/*`, and the repo instructions.

**Watch out for:**
- **Licensed fonts.** Segoe was scrubbed from history because the repo is public. A private repo changes that calculus — but *do not* assume private = allowed to commit. That's the same licensing question as §5 of the white paper. Keep `sync_fonts.py` generating from the host until someone answers it.
- **LFS budget.** `learn/output/` is 824 MB on disk today, mostly renders and WAVs. Private LFS is metered. Decide up front whether renders live in Releases only (recommended) rather than in git.
- **The scope gate assumes one project per branch.** It broke twice already (see §6). Fix it during the move, not after.
- **CodeQL / upstream CI** won't come along, which is a simplification.

---

## 4. Track 4 — Runners, gates, timings

Measured today, successful cloud render:

| Step | Duration |
|---|---|
| Checkout (LFS) | 0.5 min |
| Provision chrome-headless-shell | 1.4 min |
| **Render + package** | **59.6 min** |

**The render is CPU-bound, not setup-bound.** Local runs the same composition in 15–21 min. Setup optimisation is worth ~2 min and is not where the time is.

Three real options, in increasing order of effort:

1. **Larger GitHub runners** — simplest, costs money, likely 2–3× improvement.
2. **Chunk-parallel fan-out.** The white paper (§6.2) notes the framework already defines a plan → chunk-render → assemble contract, *and it is currently unused*. `render-batch.yml` already has `matrix` + `max-parallel: 6`, but it parallelises **across videos, not within one**. This is the highest-leverage unexploited capability you have.
3. **Azure with real job orchestration** — white paper Phase 5, gated on the font decision.

Worth noting: as cloud authoring parallelises well and render doesn't, **the render queue becomes the bottleneck the more successful batch authoring gets.** Scaling one half relocates the constraint.

---

## 5. The Scout / daily-batch question — "unless...?"

Partially yes. The two halves have different blockers:

**Render half — unblocked today.** `render-batch.yml` already has the matrix and `max-parallel: 6`; it's `workflow_dispatch` only. Adding a `schedule:` cron is a few lines. You could have nightly batch rendering this week.

**Authoring half — genuinely blocked, and I verified why.** Neither Copilot coding-agent API exposes a model parameter:

- `create_pull_request_with_copilot` — params are `owner`, `repo`, `problem_statement`, `title`, `base_ref`. No model.
- `assign_copilot_to_issue` — adds `custom_instructions`. Still no model.

`batch.py` knows this — it ends with a manual instruction: *"on each PR, select Claude Opus 5 + high reasoning and @copilot it."* That manual step is exactly why the automation didn't come together, and it's the same thing that cost us a full build cycle earlier today.

**Three ways out:**
- **(a)** Accept the default model for batch runs, reserve hand-picked models for hero videos. Cheapest, available now.
- **(b)** Drive authoring from a scheduled job calling a model API directly, instead of the Copilot coding agent. You control the model, you lose the agent's repo integration.
- **(c)** **Foundry-hosted agents — you choose the model by definition.** This is the strongest argument for Track 2 that isn't in the white paper: *model selection is the automation blocker, and Foundry removes it.* Worth adding to the paper.

---

## 6. Track 2 — Foundry

The white paper is strong and I'm not going to re-litigate it. Its shape holds up: **three workload classes** (judgment / verification / media compute), Foundry owns the first, hosts the second as tools, and must never embody the third.

Points where today's session adds evidence:

- **§4.7 "the rubric is already an evaluator" is the sleeper.** Today's session produced two defects that a *structural* evaluator would catch and a judge model would not: the gallery deploy failing for every release, and a build that passed all gates while being unrenderable from a clean clone. Deterministic evaluators earn their keep faster than judge models.
- **Add model selection to the case for Foundry** (see §5c above).
- **§4.3.2 — word-boundary timing removing the transcription stage** is the single best item in the paper. It deletes a pipeline stage rather than adding one. If Dragon HD Omni supplies it, you may not even need to change voice family.
- **Sequencing warning worth honouring:** tool plane *before* control plane. "An agent platform amplifies whatever it is given: with reliable tools it enforces a process, and without them it produces confident prose about a process." Today's near-miss — a build reporting green while being unrenderable — is that failure in miniature.

**Critical path is unchanged and non-engineering:** get the font-embedding question asked, in the paper's precise wording (§5.1). It has organisational lead time and it selects Path A (Linux, cheap, reuses existing images) vs Path B (Windows, expensive, new image).

---

## 7. Track 3 — Author experience

Your observation is the most valuable thing to come out of today, and it's worth stating precisely:

> The Highway 12 map succeeded because you specified *style* ("Lord of the Rings", minimal, dotted), *content* ("state lines, rivers, POIs"), *motion* ("pan the camera with the movements"), and *a prohibition* ("don't overlay the route, you'll get it wrong").

That last one did the most work. **A well-placed prohibition beat three rounds of iteration.** The agent's failure mode isn't inability — it's confidently filling an unspecified gap (I generated fictional maps twice before you stopped me).

**So the interview should elicit, per scene:**
1. **Reference** — "in the style of X"
2. **Content inventory** — what must literally be on screen
3. **Motion verb** — pan / hold / reveal / trace
4. **Prohibitions** — what to *not* invent ← highest value, almost never asked
5. **Fidelity class** — decorative vs **factual**. Factual visuals must be *sourced*, never generated

That fifth one deserves a hard rule in the doctrine: **geography, charts, maps, timelines, and any real place or quantity are data-sourcing problems, not image-generation problems.** Generated maps look convincing and are fictional.

Also worth adding: **prefer measuring over estimating whenever a renderer is in the loop.** I estimated label widths ~25% narrow and shipped a "fixed" layout that wasn't; a zoomed render caught it. The engine was right there.

---

## 8. Track 4b — The front end you described

You want: authoring kickoff, visual review, audio audition, storyboard/timeline, Studio integration, render gate. Today's gallery (`learn/tools/build_gallery.py`) is a static page built from Releases — a reasonable seed, but it reads *finished* artefacts only.

The gap: **everything you described operates on in-flight work, which currently lives on branches and in PRs, not in Releases.** So the front end needs a second data source before any UI work matters.

Suggested build order (each independently useful):
1. **Review page per PR** — snapshots + audio + gate results, from branch artefacts. Highest value, no new infrastructure.
2. **Audio audition** — `audition_voices` output on a page. Cheap, and needed anyway for the Phase 1 voice work.
3. **Storyboard / timeline view** — from `scenes.json` + `anchors.js`; both already machine-readable.
4. **Authoring kickoff form** — writes the brief, opens the issue. Pairs with §7's interview.
5. **Studio integration + render gate** — last; depends on all of the above.

Note the overlap: (2) is needed by Foundry Phase 1 regardless, and (3) is nearly free from data you already emit.

---

## 9. Loose ends from today

| Item | Status |
|---|---|
| Gallery deploy broken for all releases | **Fixed** (`82730b92`) — release events now redispatch onto `main` |
| Gallery duration parsing | Brittle — reads a `(NNNs)` token from the release body. Should read `manifest.json` |
| v1 release still listed | Your call — retire or relabel as superseded |
| `check_subcomps.py` P1 hole | The template-span regex matches the `<template>` inside the standard head comment, so the "script outside template" check is inert in every scene using it — and gives *misleading* advice in scenes without it. Verified with three probes. The dangerous case is still caught by the timeline check, so it's a defense-in-depth gap, not an open hole. Shared tooling — flagged, not patched |
| "Exactly one project per branch" | Broke both the video gate and the render workflow once a second project existed. Still present |
| No clean-clone render test | The gap that let a cloud build pass every gate while being unrenderable. Worth a gate |

---

## 10. Suggested first session back

1. **Ask the font question.** One email, precise wording in white paper §5.1. Longest lead time, zero engineering. Do this before anything else.
2. **Decide the render-artefact policy** for the private repo (Releases vs LFS). It constrains the extraction.
3. **Do the extraction** — it's small, well-understood, and unblocks tracks 3 and 4.
4. **Add the cron to `render-batch.yml`** — nightly batch render, cheap win, works today.
5. Then pick: Foundry Phase 1 (narration + clock) *or* the PR review page. Both are independently valuable; neither blocks the other.

**Do not** start render-migration engineering before item 1 comes back. Path A and Path B don't share an implementation.
