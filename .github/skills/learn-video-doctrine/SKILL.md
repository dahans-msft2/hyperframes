---
name: learn-video-doctrine
description: "GATEWAY — load FIRST before authoring, reviewing, or rendering any Microsoft Learn companion video in HyperFrames. Routes every decision to the skill that owns it: motion to the upstream motion-doctrine family, brand to learn-brand-doctrine, pedagogy to learn-instructional-doctrine, ship/no-ship to learn-video-rubric, voice to learn-narration-doctrine, and deliverables to learn-video-delivery. Also carries the non-negotiables that apply to every Learn video regardless of format: the mandatory AI disclosure end card, the required video structure, captions and transcripts, and the profile lock. Use whenever someone says make a Learn video, companion video, skilling session, unit video, or asks whether a video is ready to ship."
---

# Learn Video Doctrine (Gateway)

Read this before anything else. It decides **which skill owns which decision**, and it carries
the rules that hold for every Learn video no matter its format.

These rules supersede generic upstream *brand* and *pedagogy* guidance. They do **not**
supersede upstream **motion** guidance — see the routing table.

## Route map

| Decision | Skill |
|---|---|
| Motion, seams, transitions, choreography, performance | **`motion-doctrine`** (vendored) → `cut-the-curve`, `seam-craft`, `oversized-cursor`, `captions-overlay` |
| Colour, ground, type, chrome, layout | `learn-brand-doctrine` |
| What to teach, in what order, at what density | `learn-instructional-doctrine` |
| Engagement, hook, curiosity gap, narrative arc | `veritasium-video` (script), `veritasium-learn` (structure) |
| Is it good enough to ship | `learn-video-rubric` |
| Voice, pacing, tone, pronunciation | `learn-narration-doctrine` |
| Deliverables, captions, handoff, manifests | `learn-video-delivery` |
| Composition contract, `data-*`, determinism, Tailwind | `hyperframes-core` (vendored) |
| Animation runtimes, adapters, scene blueprints, transitions, seek-safe keyframes | `hyperframes-animation` (vendored) |
| `frame.md` handling, composition patterns, beat planning | `hyperframes-creative` (vendored) |
| Scene components | the **Learn-ILT kit** — `templates/blocks/catalog.json`; upstream mechanics in `hyperframes-registry` (vendored) |
| TTS + SSML + transcription + icons | repo tools: `tools/azure_tts.py`, `tools/make_ssml.py`, `npx hyperframes transcribe`, `tools/icon_index.py` (voice selection: `learn-narration-doctrine`) |
| CLI, lint, check, render | `hyperframes-cli` (vendored) |

**`motion-doctrine` is adopted whole and unmodified.** Its vector law, vector ledger,
carriers, causal motion, `seam-gate.mjs` build gate and no-idle-wobble rules are the motion
law here too. Brand never overrides motion; motion never overrides brand. They are orthogonal.

**This gateway is the router.** The upstream `/hyperframes` router skill is deliberately not
installed — it competes for the same "make me a video" intent and knows nothing about the
Learn brand, the rubric, or the profile lock. Route from this table instead. Upstream
*creation workflows* (`product-launch-video`, `faceless-explainer`, `pr-to-video`,
`music-to-video`, `slideshow`, `talking-head-recut`, `embedded-captions`) are likewise not
installed; none of them describes a Learn companion video.

Where an upstream domain skill states a palette, typography, or house-style preference, this
family wins — see the `frame.md` precedence rule in `learn-brand-doctrine`.

---

## The non-negotiables

These hold for **every** Learn video — short companion, long skilling session, motion graphic,
anything.

### 1. The AI disclosure end card is mandatory

Every video ends with it. No exceptions, no formats exempt.

Authority: the Video Content Playbook's video-type table lists **"AI disclosure"** and
**"logo end card"** as mandatory elements for *all six* video types. The evaluation rubric
lists a missing disclosure/end card as a **disqualifier**.

- Asset: `learn/assets/AI_End_Card.mp4` — 1920×1080, 30 fps, 10.667 s,
  white ground, no audio stream.
- Only one copy of the card exists in the repo. A ~17× compressed "normalized" variant was
  deleted along with the ffmpeg-concat flow it served.
- **Author it into the composition** as the final clip. Do not concatenate it after render.
  Post-hoc concat is why re-renders used to drop it.
- The seam into it is a terminal hard stop, not a narrative beat. Mark that ledger row exempt
  or `seam-gate.mjs` will fail the final boundary. See `learn-video-delivery`.

### 2. The required structure

From the playbook's canonical structure:

```
Opening   → Learn bumper · video title · learning objectives
Body      → scenes; scenarios, icons, animation, subtitles
Closing   → recap of what was learned · call to action (Learn more link)
End card  → AI disclosure + Microsoft logo
```

Long formats add chapters inside the body. Short formats do not. The profile decides.

### 3. Captions and transcripts are mandatory

Not a nice-to-have. The playbook's accessibility section requires closed captions **and**
transcripts, and information conveyed visually must also reach the viewer via audio or text.
Unreadable text or failing contrast is a rubric **disqualifier**.

### 4. The profile is locked at routing time

Every video declares a **profile** (`companion-short`, `skilling-session`, `motion-graphic`, …)
before authoring starts. The profile supplies length bounds, pacing, required structure,
dead-zone tolerance, and which automated checks run at what threshold.

Thread it to every downstream agent, exactly like a template lock. **A mismatch between the
routed profile and the profile on the scorecard is a hard error, not a warning.**

Profiles live in `learn/profiles/`.

---

## Review surfaces

Studio is the review surface, not an optional extra. Three distinct states — do not confuse them:

| Surface | Command | Gate it serves |
|---|---|---|
| **Review ledger** | `py tools/review_index.py build --project <dir>` → `review/index.html` | every gate — the audit trail of what was decided and why |
| **Voice audition** | `py tools/audition_voices.py --from-script script.md` | voice lock, before any TTS spend |
| **Storyboard board** | `npx hyperframes preview` → `?view=storyboard#project/<name>` | design-plan approval, *before* the composition is built |
| **Snapshot sheet** | `npx hyperframes check --snapshots` | build self-check — annotated overview frames + crops of every finding |
| **Final composition preview** | `npx hyperframes preview` → `#project/<name>` | render approval, after `check` passes |

Rules:

- **The storyboard board is not approval of the video.** It approves the plan. Treating a board
  sign-off as a render sign-off is how an unreviewed composition reaches TTS spend.
- **`check` must pass before the final preview is offered.** `check` reruns lint itself — never
  prepend a standalone `lint` call to it.
- **Never render merely because checks pass.** Pause at the final preview and wait for an
  explicit human approval. Checks prove the composition is *valid*, not that it is *good* —
  that judgment is the rubric's and the reviewer's.
- **Sub-compositions need a smoke test.** Static audit cannot catch a mount failure. Where
  `index.html` mounts `data-composition-src`, run `npx hyperframes snapshot --at <t1>,<t2>,<t3>`
  and treat tiny unstyled content, canvas-sized icons or registration timeouts as
  render-blocking.
- **Use one `HYPERFRAMES_RUN_ID`** across every command in a single verification loop, and
  prefer `--json` for agent calls.

### Studio-directed edits

When the reviewer says "change *this*" while Studio is open, query the selection rather than
guessing which element they mean:

```bash
npx hyperframes preview --context --json --context-fields selection
```

Use `selection.target.hfId`, falling back to its selector and source file. On `no-selection`,
ask the reviewer to click the element and rerun. This is the intended revision path for
visual feedback — it removes the round of "which box did you mean?" that otherwise eats a gate.


### 5. Vary the inputs, never the bar

The rubric is /20 across five criteria. A 20-minute skilling session and a 75-second companion
are judged against *different length bounds and different dead-zone tolerances* — but **both**
must reach 18/20 with every criterion ≥ 3 and zero disqualifiers.

---

## One system, many expressions

The failure this doctrine was built to prevent is off-brand drift. The failure it *caused* was
the opposite: every beat of every video looking identical, because the only guidance on offer
was a list of prohibitions and a single recipe. **Both are failures. Neither is the goal.**

Split every visual decision into two layers and treat them differently:

| | | |
|---|---|---|
| **The system** — invariant | Palette, type, contrast law, chrome and identity, the AI end card, the three frame obligations (ground plane / depth / object with weight) | Never varies. Not per beat, not per video, not per learning path. |
| **The expression** — free | Layout, composition, art direction, motion recipe, whether a beat uses a generated asset at all | **Expected** to vary — beat to beat and video to video. |

A beat that looks different from the beat before it is not off-brand. A beat that uses a
colour, a typeface, or a contrast level outside the system *is*. Judge those separately, and
never reach for uniformity as a proxy for consistency.

The 44 predecessors ran many layouts — blueprint, console, dashboard, spotlight,
timeline, editorial, drafting, layer-stack. **Keep that range.** What they lacked was one
system underneath. Do not solve that by collapsing the range.

**Per-beat art direction is sanctioned** inside the system. A beat may be composed to its own
content rather than poured into a template — the brand is held by palette, type and contrast,
not by every frame sharing a layout.

## Craft — do not re-derive what upstream already carries

This doctrine governs *what is on brand*. It says almost nothing about what makes motion,
light, rhythm and composition **good**, and it should not try to — that knowledge already
exists upstream and is more complete than anything restated here. Load it.

| Need | Go to |
|---|---|
| Motion principles, easing, weight, follow-through | `hyperframes-animation` → `references/motion-principles.md` |
| Atomic motion recipes to compose per scene | `hyperframes-animation` → `rules-index.md` (compose 2–4) |
| Whole-scene choreography | `hyperframes-animation` → `blueprints-index.md`, `techniques.md` |
| Kinetic type and text effects | `hyperframes-animation` → `adapters/animate-text.md` |
| Framing, balance, negative space, focal hierarchy | `hyperframes-creative` → `references/composition-patterns.md`, `video-composition.md` |
| Beat rhythm and pacing across a film | `hyperframes-creative` → `references/beat-direction.md`, `story-spine.md` |
| Style and mood vocabulary | `hyperframes-creative` → `references/visual-styles.md`, `design-picker.md` |
| Type systems | `hyperframes-creative` → `references/typography.md` |
| Charts, counters, data that moves | `hyperframes-animation` → `rules/stat-bars-and-fills`, `references/data-in-motion.md` |
| Continuity, seams, the film's current | `motion-doctrine` → then `cut-the-curve`, `seam-craft` |
| Sourcing or generating media | repo tools — `tools/icon_index.py` (icons); generate media only where a beat earns it |

**Where upstream craft and this doctrine disagree, this doctrine wins on brand — palette,
type, contrast, chrome — and upstream wins on craft.** They rarely actually conflict. A rule
that says "give the frame depth" and a rule that says "no accent-coloured body text" are
answering different questions.

---

## Order of work

0. **Preflight** — `pwsh -File learn/tools/preflight.ps1`. Do this
   **before** the script gate, not before the render. It costs seconds and it is the difference
   between finding a missing FFmpeg now and finding it after a render has captured every frame.
   First time on a machine? Run `@platform-setup-check` (Checks 21–23) instead — it covers the
   whole platform, not just this pipeline.
1. **Route** — pick the profile; lock it.
2. **Source** — resolve the Learn unit / module / topic.
3. **Design** — `learn-brand-doctrine` + the `learn-ilt` frame preset for the **system**;
   `hyperframes-creative` composition and style references for the **expression**. Choose a
   kit block (or a custom layout) per beat, not one for the video.
4. **Plan** — `learn-instructional-doctrine` for beats and density.
5. **Script** — `learn-narration-doctrine` for voice and pacing.
6. **Build** — `hyperframes-core` + `motion-doctrine`, composing from
   `hyperframes-animation` rules rather than inventing motion.
7. **Gate** — `learn-video-rubric` before spending on TTS, and again before render.
8. **Deliver** — `learn-video-delivery`.

Assets are **not** a fixed stage. Resolve them with the repo tools (`tools/icon_index.py` for icons;
generated media only where a beat earns it) — see the asset policy in `learn-brand-doctrine`. Most
beats will not need one.

Gates 7 is where work stops if the score is short. Report the criterion-level gap and iterate;
do not ask permission to fall below the bar.

## Known tensions — state them, don't hide them

- **Mayer's Voice principle** says humans learn better from a human voice than a computer
  voice. This pipeline is Azure TTS. Dragon HD voices are the mitigation, not a refutation.
  Acknowledge the trade-off honestly rather than pretending it away.
- **Two brand authorities exist.** The ILT deck theme governs ground and chrome; the playbook
  points illustrations, icons and diagrams at the Microsoft Learn primary palette. They appear
  consistent but have not been formally reconciled. See `learn-brand-doctrine`.
