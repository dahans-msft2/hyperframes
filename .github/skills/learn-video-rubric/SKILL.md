---
name: learn-video-rubric
description: "The ship/no-ship gate for Microsoft Learn videos — a 20-point, five-criterion scorecard with four hard disqualifiers, parameterized by video-type profile so short companions and long skilling sessions are judged against different bounds but the same bar. Use whenever scoring, reviewing, or approving a video; before spending on TTS; before rendering; before delivery; or when asked whether a video is ready to publish, is a winner, or needs revision. Carries the automatable checks and the human-judgment split."
---

# Learn Video Rubric — the gate

Version 2026-04-27. This is a **gate**, not a document — the same move `motion-doctrine` makes
with `seam-gate.mjs`. It runs twice: once **before TTS spend**, once **before render**.

Render and delivery are **blocked** unless:

> **total ≥ 18 · every criterion ≥ 3 · zero disqualifiers**

Below the bar, report the criterion-level gap and iterate. Do not ask permission to ship short.

## The four disqualifiers — no format is exempt

A video with any of these cannot ship or win, regardless of score.

1. On-screen **typo** in key terms or product names
2. **Factual or technical inaccuracy**
3. **Missing required disclosure / end card**
4. **Accessibility blocker** — unreadable text, failing contrast

## The five criteria (1–4 each, /20)

| # | Criterion | Level 4 | Level 3 (minimum acceptable) |
|---|---|---|---|
| 1 | **Instructional effectiveness** *(most important)* | Clear objective up front; accurate, audience-appropriate, easy to follow; strong signposting; closing recap of key takeaways | Objective present and mostly clear; accurate and understandable with minor gaps; recap present or implied |
| 2 | **Use of video as a medium** — *"could this have been a PDF?"* | Visuals change with narration; highlights/animation guide attention; on-screen content adds value beyond reading | Mostly leverages video; some static moments but format is justified |
| 3 | **Visual communication & multimedia principles** | Redundancy/signaling/contiguity applied well; minimal readable text; well-timed visuals; zero typos | Mostly strong; minor layout/timing issue or a very minor non-critical typo (still must be fixed before publish) |
| 4 | **Structure & flow** | Logical sequence, clear sections, template elements present and polished, intentional transitions | Mostly logical; minor omission or small bumper/title timing issue |
| 5 | **Length & pacing** | Within recommended length **for the video type**; brisk, no wasted time, well-sized segments | Slightly over/under but still efficient |

**Scoring rules.** Score each issue in the **single most relevant** criterion — never
double-penalize. An incoherent explanation is a Criterion 1 problem, not also a Criterion 5 one.

**Interpretation.** 18–20 publish as-is / winner-eligible · 15–17 minor revision ·
11–14 major revision · 5–10 reject.

**Brand note (transition period).** Until the Microsoft Neutral style guide is finalized, do not
heavily penalize minor brand differences. **Do** require internal consistency — one visual
system throughout.

## Profiles: vary the inputs, never the bar

Criterion 5 Level 4 says "within recommended length **for the video type**" and the scorecard
carries a `Video Type` field. The rubric defers to a per-type recommendation it never supplies.
Profiles supply it — `learn/profiles/`.

**Type-sensitive** (thresholds come from the locked profile):

- **C5** length and pacing — the obvious one
- **C4** structure — a 20-minute session needs chapters; a 90-second companion does not
- **C2** dead-zone tolerance — **the main trap.** Short-form thresholds applied to a demo-heavy
  skilling session would falsely fail it. Screen-recording and demo segments are exempt where
  the profile says so.
- **C1** — universal in substance; "objective + recap" scales to per-chapter in long form

**Type-invariant** — never relaxed:

- **C3** visual communication
- All four **disqualifiers**
- The /20 scale and the 18 / all-≥3 / zero-disqualifier bar

A profile mismatch between routing and the scorecard is a **hard error**.

## Automatable vs human

Every threshold reads from the locked profile — never a hardcoded constant.

| Rubric item | Check |
|---|---|
| Accessibility / contrast | `hyperframes check` WCAG + `tools/contrast_gate.py` |
| Missing disclosure / end card | **static**: `learn-ai-disclosure-outro` present, is the **last** clip, ends at root `data-duration` |
| Typo in key terms / product names | product-name lexicon (`content-linter` prior art) |
| Factual inaccuracy | source-anchored fact-check pass |
| **C2 "could this have been a PDF?"** | `animation-map.mjs` **dead-zone detection** — static stretches *are* the PDF failure mode |
| C4 structure + transitions | required chrome blocks present + `seam-gate.mjs` exit 0 |
| C5 length & pacing | root `data-duration` + narration WPM against profile bounds |
| C1 instructional effectiveness | human / LLM against `learn-instructional-doctrine` |
| C3 beyond contrast | human / LLM + snapshot review |

The C2 mapping is the good one: the rubric's sharpest question is already a runnable check.

## Scorecard format

```
Video          <title>
Profile        <profile>            Length  mm:ss  (bounds: mm:ss–mm:ss)
Evaluator      <agent | name>       Date    YYYY-MM-DD

C1 Instructional effectiveness   [ ]/4
C2 Use of video as a medium      [ ]/4
C3 Visual communication          [ ]/4
C4 Structure & flow              [ ]/4
C5 Length & pacing               [ ]/4
                          TOTAL  [ ]/20

Disqualifiers  none | <list>
Verdict        PUBLISH | MINOR | MAJOR | REJECT

Top strengths (2–3, what to replicate)
Top fixes (2–3, highest score impact)
```

Call out disqualifiers **explicitly**, even when the total looks healthy — a 19/20 with a typo
in a product name does not ship.

## Scoring the existing corpus

The rubric also runs **backward**. Scoring the 44 already-shipped MD-102 videos with the same
gate turns layout keep/rebuild/cut arguments into measurements — a layout that consistently
scores low on C2 is a rebuild candidate with a number attached, not a matter of taste.
