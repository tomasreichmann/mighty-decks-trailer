"""Make working voice takes and frame-aligned captions from the recording sheet.

Use the installed Supertonic 3 Python environment. Only regeneration needs the
model, numpy, soundfile, and ffmpeg. Playback uses the shipped PCM files.
"""
import json
import math
import re
import subprocess
from pathlib import Path

import numpy as np
import soundfile as sf
from supertonic import TTS


PROJECT = Path(__file__).resolve().parents[1]
SHEET = PROJECT.parent / "storyboard" / "zvuk-a-hlasy.md"
AUDIO = PROJECT / "public" / "audio"
FPS = 30
RATE = 24000
ROLES = {
    "Pašerák": "M2", "Smuggler": "M2",
    "Vyhnankyně": "F1", "Exile": "F1", "Hráčka": "F1", "Player": "F1",
    "Vypravěč": "M4", "Storyteller": "M4",
}


def read_sheet():
    cues = {"cs": [], "en": []}
    locale = None
    for line in SHEET.read_text(encoding="utf-8").splitlines():
        if line.startswith("## CS"):
            locale = "cs"
        elif line.startswith("## EN"):
            locale = "en"
        match = re.match(r"^\| (\d+)–(\d+) \| ([^|]+?) \| ([^|]+?) \|", line)
        if match and locale:
            start, end, speaker, text = match.groups()
            assert speaker in ROLES
            cues[locale].append((int(start), int(end), speaker, text))
    assert all(len(items) == 11 for items in cues.values())
    return cues


def postprocess(wav, sample_rate, budget_seconds, treatment):
    # Remove edge padding while retaining 5ms of onset and 15ms of release.
    # Measure 5ms blocks to avoid keying the subtitles to isolated clicks.
    step = sample_rate // 200
    energy = np.sqrt(np.mean(np.square(wav[:len(wav) // step * step].reshape(-1, step)), axis=1))
    active = np.flatnonzero(energy > max(0.0012, energy.max() * 0.012))
    wav = wav[max(0, (active[0] - 1) * step):(active[-1] + 4) * step]
    filters = []
    if treatment == "radio":
        filters += ["highpass=f=370", "lowpass=f=3100"]
    elif treatment == "ship":
        filters += ["highpass=f=105", "lowpass=f=7600"]
    else:
        filters += ["highpass=f=75"]
    natural_seconds = len(wav) / sample_rate
    if natural_seconds > budget_seconds - 0.02:
        # Pitch-preserving trim to the agreed window without cutting a syllable.
        filters.append(f"atempo={natural_seconds / (budget_seconds - 0.02):.6f}")
    command = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-f", "f32le", "-ar",
               str(sample_rate), "-ac", "1", "-i", "pipe:0", "-af", ",".join(filters),
               "-ar", str(RATE), "-f", "f32le", "pipe:1"]
    raw = subprocess.run(command, input=wav.astype("<f4").tobytes(),
                         capture_output=True, check=True).stdout
    processed = np.frombuffer(raw, dtype="<f4").copy()
    limit = round(budget_seconds * RATE)
    if len(processed) > limit + RATE * 0.03:
        raise ValueError("Time fitting exceeded its padding")
    processed = processed[:limit]
    # Match short-term speech levels, keep sharp consonants below the mix ceiling.
    rms = np.sqrt(np.mean(processed ** 2))
    processed *= min(0.105 / rms, 0.73 / np.abs(processed).max())
    fade = RATE // 250
    processed[:fade] *= np.linspace(0, 1, fade)
    processed[-fade:] *= np.linspace(1, 0, fade)
    return processed, natural_seconds


def srt_time(frame):
    millis = round(frame * 1000 / FPS)
    seconds, ms = divmod(millis, 1000)
    minutes, sec = divmod(seconds, 60)
    return f"{minutes//60:02d}:{minutes%60:02d}:{sec:02d},{ms:03d}"


def main():
    AUDIO.mkdir(parents=True, exist_ok=True)
    (PROJECT / "out").mkdir(exist_ok=True)
    model = TTS(model="supertonic-3", auto_download=False, intra_op_num_threads=4, inter_op_num_threads=1)
    styles = {voice: model.get_voice_style(voice_name=voice) for voice in set(ROLES.values())}
    data = {}
    for locale, cues in read_sheet().items():
        data[locale] = []
        subtitles = []
        for index, (start, limit, speaker, text) in enumerate(cues, 1):
            np.random.seed(700 + index)
            filename = f"{locale}-{index:02d}.wav"
            performance = AUDIO / "performance" / filename
            if performance.is_file():
                audio, rate = sf.read(performance)
                assert rate == RATE and audio.ndim == 1, performance
                natural = len(audio) / rate
                filename = performance.relative_to(AUDIO).as_posix()
            else:
                wav, _ = model.synthesize(text, voice_style=styles[ROLES[speaker]], lang=locale,
                                          total_steps=16, speed=1.08)
                treatment = "radio" if index == 1 else "ship" if index <= 5 else "room"
                audio, natural = postprocess(np.asarray(wav).squeeze(), model.sample_rate,
                                             (limit - start) / FPS, treatment)
            end = start + math.ceil(len(audio) * FPS / RATE)
            assert start < end <= limit
            if not performance.is_file():
                sf.write(AUDIO / filename, audio, RATE, subtype="PCM_16")
            data[locale].append(dict(text=text, startFrame=start, endFrame=end,
                                     startMs=round(start * 1000 / FPS), endMs=round(end * 1000 / FPS),
                                     timestampMs=None, confidence=None, speaker=speaker, file=filename))
            subtitles.append(f"{index}\n{srt_time(start)} --> {srt_time(end)}\n{text}\n")
            print(f"{locale} {index:02d}: {natural:.2f}s -> {start}-{end} {speaker}", flush=True)
        (PROJECT / "out" / f"Fangs-{locale.upper()}.srt").write_text("\n".join(subtitles), encoding="utf-8")
    (PROJECT / "src" / "dialogue.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n",
                                                   encoding="utf-8")


if __name__ == "__main__":
    main()
