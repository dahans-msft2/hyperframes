#!/usr/bin/env python3
"""Fail if a scaffolded project still carries `__FILL__` placeholders.

The scaffolder (`new_project.py`) stamps chrome scenes with `__FILL__` sentinels so a fresh
project lints and previews before authoring. This guard makes sure none survive to render:
run it before the QA/render gates. A clean exit (0) means every placeholder was filled; a
non-zero exit lists exactly where the unfilled ones are.

    py tools/check_placeholders.py --project output/My-Video
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

SENTINEL = "__FILL__"
SCAN_GLOBS = ("scenes.json", "scenes/*.html", "index.html", "BRIEF.md")
# BRIEF.md legitimately documents the sentinel; it is scanned for reporting but never fails the gate.
NON_BLOCKING = {"BRIEF.md"}


def main() -> int:
    ap = argparse.ArgumentParser(description="Fail if __FILL__ placeholders remain in a project.")
    ap.add_argument("--project", default=".", help="project directory (default: cwd)")
    args = ap.parse_args()

    root = Path(args.project).resolve()
    if not root.exists():
        print(f"error: {root} does not exist", file=sys.stderr)
        return 2

    blocking_hits, info_hits = 0, 0
    for pattern in SCAN_GLOBS:
        for path in sorted(root.glob(pattern)):
            rel = path.relative_to(root).as_posix()
            blocking = rel not in NON_BLOCKING
            try:
                lines = path.read_text(encoding="utf-8").splitlines()
            except (UnicodeDecodeError, OSError):
                continue
            for n, line in enumerate(lines, 1):
                if SENTINEL in line:
                    tag = "UNFILLED" if blocking else "note"
                    print(f"  [{tag}] {rel}:{n}  {line.strip()[:100]}")
                    if blocking:
                        blocking_hits += 1
                    else:
                        info_hits += 1

    if blocking_hits:
        print(f"\nFAIL: {blocking_hits} unfilled {SENTINEL} placeholder(s) remain — fill them before render.")
        return 1
    print(f"OK: no unfilled placeholders" + (f" ({info_hits} documented in BRIEF.md)" if info_hits else "") + ".")
    return 0


if __name__ == "__main__":
    sys.exit(main())
