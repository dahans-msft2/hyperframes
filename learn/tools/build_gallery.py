#!/usr/bin/env python3
"""Generate a static gallery of published Learn videos from GitHub Releases.

Each release is one delivered video (MP4 + captions + thumbnail + narration.wav master). This bakes
a self-contained `learn/gallery/index.html` — a thumbnail grid, each card linking to the video and
its source folder on `main`. No runtime API calls; regenerate whenever a release is published.

    py tools/build_gallery.py                         # -> learn/gallery/index.html
    py tools/build_gallery.py --repo owner/repo -o <path>

Structured to grow: the page has titled sections (Published today) and per-card slots so the
audition and review artifacts can be surfaced here later (see the SECTIONS note below).
"""
from __future__ import annotations

import argparse
import html
import json
import re
import subprocess
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
LEARN = TOOLS.parent
DEFAULT_REPO = "dahans-msft2/hyperframes"


def gh_json(args: list[str]) -> object:
    r = subprocess.run(["gh"] + args, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"gh {' '.join(args)} failed: {(r.stderr or r.stdout).strip()}", file=sys.stderr)
        raise SystemExit(1)
    return json.loads(r.stdout or "[]")


def asset(assets: list[dict], *, suffix: str) -> "dict | None":
    for a in assets:
        if a.get("name", "").lower().endswith(suffix):
            return a
    return None


def duration_from_body(body: str) -> "str | None":
    m = re.search(r"\((\d+)s\)", body or "")
    if not m:
        return None
    s = int(m.group(1))
    return f"{s // 60}:{s % 60:02d}" if s >= 60 else f"{s}s"


def card(rel: dict, repo: str) -> str:
    title = html.escape(rel.get("name") or rel.get("tag_name") or "Untitled")
    tag = rel.get("tag_name", "")
    assets = rel.get("assets", [])
    mp4 = asset(assets, suffix=".mp4")
    thumb = asset(assets, suffix="_thumbnail.png") or asset(assets, suffix=".png")
    mp4_url = mp4["browser_download_url"] if mp4 else f"https://github.com/{repo}/releases/tag/{tag}"
    poster = thumb["browser_download_url"] if thumb else ""
    src_url = f"https://github.com/{repo}/tree/main/learn/output/{html.escape(tag)}"
    dur = duration_from_body(rel.get("body", ""))
    published = (rel.get("published_at") or "")[:10]
    meta = "  ·  ".join(x for x in [published, dur] if x)

    media = (
        f'<video class="thumb" controls preload="none" poster="{poster}">'
        f'<source src="{mp4_url}" type="video/mp4"></video>'
        if mp4 else
        f'<a class="thumb ph" href="{mp4_url}" target="_blank" rel="noopener">'
        f'<img src="{poster}" alt="{title}"></a>'
    )
    return f"""      <article class="card">
        {media}
        <div class="body">
          <h3>{title}</h3>
          <p class="meta">{html.escape(meta)}</p>
          <div class="actions">
            <a href="{mp4_url}" target="_blank" rel="noopener">Watch ▸</a>
            <a href="{src_url}" target="_blank" rel="noopener" class="ghost">Source</a>
          </div>
        </div>
      </article>"""


def render_html(releases: list[dict], repo: str) -> str:
    cards = "\n".join(card(r, repo) for r in releases) or (
        '      <p class="empty">No videos published yet. Run <code>publish_video.py</code> to add one.</p>'
    )
    count = len(releases)
    # SECTIONS: today this is one grid of published videos. To grow (audition / review), add sibling
    # <section> blocks fed from their own data (e.g. review_index.py) — the card CSS is reusable.
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Microsoft Learn — Companion Video Gallery</title>
  <style>
    :root {{ --ink:#1b1a19; --muted:#605e5c; --accent:#0f6cbd; --line:#e1dfdd; --bg:#faf9f8; --card:#fff; }}
    * {{ box-sizing:border-box; }}
    body {{ margin:0; font:16px/1.5 "Segoe UI",system-ui,sans-serif; color:var(--ink); background:var(--bg); }}
    header {{ padding:40px 24px 20px; max-width:1200px; margin:0 auto; }}
    header h1 {{ margin:0 0 6px; font-size:28px; letter-spacing:-.01em; }}
    header p {{ margin:0; color:var(--muted); }}
    .grid {{ max-width:1200px; margin:0 auto; padding:16px 24px 64px;
             display:grid; grid-template-columns:repeat(auto-fill,minmax(320px,1fr)); gap:22px; }}
    .card {{ background:var(--card); border:1px solid var(--line); border-radius:12px; overflow:hidden;
             display:flex; flex-direction:column; box-shadow:0 1px 2px rgba(0,0,0,.04); }}
    .thumb {{ width:100%; aspect-ratio:16/9; background:#000; display:block; object-fit:cover; border:0; }}
    .thumb.ph img {{ width:100%; height:100%; object-fit:cover; }}
    .body {{ padding:14px 16px 16px; display:flex; flex-direction:column; gap:8px; flex:1; }}
    .body h3 {{ margin:0; font-size:16px; line-height:1.3; }}
    .meta {{ margin:0; color:var(--muted); font-size:13px; }}
    .actions {{ margin-top:auto; display:flex; gap:10px; padding-top:6px; }}
    .actions a {{ text-decoration:none; font-size:14px; font-weight:600; color:#fff; background:var(--accent);
                  padding:7px 14px; border-radius:6px; }}
    .actions a.ghost {{ color:var(--accent); background:transparent; border:1px solid var(--line); font-weight:500; }}
    .empty {{ color:var(--muted); }}
    footer {{ max-width:1200px; margin:0 auto; padding:0 24px 48px; color:var(--muted); font-size:13px; }}
  </style>
</head>
<body>
  <header>
    <h1>Microsoft Learn — Companion Videos</h1>
    <p>{count} published · AI-produced with the required disclosure end card · sourced from
       <a href="https://github.com/{repo}/tree/main/learn/output">learn/output</a></p>
  </header>
  <main>
    <section class="grid">
{cards}
    </section>
  </main>
  <footer>Generated from GitHub Releases. Each card streams the MP4 and links to its source on main.</footer>
</body>
</html>
"""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo", default=DEFAULT_REPO)
    ap.add_argument("-o", "--out", type=Path, default=LEARN / "gallery" / "index.html")
    args = ap.parse_args()

    releases = gh_json(["api", f"repos/{args.repo}/releases", "--paginate"])
    # newest first, skip drafts/prereleases
    releases = [r for r in releases if not r.get("draft") and not r.get("prerelease")]
    releases.sort(key=lambda r: r.get("published_at") or "", reverse=True)

    out = args.out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render_html(releases, args.repo), encoding="utf-8")
    print(f"gallery: {len(releases)} video(s) -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
