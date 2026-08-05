# MD-102 archetype compatibility audit

Date: 2026-08-04

## Scope

Audited legacy templates from:
`MD-102-Refresh-Working/md102-companion-videos/templates/`

Reviewed templates:
- blueprint
- console
- layer-stack
- spotlight
- timeline
- dashboard (used as input pattern for catalog)

## Findings

1. Legacy templates are dark-first and not aligned to current Learn ILT light-mode defaults.
2. Legacy templates use non-brand fonts (`Space Grotesk`, `JetBrains Mono`, `Fraunces`).
3. Legacy templates do not include the mandatory AI end card clip in composition markup.
4. Legacy token sets are tuned for dark grounds and cannot be copied directly into the
   current contrast law without rework.

## Result

A new six-archetype reusable pack was created under this folder with light-mode defaults and
Segoe-centric typography:

- spotlight
- catalog
- layer-stack
- timeline
- console
- blueprint

`catalog` is a derived archetype that combines useful list-surface structure from legacy
console and dashboard patterns, but is re-based to current brand constraints.

## Use

Use `py tools/archetype_scaffold.py init --project <dir>` to copy the selected archetypes into
`<project>/_archetypes/`.
