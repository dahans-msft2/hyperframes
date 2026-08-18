#!/usr/bin/env python3
"""Brand-conformance reporter for Learn-ILT kit blocks and adopted upstream blocks.

`hyperframes check` measures the RENDERED result (contrast, layout). It cannot see
*how* a block got there — a block can pass contrast while hardcoding #8661C5 everywhere,
which silently breaks the moment a host swaps the ground (dark-field flips ink to white,
but a hardcoded colour does not follow).

This tool audits the SOURCE against the five authoring rules in
`templates/blocks/_foundation.css`, so adopting an upstream registry block is a complete
sweep rather than an eyeball pass:

  R1  no hardcoded brand colours   -> read a token
  R2  no px type                   -> use the --fs-* cqw scale
  R3  contrast law                 -> text is --ink/--ink-soft; accents colour GRAPHICS only
  R4  no hardcoded ground          -> the host picks it via #root[data-ground]
  R5  host owns lifetime           -> register a paused timeline; never self-hide #root

A genuine exception (a fixed brand mark like the Microsoft logo squares, or syntax
highlighting where colour IS the information) is declared inline, mirroring the repo's
`anchor-exempt` convention:

    background: #F25022; /* brand-exempt: Microsoft logo square, not themeable */

An exemption without a reason is still a finding — the justification is the point.

Palette and type tokens are read FROM `_foundation.css`, so this never drifts from the kit.

Usage:
  py learn/tools/brand_conformance.py <file.html> [<file.html> ...] [--json] [--quiet]
  py learn/tools/brand_conformance.py learn/templates/blocks/*.html
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

FOUNDATION = pathlib.Path(__file__).resolve().parent.parent / "templates" / "blocks" / "_foundation.css"

BEGIN_MARK = re.compile(r"/\*\s*=+\s*BEGIN _foundation\.css", re.I)
END_MARK = re.compile(r"/\*\s*=+\s*END _foundation\.css", re.I)

HEX = re.compile(r"#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b")
FUNC_COLOR = re.compile(r"\b(?:rgba?|hsla?)\s*\(", re.I)
PX_TYPE = re.compile(r"font-size\s*:\s*[\d.]+px", re.I)
FONT_FAMILY = re.compile(r"font-family\s*:\s*([^;}\n]+)", re.I)
TEXT_ACCENT = re.compile(r"(?<!-)\bcolor\s*:\s*var\(\s*--accent(?!-ink)", re.I)
TEXT_LITERAL = re.compile(r"(?<!-)\bcolor\s*:\s*(#[0-9a-fA-F]{3,6}|rgba?\(|hsla?\()", re.I)
ROOT_GROUND = re.compile(r"#root\b[^{}]*\{[^{}]*background[^;{}]*gradient\(", re.I | re.S)
TIMELINE_KEY = re.compile(r'__timelines\s*\[\s*"([^"]+)"\s*\]\s*=')
COMP_ID = re.compile(r'data-composition-id\s*=\s*"([^"]+)"')
SELF_HIDE = re.compile(r'(?:to|fromTo|set)\s*\(\s*["\']#root["\'][^)]*?(?:opacity|autoAlpha)\s*:\s*0', re.I | re.S)
EXEMPT = re.compile(r"brand-exempt\s*:\s*(\S.*?)\s*(?:\*/|-->|$)", re.I)


def load_tokens() -> tuple[dict[str, tuple[int, int, int]], list[str]]:
    """Colour tokens (as RGB) and the --fs-* type scale, read from the foundation."""
    colors: dict[str, tuple[int, int, int]] = {}
    type_scale: list[str] = []
    if not FOUNDATION.exists():
        return colors, type_scale
    css = FOUNDATION.read_text(encoding="utf-8")
    for name, value in re.findall(r"(--[a-z0-9-]+)\s*:\s*([^;]+);", css, re.I):
        if name.startswith("--fs-"):
            if name not in type_scale:
                type_scale.append(name)
            continue
        # multi-stop tokens (--ground) are surfaces, not colours — never suggest them for a flat value
        if "gradient(" in value or "url(" in value:
            continue
        m = HEX.search(value)
        if m:
            colors.setdefault(name, hex_to_rgb(m.group(0)))
    return colors, type_scale


def hex_to_rgb(h: str) -> tuple[int, int, int]:
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def nearest_token(hexval: str, colors: dict[str, tuple[int, int, int]]) -> "str | None":
    if not colors:
        return None
    r, g, b = hex_to_rgb(hexval)
    name, dist = min(
        ((n, (r - c[0]) ** 2 + (g - c[1]) ** 2 + (b - c[2]) ** 2) for n, c in colors.items()),
        key=lambda t: t[1],
    )
    return f"var({name})" if dist <= 3 * (60**2) else None


def strip_foundation(text: str) -> str:
    """Blank out the verbatim foundation copy — its literals are the source of truth."""
    lines = text.split("\n")
    out, inside = [], False
    for ln in lines:
        if BEGIN_MARK.search(ln):
            inside = True
        if inside:
            out.append("")
            if END_MARK.search(ln):
                inside = False
            continue
        out.append(ln)
    return "\n".join(out)


def audit(path: pathlib.Path, colors, type_scale) -> list[dict]:
    raw = path.read_text(encoding="utf-8", errors="replace")
    has_foundation = bool(BEGIN_MARK.search(raw))
    body = strip_foundation(raw)
    lines = body.split("\n")
    f: list[dict] = []

    def add(rule, sev, line, msg, fix):
        f.append({"rule": rule, "severity": sev, "line": line, "message": msg, "fix": fix})

    if not has_foundation:
        add("R0", "error", 1, "no verbatim _foundation.css block found",
            "Paste _foundation.css between the BEGIN/END markers at the top of <style>.")

    in_comment = False
    exempt_run: "str | None" = None
    for i, ln in enumerate(lines, 1):
        stripped = ln.strip()

        # a blank line ends a standalone exemption's scope
        if not stripped:
            exempt_run = None
            continue

        # a justified exception: on the offending line, or as a comment above a run of them
        ex = EXEMPT.search(ln)
        if ex and ex.group(1).strip():
            reason = ex.group(1).strip()
            f.append({"rule": "exempt", "severity": "note", "line": i,
                      "message": f"brand-exempt: {reason}", "fix": ""})
            if not re.sub(r"<!--.*?-->|/\*.*?\*/|//.*$|<!--.*$|.*-->", "", ln).strip():
                exempt_run = reason
            continue

        # block comments (CSS and HTML) carry prose, not shipped values
        if in_comment:
            if "*/" in ln or "-->" in ln:
                in_comment = False
            continue
        if (stripped.startswith("/*") and "*/" not in stripped) or (
            stripped.startswith("<!--") and "-->" not in stripped
        ):
            in_comment = True
            continue
        if stripped.startswith("//") or stripped.startswith("*"):
            continue
        if exempt_run:
            continue

        for m in HEX.finditer(ln):
            tok = nearest_token(m.group(0), colors)
            add("R1", "error", i, f"hardcoded colour {m.group(0)}",
                f"nearest token is {tok} — confirm the ROLE (ink/accent/surface) before applying"
                if tok else "read a token (or add one to _foundation.css)")
        if FUNC_COLOR.search(ln) and "var(" not in ln:
            add("R1", "warn", i, "literal rgb()/hsl() colour",
                "read a token; translucency belongs in --paper-veil/--border/--shadow")
        for _ in PX_TYPE.finditer(ln):
            add("R2", "error", i, "font-size in px",
                f"use the cqw scale ({', '.join(type_scale[:4])}…) so type scales with the mount")
        fm = FONT_FAMILY.search(ln)
        if fm and "var(" not in fm.group(1):
            add("R1", "warn", i, f"hardcoded font-family {fm.group(1).strip()}",
                "inherit from #root, or compose .ilt-title/.ilt-body/.ilt-caption")
        if TEXT_ACCENT.search(ln):
            add("R3", "error", i, "accent token used as TEXT colour",
                "text is var(--ink)/var(--ink-soft); accents colour graphics only")
        if TEXT_LITERAL.search(ln):
            add("R3", "error", i, "text coloured with a literal",
                "text is var(--ink)/var(--ink-soft)")

    if ROOT_GROUND.search(body):
        line = body[: ROOT_GROUND.search(body).start()].count("\n") + 1
        add("R4", "error", line, "#root paints its own gradient ground",
            "delete it; the host selects the ground via #root[data-ground]")
    if SELF_HIDE.search(body):
        line = body[: SELF_HIDE.search(body).start()].count("\n") + 1
        add("R5", "error", line, "block hides its own #root (exit animation)",
            "the host owns scene lifetime; never fade #root out")

    keys = TIMELINE_KEY.findall(body)
    ids = COMP_ID.findall(body)
    stem = path.stem
    if not keys:
        add("R5", "error", 1, "no window.__timelines[\"<id>\"] registration",
            "register the paused timeline under the block id")
    else:
        for k in set(keys):
            if ids and k not in ids:
                add("R5", "error", 1, f'timeline key "{k}" has no matching data-composition-id',
                    f"id, timeline key and filename must all be \"{stem}\"")
        if stem not in ("_foundation",) and stem not in set(keys) | set(ids):
            add("R5", "warn", 1, f'filename "{stem}" differs from id/timeline key {sorted(set(keys) | set(ids))}',
                "file, data-composition-id and timeline key share ONE name")
    return f


def main() -> int:
    ap = argparse.ArgumentParser(description="Audit a block against the Learn-ILT kit foundation rules.")
    ap.add_argument("files", nargs="+", type=pathlib.Path)
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--quiet", action="store_true", help="only print files that have findings")
    args = ap.parse_args()

    colors, type_scale = load_tokens()
    report, errors = {}, 0

    for p in args.files:
        if not p.exists():
            print(f"missing: {p}", file=sys.stderr)
            errors += 1
            continue
        found = audit(p, colors, type_scale)
        report[str(p)] = found
        errors += sum(1 for x in found if x["severity"] == "error")

    if args.json:
        print(json.dumps(report, indent=2))
        return 1 if errors else 0

    for path, found in report.items():
        errs = [x for x in found if x["severity"] == "error"]
        warns = [x for x in found if x["severity"] == "warn"]
        notes = [x for x in found if x["severity"] == "note"]
        if args.quiet and not (errs or warns):
            continue
        head = f"{path}  —  {len(errs)} error(s), {len(warns)} warning(s), {len(notes)} exemption(s)"
        print(f"\n{head}\n{'-' * len(head)}")
        if not found:
            print("  CONFORMS: reads the kit foundation, no hardcoded brand values.")
        for x in sorted(found, key=lambda d: (d["severity"] != "error", d["severity"] == "note", d["line"])):
            tag = {"error": "ERROR", "warn": "warn ", "note": "exmpt"}[x["severity"]]
            print(f"  [{tag}] {x['rule']} L{x['line']}: {x['message']}")
            if x["fix"]:
                print(f"          -> {x['fix']}")

    print(f"\n{'FAIL' if errors else 'PASS'}: {errors} error(s) across {len(report)} file(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
