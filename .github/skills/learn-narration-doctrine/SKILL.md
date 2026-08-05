---
name: learn-narration-doctrine
description: "Voice and narration law for Microsoft Learn companion videos — Azure Dragon HD voice selection, word-budget and pacing maths, conversational tone, SSML use, and pronunciation rules for product names, numbers, dates and acronyms. Use when writing or reviewing narration, choosing a voice, generating TTS, estimating runtime from a script, or diagnosing pacing and pronunciation problems. Covers the azure_tts CLI contract and the transcribe handoff."
---

# Learn Narration Doctrine

Azure Speech Dragon HD is the narration engine. Kokoro (`hyperframes tts`) is a throwaway-draft
fallback only — it mispronounces numbers, times and currency, and has no SSML.

## The honest premise

Mayer's **Voice** principle says humans learn better from a human voice than a computer voice.
This pipeline is synthetic end to end. Dragon HD narrows the gap; it does not close it. That is
an accepted trade-off, and the mitigations below are how the cost is kept small:
conversational register, real contractions, SSML breathing room, and correct pronunciation.
A synthetic voice reading stiff prose sounds far worse than one reading natural speech.

## The CLI contract

```
py tools/azure_tts.py script.txt -v "en-US-Ava:DragonHDLatestNeural" -o narration.wav
py tools/azure_tts.py script.txt -v "en-US-Andrew:DragonHDLatestNeural" --rate=-5% -o narration.wav
py tools/azure_tts.py --ssml script.ssml.xml -o narration.wav
py tools/azure_tts.py --list-voices
```

- **Always quote the voice ID.** The colon breaks unquoted PowerShell parsing.
- **Use the `=` form for `--rate`.** `--rate "-5%"` fails argparse (`-5%` parses as a flag);
  write `--rate=-5%`, including inside subprocess argument lists.
- Auth is **Entra ID only** — no keys. Requires an active `az login` against the tenant that owns
  your Speech resource (set `AZURE_SPEECH_TENANT_ID` in the config). A 401 means re-login, not a
  broken config. Confirm the identity is a *user*, not a service principal:
  `az account show --query "user.type"`.
- Output is 24 kHz mono 16-bit PCM WAV — byte-compatible with the Kokoro output, so
  `npx hyperframes transcribe narration.wav` consumes it unchanged.

**Default to the SSML path — plain text reads rushed.** Plain `py tools/azure_tts.py narration.txt`
runs ~161 wpm; the SSML path lands at the corpus-natural ~138 wpm and gives each motion beat room
to land. The shipped pipeline generates SSML from the narration with `make_ssml.py`, then
synthesizes from it:

```
py tools/make_ssml.py narration.txt -o narration.ssml --voice "en-US-Ava:DragonHDLatestNeural"
py tools/azure_tts.py --ssml narration.ssml -o narration.wav
```

`make_ssml.py` bakes the locked voice + a gentle `--rate` (default `-3%`) into the SSML, adds a
breath `<break>` at every beat (paragraph) boundary, honors inline `*emphasis*` and
`[[pause:600ms]]`, and collapses any stacked breaks so a gap never reads unnaturally long.
`narration.txt` stays the word source for `diff_transcript`/anchoring — SSML changes pacing,
never words.

## Voice selection

| Voice | Register | Use for |
|---|---|---|
| `en-US-Ava:DragonHDLatestNeural` | polished conversational | **default** — Learn modules, professional narration |
| `en-US-Andrew:DragonHDLatestNeural` | warm, coaching | mentor/peer register, guidance-heavy content |
| `en-US-Emma:DragonHDLatestNeural` | friendly explainer | onboarding, welcome, introductory |
| `en-US-Phoebe:DragonHDOmniLatestNeural` | most natural, informal | when "real person" matters most |
| `en-US-Andrew:DragonHDOmniLatestNeural` | thinking-out-loud | spontaneous pacing |
| `en-US-JennyNeural` | broadcast | formal announcements |

**Lock the voice at a gate, before any TTS spend.** One voice per video. Rotating voices across
a series is a deliberate editorial choice, not a default — and if you rotate, rotate by learning
path or course, never within one video.

## The audition gate

A table is not a decision. **Hear the voice before committing to a full render.**

```
py tools/audition_voices.py --from-script script.md
py tools/audition_voices.py --text "..." --rate=-5%
```

This renders the *same* passage across the five candidates and writes `audition.html` — one
page, labelled players, side by side. Five voices on a 120-character passage costs about
$0.02, against roughly $0.20 for a full five-minute narration in the wrong voice.

**Audition the hardest sentence, not the first one.** Synthetic voices fail on hard material:
numbers, versions, acronyms, product names, symbols. An opening line like "Let's get started"
sounds flawless in every voice and tells you nothing. `--from-script` therefore scores every
sentence for difficulty and picks the worst offender rather than the opener.

Run this **before** the script is finalised where possible — if the chosen voice mangles a
product name, the cheapest fix is rewording the script, not layering on SSML.

### If every audition sample sounds identical, stop

That is the signature of the voice argument being dropped rather than five voices genuinely
sounding alike. It happened for real: the wrapper set the voice on the *synthesizer* after
construction instead of on the `SpeechConfig` before it, so `-v` was silently ignored on the
plain-text path and everything rendered in the default `en-US-AvaMultilingualNeural`. Fixed
2026-08-03. Verify with `ffprobe` durations or a waveform — identical byte sizes across voices
means the flag is not landing.

## Pacing maths

**Corpus baseline: 145 wpm (2.42 words/sec)** — measured across all 41 shipped MD-102
narrations, roughly 68 minutes of real Dragon HD audio, mostly `en-US-Davis`. Range 124–156.
That is the planning default.

**But pace is a property of the voice.** On one fixed passage, Dragon HD voices spanned
146–185 wpm — a 27% runtime swing. Budget with the voice you locked, and treat the corpus mean
as the starting point only.

| Voice | Isolated-passage rate | Note |
|---|---|---|
| `en-US-Phoebe:DragonHDOmniLatestNeural` | 185 wpm | fastest measured |
| `en-US-Andrew:DragonHDLatestNeural` | 165 wpm | |
| `en-US-Ava:DragonHDLatestNeural` | 152 wpm | current default |
| `en-US-Davis:DragonHDLatestNeural` | — | **the shipped corpus voice**, 151 wpm on `lp1m01-u02-overview` |
| `en-US-Emma:DragonHDLatestNeural` | 146 wpm | |

```
words ≈ target_content_seconds × words_per_second_for_that_voice
```

A 90-second companion is **≈218 words at the corpus mean**. The shipped
`lp1m01-u02-overview` is 225 words over 89.4 s — within 3%.

### Pace is voice × code path × content difficulty — all three

Measured on one script (203 words, `en-US-Ava:DragonHDLatestNeural`, 2026-08-03):

| Variable | Result |
|---|---|
| `azure_tts.py` plain text (`speak_text_async`) | 75.8 s — **160.7 wpm** |
| `azure_tts.py` with any `--rate`, incl. `+0%` (SSML `<prosody>`) | 88.4 s — **137.8 wpm** |
| Audition of the *hardest* sentence in that same script | **129 wpm** |

Three lessons, each of which cost a wrong budget:

1. **Passing `--rate` at all switches code path** and costs ~17% pace before the requested
   rate applies — `--rate=-6%` delivered −23%. A wpm figure without its code path is not a
   measurement. The SSML path lands inside the shipped corpus; plain text overshoots it.
2. **The audition under-predicts by design.** It deliberately renders the hardest sentence,
   so it yields a *floor*, not an average — here 129 vs an actual 160.7, a 25% miss. Use the
   audition to judge pronunciation and to compare voices against each other. Never budget
   runtime from it.
3. **Only the full-script WAV is a pacing measurement**, and measure it with `ffprobe`, not
   the SDK's self-reported `audio_duration`.

### Two corrections worth remembering

The earlier figure of **138 wpm** was not wrong because it came from a different engine — the
predecessor corpus is Dragon HD, same as now. It was simply **low**, sitting near the corpus
15th percentile. And the first attempt to fix it (152 wpm, from a single 21-word sentence) sat
near the 90th. A one-sentence sample is not a pacing measurement.

Budget against the profile's **content** length, not total — the AI end card adds 10.667 s that
carries no narration.

### Three stages, and only the last one is truth

1. **Estimate** from the corpus mean, or the voice's rate if it is known, to size the script.
2. **Verify** against the actual WAV after TTS — `ffprobe -show_entries format=duration`.
3. **Adjust the script**, not the rate. Reaching for `--rate` to hit a number changes the
   register and is audible; cutting or adding a sentence is not.

Estimates drift; the WAV is truth. `motion-doctrine` puts it plainly: audio is the clock, and
re-timing to a new VO re-opens every seam it touches — which is why the voice locks *before*
the composition is built, not after.

## Register

Write for the ear, not the page.

- **Contractions.** "You'll", "it's", "here's". Prose without them reads robotic aloud.
- **Second person.** Talk to one learner, not an audience.
- **Short sentences.** One idea each. A sentence that needs a comma-splice to survive will not
  survive a synthetic read.
- **Signpost.** "First…", "Now the important part…", "So what does that buy you?"
- **Open with the why.** The playbook's first design principle: explain why the topic matters
  and what problem it solves — before the mechanism.
- **No cultural references or humour.** Playbook accessibility rule; also a localization hazard.
- **No marketing register.** No "seamless", "powerful", "unlock", "revolutionize". Learn style
  applies to spoken words too.
- **Connect the sentences — flow beats fragments.** Easy-to-understand prose hands off from one
  sentence to the next with a connective: "so", "but", "that's why", "which means", "here's the
  catch". A beat that is a pile of true-but-unlinked statements reads *disjointed*, even when
  every sentence is clean on its own. Read the whole beat aloud; if it lurches between ideas,
  add the connective tissue or merge the fragments. Rushed comes from pace (fix with SSML
  breaths); disjointed comes from missing connectives (fix in the prose) — they are different
  faults with different fixes.

## Narration is not on-screen text

Mayer's **Redundancy** principle: narration + graphics beats narration + graphics + text. The
script is the spoken layer. On-screen text is **labels, not transcript**. Never write a beat
whose visual is the sentence being spoken.

## Pronunciation

Synthetic voices fail predictably. Fix these in the script or with SSML — never leave them to chance.

| Hazard | Handling |
|---|---|
| Product names | Spell out in full on first use: "Microsoft Intune", not "Intune" cold |
| Acronyms read as words | Write "MDM" if letters are wanted; SSML `say-as` if ambiguous |
| Version numbers | "Windows eleven", not "Windows 11", when the read matters |
| Times / dates / currency | Write them as spoken: "nine thirty", "twelve hundred dollars" |
| `/` and `-` | Write "and" or "to" — punctuation is read unpredictably |
| Paths and URLs | Never narrate a raw path; describe it and show it on screen |

SSML for prosody, emphasis and pauses:

```xml
<speak version='1.0' xml:lang='en-US' xmlns:mstts='https://www.w3.org/2001/mstts'>
  <voice name='en-US-Ava:DragonHDLatestNeural'>
    <prosody rate='-5%'>
      So the new dashboard<break time='400ms'/>
      is simpler than you'd think. <emphasis level='moderate'>Three panels.</emphasis>
    </prosody>
  </voice>
</speak>
```

Use `<break>` at beat boundaries so motion has room to land. A visual change with no audio gap
reads rushed.

## The pipeline handoff

```
script.md → narration.txt → make_ssml → azure_tts.py → narration.wav
          → hyperframes transcribe → transcript.json  (word-level)
          → beats anchored to real word times
          → captions (VTT)
```

Anchor motion to **transcript word timings**, never to estimates. If the VO is regenerated, the
transcript and every seam anchored to it are invalidated — re-run both.

Captions and transcripts are **mandatory deliverables**, not optional polish. See
`learn-video-delivery`.
