"""Audition candidate Azure TTS voices on a short passage before committing to a full render.

Renders the SAME passage across several voices and writes an A/B player page. Auditioning the
whole script is wasteful and, worse, misleading -- synthetic voices fail on hard material, not
easy material. By default this picks the single hardest sentence in the script (digits,
acronyms, product names, length) rather than the opening line.

    py tools/audition_voices.py --from-script script.md
    py tools/audition_voices.py --text "Configure Microsoft Entra ID in 3 to 5 minutes."
    py tools/audition_voices.py --from-script script.md --rate "-5%"
"""

from __future__ import annotations

import argparse
import html
import json
import pathlib
import random
import re
import subprocess
import sys
import time

# Proven picks, used as ANCHORS in a selection and as an offline fallback -- never as the
# whole list. The live catalog is the source of truth so new voices appear automatically.
ANCHORS = {
    "en-US-Ava:DragonHDLatestNeural": "polished conversational - default",
    "en-US-Andrew:DragonHDLatestNeural": "warm, coaching",
    "en-US-Emma:DragonHDLatestNeural": "friendly explainer",
    "en-US-Phoebe:DragonHDOmniLatestNeural": "most natural, informal",
    "en-US-Andrew:DragonHDOmniLatestNeural": "thinking out loud",
}

CACHE = pathlib.Path(__file__).resolve().parent.parent / ".voice-catalog.json"
CACHE_TTL = 7 * 24 * 3600


def fetch_catalog(tts, refresh=False):
    """Live en-US voice catalog, cached. Returns [] if the service can't be reached."""
    if not refresh and CACHE.exists() and (time.time() - CACHE.stat().st_mtime) < CACHE_TTL:
        try:
            return json.loads(CACHE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass
    r = subprocess.run([*tts, "--list-voices", "--json"], capture_output=True, text=True)
    if r.returncode != 0:
        return []
    try:
        voices = json.loads(r.stdout)
    except json.JSONDecodeError:
        return []
    CACHE.write_text(json.dumps(voices, indent=2), encoding="utf-8")
    return voices


def select(catalog, pool, gender, count, seed, include):
    """Spread the shortlist across gender and tier rather than returning a fixed five."""
    pool_of = {"hd": {"hd"}, "neural": {"neural"}, "multilingual": {"multilingual"},
               "all": {"hd", "neural", "multilingual"}}[pool]
    cands = [v for v in catalog if v["tier"] in pool_of]
    # The en-US query leaks fr-/zh-Multitalker entries; drop anything not actually English.
    cands = [v for v in cands if v["short_name"].lower().startswith("en-")]
    # Preview and numbered clones are near-duplicates of a shipping voice -- skip by default.
    cands = [v for v in cands if not re.search(r"(-preview|\d+):", v["short_name"], re.I)]
    # Multitalker is a multi-speaker voice, not a narrator.
    cands = [v for v in cands if "multitalker" not in v["short_name"].lower()]
    if gender != "any":
        cands = [v for v in cands if v["gender"].lower() == gender]
    if include:
        rx = re.compile(include, re.I)
        cands = [v for v in cands if rx.search(v["short_name"])]
    if not cands:
        return []

    rng = random.Random(seed)
    by_name = {v["short_name"]: v for v in cands}
    picked = [n for n in ANCHORS if n in by_name][: max(1, count // 2)]

    rest = [v for v in cands if v["short_name"] not in picked]
    rng.shuffle(rest)
    # Alternate genders so an audition never lands on five of the same voice type.
    buckets: dict[str, list[str]] = {}
    for v in rest:
        buckets.setdefault(v["gender"], []).append(v["short_name"])
    order = sorted(buckets, key=lambda g: -len(buckets[g]))
    while len(picked) < count and any(buckets.values()):
        for g in order:
            if buckets[g] and len(picked) < count:
                picked.append(buckets[g].pop())
    return [(n, by_name[n]["gender"].lower(), ANCHORS.get(n, by_name[n]["tier"])) for n in picked]

# Narration lives in ```narration fenced blocks or plain prose; strip markdown furniture.
_FENCE = re.compile(r"```(?:narration|vo)\n(.*?)```", re.S)
_STRIP = re.compile(r"^\s*(#|\||>|-\s|\*\s|\[)")


def narration_from(path: pathlib.Path) -> str:
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)  # drop metadata comment headers (URLs skew difficulty)
    section = re.search(r"^#+\s*Narration\s*$(.*?)(?=^#+\s|\Z)", text, flags=re.S | re.M | re.I)
    if section:
        text = section.group(1)  # scope to the spoken narration, not the beat plan / ledger tables
    blocks = _FENCE.findall(text)
    if blocks:
        return "\n".join(blocks)
    return "\n".join(ln for ln in text.splitlines() if ln.strip() and not _STRIP.match(ln))


def difficulty(sentence: str) -> int:
    """Rank how likely a sentence is to expose TTS failure."""
    score = 0
    score += 12 * len(re.findall(r"\d", sentence))                     # numbers, versions, times
    score += 10 * len(re.findall(r"\b[A-Z]{2,}\b", sentence))          # acronyms
    score += 6 * len(re.findall(r"\b(?:Microsoft|Azure|Entra|Intune|Windows|Defender|Purview)\b", sentence))
    score += 8 * len(re.findall(r"[/:%$@#()]", sentence))              # symbols read aloud badly
    score += len(sentence) // 12                                       # breath / pacing pressure
    return score


def hardest(text: str) -> str:
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if len(s.strip()) > 25]
    if not sentences:
        return text.strip()[:240]
    return max(sentences, key=difficulty)


def slug(voice: str) -> str:
    return voice.split(":")[0].replace("en-US-", "").lower() + ("-omni" if "Omni" in voice else "-hd")


def duration(path):
    """Seconds via ffprobe; 0.0 if unreadable."""
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        capture_output=True, text=True,
    )
    try:
        return float(r.stdout.strip())
    except ValueError:
        return 0.0


def player(outdir, passage, rendered):
    rows = "\n".join(
        f"""    <tr>
      <td><audio controls preload="none" src="{f}"></audio></td>
      <td><code>{html.escape(v)}</code></td>
      <td>{html.escape(c)}</td>
      <td class="n">{d:.2f}s</td>
      <td class="n">{w:.0f} wpm</td>
    </tr>"""
        for v, c, u, f, d, w in rendered
    )
    page = f"""<!doctype html>
<meta charset="utf-8">
<title>Voice audition</title>
<style>
  body {{ font: 15px/1.5 "Segoe UI", system-ui, sans-serif; background: #FFF8F3; color: #091F2E;
         margin: 0; padding: 40px; }}
  h1 {{ font-size: 22px; font-weight: 600; margin: 0 0 4px; }}
  p.sub {{ color: #4a5b68; margin: 0 0 24px; }}
  blockquote {{ background: #fff; border-left: 3px solid #8661C5; margin: 0 0 28px;
                padding: 14px 18px; font-size: 17px; border-radius: 0 6px 6px 0; }}
  table {{ border-collapse: collapse; width: 100%; }}
  th {{ text-align: left; font-size: 12px; letter-spacing: .06em; text-transform: uppercase;
        color: #4a5b68; padding-bottom: 6px; }}
  td {{ padding: 10px 14px 10px 0; border-bottom: 1px solid #eadfd8; vertical-align: middle; }}
  td.n {{ font-variant-numeric: tabular-nums; white-space: nowrap; }}
  code {{ background: #F7F2F9; padding: 2px 6px; border-radius: 4px; font-size: 13px; }}
  audio {{ height: 34px; }}
</style>
<h1>Voice audition</h1>
<p class="sub">Same passage, {len(rendered)} voices. Listen for numbers, acronyms and product
names &mdash; that is where synthetic narration breaks. The pace column is measured, not
assumed: use the chosen voice's wpm for the word budget.</p>
<blockquote>{html.escape(passage)}</blockquote>
<table>
  <tr><th>Listen</th><th>Voice</th><th>Character</th><th>Length</th><th>Pace</th></tr>
{rows}
</table>
"""
    dest = outdir / "audition.html"
    dest.write_text(page, encoding="utf-8")
    return dest


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--text", help="passage to audition verbatim")
    src.add_argument("--from-script", type=pathlib.Path, help="script file; picks the hardest sentence")
    ap.add_argument("--out", type=pathlib.Path, default=pathlib.Path("audition"))
    ap.add_argument("--rate", help='prosody rate, e.g. "-5%%"')
    ap.add_argument("--voices", nargs="*", help="explicit voice IDs; skips catalog selection")
    ap.add_argument("--pool", choices=["hd", "neural", "multilingual", "all"], default="hd")
    ap.add_argument("--gender", choices=["male", "female", "any"], default="any")
    ap.add_argument("--count", type=int, default=5)
    ap.add_argument("--seed", type=int, default=0, help="change to reshuffle the shortlist")
    ap.add_argument("--include", help="regex filter on voice ID")
    ap.add_argument("--refresh-catalog", action="store_true")
    args = ap.parse_args()

    # Repo-local TTS wrapper - no dependency on a personal command on PATH.
    tts = [sys.executable, str(pathlib.Path(__file__).resolve().parent / "azure_tts.py")]

    if args.voices:
        voices = [(v, "", "explicit") for v in args.voices]
    else:
        catalog = fetch_catalog(tts, args.refresh_catalog)
        if catalog:
            voices = select(catalog, args.pool, args.gender, args.count, args.seed, args.include)
            print(f"catalog: {len(catalog)} en-US voices | pool={args.pool} "
                  f"gender={args.gender} seed={args.seed} -> {len(voices)} candidates")
        else:
            voices = [(n, "", d) for n, d in ANCHORS.items()][: args.count]
            print("WARNING could not reach the voice catalog; using the static anchor list.",
                  file=sys.stderr)
        if not voices:
            print("No voices matched those filters.", file=sys.stderr)
            return 1

    passage = args.text or hardest(narration_from(args.from_script))

    args.out.mkdir(parents=True, exist_ok=True)
    print(f'passage ({len(passage)} chars, difficulty {difficulty(passage)}):\n  "{passage}"\n')

    rendered = []
    words = len(passage.split())
    for voice, character, use in voices:
        fname = f"{slug(voice)}.wav"
        dest = args.out / fname
        cmd = [*tts, passage, "-v", voice, "-o", str(dest)]
        if args.rate:
            cmd.append(f"--rate={args.rate}")  # '=' form: argparse reads a bare -5% as a flag
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0:
            err = (r.stderr or r.stdout).strip().splitlines()[-1:] or ["unknown error"]
            print(f"  FAIL  {voice:<42} {err[0]}", file=sys.stderr)
            dest.unlink(missing_ok=True)  # don't leave a 0-byte stub behind
            continue
        secs = duration(dest)
        wpm = (words / secs * 60) if secs else 0.0
        print(f"  ok    {voice:<42} {secs:5.2f}s  {wpm:5.0f} wpm  -> {fname}")
        rendered.append((voice, character, use, fname, secs, wpm))

    if not rendered:
        print("\nNo voices rendered. Check `az login --tenant <speech tenant>`.", file=sys.stderr)
        return 1

    page = player(args.out, passage, rendered)
    chars = len(passage) * len(rendered)
    paces = sorted(w for *_, w in rendered)
    print(f"\n{len(rendered)} voices | ~{chars} chars | ~${chars / 1_000_000 * 30:.3f} at Dragon HD rates")
    print(f"pace spread {paces[0]:.0f}-{paces[-1]:.0f} wpm "
          f"({(paces[-1] / paces[0] - 1) * 100:.0f}% runtime swing) -- compare voices, do NOT budget from this")
    # This passage is deliberately the hardest in the script, so these rates are a floor.
    # Measured 2026-08-03: Ava read the hard passage at 129 wpm and the full script at 160.7.
    print("NOTE: these rates are a FLOOR, not an average -- the passage is the hardest in the")
    print("      script by design. Budget runtime only from the full-script WAV via ffprobe.")
    if args.rate:
        print("      --rate also switches the wrapper to its SSML path, which is ~17% slower")
        print("      before the requested rate applies. Render the real narration the same way.")
    print(f"open {page}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
