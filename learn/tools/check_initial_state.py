#!/usr/bin/env python3
"""Catch the beat-accumulation bug that `hyperframes lint` and `check` cannot see.

THE BUG
-------
Composition children inherit `opacity: 1` from CSS. GSAP `fromTo(..., {
immediateRender: false })` does not apply the from-state until the tween
actually fires. So every element whose first tween starts later than its parent
beat becomes visible the instant that beat fades in - long before its own cue.

Beats then accumulate, a "subtractive recap" never subtracts, and BOTH `lint`
and `check` report clean while it is broken. It shipped twice before anyone
noticed, and only ever got caught by eyeballing snapshot contact sheets.

THE RULE
--------
Any element that first animates at t > 0 must have its state pinned at t = 0 -
either `tl.set(sel, { opacity: 0 }, 0)` or a CSS/inline `opacity: 0`. State must
be a pure function of timeline time.

Exit code 1 if any element is unpinned.
"""
import argparse
import pathlib
import re
import sys

SEL = r"""['"]([#.][A-Za-z0-9_\-]+)['"]"""
# A from-state of zero on any of these means the element ARRIVES later. Anything
# arriving must be pinned, or it is fully drawn from the moment its beat opens.
ZERO_PROPS = ("opacity", "scaleX", "scaleY", "scale")


def _has_zero_prop(obj):
    return any(re.search(rf"\b{p}\s*:\s*0(?:\.0+)?\s*[,}}]", obj) for p in ZERO_PROPS)


def zero_opacity_selectors(css):
    """Class names AND ids whose rule sets opacity:0 (e.g. .beat, #chrome)."""
    classes, ids = set(), set()
    for m in re.finditer(r"([^{}]+)\{([^{}]*)\}", css):
        selector, body = m.group(1), m.group(2)
        if re.search(r"opacity\s*:\s*0(?:\.0+)?\s*[;}]", body):
            classes.update(re.findall(r"\.([A-Za-z0-9_\-]+)", selector))
            ids.update("#" + i for i in re.findall(r"#([A-Za-z0-9_\-]+)", selector))
    return classes, ids


def elements_with_css_zero(html, zero_classes):
    """ids of elements hidden at t=0 by inline style or a zero-opacity class."""
    hidden = set()
    for tag in re.finditer(r"<(\w+)([^>]*)>", html):
        attrs = tag.group(2)
        idm = re.search(r'\bid\s*=\s*"([^"]+)"', attrs)
        if not idm:
            continue
        eid = "#" + idm.group(1)
        style = re.search(r'\bstyle\s*=\s*"([^"]*)"', attrs)
        if style and re.search(r"opacity\s*:\s*0(?:\.0+)?\s*(;|$)", style.group(1)):
            hidden.add(eid)
            continue
        cls = re.search(r'\bclass\s*=\s*"([^"]*)"', attrs)
        if cls and (set(cls.group(1).split()) & zero_classes):
            hidden.add(eid)
    return hidden


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("composition", type=pathlib.Path, nargs="?",
                    default=pathlib.Path("index.html"))
    args = ap.parse_args()

    html = args.composition.read_text(encoding="utf-8")
    css = "\n".join(re.findall(r"<style[^>]*>(.*?)</style>", html, re.S))
    script = "\n".join(re.findall(r"<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>", html, re.S))

    zero_classes, zero_ids = zero_opacity_selectors(css)
    css_hidden = elements_with_css_zero(html, zero_classes) | zero_ids

    pinned, arrivals = set(), {}

    # forEach over an array literal: [ "#a", "#b" ].forEach(s => tl.set(s, {...}, 0))
    for m in re.finditer(r"\[([^\[\]]*?)\]\s*\.?\s*\n?\s*\.forEach\s*\(([^;]*?)\)\s*;", script, re.S):
        sels = re.findall(SEL, m.group(1))
        body = m.group(2)
        if re.search(r"tl\.set\s*\(\s*\w+\s*,\s*\{[^}]*\}\s*,\s*0\s*\)", body):
            pinned.update(sels)
        elif re.search(r"tl\.(fromTo|to)\b", body) and _has_zero_prop(body):
            for s in sels:
                arrivals.setdefault(s, "forEach")

    # direct calls: tl.fromTo / tl.to / tl.set / appear / vanish
    for m in re.finditer(r"\b(tl\.fromTo|tl\.to|tl\.set|appear|vanish)\s*\(\s*" + SEL + r"(.*?)\)\s*;",
                         script, re.S):
        fn, sel, rest = m.group(1), m.group(2), m.group(3)
        tail = rest.rstrip()
        time_lit = re.search(r",\s*([\d.]+)\s*$", tail)
        at_zero = bool(time_lit and float(time_lit.group(1)) == 0)

        if fn == "tl.set":
            if at_zero:
                pinned.add(sel)
            continue
        if at_zero:
            continue
        # vanish / fade-out are EXITS - they need no pin, they only remove things.
        if fn == "vanish":
            continue
        if fn == "appear":
            arrivals.setdefault(sel, fn)
            continue
        # tl.fromTo: an arrival only if the FROM object starts from zero.
        if fn == "tl.fromTo":
            from_obj = re.search(r"\{(.*?)\}", tail, re.S)
            if from_obj and _has_zero_prop(from_obj.group(1)):
                arrivals.setdefault(sel, fn)
            continue
        # tl.to raising opacity toward 1 is also an arrival.
        if fn == "tl.to" and re.search(r"\bopacity\s*:\s*(?!0[,}\s])[\d.]+", tail):
            arrivals.setdefault(sel, fn)

    risky = sorted(s for s in arrivals
                   if s not in pinned and s not in css_hidden)

    print(f"arriving selectors : {len(arrivals)}   (entrances only; exits need no pin)")
    print(f"pinned at t=0      : {len(pinned)}")
    print(f"hidden by CSS      : {len(css_hidden)}")

    if risky:
        print(f"\nUNPINNED - fully drawn from the moment their beat opens ({len(risky)}):")
        for s in risky:
            print(f"  {s:<22} arrives via {arrivals[s]}")
        print("\nFix: tl.set(sel, { opacity: 0 }, 0) for each, or inline opacity:0.")
        return 1

    print("\nPASS - every arriving element is pinned at t=0")
    return 0


if __name__ == "__main__":
    sys.exit(main())
