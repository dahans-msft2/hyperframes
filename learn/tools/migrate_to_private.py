#!/usr/bin/env python3
"""Assemble the standalone Learn-video repository from this fork.

The Learn pipeline has no code dependency on the HyperFrames monorepo — the CLI arrives from
public npm (pinned in `learn/config.json`) and registry blocks are fetched on demand from the
public upstream registry. What it *does* need is the `learn/` tree, six workflows, the doctrine
skills, and the agent definitions. This script copies exactly that set and nothing else.

The copy set is `git ls-files` filtered by the manifest below, so untracked and ignored artefacts
(renders, `anchors.js`, snapshots, licensed fonts) can never leak into the new repo.

Two known defects are repaired IN TRANSIT rather than carried over:
  T1/T2  "expected exactly one learn/output/<slug>" — broke both the gate and the render the moment
         a second project existed. Replaced with branch-derived resolution (video/<slug>), matched
         case-insensitively because branches are lowercase and folders are Title-Case.
  T3     `choco install ffmpeg` — the Chocolatey feed 503s without retry and is unpinned, so an
         upstream change can silently alter encoder behaviour. Replaced with the pinned
         install-ffmpeg-windows composite action, which is copied across for the purpose.

Every transform asserts its target text exists; a missed transform is a hard failure, never a
silent skip.

Usage:
  py learn/tools/migrate_to_private.py --dest ../learn-video          # dry run (default)
  py learn/tools/migrate_to_private.py --dest ../learn-video --apply
  py learn/tools/migrate_to_private.py --dest ../learn-video --apply --with-output
"""

from __future__ import annotations

import argparse
import pathlib
import shutil
import subprocess
import sys

# ── manifest ────────────────────────────────────────────────────────────────────────────────
# Prefix rules against tracked paths. Longest match wins; an EXCLUDE beats an INCLUDE.
INCLUDE = [
    "learn/",
    ".github/skills/",
    ".github/agents/",
    ".github/docker/learn-ci.Dockerfile",
    ".github/actions/install-ffmpeg-windows/",
    ".github/copilot-instructions.md",
    ".github/ISSUE_TEMPLATE/build-video.yml",
    ".agents/skills/",
    "AGENTS.md",
    "LICENSE",  # Apache 2.0 — required attribution for the vendored skills + prompting guides
]

WORKFLOWS = [
    "video-ci.yml",
    "render-video.yml",
    "render-batch.yml",
    "build-ci-image.yml",
    "deploy-gallery.yml",
    "copilot-setup-steps.yml",
]
INCLUDE += [f".github/workflows/{w}" for w in WORKFLOWS]

# Upstream skills that are creation workflows or unrelated to Learn: they compete for the same
# "make me a video" intent that learn-video-doctrine owns.
EXCLUDE = [
    ".agents/skills/changelog-video/",
    ".agents/skills/captions-overlay/",
]

# ── transforms ──────────────────────────────────────────────────────────────────────────────
T1_OLD = """          n=$(ls -d learn/output/*/ 2>/dev/null | wc -l)
          if [ "$n" != "1" ]; then echo "::error::expected exactly one learn/output/<slug>, found $n"; exit 1; fi
          echo "dir=$(ls -d learn/output/*/ | head -1 | sed 's:/*$::')" >> "$GITHUB_OUTPUT"
"""

T1_NEW = """          # The branch names the project: video/<slug> -> learn/output/<Slug>. Branches are
          # lowercase and folders are Title-Case, so match case-insensitively. Resolving by
          # BRANCH (not "the only directory present") keeps working once main carries more
          # than one video — the assumption that broke both this gate and the render.
          slug="${GITHUB_HEAD_REF#video/}"
          want=$(echo "$slug" | tr '[:upper:]' '[:lower:]')
          dir=""
          for d in learn/output/*/; do
            d="${d%/}"
            [ -d "$d" ] || continue
            if [ "$(basename "$d" | tr '[:upper:]' '[:lower:]')" = "$want" ]; then dir="$d"; fi
          done
          if [ -z "$dir" ]; then
            echo "::error::no learn/output/<slug> matching branch '$GITHUB_HEAD_REF' (expected learn/output/$slug)"
            exit 1
          fi
          echo "dir=$dir" >> "$GITHUB_OUTPUT"
"""

T2_OLD = """            $dirs = @(Get-ChildItem learn/output -Directory -ErrorAction SilentlyContinue)
            if ($dirs.Count -ne 1) { throw "Expected exactly one learn/output/<slug> project on this branch, found $($dirs.Count) \u2014 pass --project via dispatch." }
            $p = "learn/output/$($dirs[0].Name)"
"""

T2_NEW = """            # The branch names the project: video/<slug> -> learn/output/<Slug>, matched
            # case-insensitively (branches are lowercase, folders Title-Case). Resolving by
            # BRANCH rather than "the only directory" survives a second project on main.
            $slug = ('${{ inputs.branch || github.head_ref }}' -replace '^video/', '')
            $dirs = @(Get-ChildItem learn/output -Directory -ErrorAction SilentlyContinue)
            $hit = $dirs | Where-Object { $_.Name -ieq $slug } | Select-Object -First 1
            if (-not $hit) { throw "No learn/output/<slug> matching branch '$slug'. Pass the project explicitly via dispatch, or check the folder name." }
            $p = "learn/output/$($hit.Name)"
"""

T3_OLD = """      - name: Ensure ffmpeg is available
        shell: pwsh
        run: if (-not (Get-Command ffmpeg -ErrorAction SilentlyContinue)) { choco install ffmpeg -y --no-progress }
"""

T3_NEW = """      - name: Ensure ffmpeg is available
        # A PINNED BtbN build, not `choco install ffmpeg`: the Chocolatey feed returns 503/504
        # with no retry, and its ffmpeg is unversioned — an upstream nightly could silently
        # change encoder behaviour under a pipeline whose whole contract is determinism.
        uses: ./.github/actions/install-ffmpeg-windows
"""

T4_OLD = """      # Cache the predictable render toolchain so we don't re-download chrome-headless-shell and
      # re-install ffmpeg every run. On a cache hit the install steps below are fast no-ops
      # (browser ensure sees the cached browser; the ffmpeg check finds it already present).
      - name: Cache render toolchain (chrome-headless-shell + ffmpeg)
        uses: actions/cache@v4
        with:
          path: |
            ~\\.cache\\puppeteer
            ~\\AppData\\Local\\hyperframes
            C:\\ProgramData\\chocolatey\\lib\\ffmpeg
            C:\\ProgramData\\chocolatey\\bin\\ffmpeg.exe
          key: render-toolchain-windows-hf0.7.77-v1
"""

T4_NEW = """      # Cache chrome-headless-shell so it isn't re-downloaded every run. ffmpeg is deliberately
      # NOT cached: the pinned action unpacks it into RUNNER_TEMP, which is wiped per job, so the
      # old chocolatey paths cached nothing once choco stopped being the installer.
      - name: Cache render toolchain (chrome-headless-shell)
        uses: actions/cache@v4
        with:
          path: |
            ~\\.cache\\puppeteer
            ~\\AppData\\Local\\hyperframes
          key: render-toolchain-windows-hf0.7.77-v2
"""

TRANSFORMS = [
    (".github/workflows/video-ci.yml", T1_OLD, T1_NEW, "gate: resolve project from the branch"),
    (".github/workflows/render-video.yml", T2_OLD, T2_NEW, "render: resolve project from the branch"),
    (".github/workflows/render-video.yml", T3_OLD, T3_NEW, "render: pinned ffmpeg instead of choco"),
    (".github/workflows/render-video.yml", T4_OLD, T4_NEW, "render: drop the dead chocolatey cache"),
]

# ── generated files ─────────────────────────────────────────────────────────────────────────
GITATTRIBUTES = """* text=auto eol=lf

# Narration masters and shipped media travel in LFS. Renders themselves are NOT committed —
# they are published as Release assets (see README).
learn/**/*.wav filter=lfs diff=lfs merge=lfs -text
learn/**/*.mp4 filter=lfs diff=lfs merge=lfs -text
learn/assets/grounds/*.png filter=lfs diff=lfs merge=lfs -text
learn/output/**/assets/media/**/*.png filter=lfs diff=lfs merge=lfs -text
"""

GITIGNORE = """# Everything under learn/ is governed by learn/.gitignore — including the per-project
# allowlist that opts each learn/output/<slug> in. Do NOT duplicate those rules here:
# two sources of truth for the same paths is how a licensed font or a 150 MB render
# slips in behind a rule someone thought was covered elsewhere.

node_modules/
__pycache__/
*.pyc
.DS_Store
Thumbs.db
"""

README = """# Learn companion video pipeline

HTML -> MP4 companion videos for Microsoft Learn, built on [HyperFrames](https://hyperframes.heygen.com).

This repository is **self-contained**. It has no dependency on the HyperFrames source tree:

- the CLI arrives from public npm, pinned in `learn/config.json` -> `cli.published_version`
- registry blocks are fetched on demand (`hyperframes add`) and vendored on adoption
- the doctrine and domain skills are installed under `.agents/skills/` and `.github/skills/`

## Layout

| Path | What |
|---|---|
| `learn/tools/` | deterministic pipeline tools (assemble, gates, anchors, render+package) |
| `learn/templates/blocks/` | the Learn-ILT kit — blocks built on `_foundation.css` |
| `learn/profiles/`, `learn/frame-presets/` | video-type profiles and the brand frame preset |
| `learn/docs/prompting/` | vendored upstream prompting guides (Apache 2.0) |
| `learn/output/<slug>/` | one folder per video |
| `.github/skills/learn-*` | brand, pedagogy, narration, rubric, delivery, block adoption |
| `.agents/skills/` | HyperFrames domain skills + motion doctrine |

## Conventions

- **One slug** names the branch (`video/<slug>`), the folder, and the composition id.
- **Renders are Release assets**, never commits. Narration masters live in LFS.
- **Deterministic render**: no wall-clock, no unseeded randomness, no network fetch at render time.
- **Audio is the clock**: cues anchor to transcript word times, never to an assumed words-per-second.

## Gates

```bash
py learn/tools/assemble_scenes.py --project <dir>
py learn/tools/check_subcomps.py --project <dir>
py learn/tools/check_placeholders.py --project <dir>
py learn/tools/check_initial_state.py <dir>/index.html
py learn/tools/brand_conformance.py <block>.html
npx hyperframes@<pinned> lint && npx hyperframes@<pinned> check
```
"""

GENERATED = {".gitattributes": GITATTRIBUTES, ".gitignore": GITIGNORE, "README.md": README}


def tracked_files(root: pathlib.Path) -> list[str]:
    out = subprocess.run(["git", "ls-files"], cwd=root, capture_output=True, text=True, check=True)
    return [p for p in out.stdout.splitlines() if p.strip()]


def wanted(path: str) -> bool:
    if any(path.startswith(x) for x in EXCLUDE):
        return False
    return any(path == inc or path.startswith(inc) for inc in INCLUDE)


def main() -> int:
    ap = argparse.ArgumentParser(description="Assemble the standalone Learn-video repo.")
    ap.add_argument("--dest", required=True, type=pathlib.Path)
    ap.add_argument("--apply", action="store_true", help="write files (default: dry run)")
    ap.add_argument("--with-output", action="store_true", help="include learn/output/ video projects")
    args = ap.parse_args()

    root = pathlib.Path(__file__).resolve().parent.parent.parent
    dest = args.dest.resolve()

    files = [p for p in tracked_files(root) if wanted(p)]
    if not args.with_output:
        files = [p for p in files if not p.startswith("learn/output/")]

    if not files:
        print("nothing matched the manifest — is this being run from the fork?", file=sys.stderr)
        return 1

    groups: dict[str, int] = {}
    for p in files:
        key = "/".join(p.split("/")[:2]) if "/" in p else p
        groups[key] = groups.get(key, 0) + 1

    mode = "APPLY" if args.apply else "DRY RUN"
    print(f"{mode}: {len(files)} tracked file(s) -> {dest}\n")
    for k in sorted(groups):
        print(f"  {k:<44} {groups[k]:>5}")
    print(f"\n  {'generated':<44} {len(GENERATED):>5}  ({', '.join(GENERATED)})")

    skipped = sorted({"/".join(p.split("/")[:2]) for p in tracked_files(root) if not wanted(p)})
    print(f"\n  left behind ({len(skipped)} top-level paths):")
    print("    " + ", ".join(skipped[:14]) + (" …" if len(skipped) > 14 else ""))

    if not args.apply:
        print("\nNo files written. Re-run with --apply to build the tree.")
        return 0

    dest.mkdir(parents=True, exist_ok=True)
    for p in files:
        target = dest / p
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(root / p, target)
    for name, body in GENERATED.items():
        (dest / name).write_text(body, encoding="utf-8")

    print(f"\ncopied {len(files)} file(s)")

    print("\ntransforms:")
    for rel, old, new, desc in TRANSFORMS:
        f = dest / rel
        if not f.exists():
            print(f"  FAIL  {desc}: {rel} not in the copy set")
            return 1
        raw = f.read_text(encoding="utf-8")
        crlf = "\r\n" in raw
        text = raw.replace("\r\n", "\n")
        if old not in text:
            print(f"  FAIL  {desc}: target text not found in {rel} (upstream changed — fix the transform)")
            return 1
        text = text.replace(old, new, 1)
        f.write_text(text.replace("\n", "\r\n") if crlf else text, encoding="utf-8", newline="")
        print(f"  ok    {desc}")

    print(
        "\nnext:\n"
        f"  cd {dest}\n"
        "  git init -b main && git lfs install\n"
        "  git add -A && git commit -m 'feat: Learn companion video pipeline (extracted)'\n"
        "  # then create the PRIVATE repo (org-owned if EMU) and push:\n"
        "  #   git remote add origin <url> && git push -u origin main\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
