#!/usr/bin/env python3
"""One-shot render + package: the deterministic tail of the Learn video pipeline.

Runs, in order: placeholder guard -> lint -> render -> promote scratch -> captions (VTT) ->
thumbnail -> verify, and exits 0 ONLY when a validated MP4 + VTT + thumbnail all exist. It exists
because the renderer *subagent* has repeatedly returned early, orphaning a render whose scratch
output was never promoted, captioned, or validated. The orchestrator runs THIS one blocking script
at the render gate, so packaging cannot half-finish: there is no "render started" success state —
either the deliverables exist and validate (exit 0) or it fails loudly (non-zero).

    py tools/render_and_package.py --project output/My-Video
    py tools/render_and_package.py --project output/My-Video --thumb-at 212

Assumes narration.wav + transcript.json already exist (they precede the builder). If they don't,
that is a pipeline-order error and this aborts.
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
CONFIG_JSON = LEARN / "config.json"


def die(msg: str) -> "NoReturn":  # type: ignore[name-defined]
    print(f"FAIL: {msg}", file=sys.stderr)
    raise SystemExit(1)


def run(cmd: list[str], *, cwd: Path | None = None, what: str) -> subprocess.CompletedProcess:
    print(f"  · {what} …")
    r = subprocess.run(cmd, cwd=str(cwd) if cwd else None, capture_output=True, text=True)
    if r.returncode != 0:
        tail = "\n".join((r.stderr or r.stdout).splitlines()[-12:])
        die(f"{what} failed (exit {r.returncode}):\n{tail}")
    return r


def slugify(title: str) -> str:
    words = re.findall(r"[A-Za-z0-9]+", title)
    return "-".join(w[:1].upper() + w[1:] for w in words) or "video"


def main() -> int:
    ap = argparse.ArgumentParser(description="Render a Learn composition and package the deliverables (blocking).")
    ap.add_argument("--project", required=True, help="project directory")
    ap.add_argument("--cli-version", help="pinned hyperframes CLI version (default: config.json cli.published_version)")
    ap.add_argument("--offset", type=float, help="VTT caption offset seconds (default: scenes.json narration.start)")
    ap.add_argument("--thumb-at", type=float, help="thumbnail timestamp seconds (default: 60%% through the video)")
    ap.add_argument("--lexicon", help="caption lexicon json (default: <project>/captions.lexicon.json if present)")
    ap.add_argument("--skip-render", action="store_true", help="reuse an existing renders/*.mp4 (promote+package only)")
    args = ap.parse_args()

    proj = Path(args.project).resolve()
    if not proj.is_dir():
        die(f"project {proj} does not exist")
    cfg = json.loads(CONFIG_JSON.read_text(encoding="utf-8"))
    cli = args.cli_version or cfg["cli"]["published_version"]

    scenes_path = proj / "scenes.json"
    scenes = json.loads(scenes_path.read_text(encoding="utf-8")) if scenes_path.exists() else {}
    title = scenes.get("title") or proj.name

    manifest_path = proj / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else {}
    slug = (manifest.get("deliverables", {}).get("mp4", "") or "").removesuffix(".mp4") or slugify(title)

    # Preconditions: audio + transcript must already exist (they precede the builder).
    narration_wav = proj / "narration.wav"
    transcript = proj / "transcript.json"
    index_html = proj / "index.html"
    if not index_html.exists():
        die("no index.html — assemble the composition before rendering")
    if not narration_wav.exists() or not transcript.exists():
        die("narration.wav / transcript.json missing — run TTS + transcribe before rendering (they precede the build)")

    print(f"render + package: {title}  ->  {proj.name}  (CLI {cli})")

    # 1) Placeholder guard — a scaffolded chrome scene that still says __FILL__ must NOT render.
    run([sys.executable, str(TOOLS / "check_placeholders.py"), "--project", str(proj)],
        what="placeholder guard")

    # 2) Lint (fast structural gate; the heavy browser `check` is the QA gate upstream).
    run(["npx", "--yes", f"hyperframes@{cli}", "lint"], cwd=proj, what="lint")

    # 3) Warm ffmpeg (WinGet cold-start can blow the CLI's 5s probe) + confirm it is on PATH.
    if shutil.which("ffmpeg") is None or shutil.which("ffprobe") is None:
        die("ffmpeg/ffprobe not on PATH — dot-source tools/preflight.ps1 -FixPath first")
    subprocess.run(["ffmpeg", "-hide_banner", "-version"], capture_output=True)

    # 4) Render to the scratch renders/ dir.
    if not args.skip_render:
        run(["npx", "--yes", f"hyperframes@{cli}", "render"], cwd=proj, what="render")

    renders = sorted((proj / "renders").glob("*.mp4"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not renders:
        die("render produced no renders/*.mp4")
    scratch = renders[0]

    # 5) Promote scratch -> deliverable MP4.
    final_mp4 = proj / f"{slug}.mp4"
    shutil.copy2(scratch, final_mp4)

    # 6) Captions. Offset = when narration starts in the video (scenes.json narration.start, else 3.0).
    offset = args.offset if args.offset is not None else float((scenes.get("narration") or {}).get("start", 3.0))
    lex = args.lexicon or (str(proj / "captions.lexicon.json") if (proj / "captions.lexicon.json").exists() else None)
    vtt = proj / f"{slug}.vtt"
    vtt_cmd = [sys.executable, str(TOOLS / "make_vtt.py"), str(transcript), "-o", str(vtt), "--offset", str(offset)]
    if lex:
        vtt_cmd += ["--lexicon", lex]
    run(vtt_cmd, what=f"captions (offset {offset}s{', lexicon' if lex else ''})")

    # 7) Verify the MP4, then extract a thumbnail at a frame with signal.
    def ffprobe(*entries: str) -> str:
        r = subprocess.run(["ffprobe", "-v", "error", *entries, str(final_mp4)], capture_output=True, text=True)
        return r.stdout.strip()

    duration = float(ffprobe("-show_entries", "format=duration", "-of", "default=nk=1:nw=1") or 0)
    streams = ffprobe("-show_entries", "stream=codec_type", "-of", "csv=p=0").split()
    if duration <= 0:
        die(f"rendered MP4 has no duration ({final_mp4})")
    if "video" not in streams or "audio" not in streams:
        die(f"rendered MP4 missing a stream (got: {streams or 'none'})")

    thumb_at = args.thumb_at if args.thumb_at is not None else round(duration * 0.6, 2)
    thumb = proj / f"{slug}_thumbnail.png"
    run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-ss", str(thumb_at), "-i", str(final_mp4),
         "-frames:v", "1", str(thumb)], what=f"thumbnail @ {thumb_at}s")

    # 8) Update the manifest and report.
    manifest.update({
        "title": title,
        "status": "rendered",
        "video": {"file": final_mp4.name, "duration_seconds": round(duration, 2)},
        "deliverables": {
            "mp4": final_mp4.name,
            "captions_vtt": vtt.name,
            "transcript": "transcript.json",
            "thumbnail": thumb.name,
            "narration_wav": "narration.wav",
        },
    })
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"\nOK: packaged {slug}")
    print(f"  mp4       {final_mp4.name}  ({duration:.2f}s, video+audio)")
    print(f"  captions  {vtt.name}")
    print(f"  thumbnail {thumb.name}")
    print(f"  manifest  manifest.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
