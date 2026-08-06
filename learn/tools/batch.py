#!/usr/bin/env python3
"""Batch-scaffold a slate of Learn video projects from one manifest.

`new_project.py` turns a {profile, title, source} into a ready-to-fill project. This loops it over a
manifest so a whole slate is stamped in one shot, then writes a batch queue the video-orchestrator
iterates. Batch does the SCAFFOLDING, not the gated build: each project's build still runs through
the orchestrator's gates + subagents + per-project approvals — batch just removes the repetitive
folder-stamping so N videos start from an identical, doctrine-compliant baseline.

    py tools/batch.py --manifest batch.json
    py tools/batch.py --manifest batch.json --dry-run

Manifest is JSON: either a top-level list, or {"videos": [ ... ]}. Each row:
    { "title": "...", "profile": "unit-video", "source": "<url|uid|path>"(optional), "out": "<dir>"(optional) }
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
LEARN = TOOLS.parent
NEW_PROJECT = TOOLS / "new_project.py"


def slugify(title: str) -> str:
    words = re.findall(r"[A-Za-z0-9]+", title)
    return "-".join(w[:1].upper() + w[1:] for w in words) or "Untitled"


def main() -> int:
    ap = argparse.ArgumentParser(description="Batch-scaffold Learn video projects from a manifest.")
    ap.add_argument("--manifest", required=True, help="batch manifest JSON (list or {videos:[...]})")
    ap.add_argument("--out-root", default=str(LEARN / "output"), help="where per-video dirs land (default: learn/output)")
    ap.add_argument("--dry-run", action="store_true", help="print what would be scaffolded, do nothing")
    ap.add_argument("--force", action="store_true", help="overwrite existing non-empty project dirs")
    args = ap.parse_args()

    mpath = Path(args.manifest).resolve()
    if not mpath.exists():
        print(f"error: manifest {mpath} not found", file=sys.stderr)
        return 1
    data = json.loads(mpath.read_text(encoding="utf-8"))
    rows = data.get("videos", data) if isinstance(data, dict) else data
    if not isinstance(rows, list) or not rows:
        print("error: manifest must be a non-empty list (or {videos:[...]})", file=sys.stderr)
        return 1

    out_root = Path(args.out_root).resolve()
    queue: list[dict] = []
    failures = 0

    for i, row in enumerate(rows, 1):
        title = (row or {}).get("title")
        profile = (row or {}).get("profile")
        if not title or not profile:
            print(f"  [{i}] SKIP — row missing title or profile: {row}", file=sys.stderr)
            failures += 1
            continue
        out = Path(row["out"]).resolve() if row.get("out") else (out_root / slugify(title))
        source = row.get("source")

        cmd = [sys.executable, str(NEW_PROJECT), "--profile", profile, "--title", title, "--out", str(out)]
        if source:
            cmd += ["--source", source]
        if args.force:
            cmd += ["--force"]

        if args.dry_run:
            print(f"  [{i}] would scaffold {profile:<16} -> {out}")
            queue.append({"title": title, "profile": profile, "source": source, "project": str(out), "status": "planned"})
            continue

        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0:
            print(f"  [{i}] FAIL {profile:<16} {title}", file=sys.stderr)
            print("       " + (r.stderr.strip() or r.stdout.strip()).replace("\n", "\n       "), file=sys.stderr)
            failures += 1
            queue.append({"title": title, "profile": profile, "source": source, "project": str(out), "status": "scaffold-failed"})
            continue
        print(f"  [{i}] ok   {profile:<16} -> {out.name}")
        queue.append({"title": title, "profile": profile, "source": source, "project": str(out), "status": "scaffolded"})

    if not args.dry_run:
        out_root.mkdir(parents=True, exist_ok=True)
        qpath = out_root / "batch-queue.json"
        qpath.write_text(json.dumps({"manifest": str(mpath), "videos": queue}, indent=2, ensure_ascii=False) + "\n",
                         encoding="utf-8")
        print(f"\nbatch queue -> {qpath}")

    scaffolded = sum(1 for q in queue if q["status"] == "scaffolded")
    print(f"\n{scaffolded}/{len(rows)} scaffolded" + (f", {failures} failed" if failures else "") +
          (" (dry run)" if args.dry_run else ""))
    if not args.dry_run and scaffolded:
        print("next: hand the batch queue to the video-orchestrator — one gated build per project "
              "(fill BRIEF.md placeholders, author the body, run the pipeline).")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
