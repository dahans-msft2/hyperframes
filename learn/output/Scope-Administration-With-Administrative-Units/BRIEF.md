# Scope Administration with Administrative Units

- **Profile:** `unit-video` — Unit video (~4 min)
- **Target:** ~240s content (180–300s), word budget 435–726 (target 580) @ 2.42 w/s
- **Scenes:** aim ~10 (chrome 5 stamped + ~5-16 body)
- **Max static hold:** 5.0s   ·   **Voice:** en-US-Ava:DragonHDLatestNeural
- **Source:** C:\learn-pr\learn-m365-pr\learn-m365-pr\wwl\provision-govern-identities-entra\includes\7-scope-administrative-units.md

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
