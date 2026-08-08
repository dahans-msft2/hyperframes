# Copilot repository instructions

This fork produces **Microsoft Learn companion videos** with HyperFrames (HTML → MP4). The Learn
pipeline lives under `learn/`. Most cloud-agent tasks here are **"build a Learn video"** tasks.

When your task is to build/author a Learn video composition, follow the contract below. For
unrelated framework changes, defer to the root `AGENTS.md` and normal repo conventions.

---

## Your job: author the composition, nothing else

You are the **builder**. The script and the visual design arrive **already approved** — do not
rewrite narration and do not re-decide the palette. You turn an approved plan + a pre-scaffolded
project into a render-ready composition that passes every gate. You do **not** render (that happens
locally, on licensed fonts + ffmpeg).

**This file is self-contained — everything you need to build is here or in the skills it names.**
Load the skills `hyperframes-core` (composition contract) and `motion-doctrine` (motion law), plus
the `learn-*` doctrine skills under `.github/skills/`. A fuller VS Code-only doctrine exists at
`.github/agents/hyperframes-builder.agent.md`, but the **cloud sandbox blocks `.github/agents/**`
and you do NOT need it** — the craft that used to live only there (especially the cue-anchoring
convention) is reproduced below. **Never stop or block a build for lack of access to that file.**

## What arrives on the branch

You are on a `video/<slug>` branch with a project at `learn/output/<slug>/` already scaffolded by
`new_project.py`:

- **Chrome scenes are stamped and wired** (`scenes/01-bumper`, `02-title`, `03-objectives`,
  `90-recap`, `91-cta`) with `__FILL__` placeholder CONFIG, already listed in `scenes.json`.
- **`scenes.json` has a `body_slot`** marker between opening and closing chrome — the empty region
  where the teaching-body scenes go.
- **Approved inputs are committed:** `script.md`, `design-plan.md`, `narration.wav`,
  `transcript.json`. Frozen assets (`fonts/`, `assets/grounds/`, `assets/vendor/gsap.min.js`,
  `assets/AI_End_Card.mp4`) are in place.

Fill and extend this project — **do not rebuild what is already scaffolded.**

## The build loop

Run every command from the project dir (`learn/output/<slug>/`), CLI pinned to the version in
`learn/config.json` → `cli.published_version` (currently `0.7.77`):

1. **Fill chrome** `__FILL__` from `script.md` (title lines, objective chips, recap, CTA).
2. **Author the body** per `design-plan.md`: **block** beats = copy `templates/blocks/<id>.html` →
   `scenes/<id>.html` and edit its `CONFIG` (do not touch the block's foundation `<style>` or
   timeline); **custom** beats = author on `templates/blocks/_foundation.css`, paused
   scene-relative timeline on `window.__timelines["<scene-id>"]`, `fromTo` (never `from`). Insert
   each into the `scenes` array in the `body_slot` region. Copy any block's grounds / media into
   the project's `assets/`.
3. **Anchor to real word times.** `transcript.json` is the clock — anchor beat starts AND in-scene
   cues to spoken words (`python ../../tools/word_anchors.py`), never to an assumed words-per-second.
4. **Assemble + validate**, in order:
   ```
   python ../../tools/assemble_scenes.py --project .    # scenes.json -> render-ready index.html
   python ../../tools/check_subcomps.py --project .     # cross-file mount contract (after EVERY assemble)
   python ../../tools/check_placeholders.py --project . # no __FILL__ may survive
   python ../../tools/check_initial_state.py --project .
   python ../../tools/check_cue_anchors.py --project .
   npx --yes hyperframes@0.7.77 lint
   npx --yes hyperframes@0.7.77 check                   # headless browser gate (runtime, layout, WCAG)
   ```
   **All must pass** before you finalize. `check_subcomps.py` catches the composition-id/timeline
   mismatch that `lint`/`check` cannot see and that silently stalls the render — never skip it.

Log stage timing at entry/exit:
`python ../../tools/stage_timing.py start|end --project . --stage builder --run-id <id> --status <passed|failed>`.

## Anchoring cues — the exact convention (this is where builds fail)

`transcript.json` is the clock. Every cue lands on the spoken word it belongs to — never on an
assumed words-per-second offset. The mechanism:

1. Write `anchors.json` in the project: a map of cue name -> the exact spoken phrase it lands on,
   e.g. `{ "gateApproval": "approve the request", "softDelete30": "for 30 days" }`. **Match the
   words as the transcript actually has them** — Dragon HD transcribes numbers as DIGITS, so
   "thirty days" in the script is `"30 days"` in `transcript.json`. A phrase that does not match a
   transcript word leaves the cue UNRESOLVED (this is a real, recurring prep bug — fix the phrase in
   `anchors.json`, do not invent a numeric time).
2. Generate real times (an ambiguous phrase is an ERROR, not a silent first match — disambiguate
   with `"phrase #2"`):
   `python ../../tools/word_anchors.py transcript.json --spec anchors.json -o anchors.js --lead-in <lead>`
3. Load it before the timeline: `<script src="anchors.js"></script>`, then `const W = window.__anchors;`
4. Use `W.gateApproval` as a cue's position. **NEVER `B.b6 + 7.4`.**

`check_cue_anchors.py` classifies the POSITION ARGUMENT of every timeline call (switching to a raw
numeric literal does not fool it). It passes ONLY:
- `W.<name>` — a word-anchored time (use this for content cues)
- `B.b<n>` — a beat start (itself transcript-derived)
- an offset **<= 1s** off a beat/boundary — seam mechanics, relative to a boundary not to speech
- `0` — a t=0 pin

Anything larger is a DEFECT. If a line genuinely needs a bigger offset, justify it inline:
`// anchor-exempt: <reason>`. (The seam/bookend lines `assemble_scenes.py` generates already carry
that marker — you never add it to those, and you never edit the tool to add it.) Anchoring is
**per scene** in a modular build: a scene's cues anchor to words within that scene's window,
relative to the scene's own start.

## Custom scene contract (block scenes skip all of this — they are pre-built)

A `custom` body beat is authored on `templates/blocks/_foundation.css` as a SUB-COMPOSITION:
- root wrapped in `<template>`, styled via `#root` (never a class the stylesheet scopes away), with
  `data-width` / `data-height` on the root; all of `<style>`, `<script>`, markup live INSIDE the
  `<template>`;
- register its OWN scene-relative timeline on `window.__timelines["<scene-id>"]` — times measured
  from the scene's start, `fromTo` never `from` (the host re-seeks each scene when its slot shows);
- the slot's `data-composition-id`, the scene root's `data-composition-id`, and the timeline key
  must be IDENTICAL — a mismatch is invisible to lint/check, silently stalls the render, and only
  `check_subcomps.py` catches it;
- seams are HOST-owned: set the scene's `seam` field in `scenes.json`
  (`cut-left` default, `cut-right`, `cut-up`, `cut-down`, or `hard`) and re-assemble — never
  hand-author a cross-scene transition inside a scene file.

## Two failures lint/check CANNOT see — pin and verify

- **Initial state (`check_initial_state.py`).** Children inherit `opacity:1` and
  `immediateRender:false` defers the from-state, so an element is fully drawn the moment its beat
  opens — long before its cue — and beats ACCUMULATE (a recap never subtracts) while lint+check
  stay green. Pin every arriving element hidden at t=0:
  `["#a","#b"].forEach(s => tl.set(s,{opacity:0},0));` (use `{scaleX:0}` for bars/wipes).
- **Cue anchors (`check_cue_anchors.py`)** — the convention above.

## Scene density — fewer, richer scenes, never many thin ones

Resolve the numbers from the profile (`python ../../tools/profile.py <PROFILE>`), do not guess. Aim
for the profile's scene-count target (companion-short ~5 - unit-video ~10 - skilling-session ~23),
floor every scene at `scene_seconds.min` (fold a too-thin beat into its neighbour, do not cut to a
3-5s near-empty beat), and if the plan exceeds the cap, send it back rather than building it as is.

## Hard rules

- **Determinism:** no `Date.now()`, no unseeded `Math.random()`, no render-time network fetch. GSAP
  timelines are paused and registered on `window.__timelines`.
- **Audio is the clock:** if narration changes, transcript + every anchor are invalid — do not
  re-time against estimates.
- **Do not render** — the MP4 is produced locally. Do not add or commit `*.mp4`, `*.wav` you did
  not receive, or any `*.woff2` (Segoe is licensed and git-ignored; the cloud gate uses the
  fallback font by design).
- **Do not change** narration or palette; both are approved upstream.
- **`learn/tools/**` is READ-ONLY. Never edit the shared tools** (`assemble_scenes.py`,
  `check_*.py`, etc.) to make a gate pass — they are shared across every video and an edit here
  collides with every other branch. If a gate looks wrong, the composition is wrong, not the tool:
  fix your scene/`scenes.json`. A genuine tool bug is an escalation to the human, not a per-video
  patch. (The seam/bookend lines are already `// anchor-exempt` and the font `@font-face` is skipped
  when the woff2 is absent — you do not need to touch the tool for either.)
- **Touch ONLY your own project.** The only files a video build may add or change are under
  `learn/output/<slug>/` (plus the per-slug `learn/.gitignore` block the scaffolder wrote). Never
  stage anything under `packages/producer/tests/**` — those fixtures can appear "modified" as an
  LFS artifact; leave them alone. A CI scope gate fails any PR that reaches outside its project.
- **No scene-writer fan-out here.** The parallel `@hyperframes-scene-writer` path in the builder
  doctrine is a local VS Code feature — in the cloud you author every scene yourself, sequentially.
- **Stay on the `video/<slug>` branch.** One video per branch; never touch `main` or another
  video's `learn/output/*` folder.

## Done

Done means: chrome filled, body authored and inserted, `index.html` assembled, and **every gate
above green**. Then open/complete the pull request for this `video/<slug>` branch with the gate
results in the description. The local orchestrator pulls the branch and renders on real Segoe.
