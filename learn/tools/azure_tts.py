"""azure_tts.py — repo-local Azure Speech (Dragon HD / Neural) TTS wrapper for the
HyperFrames Learn-video pipeline.

Vendored into the repo on purpose: the narration step must not depend on a personal
tool on PATH (there used to be an `azure-tts` wrapper under ~/.copilot/bin — that is
gone). This is the generic, portable version. Nothing here is tenant- or
resource-specific; every value comes from config the operator supplies.

Auth: Entra ID via the Azure CLI (`az`) — there is no API key. You need an active
`az login` against the tenant that owns your Speech resource.

Config resolution order (first hit wins):
  1. --env-file <path>
  2. ./azure-speech.env               (in the current working directory)
  3. ~/.config/azure-speech/config.env
  4. environment variables           (AZURE_SPEECH_RESOURCE_ID, AZURE_SPEECH_REGION,
                                       AZURE_SPEECH_TENANT_ID, AZURE_SPEECH_SUBSCRIPTION_ID)
Required keys: AZURE_SPEECH_RESOURCE_ID, AZURE_SPEECH_REGION, AZURE_SPEECH_TENANT_ID.
These are NOT secrets (a resource id + region + tenant); keep real secrets out of the repo.

Usage:
    py tools/azure_tts.py "Hello world" -v en-US-Ava:DragonHDLatestNeural -o out.wav
    py tools/azure_tts.py script.txt -v en-US-Andrew:DragonHDLatestNeural -o out.wav
    py tools/azure_tts.py --ssml narration.ssml -o narration.wav
    py tools/azure_tts.py script.txt --rate=-5% -o slower.wav
    py tools/azure_tts.py --list-voices
"""

import argparse
import os
import pathlib
import shutil
import subprocess
import sys

import azure.cognitiveservices.speech as speechsdk

DEFAULT_CFG = pathlib.Path.home() / ".config" / "azure-speech" / "config.env"
REQUIRED = ("AZURE_SPEECH_RESOURCE_ID", "AZURE_SPEECH_REGION")
OPTIONAL = ("AZURE_SPEECH_TENANT_ID", "AZURE_SPEECH_SUBSCRIPTION_ID")


def cfg_candidates(explicit=None):
    if explicit:
        return [pathlib.Path(explicit)]
    return [pathlib.Path.cwd() / "azure-speech.env", DEFAULT_CFG]


def load_cfg(explicit=None):
    for path in cfg_candidates(explicit):
        if path.exists():
            out = {}
            for line in path.read_text().splitlines():
                if "=" in line and not line.strip().startswith("#"):
                    k, v = line.split("=", 1)
                    out[k.strip()] = v.strip()
            missing = [k for k in REQUIRED if k not in out]
            if missing:
                sys.exit(f"{path} is missing: {', '.join(missing)}")
            out["_source"] = str(path)
            return out

    # Fallback: environment variables — no config file needed (CI / other machines).
    if all(os.getenv(k) for k in REQUIRED):
        out = {k: os.environ[k] for k in REQUIRED}
        for k in OPTIONAL:
            if os.getenv(k):
                out[k] = os.environ[k]
        out["_source"] = "environment variables"
        return out

    searched = "\n  ".join(str(p) for p in cfg_candidates(explicit))
    sys.exit(
        "No Speech config found. Provide --env-file, an azure-speech.env, "
        f"~/.config/azure-speech/config.env, or the AZURE_SPEECH_* env vars.\nSearched:\n  {searched}"
    )


def _access_token(az, tenant):
    cmd = [az, "account", "get-access-token",
           "--resource", "https://cognitiveservices.azure.com",
           "--query", "accessToken", "-o", "tsv"]
    if tenant:
        cmd += ["--tenant", tenant]
    return subprocess.check_output(cmd, text=True, timeout=60).strip()


def get_token(cfg):
    """Acquire an AAD token for the tenant that owns the resource, logging in if needed.

    No DefaultAzureCredential fallback: the resource lives in a specific tenant, and falling
    back to the ambient context (possibly a service principal in another tenant) yields an
    opaque WebSocket 401 rather than a usable error.
    """
    resource_id = cfg["AZURE_SPEECH_RESOURCE_ID"]
    tenant = cfg.get("AZURE_SPEECH_TENANT_ID") or os.getenv("AZURE_TENANT_ID")
    if not tenant:
        sys.exit(
            f"AZURE_SPEECH_TENANT_ID is not set ({cfg['_source']}).\n"
            "Auth must target the tenant that owns the Speech resource explicitly."
        )

    az = shutil.which("az")
    if not az:
        sys.exit("Azure CLI ('az') not found on PATH.")

    try:
        token = _access_token(az, tenant)
    except Exception:
        print(f"Azure CLI login required for tenant {tenant}. Starting 'az login'...",
              file=sys.stderr)
        try:
            env = {**os.environ, "AZURE_CORE_LOGIN_EXPERIENCE_V2": "off"}
            subprocess.run([az, "login", "--tenant", tenant, "--only-show-errors"],
                           check=True, env=env)
            sub = cfg.get("AZURE_SPEECH_SUBSCRIPTION_ID")
            if sub:
                subprocess.run([az, "account", "set", "--subscription", sub],
                               check=False, env=env)
            token = _access_token(az, tenant)
        except Exception as exc:
            sys.exit(
                f"Azure authentication failed for tenant {tenant}.\n  {exc}\n\n"
                f"Run 'az login --tenant {tenant}' and retry."
            )

    if not token:
        sys.exit(f"Empty token for tenant {tenant}. Run: az login --tenant {tenant}")

    # Azure Speech expects the AAD token as: aad#<resourceId>#<token>
    return f"aad#{resource_id}#{token}"


def build_synth(cfg, output_path, voice=None):
    speech_cfg = speechsdk.SpeechConfig(
        auth_token=get_token(cfg),
        region=cfg["AZURE_SPEECH_REGION"],
    )
    # Must be set on the config BEFORE the synthesizer is built; setting it after is ignored.
    if voice:
        speech_cfg.speech_synthesis_voice_name = voice
    speech_cfg.set_speech_synthesis_output_format(
        speechsdk.SpeechSynthesisOutputFormat.Riff24Khz16BitMonoPcm
    )
    audio_cfg = speechsdk.audio.AudioOutputConfig(filename=output_path)
    return speechsdk.SpeechSynthesizer(speech_config=speech_cfg, audio_config=audio_cfg)


def list_voices(cfg, as_json=False):
    speech_cfg = speechsdk.SpeechConfig(
        auth_token=get_token(cfg),
        region=cfg["AZURE_SPEECH_REGION"],
    )
    synth = speechsdk.SpeechSynthesizer(speech_config=speech_cfg, audio_config=None)
    result = synth.get_voices_async("en-US").get()
    if result.reason != speechsdk.ResultReason.VoicesListRetrieved:
        sys.exit(f"Failed to list voices: {result.error_details}")

    voices = [v for v in sorted(result.voices, key=lambda x: x.short_name) if v.locale.startswith("en-")]

    if as_json:
        import json
        print(json.dumps([
            {
                "short_name": v.short_name,
                "local_name": v.local_name,
                "gender": v.gender.name,
                "locale": v.locale,
                "tier": "hd" if "HD" in v.short_name else ("multilingual" if "Multilingual" in v.short_name else "neural"),
                "styles": list(v.style_list or []),
            }
            for v in voices
        ], indent=2))
        return

    for v in voices:
        tag = ""
        if "HD" in v.short_name:
            tag = " [HD]"
        elif "Multilingual" in v.short_name:
            tag = " [Multilingual]"
        print(f"  {v.short_name:<48} {v.gender.name:<7} {v.locale}{tag}")


def main():
    p = argparse.ArgumentParser(description="Azure Speech TTS -> 24kHz mono PCM WAV (Entra auth).")
    p.add_argument("input", nargs="?", help="Text, or path to a .txt file")
    p.add_argument("-o", "--output", default="speech.wav")
    p.add_argument("-v", "--voice", default="en-US-Ava:DragonHDLatestNeural")
    p.add_argument("--ssml", help="Path to an SSML file (voice + rate live inside it)")
    p.add_argument("--rate", default="0%", help="prosody rate; use the = form, e.g. --rate=-5%%")
    p.add_argument("--list-voices", action="store_true")
    p.add_argument("--json", action="store_true", help="machine-readable voice list")
    p.add_argument("--env-file", help="explicit path to the Speech config env file")
    args = p.parse_args()

    cfg = load_cfg(args.env_file)
    if args.list_voices:
        list_voices(cfg, as_json=args.json)
        return

    if not args.input and not args.ssml:
        sys.exit("Provide text, a .txt path, or --ssml <file>")

    synth = build_synth(cfg, args.output, voice=args.voice)

    if args.ssml:
        ssml = pathlib.Path(args.ssml).read_text(encoding="utf-8")
        result = synth.speak_ssml_async(ssml).get()
    else:
        text = pathlib.Path(args.input).read_text(encoding="utf-8") \
            if os.path.isfile(args.input) else args.input
        if args.rate != "0%":
            ssml = (
                "<speak version='1.0' xml:lang='en-US' xmlns:mstts='https://www.w3.org/2001/mstts'>"
                f"<voice name='{args.voice}'><prosody rate='{args.rate}'>{text}</prosody></voice></speak>"
            )
            result = synth.speak_ssml_async(ssml).get()
        else:
            result = synth.speak_text_async(text).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print(f"OK Generated {result.audio_duration.total_seconds():.1f}s -> {args.output}")
    else:
        detail = ""
        try:
            cd = result.cancellation_details
            if cd:
                detail = f"{cd.reason}: {cd.error_details}"
        except Exception as exc:
            detail = f"(could not read cancellation details: {exc})"
        hint = ""
        if "401" in detail or "Forbidden" in detail or "authentication" in detail.lower():
            hint = f"\nHint: run  az login --tenant {cfg.get('AZURE_SPEECH_TENANT_ID', '<tenant>')}"
        sys.exit(f"Failed: {result.reason} {detail}{hint}")


if __name__ == "__main__":
    main()
