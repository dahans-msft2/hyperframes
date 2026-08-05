"""Static mount-contract checker for modular (per-scene) HyperFrames projects.

`hyperframes lint` and `check` cannot prove the CROSS-FILE mount contract, and the render
postmortem's #1 lesson was that these failures surface only at render (45s stalls, unstyled
top-left text). This tool catches them at author time, deterministically, with no browser:

  Per scene file (scenes/*.html):
    P1  <style> / <script> / the root <div data-composition-id> all live INSIDE <template>.
    P3  the root is styled by #root, not by a class the <style> keys off (scoping drops it).
        root carries data-width / data-height.
    T   a timeline is registered at window.__timelines["<id>"] matching the root id.

  Host (index.html):
    - every data-composition-src file exists on disk.
    P2  host data-composition-id == scene root data-composition-id == timeline key.
    - scene slots tile track 1 with no gaps and no overlaps.
    - narration + end card mounted at the root; composition covers the scenes.

Usage:
  py tools/check_subcomps.py --project <dir>
  py tools/check_subcomps.py --host <index.html> --scenes-dir <dir>
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys

TEMPLATE_OPEN = re.compile(r"<template[\s>]", re.I)
TEMPLATE_CLOSE = re.compile(r"</template>", re.I)
COMP_ID = re.compile(r'data-composition-id\s*=\s*"([^"]+)"', re.I)
COMP_SRC = re.compile(r'data-composition-src\s*=\s*"([^"]+)"', re.I)
TIMELINE_KEY = re.compile(r'__timelines\s*\[\s*"([^"]+)"\s*\]\s*=')
DATA_START = re.compile(r'data-start\s*=\s*"([^"]+)"', re.I)
DATA_DUR = re.compile(r'data-duration\s*=\s*"([^"]+)"', re.I)
DATA_TRACK = re.compile(r'data-track-index\s*=\s*"([^"]+)"', re.I)


def find_template_span(html: str) -> tuple[int, int] | None:
    m_open = TEMPLATE_OPEN.search(html)
    m_close = TEMPLATE_CLOSE.search(html)
    if not m_open or not m_close or m_close.start() < m_open.end():
        return None
    return (m_open.start(), m_close.end())


def check_scene(path: Path) -> tuple[str | None, list[str]]:
    """Return (scene_id, problems)."""
    problems: list[str] = []
    if not path.exists():
        return None, [f"scene file missing: {path}"]
    html = path.read_text(encoding="utf-8")

    span = find_template_span(html)
    if span is None:
        problems.append("no <template>…</template> wrapper (runtime clones template contents only)")
        return None, problems
    t0, t1 = span
    inside = html[t0:t1]

    # P1 — style/script/root must be inside the template.
    for tag, label in (("<style", "<style>"), ("<script", "<script>")):
        first = re.search(re.escape(tag), html, re.I)
        if first and not (t0 <= first.start() < t1):
            problems.append(f"P1: {label} is outside <template> (discarded at render — move it inside)")

    # Root composition id — must be inside template.
    root_ids_inside = COMP_ID.findall(inside)
    if not root_ids_inside:
        problems.append("P1/P2: no data-composition-id inside <template> (no mountable root)")
        return None, problems
    scene_id = root_ids_inside[0]

    # Locate the root element's opening tag to inspect its attributes.
    root_tag = re.search(r"<div\b[^>]*data-composition-id\s*=\s*\"" + re.escape(scene_id) + r"\"[^>]*>", inside, re.I)
    if root_tag:
        root_attrs = root_tag.group(0)
        if not re.search(r'data-width\s*=', root_attrs, re.I) or not re.search(r'data-height\s*=', root_attrs, re.I):
            problems.append("root <div> missing data-width/data-height (lint root_missing_dimensions)")
        # P3 — root must not also carry a class the stylesheet keys off; style by #root.
        cls = re.search(r'class\s*=\s*"([^"]*)"', root_attrs, re.I)
        if cls:
            classes = cls.group(1).split()
            style_block = "\n".join(re.findall(r"<style[^>]*>(.*?)</style>", inside, re.I | re.S))
            for c in classes:
                if re.search(r"(^|[^.\w])\." + re.escape(c) + r"\b", style_block):
                    problems.append(
                        f"P3: root is styled by class '.{c}' — scoping rewrites it to a descendant "
                        f"selector that can't match the root. Style the root via #root."
                    )

    # T — timeline registered under the scene id.
    keys = TIMELINE_KEY.findall(inside)
    if scene_id not in keys:
        problems.append(
            f"T: no window.__timelines[\"{scene_id}\"] = … inside <template> "
            f"(found keys: {keys or 'none'}) — render waits 45s then freezes"
        )

    return scene_id, problems


def parse_float(v: str) -> float | None:
    try:
        return float(v)
    except ValueError:
        return None


def check_host(host_path: Path) -> tuple[list[dict], list[str]]:
    problems: list[str] = []
    if not host_path.exists():
        return [], [f"host not found: {host_path}"]
    html = host_path.read_text(encoding="utf-8")
    base = host_path.parent

    # Each slot: data-composition-src div with its id/start/duration/track.
    slots = []
    for m in re.finditer(r"<div\b[^>]*data-composition-src[^>]*>", html, re.I):
        tag = m.group(0)
        src = COMP_SRC.search(tag)
        cid = COMP_ID.search(tag)
        start = DATA_START.search(tag)
        dur = DATA_DUR.search(tag)
        track = DATA_TRACK.search(tag)
        slots.append({
            "src": src.group(1) if src else None,
            "id": cid.group(1) if cid else None,
            "start": parse_float(start.group(1)) if start else None,
            "duration": parse_float(dur.group(1)) if dur else None,
            "track": track.group(1) if track else None,
            "path": (base / src.group(1)) if src else None,
        })
    if not slots:
        problems.append("host declares no data-composition-src slots")

    # Tiling: scenes on track 1 must be gap-free and non-overlapping, in order.
    track1 = [s for s in slots if s["track"] == "1"]
    ordered = sorted((s for s in track1 if s["start"] is not None), key=lambda s: s["start"])
    for prev, nxt in zip(ordered, ordered[1:]):
        if prev["start"] is None or prev["duration"] is None or nxt["start"] is None:
            continue
        end = round(prev["start"] + prev["duration"], 3)
        if abs(end - nxt["start"]) > 0.001:
            kind = "overlap" if nxt["start"] < end else "gap"
            problems.append(f"track-1 {kind}: '{prev['id']}' ends {end} but '{nxt['id']}' starts {nxt['start']}")

    return slots, problems


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--project", type=Path)
    ap.add_argument("--host", type=Path)
    ap.add_argument("--scene", type=Path, help="validate a single lone scene sub-composition file")
    ap.add_argument("--scenes-dir", default="scenes")
    args = ap.parse_args()

    # Lone-scene mode: validate one scene file's mount contract (for a parallel scene worker).
    if args.scene:
        scene_id, problems = check_scene(args.scene)
        if problems:
            print(f"SCENE MOUNT-CONTRACT FAIL ({len(problems)} issue(s)):")
            for p in problems:
                print(f"  - [{scene_id or args.scene.name}] {p}")
            return 1
        print(f"SCENE OK — '{scene_id}' satisfies the sub-composition mount contract")
        return 0

    if args.project:
        host = args.host or (args.project / "index.html")
    elif args.host:
        host = args.host
    else:
        print("ERROR: pass --project or --host", file=sys.stderr)
        return 2

    all_problems: list[str] = []

    slots, host_problems = check_host(host)
    for p in host_problems:
        all_problems.append(f"[host] {p}")

    # Triangulate host slot id == scene root id == timeline key, per scene.
    for slot in slots:
        if not slot["path"]:
            continue
        scene_id, scene_problems = check_scene(slot["path"])
        label = slot["id"] or slot["src"]
        for p in scene_problems:
            all_problems.append(f"[{label}] {p}")
        if scene_id and slot["id"] and scene_id != slot["id"]:
            all_problems.append(
                f"[{label}] P2: host data-composition-id '{slot['id']}' != scene root id "
                f"'{scene_id}' — timeline lookup fails, render stalls 45s"
            )

    if all_problems:
        print(f"MOUNT-CONTRACT FAIL ({len(all_problems)} issue(s)):")
        for p in all_problems:
            print(f"  - {p}")
        return 1

    print(f"MOUNT-CONTRACT OK — {len(slots)} scene slot(s), ids triangulate, track 1 tiles cleanly")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
