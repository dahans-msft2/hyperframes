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


REQUIRED_INPUTS = ("script.md", "design-plan.md", "narration.wav", "transcript.json")


def _run(cmd: list[str], dry: bool) -> "subprocess.CompletedProcess | None":
    if dry:
        print("       $ " + " ".join(cmd))
        return None
    return subprocess.run(cmd, capture_output=True, text=True)


def copilot_prompt(title: str, profile: str, slug: str) -> str:
    return (
        f"@copilot Build the **{title}** {profile} in `learn/output/{slug}/`. Follow "
        "`.github/copilot-instructions.md` and the builder doctrine in "
        "`.github/agents/hyperframes-builder.agent.md`.\n"
        "1. Fill every chrome `__FILL__` from `script.md`.\n"
        "2. Author the body scenes per `design-plan.md`, inserting them into `scenes.json`'s `body_slot`.\n"
        "3. Anchor every beat + in-scene cue to `transcript.json` word times.\n"
        "4. Pass all gates from the project dir: assemble_scenes -> check_subcomps -> check_placeholders "
        "-> check_initial_state -> check_cue_anchors -> lint -> check.\n"
        "Don't render, change narration or palette, or commit fonts. Push commits to this branch and "
        "report the gate results. (Recommended kickoff model: Claude Opus 5, high reasoning.)"
    )


def handoff_one(title: str, profile: str, source: "str | None", project: Path,
                base: str, repo: str, assign: bool, dry: bool) -> dict:
    """Push one prepped video branch and open its issue + draft PR. The branch must already exist
    locally with the approved inputs committed (scaffold --cloud + script + design + TTS)."""
    slug = project.name
    branch = f"video/{slug.lower()}"
    missing = [f for f in REQUIRED_INPUTS if not (project / f).exists()]
    if missing:
        return {"slug": slug, "status": "not-ready", "missing": missing}
    if not dry and subprocess.run(["git", "-C", str(LEARN), "rev-parse", "--verify", "--quiet", branch],
                                  capture_output=True).returncode != 0:
        return {"slug": slug, "status": "no-branch", "branch": branch}

    push = _run(["git", "-C", str(LEARN), "push", "-u", "origin", branch], dry)
    if push is not None and push.returncode != 0:
        return {"slug": slug, "status": "push-failed", "err": (push.stderr or push.stdout).strip()}

    issue = _run(["gh", "issue", "create", "--repo", repo, "--title", f"Build video: {slug}",
                  "--body", f"Build **{title}** ({profile}). Source: {source or 'n/a'}. Kickoff prompt is in the PR."], dry)
    issue_url = issue.stdout.strip().splitlines()[-1] if (issue and issue.returncode == 0 and issue.stdout.strip()) else None

    pr = _run(["gh", "pr", "create", "--repo", repo, "--base", base, "--head", branch, "--draft",
               "--title", f"Build video: {title}", "--body", copilot_prompt(title, profile, slug)], dry)
    pr_url = pr.stdout.strip().splitlines()[-1] if (pr and pr.returncode == 0 and pr.stdout.strip()) else None

    if assign and (pr_url or dry):  # Auto-model kickoff; omit to @copilot manually with Opus 5
        _run(["gh", "pr", "comment", pr_url or branch, "--repo", repo,
              "--body", copilot_prompt(title, profile, slug)], dry)

    return {"slug": slug, "status": "planned" if dry else "handed-off",
            "branch": branch, "issue": issue_url, "pr": pr_url}


def main() -> int:
    ap = argparse.ArgumentParser(description="Batch-scaffold Learn video projects from a manifest.")
    ap.add_argument("--manifest", required=True, help="batch manifest JSON (list or {videos:[...]})")
    ap.add_argument("--out-root", default=str(LEARN / "output"), help="where per-video dirs land (default: learn/output)")
    ap.add_argument("--dry-run", action="store_true", help="print what would be scaffolded, do nothing")
    ap.add_argument("--force", action="store_true", help="overwrite existing non-empty project dirs")
    ap.add_argument("--handoff", action="store_true",
                    help="cloud-handoff mode: push each prepped video branch + open its issue + draft PR "
                         "(each video must already be scaffolded --cloud + scripted + TTS'd + committed)")
    ap.add_argument("--assign", action="store_true",
                    help="handoff: auto-kick the cloud agent by @copilot-commenting each PR (Auto model). "
                         "Omit to @copilot each PR manually with Opus 5.")
    ap.add_argument("--base", default="videos", help="handoff: PR base branch (default: videos archive)")
    ap.add_argument("--repo", default="dahans-msft2/hyperframes", help="handoff: owner/repo for gh")
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

    # --- cloud handoff mode: push each prepped video branch + open its issue + draft PR ---
    if args.handoff:
        results = []
        for i, row in enumerate(rows, 1):
            title, profile = (row or {}).get("title"), (row or {}).get("profile")
            if not title or not profile:
                print(f"  [{i}] SKIP — row missing title or profile", file=sys.stderr)
                continue
            project = Path(row["out"]).resolve() if row.get("out") else (out_root / slugify(title))
            res = handoff_one(title, profile, row.get("source"), project,
                              args.base, args.repo, args.assign, args.dry_run)
            results.append(res)
            line = f"  [{i}] {res['status']:<11} {project.name}"
            if res.get("missing"):
                line += f"  (missing: {', '.join(res['missing'])})"
            if res.get("pr"):
                line += f"  pr={res['pr']}"
            print(line)
        done = sum(1 for r in results if r["status"] in ("handed-off", "planned"))
        print(f"\n{done}/{len(results)} handed off" + (" (dry run)" if args.dry_run else ""))
        if done and not args.assign:
            print("next: on each PR, select Claude Opus 5 + high reasoning and @copilot it "
                  "(or re-run with --assign to auto-start on the Auto model).")
        return 0 if done == len(results) else 1

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
