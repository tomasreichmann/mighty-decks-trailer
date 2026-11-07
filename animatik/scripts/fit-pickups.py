"""Prepare frame-fitted audition takes without replacing the approved mix."""
from pathlib import Path
import json
import subprocess
import sys

import numpy as np
from scipy.io import wavfile

ROOT = Path(__file__).resolve().parents[1]
RATE = 24000
data = json.loads((ROOT / "src/dialogue.json").read_text(encoding="utf8"))
for name in sys.argv[1:]:
    loc, index = name.split('-')[-2:]
    cue = data[loc][int(index)-1]
    src = ROOT / f'pilot/sound-pickups/{name}.wav'
    samples = np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(src),
           '-ar','24000','-ac','1','-f','f32le','-']),dtype='<f4')
    if name == 'cs-10':
        # The native read pauses a full second after “Teď”. Preserve a beat
        # but fit the command before the jet without speeding up its syllables.
        samples = np.concatenate([samples[:round(.45*RATE)],samples[round(1.10*RATE):]])
    step = 120
    rms = np.sqrt(np.mean(samples[:len(samples)//step*step].reshape(-1,step)**2,axis=1))
    active = np.flatnonzero(rms > max(.0012,rms.max()*.012))
    samples = samples[max(0,(active[0]-1)*step):(active[-1]+3)*step]
    wanted = 800*(cue['endFrame']-cue['startFrame'])-100
    ratio = len(samples)/wanted
    print(name, "natural s",round(len(samples)/RATE,3),"tempo factor",round(ratio,3))
    chain = [f'atempo={ratio:.8f}']
    if loc == 'cs':
        chain += ['highpass=f=370','lowpass=f=3100'] if index == '01' else ['highpass=f=75']
    out = np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-f','f32le','-ar','24000',
              '-ac','1','-i','-','-af',','.join(chain),'-f','f32le','-'],input=samples.tobytes()),dtype='<f4').copy()
    # Correct sub-frame overlap-add rounding without changing intelligible timing.
    from scipy.signal import resample
    out = resample(out,wanted)
    out *= min(.105/np.sqrt(np.mean(out**2)),.73/np.abs(out).max())
    out[:60] *= np.linspace(0,1,60)
    out[-120:] *= np.linspace(1,0,120)
    wavfile.write(src.with_stem(src.stem+'-fit'),RATE,np.round(out*32767).astype('<i2'))
