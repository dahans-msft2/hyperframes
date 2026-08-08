#!/usr/bin/env python3
"""Publish a rendered Learn video the 'A' way: source -> main, deliverables -> a GitHub Release.

A delivered video is its `learn/output/<slug>/` folder committed to **main** (source, re-renderable
from a clone) plus a per-video **GitHub Release** holding the heavy deliverables (MP4 + captions +
thumbnail). No `videos` archive branch, no cross-branch merge, no scope-gate base drift: the source
and its release stay linked by `manifest.json`.

    py tools/publish_video.py --project output/<slug>
    py tools/publish_video.py --project output/<slug> --dry-run     # print the git + gh sequence, do nothing

Prerequisites: the project has been rendered (`render_and_package.py` -> status "rendered", with the
MP4/VTT/thumbnail present). `gh` must be authenticated. Run from the `learn/` dir.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import subprocess
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
LEARN = TOOLS.parent
DEFAULT_REPO = "dahans-msft2/hyperframes"


def die(msg: str) -> "NoReturn":  # type: ignore[name-defined]
    print(f"FAIL: {msg}", file=sys.stderr)
    raise SystemExit(1)


def run(cmd: list[str], *, dry: bool, what: str, cwd: Path | None = None) -> "subprocess.CompletedProcess | None":
    print("  $ " + " ".join(cmd))
    if dry:
        return None
    r = subprocess.run(cmd, cwd=str(cwd) if cwd else None, capture_output=True, text=True)
    if r.returncode != 0:
        die(f"{what} failed (exit {r.returncode}): {(r.stderr or r.stdout).strip()}")
    return r


def emit_gitignore_negation(slug: str, dry: bool) -> bool:
    """Track THIS video's source + render INPUTS on main; keep render OUTPUTS + QA artifacts out
    (the deliverable MP4/captions/thumbnail become Release assets). narration.wav + the end card +
    grounds are LFS-tracked so the cloud renderer has them. Idempotent, and byte-identical to
    new_project.emit_gitignore_negation so a scaffolded project needs no change at publish."""
    gi = LEARN / ".gitignore"
    text = gi.read_text(encoding="utf-8") if gi.exists() else ""
    changed = False

    header = "# --- videos: source + render inputs tracked, outputs go to a Release ---"
    if header not in text:
        text = text.rstrip("\n") + "\n\n" + "\n".join([header, "!output/", "output/*", ""])
        changed = True

    marker = f"# video: {slug}"
    if marker not in text:
        text = text.rstrip("\n") + "\n\n" + "\n".join([
            marker,
            f"!output/{slug}/",
            f"!output/{slug}/**",
            "# INPUTS (narration.wav, end card, grounds — LFS-tracked) stay so the renderer has them;",
            "# OUTPUTS + QA artifacts never enter git (the deliverable MP4/captions/thumbnail -> Release).",
            f"output/{slug}/fonts/",
            f"output/{slug}/renders/",
            f"output/{slug}/_snap*/",
            f"output/{slug}/snapshots/",
            f"output/{slug}/anchors.js",
            f"output/{slug}/{slug}.mp4",
            f"output/{slug}/{slug}_thumbnail.png",
            "",
        ])
        changed = True

    if changed and not dry:
        gi.write_text(text, encoding="utf-8")
    return changed


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--project", required=True, type=Path, help="the rendered project dir, e.g. output/<slug>")
    ap.add_argument("--repo", default=DEFAULT_REPO, help="owner/repo for the Release (default: %(default)s)")
    ap.add_argument("--tag", help="release tag (default: the slug)")
    ap.add_argument("--branch", default="main", help="branch to commit source to (default: main)")
    ap.add_argument("--dry-run", action="store_true", help="print the git + gh sequence, change nothing")
    args = ap.parse_args()

    proj = (args.project if args.project.is_absolute() else (LEARN / args.project)).resolve()
    if not proj.is_dir():
        die(f"project dir not found: {proj}")
    slug = proj.name
    tag = args.tag or slug
    dry = args.dry_run

    # 1) Require a completed render.
    manifest_path = proj / "manifest.json"
    if not manifest_path.exists():
        die(f"{manifest_path} not found — render first (render_and_package.py)")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("status") != "rendered":
        die(f"project status is '{manifest.get('status')}', not 'rendered' — render before publishing")
    title = manifest.get("title", slug)

    mp4 = proj / f"{slug}.mp4"
    vtt = proj / f"{slug}.vtt"
    thumb = proj / f"{slug}_thumbnail.png"
    missing = [p.name for p in (mp4, vtt, thumb) if not p.exists()]
    if missing:
        die(f"missing deliverable(s): {', '.join(missing)} — re-render")
    # The release carries the deliverables a viewer downloads; narration.wav is the audio master
    # and lives on main via LFS, so it is not duplicated here.
    assets = [mp4, vtt, thumb]

    duration = float((manifest.get("video") or {}).get("duration_seconds", 0))
    release_url = f"https://github.com/{args.repo}/releases/tag/{tag}"
    print(f"Publishing '{title}' ({slug}) — {duration:.1f}s")
    print(f"  source  -> {args.branch}   (learn/output/{slug}/)")
    print(f"  release -> {release_url}\n")

    # 2) Link the release into the manifest BEFORE the source commit (URL is deterministic from tag).
    manifest["release"] = {
        "tag": tag,
        "url": release_url,
        "repo": args.repo,
        "published": _dt.date.today().isoformat(),
        "assets": [p.name for p in assets],
    }
    if not dry:
        manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    # 3) Track this video's source on main.
    emit_gitignore_negation(slug, dry)

    # 4) Commit source (renders excluded by the negation) to the target branch.
    rel = f"learn/output/{slug}"
    run(["git", "-C", str(LEARN.parent), "add", rel, "learn/.gitignore"], dry=dry, what="git add")
    run(["git", "-C", str(LEARN.parent), "commit", "-m", f"video: publish {title} ({slug}) source + release link"],
        dry=dry, what="git commit")
    run(["git", "-C", str(LEARN.parent), "push", "origin", f"HEAD:{args.branch}"], dry=dry, what="git push")

    # 5) Create the Release against the pushed source commit, with the deliverables as assets.
    sha = "HEAD"
    if not dry:
        r = subprocess.run(["git", "-C", str(LEARN.parent), "rev-parse", "HEAD"], capture_output=True, text=True)
        sha = r.stdout.strip() or "HEAD"
    notes = (
        f"**{title}** — Microsoft Learn companion video ({duration:.0f}s).\n\n"
        f"Source: [`learn/output/{slug}/`](https://github.com/{args.repo}/tree/{sha}/learn/output/{slug}) "
        f"on `{args.branch}` @ `{sha[:8]}`.\n\n"
        f"Assets: MP4 (video+audio), WebVTT captions, thumbnail. The audio master (narration.wav) "
        f"is tracked on `{args.branch}` via LFS.\n\n"
        f"_This video was produced with AI assistance and carries the required AI-disclosure end card._"
    )
    run(["gh", "release", "create", tag, "--repo", args.repo, "--target", sha,
         "--title", title, "--notes", notes] + [str(p) for p in assets],
        dry=dry, what="gh release create")

    print(f"\n{'DRY-RUN — nothing changed.' if dry else 'OK: published.'}")
    print(f"  source  {args.branch}  learn/output/{slug}/")
    print(f"  release {release_url}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
