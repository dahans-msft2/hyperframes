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

# Lightbox player. Any element carrying data-mp4 opens the modal and plays that URL; data-close closes
# it. Kept as a plain constant (normal braces) so it interpolates verbatim into the page f-string.
PLAYER_JS = """
(function () {
  const modal = document.getElementById('player');
  const v = document.getElementById('player-v');
  const cap = document.getElementById('player-t');
  function open(src, title) { v.src = src; cap.textContent = title || ''; modal.hidden = false; v.play().catch(function () {}); }
  function close() { modal.hidden = true; v.pause(); v.removeAttribute('src'); v.load(); }
  document.addEventListener('click', function (e) {
    const trig = e.target.closest('[data-mp4]');
    if (trig) { e.preventDefault(); open(trig.getAttribute('data-mp4'), trig.getAttribute('data-title')); return; }
    if (e.target.closest('[data-close]')) close();
  });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !modal.hidden) close(); });
})();
"""


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
    dur = duration_from_body(rel.get("body", "")) or "\u2014"
    published = (rel.get("published_at") or "")[:10] or "\u2014"

    media = (
        f'<button class="thumb play" style="background-image:url(\'{poster}\')"'
        f' data-mp4="{mp4_url}" data-title="{title}" aria-label="Play {title}"></button>'
        if mp4 else
        f'<a class="thumb ph" href="{mp4_url}" target="_blank" rel="noopener">'
        f'<img src="{poster}" alt="{title}"></a>'
    )
    watch = f' data-mp4="{mp4_url}" data-title="{title}"' if mp4 else ""
    return f"""        <tr>
          <td class="c-thumb">{media}</td>
          <td class="c-title">
            <span class="title">{title}</span>
            <span class="sub">{html.escape(published)} \u00b7 {html.escape(dur)}</span>
          </td>
          <td class="c-act">
            <a href="{mp4_url}" target="_blank" rel="noopener"{watch}>Watch \u25b8</a>
            <a href="{src_url}" target="_blank" rel="noopener" class="ghost">Source</a>
          </td>
        </tr>"""


def render_html(releases: list[dict], repo: str) -> str:
    rows = "\n".join(card(r, repo) for r in releases)
    body = (
        f"""    <table class="tbl">
      <colgroup>
        <col class="col-thumb" /><col /><col class="col-act" />
      </colgroup>
      <tbody>
{rows}
      </tbody>
    </table>"""
        if releases else
        '    <p class="empty">No videos published yet. Run <code>publish_video.py</code> to add one.</p>'
    )
    count = len(releases)
    # SECTIONS: today this is one table of published videos. To grow (audition / review), add sibling
    # <section> blocks fed from their own data (e.g. review_index.py) — the table CSS is reusable.
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Microsoft Learn — Companion Video Gallery</title>
  <style>
    :root {{ --ink:#1b1a19; --muted:#605e5c; --accent:#0f6cbd; --line:#e1dfdd; --bg:#faf9f8; --card:#fff; }}
    * {{ box-sizing:border-box; }}
    body {{ margin:0; font:15px/1.5 "Segoe UI",system-ui,sans-serif; color:var(--ink); background:var(--bg); }}
    header {{ padding:36px 24px 12px; max-width:1100px; margin:0 auto; }}
    header h1 {{ margin:0 0 6px; font-size:26px; letter-spacing:-.01em; }}
    header p {{ margin:0; color:var(--muted); font-size:14px; }}
    main {{ max-width:1100px; margin:0 auto; padding:12px 24px 64px; }}
    .tbl {{ width:100%; table-layout:fixed; border-collapse:separate; border-spacing:0; background:var(--card);
            border:1px solid var(--line); border-radius:12px; overflow:hidden;
            box-shadow:0 1px 2px rgba(0,0,0,.04); }}
    .col-thumb {{ width:132px; }} .col-act {{ width:112px; }}
    .tbl tbody td {{ padding:9px 14px; border-bottom:1px solid var(--line); vertical-align:middle; }}
    .tbl tbody tr:last-child td {{ border-bottom:0; }}
    .tbl tbody tr:hover td {{ background:#f8f7f6; }}
    .c-thumb {{ width:132px; }}
    .thumb {{ width:120px; aspect-ratio:16/9; background:#000; display:block; object-fit:cover;
              border:0; border-radius:6px; }}
    .thumb.ph img {{ width:100%; height:100%; object-fit:cover; border-radius:6px; }}
    .thumb.play {{ position:relative; padding:0; cursor:pointer; background-size:cover;
                   background-position:center; background-color:#000; }}
    .thumb.play::after {{ content:""; position:absolute; inset:0; margin:auto; width:34px; height:34px;
                         border-radius:50%; background:rgba(0,0,0,.55); z-index:1; transition:background .15s; }}
    .thumb.play::before {{ content:""; position:absolute; inset:0; margin:auto; z-index:2;
                          border-style:solid; border-width:6px 0 6px 11px;
                          border-color:transparent transparent transparent #fff; transform:translateX(2px); }}
    .thumb.play:hover::after {{ background:var(--accent); }}
    .modal[hidden] {{ display:none; }}
    .modal {{ position:fixed; inset:0; z-index:50; display:flex; align-items:center; justify-content:center; padding:24px; }}
    .modal-bg {{ position:absolute; inset:0; background:rgba(0,0,0,.72); cursor:zoom-out; }}
    .modal-box {{ position:relative; margin:0; width:min(960px,100%); }}
    .modal-box video {{ width:100%; border-radius:10px; background:#000; display:block;
                       box-shadow:0 12px 40px rgba(0,0,0,.5); }}
    .modal-x {{ position:absolute; top:-40px; right:0; background:transparent; border:0; color:#fff;
               font-size:30px; line-height:1; cursor:pointer; }}
    .modal-box figcaption {{ color:#fff; font-size:14px; margin-top:10px; text-align:center; }}
    .c-title {{ overflow:hidden; }}
    .c-title .title {{ display:block; font-size:15px; font-weight:600; line-height:1.3;
                       overflow:hidden; text-overflow:ellipsis; }}
    .c-title .sub {{ display:block; color:var(--muted); font-size:12px; margin-top:3px; }}
    .c-act {{ white-space:nowrap; text-align:right; }}
    .c-act a {{ text-decoration:none; font-size:13px; font-weight:600; color:#fff; background:var(--accent);
                padding:6px 12px; border-radius:6px; display:block; text-align:center; }}
    .c-act a.ghost {{ color:var(--accent); background:transparent; border:1px solid var(--line);
                      font-weight:500; margin-top:6px; }}
    .empty {{ color:var(--muted); }}
    footer {{ max-width:1100px; margin:0 auto; padding:0 24px 48px; color:var(--muted); font-size:13px; }}
    @media (max-width:520px) {{
      .col-thumb {{ width:96px; }} .c-thumb {{ width:96px; }} .thumb {{ width:84px; }}
      .col-act {{ width:96px; }}
    }}
  </style>
</head>
<body>
  <header>
    <h1>Microsoft Learn — Companion Videos</h1>
    <p>{count} published · AI-produced with the required disclosure end card · sourced from
       <a href="https://github.com/{repo}/tree/main/learn/output">learn/output</a></p>
  </header>
  <main>
{body}
  </main>
  <div id="player" class="modal" hidden>
    <div class="modal-bg" data-close></div>
    <figure class="modal-box">
      <button class="modal-x" data-close aria-label="Close">\u00d7</button>
      <video id="player-v" controls playsinline preload="auto"></video>
      <figcaption id="player-t"></figcaption>
    </figure>
  </div>
  <footer>Generated from GitHub Releases. Click a thumbnail or Watch to play; Source links to main.</footer>
  <script>{PLAYER_JS}</script>
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
