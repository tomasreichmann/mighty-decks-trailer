"""Alternate English table read with the same F1 player, preserving cut boundaries."""
import importlib.util
from pathlib import Path
import subprocess

import numpy as np
import soundfile as sf
from supertonic import TTS

root = Path(__file__).resolve().parents[1]
dst = root / "pilot/sound-pickups"
dst.mkdir(exist_ok=True)
base = importlib.util.spec_from_file_location("base", root/"scripts/generate-voices.py")
mod = importlib.util.module_from_spec(base)
base.loader.exec_module(mod)
model = TTS(model="supertonic-3",auto_download=False,intra_op_num_threads=3,inter_op_num_threads=1)
voice = model.get_voice_style(voice_name="F1")
for idx, text, frames, speed in [
        (7, "I need my Success to save our ship.",55,1.00),
        (8, "I'll play the Partial.",27,1.00),
        (9, "We take the injury.",29,.97)]:
    np.random.seed(930+idx)
    wav,_ = model.synthesize(text,voice_style=voice,lang="en",total_steps=25,speed=speed)
    take,natural=mod.postprocess(np.asarray(wav).squeeze(),model.sample_rate,frames/30,"room")
    sf.write(dst / f"en-{idx:02d}.wav",take,24000)
    print(idx,len(take)/24000,natural,flush=True)
