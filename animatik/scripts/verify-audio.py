"""Check each encoded spoken cue against its master take and measured SRT.

Run after rendering. ffmpeg decodes the finished MP4, including encoder delay.
"""
import json
import re
import subprocess
from pathlib import Path

import numpy as np
from scipy.io import wavfile
from scipy.signal import correlate


ROOT = Path(__file__).resolve().parents[1]
RATE = 24000
SPF = RATE // 30


def read_wav(name):
    rate, data = wavfile.read(ROOT / "public" / "audio" / name)
    assert rate == RATE and data.ndim == 1
    return data.astype(np.float64) / 32768


def millis(stamp):
    h, m, s, ms = map(int, re.split("[:,]", stamp))
    return ((h * 60 + m) * 60 + s) * 1000 + ms


def verify(loc, cues, music="lift"):
    base = ROOT / "out" / f"Fangs-{loc.upper()}"
    subtitle_blocks = base.with_suffix(".srt").read_text(encoding="utf-8-sig").strip().split("\n\n")
    assert len(cues) == len(subtitle_blocks) == 11
    foley = read_wav(f"final-foley-{loc}.wav") + read_wav("room.wav") + read_wav("pulse.wav")
    foley += read_wav(f"music/{music}-{loc}.wav")
    video = base if music == "lift" else base.with_name(base.name + "-" + music)
    result = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", str(video.with_suffix(".mp4")),
                             "-map", "0:a:0", "-ac", "1", "-ar", str(RATE), "-f", "f32le", "-"],
                            capture_output=True, check=True)
    decoded = np.frombuffer(result.stdout, dtype="<f4")
    assert abs(len(decoded) / RATE - 50) < .06
    reference = foley.copy()
    for cue, block in zip(cues, subtitle_blocks):
        _, timing, text = block.split("\n")
        assert list(map(millis, timing.split(" --> "))) == [cue["startMs"], cue["endMs"]]
        assert text == cue["text"]
        start = cue["startFrame"] * SPF
        take = read_wav(cue["file"])
        assert len(take) <= (cue["endFrame"] - cue["startFrame"]) * SPF
        pre = 2 * SPF
        search = decoded[start-pre:start+len(take)+pre]
        offset = np.argmax(correlate(search, take, mode="valid", method="fft"))
        segment = search[offset:offset+len(take)]
        score = np.corrcoef(segment, take)[0, 1]
        lag_ms = (offset-pre) * 1000 / RATE
        assert abs(lag_ms) < 1000 / 30 and score > .85, (loc, cue["file"], lag_ms, score)
        reference[start:start+len(take)] += take
        print(f"{loc} {cue['file']} lag {lag_ms:+.1f} ms, correlation {score:.3f}")
    assert np.max(np.abs(reference)) < .98
    fx_start, fx_end = 1080 * SPF, 1350 * SPF
    # Isolate the voiceless latch, buckle, kit breathing and paper spread.
    section = foley[fx_start:fx_end]
    lag = np.argmax(correlate(decoded[fx_start-pre:fx_end+pre], section, mode="valid", method="fft"))
    fx_score = np.corrcoef(decoded[fx_start-pre+lag:fx_end-pre+lag], section)[0, 1]
    assert fx_score > .85 and abs(lag-pre) < SPF, (loc, "foley", fx_score, lag-pre)
    print(f"{loc} foley correlation {fx_score:.3f}. Reference mix peak {20*np.log10(np.max(np.abs(reference))):.1f} dBFS.")


if __name__ == "__main__":
    for locale, dialogue in json.loads((ROOT / "src" / "dialogue.json").read_text(encoding="utf-8")).items():
        verify(locale, dialogue)
        for variant in ["constancy", "getaway"]:
            if (ROOT / "out" / f"Fangs-{locale.upper()}-{variant}.mp4").exists():
                verify(locale, dialogue, variant)

