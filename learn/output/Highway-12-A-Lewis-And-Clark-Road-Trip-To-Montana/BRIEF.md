# Highway 12: A Lewis and Clark Road Trip to Montana

- **Profile:** `skilling-session` — Skilling session
- **Target:** ~1050s content (900–1200s), word budget 2178–2904 (target 2541) @ 2.42 w/s
- **Scenes:** aim ~23 (chrome 5 stamped + ~18-55 body)
- **Max static hold:** 8.0s   ·   **Voice:** en-US-Ava:DragonHDLatestNeural
- **Source:** NPS Lewis & Clark National Historic Trail (nps.gov/lecl); US-12 Northwest Passage Scenic Byway / Lewis-Clark Highway; NPS Glacier NP; historical route WA I-90 to Vantage, south to Lewiston-Clarkston, US-12 over Lolo Pass to Missoula, Flathead Lake, Glacier

## Fill the placeholders

Every `__FILL__` below must be replaced before render (guarded by `tools/check_placeholders.py`).

- `opening.bumper` → [scenes/01-bumper.html](scenes/01-bumper.html)
- `opening.title` → [scenes/02-title.html](scenes/02-title.html)
- `opening.objectives` → [scenes/03-objectives.html](scenes/03-objectives.html)
- `closing.recap` → [scenes/90-recap.html](scenes/90-recap.html)
- `closing.cta` → [scenes/91-cta.html](scenes/91-cta.html)

## Next steps

1. Write the script + beat plan (script-writer) and fill the chrome placeholders above.
2. Author the teaching-body scenes into `scenes/` and insert them into `scenes.json` between the opening and closing chrome (see `scenes.json` → `body_slot`).
3. Run the gated pipeline (voice → fact-check QA → build → snapshot QA → render).
4. Guard: `py tools/check_placeholders.py --project .` must be clean before render.
