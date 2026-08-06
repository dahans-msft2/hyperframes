#!/usr/bin/env python3
"""Compile a locked profile + composition into a native HyperFrames motion spec.

The profile is the single source of truth for how a video type must MOVE. This
turns that into `<composition>.motion.json` — the declarative sidecar that
`npx hyperframes check` evaluates against the same seeked timeline the renderer
uses (packages/cli/src/utils/motionSpec.ts). One artifact, two roles: the
builder authors AGAINST it, and check enforces it. It replaces the bespoke
`check_reveal_order.py` detector with the native `before` assertion, and it
hands the native `keepsMoving` / `staysInFrame` gates the profile's numbers.

Emitted assertions
------------------
  keepsMoving {maxStaticSec}   from profile.max_static_stretch_seconds — the
                               dead-zone budget. Whole-composition. SKIPPED for
                               profiles with dead_zone_exempt_segment_kinds
                               (legal holds on demos / screen recordings would
                               falsely fail a whole-composition assertion); those
                               keep per-scene human-judgment C2 review in QA.
  before {a, b}                from every `data-reveal-after="#a #b"` element:
                               each listed dependency must appear before it. The
                               native gate reads real seeked opacity, not code
                               shape, so it supersedes check_reveal_order.py.
  staysInFrame {selector}      from every `data-keep-in-frame` element — full-
                               frame stages that must not shift off-canvas.

Nothing is emitted for a non-rendered profile (slideshow) or when the
composition declares no reveal-order / keep-in-frame markers and the profile is
dead-zone exempt (an empty spec is invalid to the native parser).

Usage:
  py tools/emit_motion_spec.py --project <dir> --profile <name>
  py tools/emit_motion_spec.py --composition index.html --profile launch-promo
"""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
import re
import sys

TAG = re.compile(r"<\w+([^>]*)>")
_HERE = Path(__file__).resolve().parent


def _load_profile_module():
    spec = importlib.util.spec_from_file_location("_learn_profile", _HERE / "profile.py")
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return mod


def _attr(attrs: str, name: str) -> str | None:
    m = re.search(rf'\b{name}\s*=\s*"([^"]*)"', attrs)
    return m.group(1) if m else None


def _selectors(value: str) -> list[str]:
    return [s.strip() for s in value.split() if s.strip().startswith(("#", "."))]


def collect_markers(html: str) -> tuple[list[tuple[str, list[str]]], list[str]]:
    """Return (reveal_after, keep_in_frame). reveal_after: (element_selector, [deps])."""
    reveal_after: list[tuple[str, list[str]]] = []
    keep_in_frame: list[str] = []
    for tag in TAG.finditer(html):
        attrs = tag.group(1)
        eid = _attr(attrs, "id")
        if not eid:
            continue
        sel = "#" + eid
        ram = _attr(attrs, "data-reveal-after")
        if ram:
            deps = _selectors(ram)
            if deps:
                reveal_after.append((sel, deps))
        if re.search(r"\bdata-keep-in-frame\b", attrs):
            keep_in_frame.append(sel)
    return reveal_after, keep_in_frame


def composition_duration(html: str) -> float | None:
    m = re.search(r'id\s*=\s*"root"[^>]*\bdata-duration\s*=\s*"([\d.]+)"', html)
    if not m:
        m = re.search(r'\bdata-duration\s*=\s*"([\d.]+)"[^>]*id\s*=\s*"root"', html)
    return float(m.group(1)) if m else None


def endcard_start(html: str) -> float | None:
    """data-start of a trailing end-card <video>. A video plays real motion but its DOM
    rect is static, so the geometry-based keepsMoving gate false-positives on it; cap the
    motion window at its start."""
    m = re.search(r'<video[^>]*\bid\s*=\s*"[^"]*end-?card[^"]*"[^>]*>', html, re.I)
    if not m:
        return None
    ds = re.search(r'data-start\s*=\s*"([\d.]+)"', m.group(0))
    return float(ds.group(1)) if ds else None


def build_spec(profile: dict, html_files: list[Path]) -> dict:
    assertions: list[dict] = []
    seen: set[str] = set()

    def add(assertion: dict) -> None:
        key = json.dumps(assertion, sort_keys=True)
        if key not in seen:
            seen.add(key)
            assertions.append(assertion)

    exempt = bool(profile.get("dead_zone_exempt_segment_kinds"))
    max_static = profile.get("max_static_stretch_seconds")
    if not exempt and isinstance(max_static, (int, float)):
        add({"kind": "keepsMoving", "maxStaticSec": float(max_static)})

    duration: float | None = None
    motion_cap: float | None = None
    for path in html_files:
        html = path.read_text(encoding="utf-8")
        if duration is None:
            duration = composition_duration(html)
            motion_cap = endcard_start(html)
        reveal_after, keep_in_frame = collect_markers(html)
        for element, deps in reveal_after:
            for dep in deps:
                add({"kind": "before", "a": dep, "b": element})
        for sel in keep_in_frame:
            add({"kind": "staysInFrame", "selector": sel})

    # Motion sampling ranges over spec.duration; cap it at the end-card start so keepsMoving
    # doesn't flag the geometrically-static (but really playing) disclosure video.
    motion_duration = duration
    if motion_cap is not None and duration is not None and motion_cap < duration:
        motion_duration = motion_cap

    spec: dict = {"version": 1}
    if motion_duration is not None:
        spec["duration"] = motion_duration
    spec["assertions"] = assertions
    return spec


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--project", type=Path, default=Path("."), help="project dir (default cwd)")
    ap.add_argument("--composition", type=Path, help="composition html (default <project>/index.html)")
    ap.add_argument("--profile", default="companion-short", help="locked profile name")
    ap.add_argument("--out", type=Path, help="output path (default <composition>.motion.json)")
    args = ap.parse_args()

    profile_mod = _load_profile_module()
    try:
        profile = profile_mod.resolve(args.profile)
    except KeyError as err:
        print(err, file=sys.stderr)
        return 2

    if profile.get("rendered_video") is False:
        print(f"{args.profile}: not a rendered video — no motion spec emitted.")
        return 0

    composition = args.composition or (args.project / "index.html")
    if not composition.exists():
        print(f"ERROR: composition not found: {composition}", file=sys.stderr)
        return 2

    project = args.project if args.composition is None else composition.parent
    html_files = [composition]
    scenes_dir = project / "scenes"
    if scenes_dir.is_dir():
        html_files += sorted(scenes_dir.glob("*.html"))

    spec = build_spec(profile, html_files)
    if not spec["assertions"]:
        print(
            f"{args.profile}: dead-zone exempt and no reveal-order / keep-in-frame markers — "
            "no motion spec emitted (an empty native spec is invalid). C2 stays with QA review."
        )
        return 0

    out = args.out or composition.with_suffix(".motion.json")
    out.write_text(json.dumps(spec, indent=2) + "\n", encoding="utf-8")

    kinds = [a["kind"] for a in spec["assertions"]]
    summary = ", ".join(f"{k}×{kinds.count(k)}" for k in dict.fromkeys(kinds))
    print(f"wrote {out}  ({len(spec['assertions'])} assertion(s): {summary})")
    print("  → npx hyperframes check auto-discovers it; the build now gates on the profile's motion budget.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
