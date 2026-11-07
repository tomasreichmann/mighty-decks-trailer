"""Render dialogue cues at original performance speed from lossless H3 takes."""
import json
import math
from pathlib import Path
import re
import subprocess

import numpy as np
from scipy.io.wavfile import write


HERE = Path(__file__).resolve().parent
RATE = 24000


def prepare(cue):
    source = HERE / "source" / (cue["take"] + ".flac")
    source_in, source_out = cue["cut"]
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-i", str(source),
           "-ss", str(source_in), "-t", str(source_out-source_in),
           "-af", "pan=mono|c0=0.5*c0+0.5*c1,highpass=f=58",
           "-ar", str(RATE), "-f", "f32le", "-"]
    samples = np.frombuffer(subprocess.check_output(cmd), dtype="<f4").copy()
    # A two-ms fade at the silences avoids sample discontinuities.
    n = round(.002 * RATE)
    samples[:n] *= np.linspace(0, 1, n)
    samples[-n:] *= np.linspace(1, 0, n)
    levels = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-f", "f32le", "-ar", str(RATE),
         "-ac", "1", "-i", "-", "-af", "loudnorm=print_format=json", "-f", "null", "-"],
        input=samples.tobytes(), capture_output=True, check=True,
    ).stderr.decode(errors="replace")
    measured = json.loads(re.search(r'\{[^{}]*"input_i"[^{}]*\}',levels).group())
    gain = min(cue["targetLufs"] - float(measured["input_i"]), -2 - float(measured["input_tp"]))
    if not math.isfinite(gain):
        raise ValueError(f"Empty clip: {source}")
    samples *= 10 ** (gain / 20)
    end_frame = cue["start"] + math.ceil(len(samples)*30/RATE)
    if end_frame > cue["latestEnd"]:
        raise ValueError(f'{cue["id"]} exceeds frame {cue["latestEnd"]}')
    wav = HERE/(cue["id"]+".wav")
    write(wav, RATE, (np.clip(samples,-1,1)*32767).round().astype("<i2"))
    print(f'{wav.name}: {len(samples)/RATE:.3f}s, [{cue["start"]},{end_frame}), gain {gain:+.1f} dB')


if __name__=="__main__":
    for item in json.loads((HERE/"takes.json").read_text(encoding="utf8")):
        prepare(item)
