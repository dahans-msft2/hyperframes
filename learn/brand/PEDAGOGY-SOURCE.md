# Pedagogy source of truth — extracted, not paraphrased

Extracted 2026-08-03 by `tools/extract_deck_text.py`. Raw output: `_extract/playbook.json`.

**Source**: `MD-102-Refresh-Working/md102-companion-videos/_source/ilt-templates/Video Content Playbook Synthesia.pptx` (58 slides)

None of this existed anywhere in the codebase before extraction — a grep for
`signaling|contiguity|redundancy|Mayer|cognitive load|instructional design` across
`md102-companion-videos` returned **zero hits**.

---

## Slide 5 — Best Practices to Create Effective Educational Videos

| Best Practice | Considerations |
|---|---|
| Define the Training Goal and Audience | Understand who the learners are and what you want them to learn or do |
| Choose the Right Type of Video | Select the style that will communicate the content most clearly |
| Plan and Script the Content | Scripting helps keep the video concise and not forget crucial steps |
| Storyboard the Visuals | Describe what will be on screen for each segment of the script |
| Record the Video Content | Use both the visuals and audio narration to show, not just tell |
| Edit and Enhance the Video | Editing is crucial; Add titles, include visuals, zoom or highlight, adjust audio |
| Add Interactivity and Publish | Incorporate knowledge checks and prompt active engagement from learners |

## Slide 6 — Instructional Design Principles

**Focus on Learner Needs**
- Use terminology the learners know (or explain it when introduced)
- Address learners specific use cases
- Explain why the topic matters and how it solves the learner's problem

**Set Clear Objectives and Expectations**
- State what learners will learn or be able to do
- All content in the video should support these objectives

**Segment Content to Manage Cognitive Load**
- Content must be well-structured
- Chunk content into bite-sized segments or steps
- Use clear transitions or sections for each subtopic or task

**Apply Multimedia Principles** — Coherence · Signaling · Modality · Spatial Contiguity
> Speaker note: *"See slides on Richard Mayer's Principles of Multimedia Design for the full 12 multimedia principles"*

## Slide 7 — Instructional Design Principles (continued)

**Ensure Accessibility and Inclusion**
- Include closed captions
- Provide transcripts
- Important information conveyed visually must be communicated via audio or text
- Avoid cultural references or humor
- Consider localization for multilingual audiences

**Encourage Active Learning**
- Find ways to make learners engage mentally (i.e. ask a reflective question)
- Embed a quick quiz or clickable interaction if the platform allows it

**Feedback and Assessment**
- Give the correct answer and explanation in clickable interactive videos
- Collect learner feedback to improve future iterations

**Continuous Improvement**
- Monitor metrics (completion rates, etc.)
- Apply an iterative design mindset

## Slides 8–9 — Richard Mayer's 12 Principles of Multimedia Design

| Principle | Statement (verbatim) |
|---|---|
| Coherence | Humans learn best when extraneous, distracting material is not included |
| Signaling | Humans learn best when they are shown exactly what to pay attention to on the screen |
| Redundancy | Humans learn best with narration and graphics, as opposed to narration, graphics, and text |
| Spatial Contiguity | Humans learn best when relevant text and visuals are physically close together |
| Temporal Contiguity | Humans learn best when corresponding words and visuals are presented together, instead of in consecutive order |
| Segmenting | Humans learn best when information is presented in segments, rather than one long continuous stream |
| Pre-Training | Humans learn more efficiently if they already know some of the basics |
| Modality | Humans learn best from visuals and spoken words than from visuals and printed words |
| Multimedia | Humans learn best from words and pictures than just words alone |
| Personalization | Humans learn best from a more informal, conversational voice than an overly formal voice |
| Voice | Humans learn best from a human voice than a computer voice |
| Image | Humans do not necessarily learn better from a talking head video. (If there is important information to be learned, relevant visuals on the screen will be more effective than showing a talking head of an instructor.) |

Source cited in speaker notes: *How to Use Mayer's 12 Principles of Multimedia Learning [Examples Included] — Water Bear Learning*

---

## Slide 14 — Video Types for Learn Modules (the type taxonomy)

**Mandatory elements for EVERY type**: Script · voiceover · graphics + animations ·
**AI disclosure** · **logo end card**
**Optional for every type**: Presenter

| Video Type | Learning Objective | Recommended Learn Unit |
|---|---|---|
| Introduction to Product/Feature | Highlight the key functionalities and benefits of a new product or feature | Introduction, Concept |
| Walkthrough of a Process | Step-by-step guide through a specific process, showcasing each action and its purpose | Concept, Exercise |
| Explanation of a Technical Concept | Simplify and explain complex technical concepts | Concept, Exercise |
| Case studies / Use cases | Present real-world examples or scenarios showcasing the application of a product, feature, or concept | Introduction, Concept, Prepare |
| Architecture and Design Patterns | Focus on how to structure applications, services, or systems using best practices and design patterns | Concept, Exercise |
| Troubleshooting Tips | Provide solutions to common issues and how to troubleshoot them | Concept, Exercise |

> Speaker note: *"More video types can be included, as necessary."*

This is the authoritative source for the **profile registry** — and it independently confirms
the AI disclosure + logo end card rule as mandatory, matching the rubric disqualifier.

Note it lists **two** closing elements — "AI disclosure" *and* "logo end card". Our single
`AI_End_Card.mp4` carries the disclosure wordmark; whether a separate Microsoft logo card is
also required is **unresolved** and should be confirmed before shipping.

## Slide 20 — Video Structure (the canonical required structure)

```
Opening scene    → Learn bumper · Video title · Learning objectives
Scenes 1–8       → Scenarios · icons, animation, stock footage, subtitles
Closing scene    → Refresh on what was learned · Call to Action (Learn more link)
End slide        → AI disclosure + MS logo end card
```

This is the source for rubric **C4 (Structure & flow)** automation and for each profile's
`required structural elements`.

## Slide 24 — Brand Guidance and Visuals

> Use the **Microsoft Learn primary color palette** for illustrations, icons, glyphs, and diagrams

Referenced sources: Microsoft Learn Style Guide · Microsoft Learn illustrations ·
**Microsoft Learn Figma File** · WWL Learning Lab icons · WWL Learning Lab diagrams.
Adaptable: Microsoft IconCloud · Fluent Icon Collections · Azure Course Blueprints.
Speaker note also permits screenshots, screen recordings, images, and stock video footage.

See `BRAND-SOURCE.md` § "two brand authorities" — this is a different authority from the .potx
theme and has not yet been reconciled.

---

## How this maps into the doctrine

| Extracted | Lands in |
|---|---|
| Slides 6–9 principles | `learn-instructional-doctrine` |
| Mayer Redundancy + Modality | narration vs. on-screen text rules — **directly contradicts heavy on-screen text** |
| Mayer Signaling | the case for `signaling` motion; ties to `motion-doctrine` carriers |
| Mayer Segmenting + "chunk into bite-sized segments" | profile `segmentation` requirements, rubric C5 |
| Mayer Personalization + Voice | `learn-narration-doctrine` — conversational tone; the **Voice principle is in tension with TTS** and must be acknowledged, not hidden |
| Mayer Image | justifies the faceless/graphics-led house style over a talking head |
| Slide 7 accessibility | captions + transcripts are mandatory, not optional; feeds the rubric disqualifier |
| Slide 14 types | the profile registry |
| Slide 20 structure | rubric C4 + per-profile required elements |

**Note the Voice-principle tension**: Mayer says humans learn best from a human voice rather
than a computer voice, while the entire pipeline is Azure TTS. This is a known, accepted
trade-off — Dragon HD voices are the mitigation. It should be stated openly in the doctrine
rather than quietly dropped, because it is a real cost of the approach.
