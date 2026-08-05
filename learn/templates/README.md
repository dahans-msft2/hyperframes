# HyperFrames archetype templates

This folder is the reusable archetype pack for the Learn companion-video pipeline.

Use these fragments to start composition work from a known structure instead of writing every
beat layout from scratch.

## Included archetypes

| Archetype | Choose it when the meaning is carried by |
| --- | --- |
| `spotlight` | One payoff, conclusion, object, or metric |
| `catalog` | Peer items with one selected or emphasized |
| `layer-stack` | Nesting, containment, inheritance, or boundaries |
| `timeline` | Ordered state, timing, or cause and effect |
| `console` | Checks, statuses, request fields, or approvals |
| `blueprint` | Relationships, dependencies, ownership, or data flow |

The selection source of truth is `archetypes/manifest.json`. Each entry defines the content
shape, best uses, disqualifying conditions, weighted object, default ground, and an example
beat. Use those fields before choosing a fragment; don't treat the six as a style menu.

## Why this pack exists

The older MD-102 templates are useful, but they are dark-first and use legacy fonts. This pack
keeps the structural ideas and re-bases the fragments to the current Learn ILT system:

- light-mode friendly defaults
- Segoe UI / Segoe UI Semibold
- ink-first text colors
- no hard dependency on retired dark backgrounds

## Quick start

```bash
py tools/archetype_scaffold.py list
py tools/archetype_scaffold.py init --project <video-project-dir>
py tools/archetype_scaffold.py init --project <video-project-dir> --archetypes spotlight,timeline,console
```

The scaffold command copies selected archetype files into `<project>/_archetypes/` and writes a
local manifest.
