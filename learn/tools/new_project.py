#!/usr/bin/env python3
"""Scaffold a fresh, doctrine-compliant Learn video project folder for a locked profile.

The MD-102 workflow templated whole copyable project folders to batch videos fast. This is the
evolved, drift-proof version: instead of copying a stale folder, it STAMPS a fresh one every run
from the live kit blocks + frozen assets + the locked profile. What it bakes is the INVARIANT
(frozen fonts/grounds/gsap/end card + the required chrome scenes wired into scenes.json with
`__FILL__` placeholder CONFIG); what it leaves empty is the VARIANT (the teaching body, narration,
QA). The gated pipeline then runs unchanged, so quality is preserved — the template removes
boilerplate, never a checkpoint.

    py tools/new_project.py --profile unit-video --title "Explore quantum entanglement with Q#"
    py tools/new_project.py --profile companion-short --title "..." --source https://learn.microsoft.com/...
    py tools/new_project.py --profile unit-video --emit-starter   # regenerate the reference skeleton

Chrome is defined declaratively in templates/chrome.json; only elements in the profile's
`required_elements` are stamped. The end card is injected by assemble_scenes.py from
scenes.json.endcard, so it is not a scene file.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
LEARN = TOOLS.parent
sys.path.insert(0, str(TOOLS))
import profile as profile_mod  # noqa: E402  (tools/profile.py — profile resolver)

BLOCKS = LEARN / "templates" / "blocks"
CHROME_JSON = LEARN / "templates" / "chrome.json"
CONFIG_JSON = LEARN / "config.json"
FONTS_SRC = LEARN / "fonts"
GROUNDS_SRC = LEARN / "assets" / "grounds"
GSAP_SRC = LEARN / "assets" / "vendor" / "gsap.min.js"
ENDCARD_SRC = LEARN / "assets" / "AI_End_Card.mp4"

FILL = "__FILL__"


def slugify(title: str) -> str:
    words = re.findall(r"[A-Za-z0-9]+", title)
    return "-".join(w[:1].upper() + w[1:] for w in words) or "Untitled"


def stamp_block(block_html: str, block_id: str, scene_id: str, ground: str, config: dict) -> str:
    """Copy a kit block into a scene: rename ids, set ground, swap in placeholder CONFIG."""
    html = block_html
    # File name = data-composition-id = window.__timelines key = <scene id>.
    html = html.replace(f'data-composition-id="{block_id}"', f'data-composition-id="{scene_id}"')
    html = html.replace(f'window.__timelines["{block_id}"]', f'window.__timelines["{scene_id}"]')

    # Normalize the root div's data-ground: omit for content-wash (the default), else set it.
    root_re = re.compile(r'(<div\s+id="root"\b[^>]*?)(>)', re.S)
    m = root_re.search(html)
    if m:
        tag = re.sub(r'\s+data-ground="[^"]*"', "", m.group(1))
        if ground and ground != "content-wash":
            tag = tag.replace(
                f'data-composition-id="{scene_id}"',
                f'data-composition-id="{scene_id}" data-ground="{ground}"',
            )
        html = html[: m.start(1)] + tag + html[m.end(1) - 1 : ]

    # Replace the block's `var CONFIG = { ... };` with the placeholder config (valid JS: JSON literal).
    literal = json.dumps(config, indent=2, ensure_ascii=False)
    literal = "\n".join((("          " + ln) if i else ln) for i, ln in enumerate(literal.splitlines()))
    replacement = "var CONFIG = " + literal + ";"
    new_html, n = re.subn(r"var CONFIG = \{.*?\n\s*\};", lambda _: replacement, html, count=1, flags=re.S)
    if n == 0:
        raise SystemExit(f"error: no `var CONFIG = {{...}};` found in block {block_id!r} — cannot stamp {scene_id}")
    return new_html


def resolve_duration(dur: dict, scene_target: float, scene_min: float) -> float:
    if "seconds" in dur:
        return round(float(dur["seconds"]), 2)
    return round(max(scene_min, scene_target * float(dur["fraction_of_scene_target"])), 2)


def copy_asset(src: Path, dst: Path, warnings: list) -> None:
    if not src.exists():
        warnings.append(f"missing source asset {src} — not copied (regenerate before render)")
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def _git(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(LEARN), *args], capture_output=True, text=True)


def emit_gitignore_negation(slug: str) -> bool:
    """Append a per-slug negation to learn/.gitignore so THIS one project's source is trackable
    (renders + heavy artifacts stay ignored). Idempotent. Lives on the video branch, never merged
    to main — so main's blanket `output/` ignore, and every other local-only video, stay untouched."""
    gi = LEARN / ".gitignore"
    marker = f"# --- cloud handoff: {slug} ---"
    text = gi.read_text(encoding="utf-8") if gi.exists() else ""
    if marker in text:
        return False
    block = "\n".join([
        "",
        marker,
        "# Source of this video's composition is tracked so the cloud builder can hand it back;",
        "# renders + heavy artifacts stay local-only. Never merged to main.",
        "!output/",
        "output/*",
        f"!output/{slug}/",
        f"!output/{slug}/**",
        "# ignore render OUTPUTS only — keep input media (end card, screen recordings) tracked",
        f"output/{slug}/renders/",
        f"output/{slug}/{slug}.mp4",
        f"output/{slug}/{slug}_thumbnail.png",
        "",
    ])
    gi.write_text(text.rstrip("\n") + "\n" + block, encoding="utf-8")
    return True


def ensure_video_branch(slug: str, warnings: list) -> str:
    """Create/switch to video/<slug>. Non-fatal on any git problem (warns with the manual command)."""
    branch = f"video/{slug.lower()}"
    if _git("rev-parse", "--git-dir").returncode != 0:
        warnings.append(f"not a git repo — create the branch yourself: git checkout -b {branch}")
        return branch
    exists = _git("rev-parse", "--verify", "--quiet", branch).returncode == 0
    r = _git("checkout", branch) if exists else _git("checkout", "-b", branch)
    if r.returncode != 0:
        warnings.append(f"could not switch to {branch}: {(r.stderr or r.stdout).strip()} — do it manually")
    return branch


def main() -> int:
    ap = argparse.ArgumentParser(description="Scaffold a Learn video project folder for a profile.")
    ap.add_argument("--profile", required=True, help="video-type profile (see tools/profile.py)")
    ap.add_argument("--title", help="video title (required unless --emit-starter)")
    ap.add_argument("--source", help="Learn unit/topic URL, UID, or local path (records Gate 1)")
    ap.add_argument("--out", help="output dir (default: output/<slug>)")
    ap.add_argument("--emit-starter", action="store_true",
                    help="write a committable reference skeleton to templates/starters/<profile>/ (no binary assets)")
    ap.add_argument("--force", action="store_true", help="overwrite a non-empty output dir")
    ap.add_argument("--cloud", action="store_true",
                    help="prepare for cloud handoff: create the video/<slug> branch and track this "
                         "project's source (renders stay git-ignored)")
    args = ap.parse_args()

    try:
        p = profile_mod.resolve(args.profile)
    except KeyError as err:
        print(err, file=sys.stderr)
        return 1

    cfg = json.loads(CONFIG_JSON.read_text(encoding="utf-8"))
    chrome = json.loads(CHROME_JSON.read_text(encoding="utf-8"))

    if args.emit_starter:
        title = args.title or f"{p['label']} — starter skeleton"
        out = LEARN / "templates" / "starters" / args.profile
        copy_assets = False
    else:
        if not args.title:
            print("error: --title is required (unless --emit-starter)", file=sys.stderr)
            return 1
        title = args.title
        out = Path(args.out) if args.out else (LEARN / "output" / slugify(title))
        copy_assets = True

    if out.exists() and any(out.iterdir()) and not args.force:
        print(f"error: {out} exists and is not empty (use --force to overwrite)", file=sys.stderr)
        return 1

    warnings: list[str] = []
    base_dirs = ["scenes", "assets/grounds", "assets/vendor", "fonts"]
    if not args.emit_starter:
        base_dirs.append("review")
    for sub in base_dirs:
        (out / sub).mkdir(parents=True, exist_ok=True)

    # --- frozen boilerplate (fresh copies for render determinism) ---
    if copy_assets:
        for woff2 in sorted(FONTS_SRC.glob("*.woff2")):
            copy_asset(woff2, out / "fonts" / woff2.name, warnings)
        for png in sorted(GROUNDS_SRC.glob("*.png")):
            copy_asset(png, out / "assets" / "grounds" / png.name, warnings)
        copy_asset(GSAP_SRC, out / "assets" / "vendor" / "gsap.min.js", warnings)
        copy_asset(ENDCARD_SRC, out / "assets" / "AI_End_Card.mp4", warnings)
    else:
        (out / "assets" / "README.md").write_text(
            "Starter skeleton — binary assets (fonts, grounds, gsap.min.js, AI_End_Card.mp4) are\n"
            "stamped fresh by `py tools/new_project.py`; they are intentionally absent here.\n",
            encoding="utf-8",
        )

    # --- stamp chrome scenes present in this profile's required_elements ---
    required = set(p.get("required_elements", []))
    scene_target = (p.get("scene_seconds") or {}).get("target") or 20
    scene_min = (p.get("scene_seconds") or {}).get("min") or 12

    opening_scenes, closing_scenes, fill_locations = [], [], []
    for phase, bucket in (("opening", opening_scenes), ("closing", closing_scenes)):
        for elem_key in chrome["order"][phase]:
            if elem_key not in required or elem_key not in chrome["elements"]:
                continue
            elem = chrome["elements"][elem_key]
            block_file = BLOCKS / f"{elem['block']}.html"
            if not block_file.exists():
                raise SystemExit(f"error: chrome block {elem['block']!r} not found at {block_file}")
            scene_id = elem["id"]
            html = stamp_block(block_file.read_text(encoding="utf-8"), elem["block"], scene_id,
                               elem.get("ground", "content-wash"), elem["config"])
            (out / "scenes" / f"{scene_id}.html").write_text(html, encoding="utf-8")
            bucket.append({
                "id": scene_id,
                "src": f"scenes/{scene_id}.html",
                "duration": resolve_duration(elem["duration"], scene_target, scene_min),
                "seam": elem.get("seam", "cut-left"),
            })
            fill_locations.append((elem_key, f"scenes/{scene_id}.html"))

    # --- scenes.json skeleton: [openings] + <body slot> + [closings] ---
    scenes = opening_scenes + closing_scenes
    body_after = opening_scenes[-1]["id"] if opening_scenes else None
    body_before = closing_scenes[0]["id"] if closing_scenes else None
    chrome_count = len(scenes)
    body_min = body_max = None
    if p.get("scene_count_target"):
        body_min = max(1, p["scene_count_target"] - chrome_count)
    if p.get("scene_count_max"):
        body_max = max(body_min or 1, p["scene_count_max"] - chrome_count)
    body_str = (f"~{body_min}" + (f"-{body_max}" if body_max else "")) if body_min else "?"

    scenes_json: dict = {
        "title": title,
        "composition_id": "root",
        "width": cfg["composition"]["width"],
        "height": cfg["composition"]["height"],
        "root_background": "#fff8f3",
        "gsap": "assets/vendor/gsap.min.js",
        "fonts": [
            {"family": "Segoe UI", "weight": 400, "style": "normal", "src": "fonts/segoeui-regular.woff2"},
            {"family": "Segoe UI Semibold", "weight": 600, "style": "normal", "src": "fonts/segoeui-semibold.woff2"},
        ],
    }
    # narration is NOT wired at scaffold time — the wav does not exist yet, and a dangling
    # <audio src> fails lint. The pipeline adds narration (track 10, start 3.0s) after TTS.
    if cfg.get("endcard", {}).get("mandatory", True):
        scenes_json["endcard"] = {
            "src": cfg["endcard"]["asset"],
            "duration": cfg["endcard"]["seconds"],
            "track": 11,
        }
    scenes_json["bookend"] = {"intro": 0.5, "outro": 0.7, "color": "#000"}
    scenes_json["scenes"] = scenes
    scenes_json["body_slot"] = {
        "insert_after": body_after,
        "before": body_before,
        "target_scene_count": body_min,
        "max_scene_count": body_max,
        "note": "Author the teaching-body scenes here (each on the kit foundation), then insert them into "
                "'scenes' between the opening and closing chrome. The builder re-times all durations to "
                "real narration word anchors.",
    }
    (out / "scenes.json").write_text(json.dumps(scenes_json, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    # --- seed the review ledger (real projects only; a starter carries no per-video state) ---
    secs = p.get("content_seconds") or {}
    if not args.emit_starter:
        def record_gate(gate: int, note: str) -> None:
            r = subprocess.run(
                [sys.executable, str(TOOLS / "review_index.py"), "record", "--project", str(out),
                 "--gate", str(gate), "--status", "passed", "--note", note],
                capture_output=True, text=True,
            )
            if r.returncode != 0:
                warnings.append(f"gate {gate} seed failed: {r.stderr.strip() or r.stdout.strip()}")

        if args.source:
            record_gate(1, f"Source: {args.source}")
        record_gate(2, f"Profile LOCKED: {p['name']} (~{secs.get('target')}s, "
                       f"{p.get('word_target', '?')} words, ~{p.get('scene_count_target', '?')} scenes, "
                       f"{p['max_static_stretch_seconds']}s static). Scaffolded by new_project.py.")

    # --- manifest stub + BRIEF.md (the single human entry point) ---
    (out / "manifest.json").write_text(json.dumps({
        "title": title,
        "type": p["name"],
        "profile": p["name"],
        "status": "scaffolded",
        "voice": cfg["narration"]["default_voice"],
        "source": args.source or None,
        "deliverables": {
            "mp4": f"{slugify(title)}.mp4",
            "captions_vtt": f"{slugify(title)}.vtt",
            "thumbnail": f"{slugify(title)}_thumbnail.png",
        },
    }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    brief = [
        f"# {title}",
        "",
        f"- **Profile:** `{p['name']}` — {p['label']}",
        f"- **Target:** ~{secs.get('target')}s content ({secs.get('min')}–{secs.get('max')}s), "
        f"word budget {p.get('word_budget', {}).get('min', '?')}–{p.get('word_budget', {}).get('max', '?')} "
        f"(target {p.get('word_target', '?')}) @ {p['words_per_second']} w/s",
        f"- **Scenes:** aim ~{p.get('scene_count_target', '?')} "
        f"(chrome {chrome_count} stamped + {body_str} body)",
        f"- **Max static hold:** {p['max_static_stretch_seconds']}s   ·   **Voice:** {cfg['narration']['default_voice']}",
        f"- **Source:** {args.source or '_(fill in the Learn unit/topic)_'}",
        "",
        "## Fill the placeholders",
        "",
        f"Every `{FILL}` below must be replaced before render (guarded by `tools/check_placeholders.py`).",
        "",
    ]
    for elem_key, rel in fill_locations:
        brief.append(f"- `{elem_key}` → [{rel}]({rel})")
    brief += [
        "",
        "## Next steps",
        "",
        "1. Write the script + beat plan (script-writer) and fill the chrome placeholders above.",
        "2. Author the teaching-body scenes into `scenes/` and insert them into `scenes.json` "
        "between the opening and closing chrome (see `scenes.json` → `body_slot`).",
        "3. Run the gated pipeline (voice → fact-check QA → build → snapshot QA → render).",
        f"4. Guard: `py tools/check_placeholders.py --project .` must be clean before render.",
        "",
    ]
    (out / "BRIEF.md").write_text("\n".join(brief), encoding="utf-8")

    # --- cloud handoff: branch + per-slug gitignore so the source is trackable for the builder ---
    branch = None
    if args.cloud and not args.emit_starter:
        slug = out.name
        emit_gitignore_negation(slug)
        branch = ensure_video_branch(slug, warnings)

    # --- report ---
    print(f"scaffolded {p['name']} project -> {out}")
    print(f"  chrome scenes: {', '.join(s['id'] for s in scenes) or '(none for this profile)'}")
    print(f"  body slot: {body_str} scene(s) between "
          f"{body_after or '(start)'} and {body_before or '(end)'}")
    print(f"  assets: {'copied fresh' if copy_assets else 'skipped (starter skeleton)'}")
    print(f"  placeholders to fill: {len(fill_locations)} chrome element(s) - see BRIEF.md")
    if branch:
        print(f"  cloud handoff: on branch '{branch}' — source tracked, renders git-ignored")
    for w in warnings:
        print(f"  ! {w}")
    print("\nnext: fill BRIEF.md placeholders, author body scenes, run the pipeline.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
