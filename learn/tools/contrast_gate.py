"""WCAG 2.1 contrast gate for brand token pairs.

Runs at design time on the palette itself, before any layout is authored, because
bright accents on a light ground is where contrast quietly fails.

A ground may be a solid hex OR a path to an image (grounds are photographic in the
Learn ILT system). An image ground is judged on its WORST pixel, not its average --
averaging is exactly the approximation that let a 1.67:1 region pass as "4.41 on bg".
The report also breaks each image ground into a 3x3 zone map so a layout can be told
where text is safe rather than only whether it is safe somewhere.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# WCAG 2.1 thresholds.
NORMAL_AA = 4.5
LARGE_AA = 3.0
NORMAL_AAA = 7.0

# Pixels sampled across an image ground's long edge. 240 keeps a full palette run
# under a second while still catching the tight colour cores that fail.
SAMPLE_W = 240


def _srgb_to_linear(c: float) -> float:
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _rgb_luminance(rgb: tuple[float, float, float]) -> float:
    r, g, b = (c / 255 for c in rgb[:3])
    return (0.2126 * _srgb_to_linear(r) + 0.7152 * _srgb_to_linear(g)
            + 0.0722 * _srgb_to_linear(b))


def _hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    h = hex_color.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def luminance(hex_color: str) -> float:
    return _rgb_luminance(_hex_to_rgb(hex_color))


def _ratio_lum(a: float, b: float) -> float:
    hi, lo = max(a, b), min(a, b)
    return (hi + 0.05) / (lo + 0.05)


def ratio(fg: str, bg: str) -> float:
    return _ratio_lum(luminance(fg), luminance(bg))


def is_image_ground(value: str) -> bool:
    return value.lower().endswith((".png", ".jpg", ".jpeg", ".webp"))


def load_ground_pixels(path: Path) -> tuple[list[tuple[int, int, int]], int, int]:
    """Downsample an image ground to a sampling grid of RGB tuples."""
    try:
        from PIL import Image
    except ImportError:
        raise SystemExit("image grounds need Pillow: py -m pip install pillow")
    im = Image.open(path).convert("RGB")
    h = max(1, round(SAMPLE_W * im.height / im.width))
    im = im.resize((SAMPLE_W, h), Image.Resampling.LANCZOS)
    return list(im.getdata()), SAMPLE_W, h


def image_ratios(fg_hex: str, px: list[tuple[int, int, int]]) -> tuple[float, float]:
    """Worst and best contrast of one foreground across every sampled pixel."""
    fl = luminance(fg_hex)
    rs = [_ratio_lum(fl, _rgb_luminance(p)) for p in px]
    return min(rs), max(rs)


def zone_map(fg_hex: str, px: list[tuple[int, int, int]], w: int, h: int) -> list[list[float]]:
    """Worst contrast per cell of a 3x3 grid -- the 'where is text safe' answer."""
    fl = luminance(fg_hex)
    out = []
    for gy in range(3):
        row = []
        for gx in range(3):
            x0, x1 = gx * w // 3, (gx + 1) * w // 3
            y0, y1 = gy * h // 3, (gy + 1) * h // 3
            cell = [px[y * w + x] for y in range(y0, y1) for x in range(x0, x1)]
            row.append(round(min(_ratio_lum(fl, _rgb_luminance(p)) for p in cell), 2))
        out.append(row)
    return out


def verdict(r: float) -> str:
    if r >= NORMAL_AAA:
        return "AAA"
    if r >= NORMAL_AA:
        return "AA"
    if r >= LARGE_AA:
        return "AA-large"
    return "FAIL"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("palette", type=Path, help="JSON: {grounds:{}, inks:{}, accents:{}}")
    ap.add_argument("--min", type=float, default=LARGE_AA,
                    help="fail the run if any pair falls below this (default 3.0)")
    ap.add_argument("--zones", action="store_true",
                    help="print the 3x3 safe-zone map for each image ground")
    args = ap.parse_args()

    p = json.loads(args.palette.read_text(encoding="utf-8"))
    grounds = p["grounds"]
    foregrounds = {**p.get("inks", {}), **p.get("accents", {})}
    # Which foregrounds are actually meant to carry text on which ground. Without this
    # the gate flags every nonsensical pairing (white ink on white paper) and its exit
    # code stops meaning anything.
    text_on = p.get("text_on")

    worst = 99.0
    print(f"{'foreground':<22}{'ground':<20}{'ratio':>7}  verdict")
    print("-" * 64)
    rows = []
    for gname, gval in grounds.items():
        img = None
        if is_image_ground(gval):
            gpath = (args.palette.parent / gval).resolve()
            if not gpath.exists():
                print(f"GATE FAIL: ground '{gname}' -> missing image {gpath}")
                return 1
            img = load_ground_pixels(gpath)

        for fname, fval in foregrounds.items():
            if img is not None:
                px, w, h = img
                r, best = image_ratios(fval, px)
                v = verdict(r)
                row = {"fg": fname, "fg_hex": fval, "bg": gname, "bg_src": gval,
                       "ratio": round(r, 2), "ratio_best": round(best, 2),
                       "measured": "worst pixel", "verdict": v}
                if args.zones:
                    row["zones"] = zone_map(fval, px, w, h)
                detail = f" (best {best:.2f})"
            else:
                # A token against its own colour is not a real pairing.
                if fval.upper() == gval.upper():
                    continue
                r = ratio(fval, gval)
                v = verdict(r)
                row = {"fg": fname, "fg_hex": fval, "bg": gname, "bg_hex": gval,
                       "ratio": round(r, 2), "measured": "solid", "verdict": v}
                detail = ""

            rows.append(row)
            row["text_pairing"] = text_on is None or fname in text_on.get(gname, [])
            if row["text_pairing"]:
                flag = "  <-- TEXT PAIRING" if v in ("FAIL", "AA-large") else "  (text)"
            else:
                flag = ""
            print(f"{fname:<22}{gname:<20}{r:>7.2f}  {v}{detail}{flag}")
            if row["text_pairing"]:
                worst = min(worst, r)

        if args.zones and img is not None:
            px, w, h = img
            ink = foregrounds.get("text") or next(iter(foregrounds.values()))
            print(f"    safe-zone map for ink on {gname} (worst ratio per third):")
            for zrow in zone_map(ink, px, w, h):
                print("      " + "  ".join(f"{z:6.2f}" for z in zrow))
        print()

    out = args.palette.with_name(args.palette.stem + "-contrast.json")
    out.write_text(json.dumps(rows, indent=2), encoding="utf-8")
    print(f"wrote {out}")

    judged = [r for r in rows if r.get("text_pairing")]
    failures = [r for r in judged if r["ratio"] < args.min]
    if failures:
        print(f"\nGATE FAIL: {len(failures)} declared text pairing(s) below {args.min}")
        for f in failures:
            print(f"  {f['fg']} on {f['bg']} = {f['ratio']}")
        return 1
    scope = f"{len(judged)} declared text pairing(s)" if text_on else "all pairs"
    print(f"\nGATE PASS: {scope} >= {args.min} (worst {worst:.2f})")
    if text_on:
        decorative = len(rows) - len(judged)
        print(f"  {decorative} non-text pairing(s) reported but not gated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
