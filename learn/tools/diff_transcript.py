#!/usr/bin/env python3
"""Diff a Whisper transcript against the narration it was generated from.

TTS says a word confidently and Whisper hears something else. That is invisible
in the WAV and invisible in the render - it only shows up in the captions, where
it is a factual error. On one build Whisper heard "MDM" in the very beat that
teaches MDM vs MAM, inverting the lesson.

Distinguishes real mishearings from benign orthography (numeral normalization,
hyphenation), so a clean run means clean and a dirty run means look.

Exit 1 if any difference is not a known-benign class.
"""
import argparse
import json
import pathlib
import re
import sys
from difflib import SequenceMatcher

# Differences that are spelling, not hearing. Compared on the normalized forms.
BENIGN = [
    (r"^a hundred$", r"^100$"),
    (r"^one hundred$", r"^100$"),
    (r"^multifactor$", r"^multi-factor$"),
    (r"^(\w+)-(\w+)$", r"^\1 \2$"),        # hyphen dropped
    (r"^(\w+) (\w+)$", r"^\1-\2$"),        # hyphen added
    (r"^percent$", r"^%$"),
]


def norm(s):
    s = s.lower().replace("\u2019", "'").replace("\u2014", " ").replace("\u2013", " ")
    return re.sub(r"[^a-z0-9'\-]", "", s)


def is_benign(src, hyp):
    a, b = " ".join(src), " ".join(hyp)
    for pa, pb in BENIGN:
        try:
            if re.match(pa, a) and re.match(pb.replace(r"\1", "").replace(r"\2", ""), b):
                return True
            if re.match(pa, a) and re.search(pb.replace(r"\1", r"(\w+)").replace(r"\2", r"(\w+)"), b):
                return True
        except re.error:
            continue
    # hyphen-only difference
    if a.replace("-", " ") == b.replace("-", " "):
        return True
    if a.replace("-", "") == b.replace("-", ""):
        return True
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("narration", type=pathlib.Path, help="narration.txt (source of truth)")
    ap.add_argument("transcript", type=pathlib.Path, help="transcript.json from hyperframes transcribe")
    ap.add_argument("--hazard", action="append", default=[],
                    help="word to report timings for (repeatable), e.g. --hazard MAM")
    args = ap.parse_args()

    src = args.narration.read_text(encoding="utf-8")
    data = json.loads(args.transcript.read_text(encoding="utf-8"))
    words = data if isinstance(data, list) else data.get("words", data)

    src_tokens = [norm(t) for t in re.split(r"\s+", src) if norm(t)]
    hyp_tokens = [norm(w["text"]) for w in words if norm(w.get("text", ""))]
    print(f"narration {len(src_tokens)} words | transcript {len(hyp_tokens)} words")

    sm = SequenceMatcher(None, src_tokens, hyp_tokens, autojunk=False)
    real = 0
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        s, h = src_tokens[i1:i2], hyp_tokens[j1:j2]
        benign = is_benign(s, h)
        if not benign:
            real += 1
        label = "benign " if benign else "MISHEARD"
        ctx = " ".join(src_tokens[max(0, i1 - 3):i1])
        print(f"\n  [{label}] after: ...{ctx}")
        print(f"      narration : {' '.join(s) or '(nothing)'}")
        print(f"      transcript: {' '.join(h) or '(nothing)'}")

    for hz in args.hazard:
        hits = [w for w in words if norm(w.get("text", "")) == norm(hz)]
        times = ", ".join(f"{w['start']:.2f}s" for w in hits) or "NOT FOUND as one token"
        print(f"\n  hazard {hz!r}: {len(hits)}x  {times}")

    print(f"\n{'CLEAN - no mishearings' if real == 0 else f'{real} MISHEARING(S) - fix before shipping captions'}")
    return 1 if real else 0


if __name__ == "__main__":
    sys.exit(main())
