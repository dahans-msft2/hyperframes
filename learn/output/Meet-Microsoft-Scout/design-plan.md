# Design plan — Meet Microsoft Scout

**Preset:** learn-ilt · **Profile:** companion-short
Chrome is already scaffolded (bumper, title, objectives, recap, cta). Body = 3 teaching beats.
Dark-field is spent **once**, on the trust beat (its gravitas earns it).

## Per-beat plan

| # | Scene id | Kit block | Ground | Focal / config | Seam in |
|---|----------|-----------|--------|----------------|---------|
| 01 | `01-bumper` | `bumper` (brand) | hero-swoosh | kicker: **Microsoft 365** | — |
| 02 | `02-title` | `title-hero` | hero-swoosh | title: "Meet / Microsoft Scout"; subtitle: "Your always-on personal agent" | cut-left |
| 03 | `03-objectives` | `list-steps` (chrome) | content-wash | 3 chips: **What it is** · **What it does** · **In your control** | cut-left |
| 04 | `04-what-it-is` | `callout-note` | section-field | label **NEW CATEGORY**, term **Autopilot**, body: always-on agent, own identity, acts on your behalf — grounded in Microsoft 365 | cut-left |
| 05 | `05-what-it-does` | `list-specs` | content-wash | 4 capability rows — Schedule / Deliverables / Meetings / Risks (see below); Work IQ as caption | cut-left |
| 06 | `06-trust` | `diagram-layers` | **dark-field** | concentric protection: outer **Your permissions & policies** → **Microsoft Purview** → **Governed Entra identity** → core **Scout acts** | cut-up |
| 90 | `90-recap` | `title-hero` (chrome) | hero-swoosh | recap payoff line | cut-up |
| 91 | `91-cta` | `title-hero` (chrome) | hero-swoosh | CTA: preview via Frontier | cut-left |
| — | endcard | AI disclosure clip | — | mandatory final clip | — |

## Beat 05 capability rows (`list-specs`)
- **Schedules** — meetings across time zones
- **Protects time** — blocks focus time for deliverables you owe
- **Surfaces signal** — flags the meetings that matter
- **Catches risk** — spots stalled decisions before they block

## Notes for the builder
- `04` spends `section-field` as the one segment-opener cool ground; `06` spends the single `dark-field`. No other scene uses either.
- `list-specs` label/value rows carry the four capabilities; keep Work IQ in the caption, not a 5th row.
- `diagram-layers` auto-inverts to white ink on dark-field — never hardcode white.
- Anchor every beat start + in-scene cue to `transcript.json` word times.
