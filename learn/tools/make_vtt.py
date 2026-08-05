#!/usr/bin/env python3
"""Build a WebVTT caption file from a HyperFrames transcript.json.

The transcript is a flat array of {text, start, end}. Cues are grouped to match
the shipped MD-102 house style: <=2 lines, ~48 chars per line, broken on sentence
ends where possible, and never longer than MAX_SECS.
"""
import argparse
import json
import pathlib
import re

MAX_CHARS_PER_LINE = 48
MAX_LINES = 2
MAX_SECS = 5.5
SENTENCE_END = (".", "?", "!", ":")


def wrap(text):
    lines, cur = [], ""
    for word in text.split():
        candidate = f"{cur} {word}".strip()
        if len(candidate) > MAX_CHARS_PER_LINE and cur:
            lines.append(cur)
            cur = word
        else:
            cur = candidate
    if cur:
        lines.append(cur)
    return lines


def group(words):
    """Yield lists of word dicts, each list becoming one cue."""
    cue, budget = [], MAX_CHARS_PER_LINE * MAX_LINES
    for w in words:
        # Decide BEFORE appending. The previous version appended first and then
        # tested, so a cue could overshoot the budget by a whole word and wrap
        # to a third line - violating the <=2 line rule this module documents.
        if cue:
            candidate = " ".join(x["text"] for x in cue + [w])
            if (
                len(candidate) > budget
                or len(wrap(candidate)) > MAX_LINES
                or (w["end"] - cue[0]["start"]) > MAX_SECS
            ):
                yield cue
                cue = [w]
                continue
        cue.append(w)
        text = " ".join(x["text"] for x in cue)
        ends_sentence = w["text"].rstrip('"\u201d').endswith(SENTENCE_END)
        # Flush on a sentence end only once the cue has enough body to stand alone.
        if ends_sentence and len(text) >= budget * 0.45:
            yield cue
            cue = []
    if cue:
        yield cue


def stamp(t):
    ms = round(t * 1000)
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d}.{ms:03d}"


def _bare(s):
    return re.sub(r"[^\w-]", "", s).lower()


def apply_lexicon(words, lex):
    """Merge multi-word names into single tokens and fix Whisper's spelling.

    Two defects this prevents, both seen in shipped output:
      * "Microsoft" ended one cue and "Defender" opened the next - a product
        name split across a cue boundary. No post-hoc text substitution can
        repair that, because the two halves live in different cues. Merging
        BEFORE grouping makes the name unsplittable.
      * Whisper lowercases product role names ("privileged role administrator").
        The canonical spelling in the lexicon restores them.

    A token containing spaces still renders correctly - cues join on " ".
    """
    phrases = sorted((p for p in lex.get("phrases", [])),
                     key=lambda p: -len(p.split()))
    keyed = [(p, [_bare(t) for t in p.split()]) for p in phrases]
    hyphenate = [tuple(pair) for pair in lex.get("hyphenate", [])]
    respell = lex.get("respell", {})

    out, i, merges = [], 0, 0
    while i < len(words):
        hit = None
        for canonical, keys in keyed:
            span = words[i:i + len(keys)]
            if len(span) == len(keys) and [_bare(t["text"]) for t in span] == keys:
                hit = (canonical, span)
                break
        if hit:
            canonical, span = hit
            last = span[-1]["text"]
            trail = last[len(last.rstrip(".,;:?!")):]
            out.append({"text": canonical + trail,
                        "start": span[0]["start"], "end": span[-1]["end"]})
            i += len(span)
            merges += 1
            continue

        w = dict(words[i])
        pair = (_bare(w["text"]), _bare(words[i + 1]["text"])) if i + 1 < len(words) else None
        if pair and pair in hyphenate:
            nxt = words[i + 1]["text"]
            trail = nxt[len(nxt.rstrip(".,;:?!")):]
            w["text"] = f"{w['text']}-{_bare(nxt)}{trail}"
            w["end"] = words[i + 1]["end"]
            out.append(w)
            i += 2
            merges += 1
            continue

        stripped = w["text"].rstrip(".,;:?!")
        if stripped in respell:
            w["text"] = respell[stripped] + w["text"][len(stripped):]
        out.append(w)
        i += 1
    return out, merges


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("transcript", type=pathlib.Path)
    ap.add_argument("-o", "--output", type=pathlib.Path, required=True)
    ap.add_argument("--offset", type=float, default=0.0,
                    help="seconds to shift every cue; use only if audio is offset in the composition")
    ap.add_argument("--lexicon", type=pathlib.Path,
                    help='JSON: {"phrases": [...], "hyphenate": [[a,b]], "respell": {from: to}}')
    args = ap.parse_args()

    words = json.loads(args.transcript.read_text(encoding="utf-8"))

    if args.lexicon:
        lex = json.loads(args.lexicon.read_text(encoding="utf-8"))
        words, merges = apply_lexicon(words, lex)
        print(f"lexicon: {merges} token merge(s) applied")

    out = ["WEBVTT", ""]
    n = 0
    for cue in group(words):
        n += 1
        text = " ".join(w["text"] for w in cue)
        out.append(str(n))
        out.append(f"{stamp(cue[0]['start'] + args.offset)} --> {stamp(cue[-1]['end'] + args.offset)}")
        out.extend(wrap(text))
        out.append("")

    args.output.write_text("\n".join(out), encoding="utf-8")
    print(f"{n} cues -> {args.output}")
    print(f"covers {stamp(words[0]['start'] + args.offset)} - {stamp(words[-1]['end'] + args.offset)}")


if __name__ == "__main__":
    main()
