"""Stage timing instrumentation for the Learn HyperFrames pipeline.

Examples:
  py tools/stage_timing.py start --project <dir> --stage script-writer --run-id <id>
  py tools/stage_timing.py end --project <dir> --stage script-writer --run-id <id> --status passed
  py tools/stage_timing.py summary --project <dir> --run-id <id>
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
from typing import Any

DEFAULT_STAGE_ORDER = [
    "orchestrator",
    "script-writer",
    "designer",
    "builder",
    "qa",
    "renderer",
]


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def parse_iso(value: str) -> datetime:
    fixed = value.replace("Z", "+00:00")
    return datetime.fromisoformat(fixed)


def events_path(project: Path) -> Path:
    return project / "review" / "stage-timing-events.json"


def summary_json_path(project: Path) -> Path:
    return project / "review" / "stage-timing-summary.json"


def summary_md_path(project: Path) -> Path:
    return project / "review" / "stage-timing-summary.md"


def load_events(project: Path) -> list[dict[str, Any]]:
    path = events_path(project)
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
    if isinstance(data, list):
        return data
    return []


def save_events(project: Path, events: list[dict[str, Any]]) -> None:
    path = events_path(project)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(events, indent=2), encoding="utf-8")


def parse_meta(pairs: list[str]) -> dict[str, str]:
    out: dict[str, str] = {}
    for pair in pairs:
        if "=" not in pair:
            raise ValueError(f"invalid --meta entry '{pair}'. expected key=value")
        key, value = pair.split("=", 1)
        key = key.strip()
        if not key:
            raise ValueError(f"invalid --meta entry '{pair}'. key is empty")
        out[key] = value.strip()
    return out


def append_event(
    project: Path,
    kind: str,
    stage: str,
    run_id: str,
    note: str | None,
    status: str | None,
    meta: dict[str, str],
) -> None:
    events = load_events(project)
    events.append(
        {
            "kind": kind,
            "stage": stage,
            "run_id": run_id,
            "at": now_iso(),
            "status": status,
            "note": note,
            "meta": meta,
        }
    )
    save_events(project, events)


def find_open_start(
    events: list[dict[str, Any]],
    stage: str,
    run_id: str,
) -> dict[str, Any] | None:
    active: list[dict[str, Any]] = []
    for event in events:
        if event.get("run_id") != run_id or event.get("stage") != stage:
            continue
        kind = event.get("kind")
        if kind == "start":
            active.append(event)
        elif kind == "end" and active:
            active.pop(0)
    return active[0] if active else None


def build_attempts(events: list[dict[str, Any]], run_id: str | None) -> list[dict[str, Any]]:
    starts: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    attempts: list[dict[str, Any]] = []

    for event in events:
        stage = str(event.get("stage") or "")
        event_run = str(event.get("run_id") or "")
        if run_id and event_run != run_id:
            continue

        key = (event_run, stage)
        kind = event.get("kind")
        if kind == "start":
            starts[key].append(event)
            continue

        if kind == "end":
            start_event = starts[key].pop(0) if starts[key] else None
            elapsed = None
            if start_event is not None:
                elapsed = (parse_iso(event["at"]) - parse_iso(start_event["at"])).total_seconds()
            attempts.append(
                {
                    "stage": stage,
                    "run_id": event_run,
                    "start_at": start_event.get("at") if start_event else None,
                    "end_at": event.get("at"),
                    "seconds": round(elapsed, 3) if elapsed is not None else None,
                    "status": event.get("status") or "unknown",
                    "note": event.get("note") or "",
                }
            )

    for (event_run, stage), open_starts in starts.items():
        for open_start in open_starts:
            attempts.append(
                {
                    "stage": stage,
                    "run_id": event_run,
                    "start_at": open_start.get("at"),
                    "end_at": None,
                    "seconds": None,
                    "status": "open",
                    "note": open_start.get("note") or "",
                }
            )

    return attempts


def stage_rollup(attempts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    bucket: dict[str, dict[str, Any]] = {}
    for row in attempts:
        stage = row["stage"]
        data = bucket.setdefault(
            stage,
            {
                "stage": stage,
                "attempts": 0,
                "completed_attempts": 0,
                "total_seconds": 0.0,
                "latest_seconds": None,
                "latest_status": "none",
            },
        )
        data["attempts"] += 1
        if row.get("seconds") is not None:
            data["completed_attempts"] += 1
            data["total_seconds"] += float(row["seconds"])
            data["latest_seconds"] = float(row["seconds"])
        data["latest_status"] = row.get("status") or "unknown"

    ordered: list[dict[str, Any]] = []
    seen: set[str] = set()
    for stage in DEFAULT_STAGE_ORDER:
        if stage in bucket:
            ordered.append(bucket[stage])
            seen.add(stage)
    for stage in sorted(bucket):
        if stage not in seen:
            ordered.append(bucket[stage])

    for row in ordered:
        done = row["completed_attempts"]
        row["average_seconds"] = round(row["total_seconds"] / done, 3) if done else None
        row["total_seconds"] = round(row["total_seconds"], 3)

    return ordered


def write_summary_files(project: Path, run_id: str | None, attempts: list[dict[str, Any]]) -> None:
    rollup = stage_rollup(attempts)
    payload = {
        "generated_at_utc": now_iso(),
        "run_id": run_id,
        "attempts": attempts,
        "stages": rollup,
    }
    summary_json_path(project).parent.mkdir(parents=True, exist_ok=True)
    summary_json_path(project).write_text(json.dumps(payload, indent=2), encoding="utf-8")

    header = [
        "# Stage timing summary",
        "",
        f"- Project: {project}",
        f"- Run ID: {run_id or 'all'}",
        f"- Generated (UTC): {payload['generated_at_utc']}",
        "",
        "| Stage | Attempts | Completed | Total sec | Avg sec | Latest sec | Latest status |",
        "|---|---:|---:|---:|---:|---:|---|",
    ]

    rows = []
    for row in rollup:
        rows.append(
            "| {stage} | {attempts} | {completed_attempts} | {total} | {avg} | {latest} | {status} |".format(
                stage=row["stage"],
                attempts=row["attempts"],
                completed_attempts=row["completed_attempts"],
                total=f"{row['total_seconds']:.3f}",
                avg=(f"{row['average_seconds']:.3f}" if row["average_seconds"] is not None else "-"),
                latest=(f"{row['latest_seconds']:.3f}" if row["latest_seconds"] is not None else "-"),
                status=row["latest_status"],
            )
        )

    summary_md_path(project).write_text("\n".join(header + rows) + "\n", encoding="utf-8")


def cmd_start(args: argparse.Namespace) -> int:
    project = args.project.resolve()
    run_id = args.run_id or "default"
    meta = parse_meta(args.meta)

    existing = load_events(project)
    if find_open_start(existing, args.stage, run_id):
        print(
            f"WARN: stage '{args.stage}' already has an open start for run '{run_id}'.",
            file=sys.stderr,
        )

    append_event(project, "start", args.stage, run_id, args.note, None, meta)
    print(f"started  {args.stage}  run={run_id}")
    return 0


def cmd_end(args: argparse.Namespace) -> int:
    project = args.project.resolve()
    run_id = args.run_id or "default"
    meta = parse_meta(args.meta)

    existing = load_events(project)
    open_start = find_open_start(existing, args.stage, run_id)
    if open_start is None:
        print(
            f"WARN: no open start found for stage '{args.stage}' and run '{run_id}'.",
            file=sys.stderr,
        )

    append_event(project, "end", args.stage, run_id, args.note, args.status, meta)
    print(f"ended    {args.stage}  run={run_id}  status={args.status}")
    return 0


def cmd_summary(args: argparse.Namespace) -> int:
    project = args.project.resolve()
    events = load_events(project)
    attempts = build_attempts(events, args.run_id)
    write_summary_files(project, args.run_id, attempts)

    rollup = stage_rollup(attempts)
    if not rollup:
        print("no timing data")
        return 0

    print(f"stage timing for {project}")
    print("stage            attempts  done   total(s)  avg(s)  latest(s)  status")
    for row in rollup:
        avg = f"{row['average_seconds']:.3f}" if row["average_seconds"] is not None else "-"
        latest = f"{row['latest_seconds']:.3f}" if row["latest_seconds"] is not None else "-"
        print(
            f"{row['stage']:<16} {row['attempts']:>8} {row['completed_attempts']:>5} "
            f"{row['total_seconds']:>10.3f} {avg:>7} {latest:>10} {row['latest_status']}"
        )

    print(f"\njson: {summary_json_path(project)}")
    print(f"md:   {summary_md_path(project)}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("start", help="record stage start")
    s.add_argument("--project", type=Path, required=True)
    s.add_argument("--stage", required=True)
    s.add_argument("--run-id", help="defaults to 'default'")
    s.add_argument("--note")
    s.add_argument("--meta", action="append", default=[], help="key=value")

    e = sub.add_parser("end", help="record stage end")
    e.add_argument("--project", type=Path, required=True)
    e.add_argument("--stage", required=True)
    e.add_argument("--run-id", help="defaults to 'default'")
    e.add_argument("--status", default="passed")
    e.add_argument("--note")
    e.add_argument("--meta", action="append", default=[], help="key=value")

    r = sub.add_parser("summary", help="build rollups and summaries")
    r.add_argument("--project", type=Path, required=True)
    r.add_argument("--run-id", help="filter summary to one run id")

    return ap


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        if args.cmd == "start":
            return cmd_start(args)
        if args.cmd == "end":
            return cmd_end(args)
        if args.cmd == "summary":
            return cmd_summary(args)
    except Exception as exc:  # pragma: no cover
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
