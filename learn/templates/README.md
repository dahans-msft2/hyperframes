# HyperFrames Learn-ILT template kit

This folder is the Learn companion-video component kit. It is one registry: **kit blocks**.

## Kit blocks (`blocks/`)

Pre-built, pre-animated, on-brand sub-composition scenes — a finished, brand-correct, seek-safe
GSAP timeline per block, all built on the shared `blocks/_foundation.css` contract (one token set,
one cqw type scale, four grounds via `#root[data-ground]`, shared primitives).

The selection source of truth is `blocks/catalog.json`. Each entry defines the block's
`content_shape`, `best_for`, `avoid_when`, `default_ground`, and `config` — match a beat's teaching
relationship to those fields; don't treat the catalog as a style menu.

To use a block: copy `blocks/<id>.html` into `<project>/scenes/`, edit its `CONFIG` object, set
`data-ground` on `#root`, and add it to `scenes.json`. The file name = `data-composition-id` =
`window.__timelines` key = `<id>`.

## Custom scenes (the escape hatch)

When a beat's teaching relationship genuinely matches no block, it is authored as a **custom**
scene on the same `_foundation.css` foundation (same tokens, `--fs-*` scale, grounds, contrast
law). Prefer splitting or reframing the beat so a block fits; if you author the same custom shape
twice, promote it to a catalogued kit block instead.

> The six MD-102 transition archetypes were folded into the kit: `spotlight`→`stat-spotlight`/
> `title-hero`, `timeline`→`list-steps`, `blueprint`→`diagram-flow`, `catalog`→`list-select`,
> `layer-stack`→`diagram-layers`, `console`→`console-status`. There is no separate archetype pack.

## Scaffolding a project (batching many videos fast)

The MD-102 workflow copied whole project folders to batch videos. The drift-proof version is a
generator: `tools/new_project.py` stamps a fresh project from the LIVE kit + frozen assets + the
locked profile every run, so a folder can never go stale.

```
py tools/new_project.py --profile unit-video --title "…" --source "<learn url|uid>"
```

It bakes the INVARIANT and leaves the VARIANT empty:

- **Baked:** frozen fonts / grounds / gsap / AI end card; the required **chrome** scenes (bumper,
  title, objectives, recap, cta) stamped from the kit with `__FILL__` placeholder CONFIG; a
  `scenes.json` skeleton (chrome wired + a `body_slot`); a seeded Gate-2 ledger; a `BRIEF.md`.
- **Empty:** the teaching-body scenes, narration, and QA — authored per video by the gated pipeline.

The chrome definition (which block stamps each required element, its ground / seam / placeholders)
lives in `chrome.json`. Reference skeletons for each type live in `starters/<profile>/` (regenerate
with `--emit-starter`; binary assets are intentionally omitted — the generator copies them fresh).

Before render, `tools/check_placeholders.py --project <dir>` must be clean — no `__FILL__` may survive.
