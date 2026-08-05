---
name: learn-instructional-doctrine
description: "Instructional design law for Microsoft Learn companion videos — Richard Mayer's 12 principles of multimedia design, the WWL best-practice sequence, cognitive-load segmentation, accessibility requirements, and the video-type taxonomy. Use when planning what a video teaches and in what order, writing a beat plan or storyboard, deciding how much text belongs on screen, choosing a video type, or reviewing whether content is instructionally sound. These rules SUPERSEDE generic content and storytelling guidance for Learn training video."
---

# Learn Instructional Doctrine

Extracted verbatim from the *Video Content Playbook* (slides 5–9, 14, 20). Full source:
`learn/brand/PEDAGOGY-SOURCE.md`.

None of this existed in the codebase before extraction — a grep for
`signaling|contiguity|redundancy|Mayer|cognitive load` across the predecessor video work
returned zero hits. Forty-four videos shipped without it.

## Mayer's 12 principles — the operative law

| Principle | Statement |
|---|---|
| **Coherence** | Humans learn best when extraneous, distracting material is not included |
| **Signaling** | Humans learn best when shown exactly what to pay attention to on screen |
| **Redundancy** | Humans learn best with narration + graphics, **as opposed to** narration + graphics + text |
| **Spatial Contiguity** | Relevant text and visuals should be physically close together |
| **Temporal Contiguity** | Corresponding words and visuals presented together, not consecutively |
| **Segmenting** | Information in segments, not one long continuous stream |
| **Pre-Training** | Learners do better if they already know some of the basics |
| **Modality** | Visuals + **spoken** words beat visuals + printed words |
| **Multimedia** | Words + pictures beat words alone |
| **Personalization** | Informal, conversational voice beats overly formal |
| **Voice** | A human voice beats a computer voice |
| **Image** | A talking head does **not** necessarily help; relevant on-screen visuals beat a presenter |

### The three that most change how you author

**Redundancy + Modality together forbid the default instinct.** The reflex is to put the
narration on screen as bullets. Mayer says that is *worse* than narration + graphics alone.
On-screen text should be **labels, not transcripts** — a few anchoring words, not the sentence
being spoken. This is the single most common failure in training video.

**Signaling is why motion exists here.** Motion is not decoration; it is the mechanism that
directs attention. This is where instructional doctrine hands off to `motion-doctrine` —
carriers and causal motion *are* signaling, implemented.

**Image justifies the house style.** A faceless, graphics-led video is not a budget compromise.
Mayer says relevant visuals outperform a presenter when there is real information to convey.
Presenter is listed as *optional* in the playbook's own type table for exactly this reason.

## The best-practice sequence

1. Define the training goal and audience — who they are, what they should learn or do
2. Choose the right type of video for the content
3. Plan and script — scripting keeps it concise and prevents dropped steps
4. Storyboard the visuals — what is on screen for each segment of script
5. Record — **show, don't just tell**; use visuals *and* narration
6. Edit and enhance — titles, visuals, zoom or highlight, audio balance
7. Add interactivity and publish — knowledge checks, active engagement

## Design principles

**Focus on learner needs** — use terminology they know or explain it on introduction; address
their actual use cases; explain *why it matters* and what problem it solves.

**Set clear objectives** — state what they will learn or be able to do. Every element in the
video must support those objectives. Anything that doesn't is a Coherence violation.

**Segment to manage cognitive load** — well-structured content, chunked into bite-sized
segments or steps, with clear transitions between subtopics. Long formats need explicit
chapters; short formats need clean beat boundaries.

**Accessibility is mandatory, not optional** — closed captions, transcripts, and anything
conveyed visually must also reach the viewer through audio or text. Avoid cultural references
and humour. Consider localization.

**Encourage active learning** — a reflective question, a prediction, a quick check.

## Engagement — pull the learner through (Veritasium method)

Mayer keeps cognitive load low; he does not make anyone *want* to watch. A video can be
perfectly coherent and still be dry. Derek Muller's (Veritasium) engagement method is the
complement — it earns and holds attention. Use both: Mayer is **subtractive** (cut the noise),
Muller is **motivational** (create the pull).

**The levers** — add the ones a script is missing; a few strong ones beat ten gimmicks:

1. **Curiosity gap first.** Lead the body with a question, puzzle, or surprising claim the
   learner *wants* resolved — not a definition or a feature list. Create the itch before the
   scratch, inside the first ~15–30 seconds of content.
2. **Need-to-know before the answer.** Establish the problem and the stakes before the
   solution: "here's the painful thing that happens without this — now here's the fix." Don't
   answer a question the learner was never made to ask.
3. **Why-care, early and concrete.** Tie it to the learner's actual job in the opening, not a
   dutiful aside at the end. (This upgrades "open with why" from a line into a hook.)
4. **Question-driven arc.** Each beat ends by opening the next question, so the video reads like
   a story with tension and resolution, not a flat agenda. Withhold, build, deliver — never
   front-load the conclusion.
5. **Concrete before abstract.** Lead with a vivid, specific scenario; generalize to the concept
   afterward. Story and specifics before taxonomy and definitions.
6. **Predict before reveal.** Before a demo, a result, or a screen recording, prompt a
   commitment — "what do you think happens when…?" A reveal without a prediction teaches little.
   Where it fits, let a wrong guess stay on screen and have reality contradict it; the
   contradiction *is* the lesson.
7. **Productive-failure loop (where earned).** Let the learner guess, be wrong safely, see the
   gap, then re-apply the corrected model on a fresh case. Wrong answers are the mechanism, not
   a fail state.
8. **Cognitive conflict (sparingly).** Only where the learner holds a strong, specific wrong
   prior — surface it and let reality break it. One tool, never the headline; never manufacture a
   misconception that isn't real.

**Reconcile with the required structure — don't fight it.** The mandatory opening (bumper, title,
objectives) still ships; the rubric scores it. Engagement changes *how* it lands: lead the body
with the curiosity gap, and frame the objectives as **stakes** ("what breaks without this")
rather than a dry checklist. The hook serves the objective, never replaces it — and it must be
honest, because the video has to pay off the tension it raises. And engagement has a budget too:
don't bury the content under hooks, quizzes and callouts.

**For a focused pass, invoke the skills** (both *propose*, they don't rewrite): `veritasium-video`
generates candidate hooks, predict-before-reveal beats, and a mystery-structured outline for a
script; `veritasium-learn` reframes and resequences a unit's structure into a question-driven arc.

## Video types (the taxonomy)

Mandatory for **every** type: script · voiceover · graphics + animations · **AI disclosure** ·
**logo end card**. Optional for every type: presenter.

| Type | Objective | Learn unit |
|---|---|---|
| Introduction to Product/Feature | Key functionality and benefits of something new | Introduction, Concept |
| Walkthrough of a Process | Step-by-step through a process, each action and its purpose | Concept, Exercise |
| Explanation of a Technical Concept | Simplify and explain something complex | Concept, Exercise |
| Case studies / Use cases | Real-world scenarios applying a product or concept | Introduction, Concept, Prepare |
| Architecture and Design Patterns | How to structure applications, services, systems | Concept, Exercise |
| Troubleshooting Tips | Common issues and how to resolve them | Concept, Exercise |

More types may be added as needed — but a new type inherits the mandatory elements.

## The required structure

```
Opening   → Learn bumper · video title · learning objectives
Body      → scenes; scenarios, icons, animation, subtitles
Closing   → recap of what was learned · call to action (Learn more link)
End card  → AI disclosure + Microsoft logo
```

The opening is where **objectives** are stated and the closing is where they are **recapped**.
Both are structural requirements, not stylistic choices — the rubric scores their absence.

## Beat-planning heuristics

- One idea per beat. If a beat needs "and", it is two beats.
- Visual changes **with** the narration, not after it (Temporal Contiguity).
- Labels near the thing they label (Spatial Contiguity).
- If a stretch of video has no visual change, it has become a PDF — the rubric measures this
  directly as dead-zone detection.
- Cut anything that does not serve a stated objective. Coherence is a subtraction principle.

## The honest tension

Mayer's **Voice** principle says a human voice beats a computer voice, and this pipeline is
Azure TTS end to end. Dragon HD voices narrow the gap; they do not close it. State the
trade-off rather than pretending the principle doesn't apply.
