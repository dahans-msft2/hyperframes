---
name: learn-video-delivery
description: "The deliverables contract and render-time gotchas for Microsoft Learn companion videos — the mandatory AI disclosure end card, caption and transcript requirements, output naming and folder layout, handoff manifests, and the render pitfalls that silently break output (re-render dropping the outro, VTT offset drift, fonts, working directory). Use when rendering, packaging, publishing, or handing off a video, or when a rendered output is missing its end card or has desynced captions."
---

# Learn Video Delivery

What ships, in what shape, and the render-time traps that quietly break it.

## The deliverable set

Every video ships four artifacts:

| Artifact | Notes |
|---|---|
| `<slug>.mp4` | H.264. Composition renders at 1920×1080; deliverable may be downscaled per destination |
| `<slug>.vtt` | WebVTT captions — **mandatory**, not optional |
| `<slug>_thumbnail.png` | matched to the video's own hero frame |
| manifest row | title, profile, duration, learning path / module / unit, AI-generated flag |

Output root: `learn/output/<Video-Title>/`. Renders land in `renders/`; the
packaged deliverable set is promoted from there. Never treat `renders/` as the ship point.

Transcripts are required alongside captions — the playbook's accessibility rule asks for both,
and anything conveyed visually must also reach the viewer via audio or text.

## The AI disclosure end card

**Mandatory on every video.** Missing it is a rubric disqualifier and a violation of the
playbook's per-type mandatory-elements table.

- Asset: `assets/AI_End_Card.mp4` — 1920×1080, 30 fps, **10.667 s**, white ground, **no audio stream**
- This is the **only** copy in the repo, by design. A ~17× compressed "normalized" variant (silent
  AAC track, ~394 kbps, visibly degraded) once sat beside it for the retired ffmpeg-concat flow.
  It was deleted: authoring the card into the composition re-encodes anyway, so the normalized
  copy could only ever double-compress. Nothing to choose between means nothing to get wrong.
- Its lack of an audio track is an **advantage** — no silent stream fighting the narration mix.

**Author it in; never concatenate it on.** As the final clip in the composition it survives
re-render by construction, the check becomes a static assertion, and caption timing accounts
for it natively with no concat offset.

Static assertions:
1. the outro block is present
2. it is the **last** clip
3. its end == root `data-duration` (no trailing gap)

**Seam exemption.** The cut into the end card is a terminal hard stop, not a narrative beat.
Mark that ledger row exempt or `seam-gate.mjs` flags the final boundary as a dead beat or
mirrored vector. Record the exemption so nobody later "fixes" it into a violation.

**Open question.** The playbook lists "AI disclosure" **and** "logo end card" as two elements.
Our single card carries the disclosure wordmark. Whether a separate Microsoft logo card is also
required is unresolved — confirm before a publish run.

## Render gotchas

These were all learned the hard way on the predecessor corpus.

**Run the render from the project directory.** `Set-Location '<dir>'; npx hyperframes render`.
The terminal tool strips `cd` from piped or backgrounded commands, and a render started from
the wrong cwd fails in confusing ways.

**Embed fonts.** Nothing is fetched at render time. `@font-face` from the project's own
`fonts/` — a system-font lookup is not deterministic and drifts between machines.

**Audio detection needs a plain `id` and `src`** on the `<audio>`/`<video>` element.

**Timing:** `data-start` + `data-end` on clips; root `data-duration` **caps total length**. If
the root duration is short, the tail is silently truncated — including the end card.

**Caption offset.** A composition whose audio has `data-start="2"` puts composition time at
WAV time + 2.0. VTT cues must carry the same offset. This desync is easy to miss because the
first cue looks fine.

**Re-renders invalidate downstream artifacts.** Historically a fresh render dropped the outro
and left stale captions. Authoring the outro in fixes half of that; captions must still be
regenerated after every render, not reused.

**Multi-line PowerShell COM gets mangled** by the terminal tool. Put PowerPoint/COM work in a
`.ps1` and invoke the file.

## Pre-delivery checklist

- [ ] `hyperframes check` passes — lint, runtime, layout, WCAG contrast
- [ ] `seam-gate.mjs` exits 0 (end-card row exempt)
- [ ] Rubric ≥ 18, every criterion ≥ 3, **zero disqualifiers**
- [ ] End card present, last clip, ends at root `data-duration`
- [ ] Captions regenerated from the **current** transcript, offset verified against `data-start`
- [ ] Transcript shipped
- [ ] Duration inside the locked profile's bounds
- [ ] Thumbnail generated from the video's own frame
- [ ] Manifest row written
- [ ] Fonts embedded, not system-resolved

## Handoff

Manifests are generated, never hand-edited — regenerate when renders or titles change. The
predecessor pipeline's manifest shapes (WIT bulk-create rows, PSOT rollup, published-video
catalogue) remain the target formats; the `AIGenerated` flag is `TRUE` and
`VideoProductionType` records the toolchain.
