#!/usr/bin/env python3
"""Fail a composition whose cue timings are hand-estimated instead of word-anchored.

`word_anchors.py` makes anchoring POSSIBLE. This makes it ENFORCED - because the
builder agent already carried the rule "anchor to real word times, never
estimates" in prose, and a build still shipped with most of its timings as
estimates. A rule with no gate is a suggestion.

It classifies the POSITION ARGUMENT of every timeline call, not text patterns in
the file. That distinction matters: an earlier cut of this tool matched
`B.bN + x` expressions, and therefore scored a composition built entirely from
raw numeric literals as 100% anchored - a false pass of exactly the kind of bug
it exists to catch.

  W.gateApproval    anchored to a spoken word                     GOOD
  B.b6              a beat start, itself derived from transcript  GOOD
  B.b7 - 0.55       seam mechanics, relative to a boundary        allowed under --max-offset
  B.b6 + 7.4        a content cue guessed from assumed w/s        DEFECT
  63.31             a raw literal - anchored to nothing at all    DEFECT

Opt out of one line with a trailing comment:  // anchor-exempt: <reason>
"""
import argparse
import pathlib
import re
import sys

HELPERS = ("appear", "vanish")                                     # time is argument 2
TIMELINE = ("tl.fromTo", "tl.to", "tl.set", "tl.add", "tl.call")   # time is the last argument
CALL = re.compile(r"\b(tl\.\w+|appear|vanish)\s*\(")


def split_args(src, open_paren):
    """Return the top-level argument strings of a call whose '(' is at open_paren."""
    depth, args, cur, i = 0, [], "", open_paren
    while i < len(src):
        c = src[i]
        if c in "([{":
            depth += 1
            if depth == 1:
                i += 1
                continue
        elif c in ")]}":
            depth -= 1
            if depth == 0:
                args.append(cur.strip())
                return args
        if depth == 1 and c == ",":
            args.append(cur.strip())
            cur = ""
        else:
            cur += c
        i += 1
    return args


def classify(expr, max_offset):
    e = expr.strip()
    if re.match(r"^W\.\w+\s*$", e):
        return "anchored"
    if re.match(r"^B\.\w+\s*$", e):
        return "beat"
    m = re.match(r"^B\.\w+\s*([+\-])\s*([\d.]+)\s*$", e)
    if m:
        return "seam" if float(m.group(2)) <= max_offset else "guess"
    if re.match(r"^[\d.]+$", e):
        return "literal-zero" if float(e) == 0 else "literal"
    return "other"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("composition", type=pathlib.Path, nargs="?",
                    default=pathlib.Path("index.html"))
    ap.add_argument("--max-offset", type=float, default=1.0,
                    help="largest offset from a beat boundary still counted as seam mechanics")
    args = ap.parse_args()

    html = args.composition.read_text(encoding="utf-8")
    script = "\n".join(re.findall(r"<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>", html, re.S))
    if not script.strip():
        print("no inline timeline script found", file=sys.stderr)
        return 1

    lines = script.splitlines()
    counts = {k: 0 for k in ("anchored", "beat", "seam", "guess",
                             "literal", "literal-zero", "other")}
    offenders, exempt = [], 0

    for m in CALL.finditer(script):
        fn = m.group(1)
        argv = split_args(script, m.end() - 1)
        if len(argv) < 2:
            continue
        if fn in HELPERS:
            expr = argv[1]
        elif fn in TIMELINE:
            expr = argv[-1]
        else:
            continue

        kind = classify(expr, args.max_offset)
        line_no = script.count("\n", 0, m.start()) + 1
        src_line = lines[line_no - 1].strip() if line_no <= len(lines) else ""

        if kind in ("guess", "literal") and "anchor-exempt" in src_line:
            exempt += 1
            continue
        counts[kind] += 1
        if kind in ("guess", "literal"):
            offenders.append((line_no, kind, expr, src_line[:80]))

    good = counts["anchored"] + counts["beat"] + counts["seam"] + counts["literal-zero"]
    bad = counts["guess"] + counts["literal"]
    total = good + bad
    pct = good / total * 100 if total else 0.0

    print(f"word-anchored   W.*             {counts['anchored']}")
    print(f"beat starts     B.*             {counts['beat']}")
    print(f"seam mechanics  <={args.max_offset}s         {counts['seam']}")
    print(f"t=0 pins                        {counts['literal-zero']}")
    print(f"exempted                        {exempt}")
    print(f"guessed offsets B.* >{args.max_offset}s      {counts['guess']}")
    print(f"raw numeric literals            {counts['literal']}")
    print(f"\n{total} timeline positions | anchored coverage {pct:.0f}%")

    if not total:
        print("\nno timeline positions found - is this a composition?", file=sys.stderr)
        return 1

    if offenders:
        print(f"\n{len(offenders)} unanchored cue(s). Each is a guess against an assumed")
        print("words-per-second, and drifts when the voice runs faster or slower:\n")
        for line_no, kind, expr, src in offenders[:40]:
            tag = "literal" if kind == "literal" else "offset "
            print(f"  line {line_no:>4}  [{tag}] {expr:<14} {src}")
        if len(offenders) > 40:
            print(f"  ... and {len(offenders) - 40} more")
        print("\nFix: add each cue to anchors.json, regenerate with tools/word_anchors.py,")
        print("     and reference W.<name>.")
        return 1

    print("\nPASS - every cue position is anchored")
    return 0


if __name__ == "__main__":
    sys.exit(main())
