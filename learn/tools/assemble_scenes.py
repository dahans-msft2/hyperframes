"""Assemble per-scene sub-composition files into one render-ready host index.html.

Modular composition contract (see hyperframes-core references/sub-compositions.md):
  - Each scene is its own file: scenes/<NN>-<id>.html, wrapped in <template>, with a
    self-contained, scene-relative GSAP timeline registered at window.__timelines["<id>"].
  - This host is a STANDALONE composition (root <div> directly in <body>, no template).
    It declares one slot per scene, tiles them on a track, mounts the narration audio and
    the AI end card at the root, and registers a thin root timeline.

Why modular: a 300-line-per-beat monolith is hard to review, expensive to load, and a
single edit re-times everything. Per-scene files are inspected, previewed, and changed in
isolation; the render still flattens to one MP4.

Seam boundary (honors the design contract):
  - WITHIN a scene: motion lives in the scene file's own timeline.
  - BETWEEN scenes: this host owns the seam. The default is a hard cut on one track with an
    OPAQUE root ground, which is white-flash-safe by construction (seam-craft). Cross-scene
    cut-the-curve is a host-timeline concern to be stamped here later; the schema already
    carries a per-scene `seam` field so that injector is a drop-in.

Usage:
  py tools/assemble_scenes.py --project <dir>                 # reads <dir>/scenes.json
  py tools/assemble_scenes.py --scenes <path> --out <path>
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any

TOOLS = Path(__file__).resolve().parent
ENGINE = TOOLS.parent

# Cross-scene cut-the-curve directions. Ported from motion-doctrine seam-stamp.mjs:
# exit travels 12% one way and fades (power3.in); entry ignites from -10% the same
# direction and decelerates (power4.out). Adjacent (no overlap) — the fade trick sells it.
SEAM_DIRS = {
    "cut-left": ("xPercent", -1),
    "cut-right": ("xPercent", 1),
    "cut-up": ("yPercent", -1),
    "cut-down": ("yPercent", 1),
}
HARD_SEAMS = {"hard", "none", "cut", ""}


def die(msg: str) -> None:
    print(f"ERROR: assemble_scenes: {msg}", file=sys.stderr)
    raise SystemExit(1)


def r3(x: float) -> float:
    return round(x * 1000) / 1000


def load_scenes(path: Path) -> dict[str, Any]:
    if not path.exists():
        die(f"scenes manifest not found: {path}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        die(f"scenes manifest is not valid JSON: {exc}")
    return {}


def font_faces(fonts: list[dict[str, Any]], project_dir: Path | None = None) -> str:
    blocks = []
    for f in fonts:
        family = f["family"]
        weight = f.get("weight", 400)
        src = f["src"]
        style = f.get("style", "normal")
        if project_dir is not None:
            src_path = Path(src)
            if not src_path.is_absolute():
                src_path = project_dir / src_path
            if not src_path.exists():
                continue
        blocks.append(
            "      @font-face {\n"
            f'        font-family: "{family}";\n'
            f"        font-weight: {weight};\n"
            f"        font-style: {style};\n"
            f'        src: url("{src}") format("woff2");\n'
            "        font-display: block;\n"
            "      }"
        )
    return "\n\n".join(blocks)


def build_html(manifest: dict[str, Any], scenes_dir_name: str, project_dir: Path | None = None) -> tuple[str, dict[str, Any]]:
    width = int(manifest.get("width", 1920))
    height = int(manifest.get("height", 1080))
    cid = manifest.get("composition_id", "root")
    ground = manifest.get("root_background", "#fff8f3")
    gsap_src = manifest.get("gsap", "assets/vendor/gsap.min.js")
    anchors_src = manifest.get("anchors")
    fonts = manifest.get("fonts", [])
    title = manifest.get("title", "Learn companion video")

    scenes = manifest.get("scenes", [])
    if not scenes:
        die("scenes manifest has no scenes")

    # Tile scenes sequentially (hard cut). Each scene occupies [start, start+duration).
    tiled = []
    cursor = 0.0
    for i, sc in enumerate(scenes):
        if "id" not in sc or "duration" not in sc:
            die(f"scene[{i}] needs both 'id' and 'duration'")
        dur = float(sc["duration"])
        if dur <= 0:
            die(f"scene '{sc['id']}' has non-positive duration {dur}")
        src = sc.get("src", f"{scenes_dir_name}/{sc['id']}.html")
        tiled.append({"id": sc["id"], "src": src, "start": r3(cursor), "duration": r3(dur),
                      "seam": sc.get("seam")})
        cursor += dur
    scenes_total = r3(cursor)

    # Cross-scene seams on the ROOT timeline. Each scene's `seam` is the transition INTO it
    # from the previous scene. The first scene has no incoming seam; a non-first scene defaults
    # to cut-left so a modular video keeps the monolith's film grammar unless told otherwise.
    seam_lines: list[str] = []
    for i in range(1, len(tiled)):
        prev, cur = tiled[i - 1], tiled[i]
        seam = (cur.get("seam") or "cut-left").strip().lower()
        if seam in HARD_SEAMS:
            continue
        if seam not in SEAM_DIRS:
            die(f"scene '{cur['id']}' has unknown seam '{seam}'. use one of: "
                + ", ".join(list(SEAM_DIRS) + ["hard"]))
        prop, direction = SEAM_DIRS[seam]
        cut = cur["start"]
        exit_at = r3(cut - 0.34)
        seam_lines.append(f'      // SEAM {prev["id"]} -> {cur["id"]} : {seam} (cut @{cut})')
        seam_lines.append(
            f'      tl.to("#slot-{prev["id"]}", {{ {prop}: {12 * direction}, autoAlpha: 0, '
            f'duration: 0.34, ease: "power3.in" }}, {exit_at});'
        )
        seam_lines.append(f'      tl.set("#slot-{prev["id"]}", {{ autoAlpha: 0 }}, {cut});')
        seam_lines.append(
            f'      tl.fromTo("#slot-{cur["id"]}", {{ {prop}: {-10 * direction}, autoAlpha: 0.35 }}, '
            f'{{ {prop}: 0, autoAlpha: 1, duration: 0.42, ease: "power4.out", immediateRender: false }}, {cut});'
        )

    narration = manifest.get("narration")
    narration_dur = r3(float((narration or {}).get("duration", scenes_total)))
    narration_start = r3(float((narration or {}).get("start", 0)))
    narration_track = int((narration or {}).get("track", 10))
    narration_src = (narration or {}).get("src", "narration.wav")

    endcard = manifest.get("endcard")
    endcard_dur = r3(float((endcard or {}).get("duration", 0)))
    endcard_src = (endcard or {}).get("src", "assets/AI_End_Card.mp4")
    endcard_track = int((endcard or {}).get("track", 11))

    total = r3(scenes_total + (endcard_dur if endcard else 0))

    # Fade bookends: a short fade-in "breath" at the top and a fade-to-black on the end card's
    # tail (no added time — it lands inside the end card's existing window). Default on.
    bookend = manifest.get("bookend", {})
    intro_fade = r3(float(bookend.get("intro", 0.5)))
    outro_fade = r3(float(bookend.get("outro", 0.7)))
    fade_color = bookend.get("color", "#000")
    outro_anchor = bookend.get("outro_anchor")
    outro_start = None
    if outro_fade > 0:
        outro_start = f"W.{outro_anchor}" if outro_anchor else r3(total - outro_fade)
    bookend_lines: list[str] = []
    if intro_fade > 0:
        bookend_lines.append('      gsap.set("#fade-in", { autoAlpha: 1 });')
        bookend_lines.append(
            f'      tl.to("#fade-in", {{ autoAlpha: 0, duration: {intro_fade}, ease: "power2.out" }}, 0);'
        )
    if outro_start is not None:
        bookend_lines.append(
            f'      tl.fromTo("#fade-out", {{ autoAlpha: 0 }}, '
            f'{{ autoAlpha: 1, duration: {outro_fade}, ease: "power2.in", immediateRender: false }}, {outro_start});'
        )

    # ---- head ----
    head_scripts = [f'    <script src="{gsap_src}"></script>']
    if anchors_src:
        head_scripts.append(f'    <script src="{anchors_src}"></script>')

    ff = font_faces(fonts, project_dir=project_dir)
    slot_selector = "#root > div[data-composition-src]"
    fallback_fonts = """      @font-face {
        font-family: "Segoe UI";
        font-weight: 400;
        font-style: normal;
        src: local("Segoe UI");
        font-display: block;
      }

      @font-face {
        font-family: "Segoe UI";
        font-weight: 600;
        font-style: normal;
        src: local("Segoe UI");
        font-display: block;
      }

      @font-face {
        font-family: "Segoe UI Variable";
        font-weight: 400;
        font-style: normal;
        src: local("Segoe UI Variable");
        font-display: block;
      }

      @font-face {
        font-family: "Segoe UI Variable";
        font-weight: 600;
        font-style: normal;
        src: local("Segoe UI Variable");
        font-display: block;
      }"""
    style = f"""    <style>
{fallback_fonts}
{ff}

      * {{ box-sizing: border-box; }}

      html, body {{
        width: {width}px; height: {height}px;
        margin: 0; overflow: hidden;
        background: {ground};
        font-family: "Segoe UI", "Segoe UI Variable", "Arial", sans-serif;
      }}

      #root {{
        position: relative;
        width: {width}px; height: {height}px;
        overflow: hidden;
        /* Opaque stage ground: white-flash guard for any seam dip (seam-craft). */
        background: {ground};
      }}

      /* Scene slots fill the root and stack by mount order. */
      {slot_selector} {{ position: absolute; inset: 0; }}

      /* Fade bookends: opaque covers above everything; the timeline drives their opacity. */
      .fade-cover {{ position: absolute; inset: 0; background: {fade_color}; z-index: 100; pointer-events: none; }}
    </style>"""

    # ---- body ----
    slots = []
    if narration:
        slots.append(
            f'      <audio id="narration" class="clip" src="{narration_src}" '
            f'data-start="{narration_start}" data-duration="{narration_dur}" data-track-index="{narration_track}"></audio>'
        )
    for sc in tiled:
        slots.append(
            f'      <div id="slot-{sc["id"]}" class="clip"\n'
            f'           data-composition-id="{sc["id"]}"\n'
            f'           data-composition-src="{sc["src"]}"\n'
            f'           data-start="{sc["start"]}" data-duration="{sc["duration"]}"\n'
            f'           data-track-index="1"\n'
            f'           data-width="{width}" data-height="{height}"></div>'
        )
    if endcard and endcard_dur > 0:
        slots.append(
            f'      <video id="ai-end-card" class="clip" src="{endcard_src}" '
            f'data-start="{scenes_total}" data-duration="{endcard_dur}" '
            f'data-track-index="{endcard_track}" muted></video>'
        )
    if intro_fade > 0:
        slots.append(
            f'      <div id="fade-in" class="fade-cover clip" data-start="0" '
            f'data-duration="{intro_fade}" data-track-index="20"></div>'
        )
    if outro_start is not None:
        slots.append(
            f'      <div id="fade-out" class="fade-cover clip" data-start="{outro_start}" '
            f'data-duration="{outro_fade}" data-track-index="20"></div>'
        )

    slots_html = "\n\n".join(slots)

    seam_block = ""
    if seam_lines:
        seam_block = (
            "\n\n      // <seams:auto> — cross-scene cut-the-curve, stamped by assemble_scenes.py from scenes.json.\n"
            + "\n".join(seam_lines)
            + "\n      // </seams:auto>"
        )

    bookend_block = ""
    if bookend_lines:
        bookend_block = (
            "\n\n      // <bookends> — fade-in breath + fade-to-black on the end card.\n"
            + "\n".join(bookend_lines)
            + "\n      // </bookends>"
        )

    body = f"""  <body>
    <div id="root" data-composition-id="{cid}" data-start="0" data-duration="{total}"
         data-width="{width}" data-height="{height}" data-resolution="landscape">

{slots_html}
    </div>

    <script>
      window.__timelines = window.__timelines || {{}};
      // Thin root timeline: scene motion lives in each scene file. This timeline carries only
      // the cross-scene seams, stamped against the slot-<id> hosts.
      const tl = gsap.timeline({{ paused: true }});
      const W = window.__anchors || {{}};
      window.__timelines["{cid}"] = tl;{seam_block}{bookend_block}
    </script>
  </body>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width={width}, height={height}">
    <title>{title}</title>
{chr(10).join(head_scripts)}
{style}
  </head>
{body}
</html>
"""

    summary = {
        "scenes": len(tiled),
        "seams": sum(1 for ln in seam_lines if ln.lstrip().startswith("// SEAM")),
        "scenes_total_seconds": scenes_total,
        "endcard_seconds": endcard_dur,
        "composition_seconds": total,
        "narration_seconds": narration_dur,
        "tiled": tiled,
    }
    return html, summary


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--project", type=Path, help="project dir (reads <dir>/scenes.json, writes <dir>/index.html)")
    ap.add_argument("--scenes", type=Path, help="explicit scenes.json path")
    ap.add_argument("--out", type=Path, help="explicit output index.html path")
    ap.add_argument("--scenes-dir", default="scenes", help="scene file subdir name (default: scenes)")
    args = ap.parse_args()

    if args.scenes:
        scenes_path = args.scenes
    elif args.project:
        scenes_path = args.project / "scenes.json"
    else:
        die("pass --project or --scenes")

    manifest = load_scenes(scenes_path)

    if args.out:
        out_path = args.out
    elif args.project:
        out_path = args.project / "index.html"
    else:
        out_path = scenes_path.parent / "index.html"

    project_dir = args.project.resolve() if args.project else scenes_path.parent.resolve()
    html, summary = build_html(manifest, args.scenes_dir, project_dir=project_dir)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")

    print(f"assembled {summary['scenes']} scene(s), {summary['seams']} cross-scene seam(s) -> {out_path}")
    print(f"  scenes total : {summary['scenes_total_seconds']}s")
    print(f"  end card     : {summary['endcard_seconds']}s")
    print(f"  composition  : {summary['composition_seconds']}s")
    for sc in summary["tiled"]:
        print(f"  [{sc['start']:>8}] {sc['id']:<24} {sc['duration']}s  ({sc['src']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
