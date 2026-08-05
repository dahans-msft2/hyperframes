"""Convert the locally-installed Segoe UI system fonts to WOFF2 for hermetic renders.

Segoe UI is licensed, not redistributable. Each machine generates its own WOFF2 from its own
Windows install; the output is gitignored and never committed. For non-Windows or CI renders
use Selawik (SIL OFL, metric-compatible) instead -- see FRAME.md.
"""

from __future__ import annotations

import argparse
import pathlib
import sys

FACES = {
    "segoeui-regular.woff2": ("segoeui.ttf", "Segoe UI", 400, "normal"),
    "segoeui-italic.woff2": ("segoeuii.ttf", "Segoe UI", 400, "italic"),
    "segoeui-semibold.woff2": ("seguisb.ttf", "Segoe UI Semibold", 600, "normal"),
    "segoeui-bold.woff2": ("segoeuib.ttf", "Segoe UI", 700, "normal"),
}

SYSTEM_FONTS = pathlib.Path(r"C:\Windows\Fonts")


def convert(src: pathlib.Path, dest: pathlib.Path) -> None:
    from fontTools.ttLib import TTFont

    font = TTFont(str(src))
    font.flavor = "woff2"
    font.save(str(dest))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", default=None, help="output folder (default: ../fonts)")
    ap.add_argument("--css", action="store_true", help="also emit fonts.css with @font-face rules")
    args = ap.parse_args()

    out = pathlib.Path(args.out) if args.out else pathlib.Path(__file__).resolve().parent.parent / "fonts"
    out.mkdir(parents=True, exist_ok=True)

    missing: list[str] = []
    rules: list[str] = []

    for name, (ttf, family, weight, style) in FACES.items():
        src = SYSTEM_FONTS / ttf
        if not src.exists():
            missing.append(f"{ttf} ({family} {weight} {style})")
            continue
        dest = out / name
        convert(src, dest)
        print(f"  {name:<26} <- {ttf:<14} {dest.stat().st_size / 1024:7.1f} KB")
        rules.append(
            "@font-face {\n"
            f'  font-family: "{family}";\n'
            f"  font-weight: {weight};\n"
            f"  font-style: {style};\n"
            f'  src: url("fonts/{name}") format("woff2");\n'
            "  font-display: block;\n"
            "}"
        )

    if missing:
        print("\nMISSING system fonts -- renders will substitute silently:", file=sys.stderr)
        for m in missing:
            print(f"  - {m}", file=sys.stderr)
        return 1

    if args.css:
        css = out / "fonts.css"
        css.write_text("\n\n".join(rules) + "\n", encoding="utf-8")
        print(f"\n  wrote {css}")

    print(f"\nOK - {len(FACES)} faces in {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
