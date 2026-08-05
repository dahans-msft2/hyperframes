"""Per-video review ledger — one page that accumulates every gate artifact as the pipeline runs.

Gate artifacts otherwise scatter across folders and formats, and the QA scorecards exist only
in chat, so a decision made at gate 4 is unreviewable by gate 8. This keeps an append-only
record and renders it as a single page.

This does NOT replace Studio. Studio owns preview and the final composition review; this links
out to it. What lives here is the audit trail: what was decided, when, against which artifact.

    py tools/review_index.py record --project <dir> --gate 4 --name "Voice" \\
        --status passed --artifact _audition/audition.html --note "Ava locked, 152 wpm"
    py tools/review_index.py build --project <dir>
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import pathlib
import sys

GATES = {
    1: "Concept and source",
    2: "Video type and profile",
    3: "Look",
    4: "Voice",
    5: "Script",
    6: "Fact-check QA",
    7: "Snapshot QA",
    8: "Render",
    9: "Delivery",
}

# Gate 8 is the render gate. Authorization (a human approving the spend) and completion
# (a validated MP4 exists) are SEPARATE facts — recording approval as 'passed' once made the
# page claim a finished render when nothing had rendered. Approval is 'authorized'; only a
# probed artifact is 'passed'.
RENDER_GATE = 8

STATUS_STYLE = {
    "passed": ("#389A91", "passed"),
    "authorized": ("#B0791F", "authorized"),
    "running": ("#0078D4", "running"),
    "iterate": ("#BF3AC4", "iterate"),
    "failed": ("#C4453A", "failed"),
    "blocked": ("#7A2E2A", "blocked"),
    "pending": ("#8891a0", "pending"),
}


def ledger_path(project: pathlib.Path) -> pathlib.Path:
    return project / "review" / "gates.json"


def load(project: pathlib.Path) -> list[dict]:
    p = ledger_path(project)
    if not p.exists():
        return []
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []


def record(project: pathlib.Path, gate: int, name: str, status: str,
           artifact: str | None, note: str | None) -> None:
    entries = load(project)
    entries.append({
        "gate": gate,
        "name": name or GATES.get(gate, f"Gate {gate}"),
        "status": status,
        "artifact": artifact,
        "note": note,
        "at": dt.datetime.now().isoformat(timespec="seconds"),
    })
    p = ledger_path(project)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(entries, indent=2), encoding="utf-8")


def build(project: pathlib.Path) -> pathlib.Path:
    entries = load(project)
    timing_md = project / "review" / "stage-timing-summary.md"
    timing_link = (
        '<a href="stage-timing-summary.md">stage timing summary</a>'
        if timing_md.exists()
        else '<span class="dim">stage timing summary missing</span>'
    )
    # Latest entry per gate wins; earlier attempts stay in gates.json as history.
    latest: dict[int, dict] = {}
    attempts: dict[int, int] = {}
    for e in entries:
        latest[e["gate"]] = e
        attempts[e["gate"]] = attempts.get(e["gate"], 0) + 1

    rows = []
    for g in sorted(GATES):
        e = latest.get(g)
        status = e["status"] if e else "pending"
        colour, label = STATUS_STYLE.get(status, STATUS_STYLE["pending"])
        name = html.escape(e["name"] if e else GATES[g])
        note = html.escape(e.get("note") or "") if e else ""
        when = (e.get("at") or "").replace("T", " ") if e else ""
        art = e.get("artifact") if e else None
        # review/index.html sits one level down, so project-relative paths need a hop up.
        link = f'<a href="../{html.escape(art)}">open</a>' if art else "<span class=dim>—</span>"
        tries = f' <span class="dim">×{attempts[g]}</span>' if e and attempts[g] > 1 else ""
        rows.append(f"""    <tr>
      <td class="g">{g}</td>
      <td>{name}{tries}</td>
      <td><span class="pill" style="--c:{colour}">{label}</span></td>
      <td>{link}</td>
      <td class="note">{note}</td>
      <td class="dim n">{when}</td>
    </tr>""")

    done = sum(1 for e in latest.values() if e["status"] == "passed")
    page = f"""<!doctype html>
<meta charset="utf-8">
<title>Review — {html.escape(project.name)}</title>
<style>
  body {{ font: 15px/1.55 "Segoe UI", system-ui, sans-serif; color: #091F2E; margin: 0;
         padding: 44px 48px;
         background: radial-gradient(120% 90% at 18% 8%, #FFFCFA, #FFF9F5 42%, #FFFAEF 68%, #F7F2F9 100%); }}
  h1 {{ font-size: 24px; font-weight: 600; margin: 0 0 2px; letter-spacing: -.01em; }}
  p.sub {{ color: #4a5b68; margin: 0 0 28px; }}
  table {{ border-collapse: collapse; width: 100%; max-width: 1100px;
           background: rgba(255,255,255,.62); backdrop-filter: blur(20px);
           border-radius: 10px; overflow: hidden; }}
  th {{ text-align: left; font-size: 11px; letter-spacing: .08em; text-transform: uppercase;
        color: #4a5b68; padding: 12px 16px; border-bottom: 1px solid #eadfd8; font-weight: 600; }}
  td {{ padding: 12px 16px; border-bottom: 1px solid #f0e7e1; vertical-align: top; }}
  td.g {{ font-variant-numeric: tabular-nums; color: #8891a0; width: 34px; }}
  td.note {{ color: #4a5b68; }}
  td.n {{ font-variant-numeric: tabular-nums; white-space: nowrap; }}
  .dim {{ color: #9aa5b1; }}
  .pill {{ display: inline-block; padding: 2px 10px; border-radius: 99px; font-size: 12px;
           font-weight: 600; color: #fff; background: var(--c); }}
  a {{ color: #0078D4; }}
</style>
<h1>{html.escape(project.name)}</h1>
<p class="sub">{done} of {len(GATES)} gates passed &middot; newest attempt shown, full history in
<code>review/gates.json</code> &middot; {timing_link}</p>
<table>
  <tr><th>#</th><th>Gate</th><th>Status</th><th>Artifact</th><th>Note</th><th>When</th></tr>
{chr(10).join(rows)}
</table>
"""
    dest = project / "review" / "index.html"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(page, encoding="utf-8")
    return dest


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("record", help="append a gate result")
    r.add_argument("--project", type=pathlib.Path, required=True)
    r.add_argument("--gate", type=int, required=True, choices=sorted(GATES))
    r.add_argument("--name")
    r.add_argument("--status", required=True, choices=sorted(STATUS_STYLE))
    r.add_argument("--artifact", help="path relative to the project dir")
    r.add_argument("--note")

    b = sub.add_parser("build", help="render review/index.html")
    b.add_argument("--project", type=pathlib.Path, required=True)

    args = ap.parse_args()
    if args.cmd == "record":
        # A render is 'passed' only with an artifact to probe. Permission is 'authorized'.
        if args.gate == RENDER_GATE and args.status == "passed" and not args.artifact:
            print(
                "ERROR: Gate 8 (Render) 'passed' requires --artifact (a validated MP4 or the "
                "render attempt manifest). Record human approval as --status authorized instead.",
                file=sys.stderr,
            )
            return 2
        record(args.project, args.gate, args.name, args.status, args.artifact, args.note)
    dest = build(args.project)
    print(dest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
