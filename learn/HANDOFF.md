# HANDOFF — Microsoft Learn companion-video pipeline, re-homed into this fork

**Written:** 2026-08-05 · **Repo:** `C:\Dev\repos\hyperframes` (fork `dahans-msft2/hyperframes`, push access)
**Branch:** `feature/learn-video-fork-phase0` (5 commits, **local only — NOT pushed**)

You are picking up a session that was running in a multi-root workspace; it's now handed off to
this single-root fork window. **A chat session can't transfer between windows**, so this file +
memory notes carry the context.

## First: read these
- Repo memory: `/memories/repo/hyperframes-fork-learn.md` (Phase-0 findings, verified facts).
- User memory: `/memories/vscode-agent-sandbox.md` (the sandbox fix — applies to ALL your projects).
- This file (the plan + status).

---

## The goal (decided with the user)

The Learn companion-video pipeline used to live in `learning-lab-agents` and felt **overengineered**
— a thin, bespoke re-build of what upstream HyperFrames already does better, *except for branding*.
Decision: **re-home it into this fork (Option C — hybrid), fully SELF-CONTAINED.**

- **Keep** upstream's engine: the 132 registry blocks, motion-doctrine skills
  (`.agents/skills/{motion-doctrine,cut-the-curve,oversized-cursor,seam-craft}`), and the CLI.
- **Bring in ONLY the Learn delta**, copied INTO the fork (never referenced across repos):
  brand preset, doctrine skills, contrast/rubric/caption/end-card tools, Dragon HD TTS.
- **Keep** the 7 `.agent.md` orchestrator agents but rewire them as thin Learn wrappers over the
  upstream skill roles (they have NO upstream equivalent). *(Not started — Phase 1+.)*
- **HARD CONSTRAINT — self-contained:** the pipeline must not reference `learning-lab-agents`.
  Learn skills go in `.github/skills/` (fork-owned, OUTSIDE the `.agents/skills` sync set so
  `hyperframes skills update` can't clobber them). Copy assets/tools in with fork-relative paths.
- **Verification approach:** command reliability (fixed, see below), narration/table-read gates,
  builder batching, then build "Video 3" as an end-to-end proof.

---

## STATUS: Phase 0 is COMPLETE. All green, all committed (local).

Commits on `feature/learn-video-fork-phase0` (newest first):
```
23348a22  remove misdirected .vscode sandbox setting (real fix is user-level; see below)
23c85dc9  Phase 0-C  port learn-narration-doctrine skill; Dragon HD smoke test passed
57457d65  Phase 0-B  CSS backdrop-filter glass on-brand (check 46/46 AA); WebGPU glass FAILS gate
c6930e59  Phase 0-A  real upstream data-chart block restyled on-brand (check 89/89 AA)
2c802dbf  Phase 0    learn-ilt brand preset + on-brand cut-the-curve spike (lint+check clean)
```
Nothing is pushed. `learning-lab-agents` self-containment gate PASSED (opening the fork single-root
loads zero learning-lab-agents skills).

### What Phase 0 proved
1. **Core gate:** an on-brand Learn composition (warm gradient ground + mandatory dither, ink text,
   Segoe, a cut-the-curve seam) passes `lint` + `check` incl. WCAG AA, self-contained in the fork.
2. **A — real upstream blocks go on-brand:** `hyperframes add data-chart` works self-contained;
   rebrand = edit the block's LITERAL hex/fonts (it ignores its own `--bg-color` param). Removed its
   render-time Google Fonts fetch (determinism). → check 89/89 AA.
3. **B (big finding) — upstream WebGPU/html-in-canvas glass blocks FAIL the Learn gate:** their text
   is composited into a canvas → INVISIBLE to the contrast audit (the Learn brand's core check); and
   their vendored lib path breaks under sub-comp mount (`LiquidGlass is not defined`). ⇒ Build Learn
   "WOW" with **CSS `backdrop-filter` glass + DOM/SVG/GSAP**, NOT WebGPU blocks. Proven at
   `phase0-glass-css` → check 46/46 AA.
4. **C — narration reaches:** Dragon HD (Ava) produced a 5.4s WAV; `az` identity is a user; skill ported.

### Files created (this fork)
- `learn/frame-presets/learn-ilt/FRAME.md` — the Learn brand preset (grounds, contrast law,
  typography, glass band, dither). Real reusable deliverable.
- `learn/spikes/phase0-spike/` — cut-the-curve seam spike (index.html + frame.md + hyperframes.json).
- `learn/spikes/phase0-block/` — the restyled real `data-chart` block.
- `learn/spikes/phase0-glass-css/` — the CSS glass band (the correct Learn glass idiom).
- `.github/skills/learn-narration-doctrine/SKILL.md` — ported narration doctrine.

---

## Environment / gotchas (verified — save yourself the churn)

- **CLI:** `bun` is NOT installed and the fork's own CLI isn't built (`packages/cli/dist` missing).
  Use the pinned published CLI: **`npx --yes hyperframes@0.7.77 <verb>`**. (Building the fork's own
  CLI — install bun + build — is a Phase-1 follow-up for full self-containment.)
- **Sandbox (SOLVED):** the "every command re-runs" tax was VS Code's agent sandbox. Root cause:
  `chat.agent.sandbox.enabledWindows: "on"` (flipped on by an experiment) using a backend gated
  behind velocity flags not enabled here → `E_NOTIMPL`. **Fix applied to USER settings:**
  `"chat.agent.sandbox.advanced.windows.schemaVersion": "0.4.0-alpha"` (mature AppContainer backend).
  Verified working live. If this new window still throws `E_NOTIMPL`, **Developer: Reload Window**.
- **File tools never hit the sandbox** — only terminal commands do. Author freely with edit tools.
- **.gitignore traps:** `*-brand/` (line 151) silently ignores any dir ending `-brand` — DON'T name
  Learn dirs that way. `.vscode/` (line 29) is ignored. CRLF→LF warnings on commit are benign.
- **Composition contract:** root `#root` needs `data-composition-id`, `data-start="0"`,
  `data-width/height`, `data-duration`; visible timed elements need `class="clip"` AND must be
  DIRECT children of root (put an inner wrapper INSIDE the clip to transform); set initial transforms
  via `gsap.set` (NEVER CSS transform → `gsap_css_transform_conflict`); one paused
  `gsap.timeline` on `window.__timelines["<id>"]`; GSAP 3.14.2 CDN; no render-time network fetches.
  OS fonts need `@font-face { src: local("Segoe UI Semibold"), local("Segoe UI"); }` or lint fails.
- **`preview`** is a long-running server — run it from INSIDE a project dir, don't pipe it through
  `Select-Object` (hides the URL). It prints `http://localhost:<port>`.

---

## NEXT — Phase 1 (vendor the Learn delta), then 2–5

1. **Phase 1 — port the rest of the Learn delta into the fork (self-contained):**
   - Brand assets: copy the ground PNGs, fonts (Segoe woff2), icons, and `AI_End_Card.mp4` from
     `learning-lab-agents/video/hyperframes-scripts/{assets,brand}` into the fork; rewrite paths.
   - Doctrine skills → `.github/skills/`: `learn-video-doctrine`, `learn-brand-doctrine`,
     `learn-instructional-doctrine`, `learn-video-rubric`, `learn-video-delivery` (narration already done).
     De-dupe: their "route to motion-doctrine" now points at THIS fork's `.agents/skills` copies.
   - Net-new tools → `learn/tools/`: `contrast_gate.py`, mandatory AI-end-card injection, caption
     lexicon + `make_vtt`, rubric scorer, and the Dragon HD TTS (`azure_tts.py` + `make_ssml.py` from
     `learning-lab-agents/video/hyperframes-scripts/tools`, with the fixed-wrapper gotchas). Azure
     Speech + Entra `az login` stay an ENV prerequisite (never vendor credentials).
   - The 7 `.agent.md` agents → `.github/agents/`, rewired to upstream frame-worker / general-video
     companion roles + registry blocks + motion-doctrine (builder/scene-writer), Learn preset (designer),
     Learn pedagogy+rubric (script-writer/qa).
   - Audit the bespoke verification: KEEP only Learn-specific checks (contrast, dead-zone, table-read,
     reveal-order, end-card, caption lexicon, rubric); DROP generic ones upstream `lint`/`check` covers.
2. **Phase 2 — command reliability:** single entrypoint = `npx hyperframes` (+ thin wrapper); the
   sandbox fix above already removes the re-run tax.
3. **Phase 3 — narration/table enforcement:** add gates — table-read detector (narration overlapping
   on-screen table text), dead-zone detector (content reveal >2s after scene start), SSML list cadence.
4. **Phase 4 — builder batching + checkpoint:** upstream frame-worker wave dispatch (2–3 scenes/worker)
   + a `build-progress.json` so a silent death loses one batch, not the run; snapshot-check per batch.
5. **Phase 5 — build Video 3** end-to-end as the proof; score vs the 20-pt rubric (≥18, every criterion
   ≥3, zero disqualifiers); measure re-run rate, dead zones, table-reads, WOW.

### Later goal (after Video 3)
Build OUR OWN Learn-branded registry blocks that are flashier / more-featured — as **DOM/CSS/SVG/GSAP**
blocks (use `#id` selectors, not `[data-composition-id]`), NOT ports of upstream WebGPU blocks (they
fail the gate — see finding B).

---

## To resume in this window
```
git -C C:\Dev\repos\hyperframes log --oneline -6        # confirm you're on the branch with 5 Phase-0 commits
cd C:\Dev\repos\hyperframes\learn\spikes\phase0-spike
npx --yes hyperframes@0.7.77 preview                # eyeball the on-brand spike + cut-the-curve seam
```
Then start Phase 1. Delete this HANDOFF.md when you no longer need it.
