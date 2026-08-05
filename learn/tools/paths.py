"""Resolve every canonical path in the Learn HyperFrames pipeline from one anchor.

Agents and tools waste time guessing where things live — which clone root owns a
UID, where the brand preset is, where a project's review folder sits — and then
re-search when a guess misses. This tool answers all of that once. The engine
anchor is this file's own location, so the result is correct regardless of the
caller's working directory.

Examples:
  py tools/paths.py                              # engine paths as JSON
  py tools/paths.py --project <dir>              # add project-scoped paths
  py tools/paths.py --project <dir> --write      # also write <project>/review/paths.json
  py tools/paths.py --format env                 # KEY=VALUE lines for a shell
  py tools/paths.py --format table               # human-readable

Consume it once per stage and derive everything from the result. Do not re-search.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
from typing import Any

# The engine root is this file's parent's parent (tools/ -> hyperframes-scripts/).
ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT / "config.json"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def load_config() -> dict[str, Any]:
    if not CONFIG_PATH.exists():
        return {}
    try:
        return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def node(path: Path) -> dict[str, Any]:
    resolved = path.resolve()
    return {"path": str(resolved), "exists": resolved.exists()}


def first_existing(*candidates: Path) -> Path:
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return candidates[-1]


def engine_paths(config: dict[str, Any]) -> dict[str, dict[str, Any]]:
    brand = config.get("brand", {})
    profile = config.get("profile", {})
    endcard = config.get("endcard", {})

    preset_rel = brand.get("preset_path", "brand/frame-presets/learn-ilt/FRAME.md")
    profiles_rel = profile.get("registry", "profiles/profiles.json")
    endcard_rel = endcard.get("asset", "assets/AI_End_Card.mp4")

    return {
        "pipeline_root": node(ROOT),
        "config": node(CONFIG_PATH),
        "tools": node(ROOT / "tools"),
        "brand": node(ROOT / "brand"),
        "brand_source": node(ROOT / "brand" / "BRAND-SOURCE.md"),
        "frame_preset": node(ROOT / preset_rel),
        "profiles_registry": node(ROOT / profiles_rel),
        "assets": node(ROOT / "assets"),
        "endcard": node(ROOT / endcard_rel),
        "grounds": node(ROOT / "assets" / "grounds"),
        # preflight.ps1 accepts either assets/fonts or a top-level fonts/ dir.
        "fonts": node(first_existing(ROOT / "assets" / "fonts", ROOT / "fonts")),
        # Brand icon library is referenced in place from the sibling animagent-v2 dir.
        "icons": node(ROOT.parent / "animagent-v2" / "icons"),
        "icon_index": node(ROOT / "assets" / "icon-index.json"),
        "archetypes": node(ROOT / "templates" / "archetypes"),
        "archetype_manifest": node(ROOT / "templates" / "archetypes" / "manifest.json"),
        "caption_lexicon": node(ROOT / "tools" / "caption-lexicon.json"),
        "output_root": node(ROOT / config.get("output", {}).get("root", "../hyperframes-output")),
    }


def project_paths(project: Path, config: dict[str, Any]) -> dict[str, dict[str, Any]]:
    project = project.resolve()
    renders_rel = config.get("output", {}).get("renders", "renders")
    review = project / "review"
    return {
        "dir": node(project),
        "review": node(review),
        "renders": node(project / renders_rel),
        "paths_json": node(review / "paths.json"),
        "gates": node(review / "gates.json"),
        "timing_events": node(review / "stage-timing-events.json"),
        "timing_summary": node(review / "stage-timing-summary.md"),
        "review_index": node(review / "index.html"),
    }


def resolve(project: Path | None) -> dict[str, Any]:
    config = load_config()
    payload: dict[str, Any] = {
        "generated_at_utc": now_iso(),
        "pipeline_root": str(ROOT),
        "cli_version": config.get("cli", {}).get("published_version"),
        "paths": engine_paths(config),
        "project": None,
    }
    if project is not None:
        payload["project"] = project_paths(project, config)

    missing = [name for name, info in payload["paths"].items() if not info["exists"]]
    if payload["project"]:
        missing += [
            f"project.{name}"
            for name, info in payload["project"].items()
            if not info["exists"]
        ]
    payload["missing"] = missing
    return payload


def flatten_env(payload: dict[str, Any]) -> list[str]:
    lines: list[str] = []
    if payload.get("cli_version"):
        lines.append(f"HF_CLI_VERSION={payload['cli_version']}")
    for name, info in payload["paths"].items():
        lines.append(f"HF_{name.upper()}={info['path']}")
    if payload.get("project"):
        for name, info in payload["project"].items():
            lines.append(f"HF_PROJECT_{name.upper()}={info['path']}")
    return lines


def render_table(payload: dict[str, Any]) -> list[str]:
    rows = ["Engine paths (anchor: %s)" % payload["pipeline_root"], ""]
    if payload.get("cli_version"):
        rows.append(f"  pinned CLI: hyperframes@{payload['cli_version']} (config.json)")
        rows.append("")
    width = max(len(n) for n in payload["paths"])
    for name, info in payload["paths"].items():
        mark = "ok " if info["exists"] else "MISS"
        rows.append(f"  [{mark}] {name.ljust(width)}  {info['path']}")
    if payload.get("project"):
        rows += ["", "Project paths", ""]
        width = max(len(n) for n in payload["project"])
        for name, info in payload["project"].items():
            mark = "ok " if info["exists"] else "MISS"
            rows.append(f"  [{mark}] {name.ljust(width)}  {info['path']}")
    if payload["missing"]:
        rows += ["", "Missing: " + ", ".join(payload["missing"])]
    return rows


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--project", type=Path, help="project directory to add project-scoped paths")
    ap.add_argument("--format", choices=["json", "env", "table"], default="json")
    ap.add_argument("--write", action="store_true", help="write <project>/review/paths.json (requires --project)")
    args = ap.parse_args()

    if args.write and args.project is None:
        print("ERROR: --write requires --project", file=sys.stderr)
        return 2

    payload = resolve(args.project)

    if args.write:
        dest = Path(payload["project"]["paths_json"]["path"])
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        # Refresh existence now that the file was written.
        payload = resolve(args.project)

    if args.format == "json":
        print(json.dumps(payload, indent=2))
    elif args.format == "env":
        print("\n".join(flatten_env(payload)))
    else:
        print("\n".join(render_table(payload)))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
