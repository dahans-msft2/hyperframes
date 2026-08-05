"""Discover and resolve brand icons for a Learn companion video.

The icon library (assets/icons/) has ~1500 nested SVG/PNG files across Azure, M365/Office,
GitHub, Power Platform, Security, and Healthcare sets. Nobody can find an icon by spelunking,
and copying all of them into every project would bloat each render. This tool indexes them,
searches by name, and copies just the ones a video needs into the project (icons must live in
the PROJECT at render time, exactly like fonts and the end card).

  py tools/icon_index.py build                       # (re)build assets/icons/index.json
  py tools/icon_index.py find entra                  # search by name
  py tools/icon_index.py find defender --set Security --format svg
  py tools/icon_index.py add --project <dir> Entra   # copy the icon into <dir>/assets/icons/
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parent.parent
# Icons are referenced IN PLACE from the sibling animagent-v2 library (already in the repo) —
# no duplicate copy. Only the icons a video actually uses are copied INTO that project (`add`).
SOURCE = ROOT.parent / "animagent-v2" / "icons"
INDEX = ROOT / "assets" / "icon-index.json"


def build_index() -> int:
    if not SOURCE.exists():
        print(f"ERROR: icon source not found: {SOURCE}", file=sys.stderr)
        return 2
    entries = []
    for path in sorted(SOURCE.rglob("*")):
        if path.suffix.lower() not in (".svg", ".png"):
            continue
        rel = path.relative_to(SOURCE)
        entries.append({
            "name": path.stem,
            "key": path.stem.lower(),
            "set": rel.parts[0] if rel.parts else "",
            "format": path.suffix.lower().lstrip("."),
            "rel": rel.as_posix(),  # relative to the animagent-v2 icon source
        })
    INDEX.parent.mkdir(parents=True, exist_ok=True)
    INDEX.write_text(json.dumps(entries, indent=2), encoding="utf-8")
    print(f"indexed {len(entries)} icon(s) from {SOURCE} -> {INDEX}")
    return 0


def load_index() -> list[dict]:
    if not INDEX.exists():
        build_index()
    return json.loads(INDEX.read_text(encoding="utf-8"))


def search(query: str, icon_set: str | None, fmt: str | None) -> list[dict]:
    q = query.lower()
    hits = []
    for e in load_index():
        if q not in e["key"]:
            continue
        if icon_set and icon_set.lower() not in e["set"].lower():
            continue
        if fmt and e["format"] != fmt.lower():
            continue
        hits.append(e)
    # Exact name matches first, then shortest name (most specific), then path.
    hits.sort(key=lambda e: (e["key"] != q, len(e["name"]), e["rel"]))
    return hits


def cmd_find(query: str, icon_set: str | None, fmt: str | None, limit: int) -> int:
    hits = search(query, icon_set, fmt)
    if not hits:
        print(f"no icon matches '{query}'" + (f" (set={icon_set})" if icon_set else ""))
        return 1
    for e in hits[:limit]:
        print(f"  {e['name']:<28} {e['format']:<4} {e['set']:<38} {e['rel']}")
    if len(hits) > limit:
        print(f"  … {len(hits) - limit} more (narrow with --set / --format / a longer query)")
    return 0


def cmd_add(project: Path, name: str, icon_set: str | None, fmt: str | None) -> int:
    hits = search(name, icon_set, fmt)
    if not hits:
        print(f"ERROR: no icon matches '{name}'", file=sys.stderr)
        return 1
    exact = [e for e in hits if e["key"] == name.lower()]
    chosen = (exact or hits)[0]
    if len(exact) > 1 or (not exact and len(hits) > 1):
        print(f"note: '{name}' matched {len(hits)} icons; taking {chosen['name']} ({chosen['set']}). "
              f"Disambiguate with --set/--format if wrong.")
    src = SOURCE / chosen["rel"]
    dest_dir = project / "assets" / "icons"
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / src.name
    shutil.copy2(src, dest)
    project_rel = dest.relative_to(project).as_posix()
    print(f"copied {chosen['name']} -> {dest}")
    print(f"use in a scene as: assets/icons/{src.name}   (host-relative)  |  ../{project_rel}   (from scenes/)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("build", help="rebuild assets/icon-index.json from ../animagent-v2/icons")

    p_find = sub.add_parser("find", help="search icons by name")
    p_find.add_argument("query")
    p_find.add_argument("--set", dest="icon_set", help="filter by icon set (substring)")
    p_find.add_argument("--format", dest="fmt", choices=["svg", "png"])
    p_find.add_argument("--limit", type=int, default=20)

    p_add = sub.add_parser("add", help="copy an icon into a project's assets/icons/")
    p_add.add_argument("--project", type=Path, required=True)
    p_add.add_argument("name")
    p_add.add_argument("--set", dest="icon_set")
    p_add.add_argument("--format", dest="fmt", choices=["svg", "png"])

    args = ap.parse_args()
    if args.cmd == "build":
        return build_index()
    if args.cmd == "find":
        return cmd_find(args.query, args.icon_set, args.fmt, args.limit)
    if args.cmd == "add":
        return cmd_add(args.project, args.name, args.icon_set, args.fmt)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
