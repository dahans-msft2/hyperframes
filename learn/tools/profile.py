"""Resolve a video-type profile with defaults merged, and derive word/length budgets.

Profiles parameterize the rubric: same 18/20 bar, different bounds per video type.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REGISTRY = Path(__file__).resolve().parent.parent / "profiles" / "profiles.json"


def load() -> dict:
    return json.loads(REGISTRY.read_text(encoding="utf-8"))


def resolve(name: str) -> dict:
    reg = load()
    profiles = reg["profiles"]
    if name not in profiles:
        raise KeyError(f"unknown profile {name!r}. known: {', '.join(sorted(profiles))}")

    merged = {**reg["defaults"], **profiles[name]}

    # `required_elements_add` extends rather than replaces the default element list.
    extra = merged.pop("required_elements_add", [])
    if extra:
        merged["required_elements"] = list(merged["required_elements"]) + list(extra)

    merged["name"] = name

    secs = merged.get("content_seconds") or {}
    wps = merged.get("words_per_second", 2.53)
    # Always derived, never stored -- a persisted budget silently outlives a pace change.
    if merged.get("narrated", True) and secs.get("min") and secs.get("max"):
        merged["word_budget"] = {
            "min": int(secs["min"] * wps),
            "max": int(secs["max"] * wps),
        }
        if secs.get("target"):
            merged["word_target"] = int(secs["target"] * wps)

    # Scene density: aim for content_target / scene_target scenes; the cap is the point past
    # which scenes are too thin to teach (content_max / scene_min). Derived, never stored.
    sc = merged.get("scene_seconds") or {}
    if merged.get("narrated", True) and secs.get("target") and sc.get("target"):
        merged["scene_count_target"] = max(1, round(secs["target"] / sc["target"]))
        if secs.get("max") and sc.get("min"):
            merged["scene_count_max"] = max(1, int(secs["max"] // sc["min"]))

    if secs.get("max"):
        card = merged["end_card_seconds"] if merged.get("end_card_counts_toward_target") else 0
        merged["total_seconds_max"] = round(secs["max"] + (0 if card else merged["end_card_seconds"]), 3)

    return merged


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("profile", nargs="?", help="profile name; omit to list")
    ap.add_argument("--json", action="store_true", help="emit raw JSON")
    args = ap.parse_args()

    reg = load()
    if not args.profile:
        print(f"profiles.json v{reg['version']}\n")
        for key, val in reg["profiles"].items():
            secs = val.get("content_seconds") or {}
            rng = f"{secs.get('min')}–{secs.get('max')}s" if secs.get("min") else "n/a"
            star = " *default" if val.get("default") else ""
            print(f"  {key:<24} {rng:<14} {val['label']}{star}")
        return 0

    try:
        p = resolve(args.profile)
    except KeyError as err:
        print(err, file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(p, indent=2))
        return 0

    secs = p.get("content_seconds") or {}
    print(f"profile           {p['name']}  —  {p['label']}")
    print(f"source            {p.get('source', '—')}")
    print(f"content length    {secs.get('min')}–{secs.get('max')}s (target {secs.get('target')})")
    if p.get("word_budget"):
        wb = p["word_budget"]
        print(f"word budget       {wb['min']}–{wb['max']} words @ {p['words_per_second']} w/s"
              + (f"  (target {p['word_target']})" if p.get("word_target") else ""))
    print(f"end card          {p['end_card_seconds']}s, "
          f"{'inside' if p.get('end_card_counts_toward_target') else 'on top of'} the target")
    print(f"max static hold   {p['max_static_stretch_seconds']}s")
    sc = p.get("scene_seconds") or {}
    if p.get("scene_count_target"):
        cap = f", never more than ~{p['scene_count_max']}" if p.get("scene_count_max") else ""
        print(f"scene density     aim ~{p['scene_count_target']} scenes "
              f"(~{sc.get('target')}s each, floor {sc.get('min')}s/scene{cap})")
    if p.get("dead_zone_exempt_segment_kinds"):
        print(f"dead-zone exempt  {', '.join(p['dead_zone_exempt_segment_kinds'])}")
    print(f"chapters          {'required' if p.get('chapters_required') else 'not required'}")
    print(f"rubric bar        >= {p['rubric']['min_total']}/20, "
          f"every criterion >= {p['rubric']['min_per_criterion']}, "
          f"{p['rubric']['max_disqualifiers']} disqualifiers")
    print("required elements")
    for el in p["required_elements"]:
        print(f"  · {el}")
    if p.get("$note"):
        print(f"\nnote: {p['$note']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
