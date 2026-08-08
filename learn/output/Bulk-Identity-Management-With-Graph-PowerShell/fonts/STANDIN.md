# LOCAL GATE STAND-IN — NOT SEGOE UI. DO NOT RENDER WITH THESE.

`segoeui-regular.woff2` / `segoeui-semibold.woff2` in this folder are **Noto Sans**, built
locally so `npx hyperframes check` could evaluate real text metrics, layout, and WCAG contrast
in a Linux container that has no Segoe UI and no network access to Selawik.

Noto Sans is *wider* than Segoe UI, so a layout that clears the gate here also clears it with
the real face — the check is conservative, not optimistic.

Both files are gitignored (`learn/.gitignore` -> `fonts/*.woff2`) and are never committed.

**Before rendering, regenerate the real faces on the render host:**

    py tools/sync_fonts.py --css        # Windows: converts the licensed system Segoe UI
    # non-Windows: install Selawik (SIL OFL, metric-compatible) per the learn-ilt preset
