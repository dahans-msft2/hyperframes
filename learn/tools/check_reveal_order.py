#!/usr/bin/env python3
"""Enforce semantic reveal ORDER within a composition or scene.

The render postmortem's finding #10: automated checks passed while connectors appeared before
their endpoint nodes and labels appeared before their narration. `lint`/`check` see a structurally
valid, internally consistent timeline; they cannot know a link should not exist before the two
things it links. `check_cue_anchors.py` enforces that cues are word-anchored, but says nothing
about the order of two elements relative to EACH OTHER.

The contract is inline and machine-readable: an element declares what must reveal before it.

  <div id="link-ab" data-reveal-after="#node-a #node-b" ...></div>

This tool then:
  1. Requires every data-reveal-after element to be pinned hidden at t=0 (else it is drawn the
     instant its scene opens, regardless of its tween — the accumulation bug).
  2. Computes each element's earliest reveal position from the timeline and asserts the element
     reveals no earlier than every dependency. A connector before its node fails.

Anchored reveal positions (W.*) are tied to a spoken word by construction and are reported as
verified-by-anchor rather than compared numerically.

  py tools/check_reveal_order.py index.html
  py tools/check_reveal_order.py scenes/03-flow.html
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys

SEL = re.compile(r"""^\s*['"]([#.][A-Za-z0-9_\-]+)['"]""")
CALL = re.compile(r"\b(tl\.\w+|appear|vanish)\s*\(")
VIS_PROPS = ("opacity", "autoAlpha")
EPS = 0.001


def split_args(src: str, open_paren: int) -> list[str]:
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


def first_selector(arg: str) -> str | None:
    m = SEL.match(arg)
    return m.group(1) if m else None


def prop_value(obj: str, prop: str) -> float | None:
    m = re.search(rf"\b{prop}\s*:\s*([\d.]+)", obj)
    return float(m.group(1)) if m else None


def is_hidden(obj: str) -> bool:
    return any(prop_value(obj, p) == 0 for p in VIS_PROPS)


def is_visible(obj: str) -> bool:
    return any((v is not None and v > 0) for v in (prop_value(obj, p) for p in VIS_PROPS))


def parse_position(expr: str) -> tuple[str, float | None]:
    e = expr.strip()
    if re.match(r"^[\d.]+$", e):
        return "numeric", float(e)
    if re.match(r"^W\.\w+", e):
        return "anchored", None
    if re.match(r"^B\.\w+", e):
        return "beat", None
    return "other", None


def css_hidden_ids(html: str) -> set[str]:
    css = "\n".join(re.findall(r"<style[^>]*>(.*?)</style>", html, re.S))
    zero_classes, zero_ids = set(), set()
    for m in re.finditer(r"([^{}]+)\{([^{}]*)\}", css):
        if re.search(r"opacity\s*:\s*0(?:\.0+)?\s*[;}]", m.group(2)):
            zero_classes.update(re.findall(r"\.([A-Za-z0-9_\-]+)", m.group(1)))
            zero_ids.update("#" + i for i in re.findall(r"#([A-Za-z0-9_\-]+)", m.group(1)))
    hidden = set(zero_ids)
    for tag in re.finditer(r"<\w+([^>]*)>", html):
        attrs = tag.group(1)
        idm = re.search(r'\bid\s*=\s*"([^"]+)"', attrs)
        if not idm:
            continue
        eid = "#" + idm.group(1)
        style = re.search(r'\bstyle\s*=\s*"([^"]*)"', attrs)
        if style and re.search(r"opacity\s*:\s*0(?:\.0+)?\s*(;|$)", style.group(1)):
            hidden.add(eid)
        cls = re.search(r'\bclass\s*=\s*"([^"]*)"', attrs)
        if cls and (set(cls.group(1).split()) & zero_classes):
            hidden.add(eid)
    return hidden


def reveal_dependencies(html: str) -> dict[str, list[str]]:
    """id-selector -> list of dependency selectors from data-reveal-after."""
    deps = {}
    for tag in re.finditer(r"<\w+([^>]*)>", html):
        attrs = tag.group(1)
        idm = re.search(r'\bid\s*=\s*"([^"]+)"', attrs)
        ram = re.search(r'\bdata-reveal-after\s*=\s*"([^"]*)"', attrs)
        if idm and ram:
            deps["#" + idm.group(1)] = [d.strip() for d in ram.group(1).split() if d.strip()]
    return deps


def analyze_timeline(html: str):
    """Return (reveal_pos, anchored, pinned0). reveal_pos: sel -> earliest numeric reveal."""
    script = "\n".join(re.findall(r"<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>", html, re.S))
    reveal_pos: dict[str, float] = {}
    anchored: set[str] = set()
    pinned0: set[str] = set()

    # forEach hide-at-0: [ "#a", "#b" ].forEach(s => tl.set(s, { opacity: 0 }, 0))
    for m in re.finditer(r"\[([^\[\]]*?)\]\s*\.?\s*\n?\s*\.forEach\s*\(([^;]*?)\)\s*;", script, re.S):
        body = m.group(2)
        if re.search(r"tl\.set\b", body) and is_hidden(body) and re.search(r",\s*0\s*\)", body):
            pinned0.update(re.findall(r"['\"]([#.][A-Za-z0-9_\-]+)['\"]", m.group(1)))

    for m in CALL.finditer(script):
        fn = m.group(1)
        argv = split_args(script, m.end() - 1)
        if len(argv) < 2:
            continue
        sel = first_selector(argv[0])
        if not sel:
            continue
        pos_kind, pos_val = parse_position(argv[-1])

        revealed = False
        if fn == "tl.set":
            obj = argv[1]
            if is_hidden(obj) and pos_kind == "numeric" and pos_val == 0:
                pinned0.add(sel)
            elif is_visible(obj):
                revealed = True
        elif fn == "tl.fromTo" and len(argv) >= 3:
            if is_hidden(argv[1]):  # arrival: from-state is hidden
                revealed = True
        elif fn == "tl.to":
            if is_visible(argv[1]):
                revealed = True
        elif fn == "appear":
            revealed = True

        if revealed:
            if pos_kind == "numeric" and pos_val is not None:
                reveal_pos[sel] = min(reveal_pos.get(sel, pos_val), pos_val)
            else:
                anchored.add(sel)

    return reveal_pos, anchored, pinned0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("composition", type=pathlib.Path, nargs="?", default=pathlib.Path("index.html"))
    args = ap.parse_args()

    if not args.composition.exists():
        print(f"ERROR: not found: {args.composition}", file=sys.stderr)
        return 2
    html = args.composition.read_text(encoding="utf-8")

    deps = reveal_dependencies(html)
    if not deps:
        print("no data-reveal-after declarations — nothing to enforce (add them to connectors, "
              "milestones, and labels whose order matters)")
        return 0

    reveal_pos, anchored, pinned0 = analyze_timeline(html)
    hidden0 = pinned0 | css_hidden_ids(html)

    problems: list[str] = []
    verified = 0
    for el, dep_list in deps.items():
        if el not in hidden0:
            problems.append(f"{el}: declares data-reveal-after but is NOT pinned hidden at t=0 "
                            f"(drawn the instant the scene opens). Add tl.set(\"{el}\", {{opacity:0}}, 0).")
        el_pos = reveal_pos.get(el)
        for dep in dep_list:
            dep_pos = reveal_pos.get(dep)
            if el in anchored or dep in anchored:
                verified += 1  # tied to a spoken word by construction
                continue
            if el_pos is None or dep_pos is None:
                problems.append(f"{el}: cannot verify order vs {dep} "
                                f"(no numeric reveal found for {'itself' if el_pos is None else dep}).")
                continue
            if el_pos < dep_pos - EPS:
                problems.append(f"{el} reveals at {el_pos} but its dependency {dep} reveals later "
                                f"at {dep_pos} — it appears BEFORE what it depends on.")
            else:
                verified += 1

    if problems:
        print(f"REVEAL-ORDER FAIL ({len(problems)} issue(s), {verified} ok):")
        for p in problems:
            print(f"  - {p}")
        return 1

    print(f"REVEAL-ORDER OK — {len(deps)} declared element(s), {verified} dependency check(s) verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
