---
name: learn-block-adoption
description: "How to bring an UPSTREAM HyperFrames registry block (382 published items) into the Learn-ILT kit and re-brand it, instead of hand-authoring a scene from scratch. Use when no kit block in templates/blocks/catalog.json matches the content shape you need — a map, a timeline, a comparison table, a device mock, a shader transition, a 3D reveal. Covers discovery, install, the token remap recipe, the brand-conformance gate, justified exemptions, and when to promote an adopted block into the kit. Read BEFORE authoring a custom scene: adoption is the middle path between a kit block and bespoke HTML."
---

# Adopting an upstream block into the Learn-ILT kit

There are **three** ways to make a scene. Most doctrine only tells you about two.

| Path | When | Cost |
|---|---|---|
| 1. **Kit block** | `templates/blocks/catalog.json` already has the content shape | Lowest — edit CONFIG |
| 2. **Adopt upstream** ← *this skill* | The shape exists in the **registry** but not the kit | Low — install + remap tokens |
| 3. **Author custom** | Genuinely novel shape, or the material is factual/bespoke | Highest |

**Always check path 2 before falling to path 3.** The registry publishes **382 items** — charts, maps,
device mocks, code windows, lower-thirds, shader transitions, 3D reveals, liquid-glass surfaces. Hand-
authoring something the registry already solved is the single most common waste in this pipeline.

`chart-bar.html` in the kit *is* the upstream `data-chart` block, adopted and re-branded. This skill is
that process, written down.

---

## 1. Discover

The CLI resolves the registry from the public upstream repo — you do **not** need the hyperframes repo
checked out, and you do not need our fork:

```
https://raw.githubusercontent.com/heygen-com/hyperframes/main/registry
```

```bash
npx hyperframes@<pinned> catalog            # browse blocks + components
npx hyperframes@<pinned> catalog --search map
```

Pin `<pinned>` to `learn/config.json` → `cli.published_version`.

> **The registry tracks `main`, not your pinned CLI version.** A block can change upstream under you.
> That is exactly why adoption ends in **vendoring** a copy into the kit (step 5) rather than
> referencing the registry at build time.

## 2. Decide it is actually the right shape

Match on **content relationship**, not on looks — the same rule the kit catalog uses:

- enumerated rows → `list-`   · nodes + relationships → `diagram-`
- one big number → `stat-`    · multi-point data → `chart-`
- real geography / place → a map block, **and see the fidelity rule below**

**Fidelity rule (non-negotiable).** If the block renders anything *factual* — geography, a real
quantity, a timeline of real events — the block supplies the **presentation**; you still supply
**sourced data**. Never accept a block's decorative sample geometry as fact, and never generate
factual geometry from an image model. Consult `learn/docs/prompting/data-and-maps.mdx` before
building any map or data scene.

## 3. Install into a scratch project

Adopt in a throwaway project first, never straight into `learn/templates/blocks/`:

```bash
npx hyperframes@<pinned> init _scratch && cd _scratch
npx hyperframes@<pinned> add <block-id>
```

Then read the block: what is CONFIG-driven, what is hardcoded, what its timeline does, and whether it
mounts as a sub-composition.

## 4. Re-brand — the remap recipe

**First decide which KIND of adoption this is.** Getting this wrong is the main way adoption goes
badly, and the reporter's finding count is the tell:

| Kind | Signature | What you do |
|---|---|---|
| **Surface remap** | Findings are scattered literals over a neutral layout — a chart, a list, a panel | Swap values for tokens, in place. The recipe below |
| **Mechanism transplant** | The block carries a whole competing *visual system* — its own dark chrome, its own window frame, a display typeface it ships as an asset | Keep the **mechanism** (the timeline, the diff logic, the layout maths); rebuild the **chrome** on the kit, or on the nearest existing kit block |

Two live examples:

- `data-chart` → `chart-bar` was a **surface remap**: neutral chart, literals swapped for tokens.
- `code-diff` is a **mechanism transplant**: 29 distinct colours that are a *coherent GitHub-dark
  theme* (`#e1e4e8` ×36, dark syntax palette, macOS traffic-light buttons). Tokenising it one hex at
  a time produces a Learn-coloured imitation of someone else's design system. The right adoption is
  to take its **diff mechanics** — added/removed line treatment, the reveal timeline — onto the kit's
  existing `code-window`.
- `hw-pipeline` should be **rejected outright**: it is a hand-drawn flowchart that ships a Caveat
  handwriting font. It conflicts with Learn typography and duplicates `diagram-flow`. Not every
  registry block is adoptable — say so and move on.

> **Signal:** many findings concentrated in one coherent palette = transplant. Scattered one-off
> literals = remap. A high count alone does not decide it; look at whether the colours agree with
> each other.

### The remap recipe (surface remap)

Run the reporter to get the complete sweep. Do not eyeball this; a missed hardcoded colour survives
every other gate and only breaks when a host swaps the ground:

```bash
py learn/tools/brand_conformance.py _scratch/blocks/<block-id>.html
```

It audits the five foundation rules and, for every hardcoded colour, names the **nearest** token.
Then apply judgment — nearest is a hint, not an answer:

| Upstream pattern | Becomes | Note |
|---|---|---|
| Body / heading colour | `var(--ink)` / `var(--ink-soft)` | **All** text. No exceptions except syntax highlighting |
| Chart series, bars, strokes, chips | `var(--accent)` … `var(--accent-4)` | Graphics only |
| Card / panel fill | `var(--paper)` or `var(--paper-veil)` | Veil over a busy ground |
| Page background, gradient | **delete it** | The host picks the ground via `#root[data-ground]` |
| `font-size: 32px` | `var(--fs-h3)` etc. | Never px — the cqw scale keeps type above the `--fs-micro` floor |
| `font-family: Inter/Roboto/...` | delete, or compose `.ilt-title` / `.ilt-body` / `.ilt-caption` | Inherit Segoe from `#root` |
| Radius / shadow literals | `var(--radius)`, `var(--shadow)` | |

**Choose by ROLE, not by nearest hue.** A muted blue may be numerically closest to `--accent-3`
(teal) while semantically belonging to `--accent-2` (blue). The reporter says "confirm the ROLE"
for exactly this reason.

**Structural edits** the same pass:

1. Paste `_foundation.css` **verbatim** between the `BEGIN`/`END` markers at the top of `<style>`.
2. Rename so **file stem = `data-composition-id` = `__timelines` key**, using `<category>-<variant>`.
3. Delete any self-hiding exit animation on `#root` — the host owns scene lifetime.
4. Keep the timeline **paused** and registered on `window.__timelines[...]`.
5. Strip render-time network fetches (CDN scripts, remote JSON). Vendor what it needs, or extract
   the data offline and embed it. Several registry blocks fetch d3/topojson from a CDN at runtime —
   that violates determinism and **must** be removed, not merely tolerated.

## 5. Verify — three gates, in order

```bash
py learn/tools/brand_conformance.py <block>.html   # source: 0 errors
npx hyperframes@<pinned> check                     # rendered: contrast, layout, runtime, motion
npx hyperframes@<pinned> snapshot --at <t>         # eyes: does it read as Learn?
```

Then **prove the ground swap**, which is the whole point of tokenizing: render it under
`data-ground="dark-field"`. Ink flips to white automatically. Anything that stays dark was a
hardcoded colour the sweep missed.

## 6. Justified exceptions

Some values genuinely must not be tokenized. Declare them inline — a bare exception is a finding,
the reason is the point:

```html
<!-- brand-exempt: Microsoft logo squares are a fixed corporate mark, never themed -->
```
```css
color: var(--accent); /* brand-exempt: syntax highlighting — colour IS the information */
```

Legitimate: fixed corporate marks, semantic colour (error red), syntax highlighting, a neutral media
letterbox. **Not** legitimate: "it looked better", or the block's original palette.

A standalone exemption comment covers the run of lines beneath it, to a blank line.

## 7. Promote into the kit — only on the second use

Leave an adopted block in the project the first time. When you reach for the **same shape twice**,
promote it:

1. Copy to `learn/templates/blocks/<category>-<variant>.html`.
2. Add a `catalog.json` entry: `id`, `category`, `summary`, `content_shape`, `best_for`,
   `avoid_when`, `default_ground`, `config`, `file`.
3. Note the upstream origin in the block's header comment (as `chart-bar` does for `data-chart`) —
   provenance makes future upstream diffs possible.
4. Confirm `brand_conformance.py` is clean across the whole kit, not just the new file.

Upstream is **Apache 2.0** — vendoring is permitted; retain attribution.

## Anti-patterns

- **Hand-authoring a shape the registry already publishes.** Check `catalog` first.
- **Adopting without the sweep.** Contrast can pass while the block is riddled with literals; it
  breaks on the first ground swap.
- **Trusting nearest-colour.** It is a hint. Roles are semantic.
- **Keeping a CDN fetch.** Deterministic render forbids it. Extract offline and embed.
- **Promoting on first use.** One-offs belong in the project.
- **Treating a block's sample data as fact.** Presentation is adopted; data is sourced.
