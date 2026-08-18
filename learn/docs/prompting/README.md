# Vendored: HyperFrames prompting guides

33 authoring guides copied verbatim from the upstream HyperFrames docs site
(`docs/prompting/` in `heygen-com/hyperframes`), vendored here so an agent working in this
repository can consult them **without a network fetch** — the public docs site is not readable
from inside a private repo, and the upstream repo is not a dependency of this pipeline.

**Licence.** HyperFrames is Apache License 2.0. These files are redistributed unmodified under
that licence; copyright remains with the HyperFrames authors. See the upstream `LICENSE`.

**These are craft guidance, not law.** Where any of them states a palette, typography, or
house-style preference, the `learn-*` doctrine skills win — see the precedence rule in
`learn-brand-doctrine`. Read them for *technique*: how to specify, what vocabulary changes output,
which failure modes recur.

They retain MDX syntax (`import`, JSX components) from the docs site. Prose reads fine; ignore the
component tags.

## Highest-value entries for this pipeline

| File | Why it matters here |
|---|---|
| `specification-dial.mdx` | How much to specify. *"Density never hurts — a stronger model just uses less of its own taste."* The single best guide for the author interview |
| `vocabulary.mdx` | The exact words that turn a mood into a specific framework setting |
| `data-and-maps.mdx` | **Read before any map or data scene.** Factual visuals are sourced, never generated |
| `rules-and-anti-patterns.mdx` | Recurring failure modes |
| `visual-specs.mdx`, `storyboards.mdx` | Turning a beat plan into an implementable spec |
| `motion.mdx` | Deep motion craft — subordinate to `motion-doctrine` where they disagree |
| `iterating.mdx`, `recreating-references.mdx` | Revision loops and matching a reference |
| `rendering-and-output.mdx` | Output settings and formats |

## Refreshing

These are a **snapshot**, not a live mirror. To update, re-copy from upstream `docs/prompting/`
and diff — do not edit in place, or the next refresh silently discards local changes.
