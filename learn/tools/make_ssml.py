"""narration.txt -> narration.ssml — breathing-room SSML for Azure Dragon HD.

Why this exists: the plain-text azure_tts.py path runs ~161 wpm and reads *rushed*; the
`--ssml` path lands at the shipped-corpus ~138 wpm and gives motion room to land
(see learn-narration-doctrine, "Pace is voice x code path x content difficulty"). This
tool emits the SSML that path wants — a <prosody rate> wrapper, a <break> at every beat
(paragraph) boundary for a breath, and optional per-sentence breaths — from the SAME words
that are in narration.txt, so the Whisper transcript still aligns to the words and every
cue anchor stays valid. Words are never changed; only pacing and pauses.

Plain text works with zero markup. Optional inline authoring:
  *emphasised*                 -> <emphasis level="moderate">emphasised</emphasis>
  [[pause]] / [[pause:600ms]]  -> a <break> exactly there (a beat boundary mid-paragraph)
A blank line between paragraphs is a beat boundary and gets a breath break automatically.

Usage:
  py tools/make_ssml.py narration.txt -o narration.ssml
  py tools/make_ssml.py narration.txt -o narration.ssml --voice en-US-Andrew:DragonHDLatestNeural --rate=-5%
  py tools/make_ssml.py narration.txt -o narration.ssml --sentence-break 150ms

Then, in the renderer:
  py tools/azure_tts.py --ssml narration.ssml -o narration.wav   # voice + rate live INSIDE the SSML
"""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys
from xml.sax.saxutils import escape

SSML_NS = "http://www.w3.org/2001/10/synthesis"
MSTTS_NS = "https://www.w3.org/2001/mstts"

# split on sentence-final punctuation followed by whitespace; keeps the punctuation
_SENTENCE_RE = re.compile(r"(?<=[.!?])\s+")
_EMPHASIS_RE = re.compile(r"\*(.+?)\*")
_PAUSE_RE = re.compile(r"\[\[pause(?::\s*([0-9]+(?:ms|s)?))?\]\]", re.IGNORECASE)
_BREAK_RUN_RE = re.compile(r'(?:<break time="([0-9]+(?:ms|s)?)"/>\s*){2,}')


def _to_ms(token: str) -> int:
    token = token.strip().lower()
    if token.endswith("ms"):
        return int(token[:-2])
    if token.endswith("s"):
        return int(float(token[:-1]) * 1000)
    return int(token)


def collapse_breaks(text: str) -> str:
    """Two stacked breaks read as one unnaturally long gap — keep only the longest."""
    def repl(m: re.Match[str]) -> str:
        times = re.findall(r'<break time="([0-9]+(?:ms|s)?)"/>', m.group(0))
        return f'<break time="{max(_to_ms(t) for t in times)}ms"/> '
    return _BREAK_RUN_RE.sub(repl, text)



def die(msg: str) -> None:
    print(f"ERROR: make_ssml: {msg}", file=sys.stderr)
    raise SystemExit(1)


def norm_rate(rate: str) -> str:
    """Accept '-3', '-3%', '+0%', '0' -> a valid prosody rate string like '-3%'."""
    r = rate.strip()
    if r.endswith("%"):
        core = r[:-1]
    else:
        core = r
    try:
        float(core)
    except ValueError:
        die(f"--rate must be a percentage like -3% or -5, got {rate!r}")
    if not core.startswith(("+", "-")):
        core = "+" + core
    return core + "%"


def norm_ms(value: str, flag: str) -> str:
    """Accept '400', '400ms', '1s' -> a valid break time token."""
    v = value.strip().lower()
    if v in ("0", "0ms"):
        return ""
    if v.endswith("ms") or v.endswith("s"):
        return v
    if v.isdigit():
        return v + "ms"
    die(f"{flag} must be a duration like 400ms or 1s, got {value!r}")
    return ""


def markup_inline(text: str) -> str:
    """Escape text for XML, then re-introduce sanctioned inline SSML from author markers."""
    out = escape(text)
    out = _PAUSE_RE.sub(lambda m: f'<break time="{m.group(1) or "400ms"}"/>', out)
    out = _EMPHASIS_RE.sub(lambda m: f'<emphasis level="moderate">{m.group(1)}</emphasis>', out)
    return out


def build_body(raw: str, paragraph_break: str, sentence_break: str) -> str:
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", raw.strip()) if p.strip()]
    if not paragraphs:
        die("narration is empty")

    pieces: list[str] = []
    for pi, para in enumerate(paragraphs):
        # collapse hard-wrapped lines inside a paragraph into one flow
        flow = " ".join(line.strip() for line in para.splitlines() if line.strip())
        if sentence_break:
            sentences = _SENTENCE_RE.split(flow)
            joiner = f'<break time="{sentence_break}"/> '
            body = joiner.join(markup_inline(s) for s in sentences if s)
        else:
            body = markup_inline(flow)
        body = collapse_breaks(body)
        pieces.append(f"      <p>{body}</p>")
        if paragraph_break and pi < len(paragraphs) - 1:
            pieces.append(f'      <break time="{paragraph_break}"/>')
    return "\n".join(pieces)


def build_ssml(raw: str, voice: str, rate: str, lang: str,
               paragraph_break: str, sentence_break: str) -> str:
    body = build_body(raw, paragraph_break, sentence_break)
    return (
        f"<speak version=\"1.0\" xmlns=\"{SSML_NS}\" xmlns:mstts=\"{MSTTS_NS}\" "
        f"xml:lang=\"{lang}\">\n"
        f"  <voice name=\"{escape(voice, {chr(34): '&quot;'})}\">\n"
        f"    <prosody rate=\"{rate}\">\n"
        f"{body}\n"
        f"    </prosody>\n"
        f"  </voice>\n"
        f"</speak>\n"
    )


def main() -> None:
    ap = argparse.ArgumentParser(description="Convert narration.txt to breathing-room SSML.")
    ap.add_argument("input", help="plain narration text file (paragraphs split by blank lines)")
    ap.add_argument("-o", "--out", required=True, help="output .ssml path")
    ap.add_argument("--voice", default="en-US-Ava:DragonHDLatestNeural",
                    help="Dragon HD voice id (baked into the SSML <voice>)")
    ap.add_argument("--rate", default="-3%",
                    help="prosody rate, e.g. -3%% (default) or -5%%. The SSML path already runs "
                         "~138 wpm; this trims a touch more so it never reads rushed.")
    ap.add_argument("--lang", default="en-US")
    ap.add_argument("--paragraph-break", default="400ms",
                    help="breath break at each beat/paragraph boundary (default 400ms; 0 to disable)")
    ap.add_argument("--sentence-break", default="0",
                    help="optional breath break between sentences within a paragraph "
                         "(default 0 = off; ~150ms adds gentle breathing without sounding choppy)")
    args = ap.parse_args()

    src = Path(args.input)
    if not src.exists():
        die(f"input not found: {src}")
    raw = src.read_text(encoding="utf-8")

    ssml = build_ssml(
        raw,
        voice=args.voice,
        rate=norm_rate(args.rate),
        lang=args.lang,
        paragraph_break=norm_ms(args.paragraph_break, "--paragraph-break"),
        sentence_break=norm_ms(args.sentence_break, "--sentence-break"),
    )

    # self-check: the emitted SSML must be well-formed XML
    import xml.etree.ElementTree as ET
    try:
        ET.fromstring(ssml)
    except ET.ParseError as exc:
        die(f"generated SSML is not well-formed ({exc}). Check for stray < or & in the narration.")

    out = Path(args.out)
    out.write_text(ssml, encoding="utf-8")
    words = len(re.findall(r"\b\w+\b", raw))
    print(f"SSML OK -> {out}  ({words} words, voice {args.voice}, rate {norm_rate(args.rate)}, "
          f"paragraph-break {args.paragraph_break}, sentence-break {args.sentence_break})")


if __name__ == "__main__":
    main()
