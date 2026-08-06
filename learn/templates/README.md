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
