"""Fit the selected hybrid reading and measured pickups to both 50 s mixes."""
import json
import math
from pathlib import Path
import subprocess
from shutil import copyfile

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt

ROOT = Path(__file__).resolve().parents[1]
AUDIO = ROOT / 'public' / 'audio'
RATE, SPF = 24000, 800


def decode(path):
    if path.suffix == '.wav':
        rate, samples = wavfile.read(path)
        if rate == RATE and samples.ndim == 1 and samples.dtype == np.int16:
            return samples.astype(np.float32) / 32768
    out = subprocess.check_output(['ffmpeg', '-v', 'error', '-i', str(path), '-map', '0:a:0',
                                   '-ar', str(RATE), '-ac', '1', '-f', 'f32le', '-'])
    return np.frombuffer(out, dtype='<f4')


def save(path, samples):
    assert np.max(np.abs(samples)) < 1, (path, np.max(np.abs(samples)))
    wavfile.write(path, RATE, np.round(samples * 32767).astype('<i2'))


def stamp(ms):
    sec, ms = divmod(ms, 1000)
    minute, sec = divmod(sec, 60)
    return f'{minute//60:02d}:{minute%60:02d}:{sec:02d},{ms:03d}'


def set_take(cue, name, frame, samples):
    end = frame + math.ceil(len(samples) / SPF)
    cue.update(file=name, startFrame=frame, endFrame=end, startMs=round(frame*1000/30),
               endMs=round(end*1000/30))


def cloth_and_boots():
    """Separate the sleeve tear and receding boot soles from the impact."""
    effects = np.zeros(50 * RATE)
    rng = np.random.default_rng(534)
    def noise(t, low, high):
        sos = butter(3, (low,high), btype='bandpass', fs=RATE, output='sos')
        n = sosfilt(sos,rng.normal(size=len(t)))
        return n / np.max(np.abs(n))
    def add(frame, sound):
        begin = frame * SPF
        effects[begin:begin+len(sound)] += sound
    # The claw catches thread after the stock's dry contact. Uneven little
    # fibre ruptures accelerate and then decelerate as the weave gives.
    t = np.arange(round(.44 * RATE)) / RATE
    fibres = np.maximum(0, np.sin(2*np.pi*(24*t+36*t*t))) ** 3
    tear = (.20+.80*fibres)*noise(t,860,3950)
    add(538,.37*tear*np.sin(np.pi*t/.44)**.75)
    # Two different sole strikes, with a scuff trailing the toe. Each later
    # strike loses level and upper frequencies as it recedes behind the hatch.
    for i,(frame,level) in enumerate([(561,.30),(574,.28),(587,.26),(600,.25),
                                      (609,.23),(619,.20),(630,.16)]):
        t = np.arange(round(.18*RATE)) / RATE
        sole = np.sin(2*np.pi*((340-12*i)*t+7*(1-np.exp(-17*t))))*np.exp(-t/.032)
        sole += .55*noise(t,420,2700-120*i)*np.exp(-t/.025)
        toe = noise(t,620,2400-100*i)*np.exp(-np.maximum(t-.065,0)/.031)*np.clip((t-.047)/.018,0,1)
        add(frame,level * (sole+.54*toe) * np.minimum(1,t/.002))
    return effects


def main():
    data_path = ROOT / 'src/dialogue.json'
    data = json.loads(data_path.read_text(encoding='utf8'))
    quiet = decode(ROOT / 'pilot/files/quiet-native.mp4')
    hybrid = decode(ROOT / 'pilot/files/hybrid-sam.mp4')
    for idx, (a,b) in enumerate([(8,66), (74,109), (117,144)], 7):
        name = f'performance/cs-{idx:02d}.wav'
        take = quiet[a*SPF:b*SPF].copy()
        take[:48] *= np.linspace(0,1,48)
        take[-48:] *= np.linspace(1,0,48)
        save(AUDIO/name, take)
        set_take(data['cs'][idx-1], name, 750+a, take)
    # The English dub starts with the illustrated mouth opening; “injury”
    # continues over the cut to the smuggler's arm at frame 882.
    for idx, start in [(7,758),(8,824),(9,873)]:
        name = f'performance/en-{idx:02d}.wav'
        copyfile(ROOT / f'pilot/sound-pickups/en-{idx:02d}-fit.wav', AUDIO/name)
        set_take(data['en'][idx-1],name,start,decode(AUDIO/name))

    # Difference of the accepted pilot and its source voice recovers the
    # selected recorded crate without adding the Czech line to English.
    impact = hybrid[119*SPF:132*SPF] - quiet[119*SPF:132*SPF]
    retreat = cloth_and_boots()
    for loc in data:
        foley = decode(AUDIO/f'foley-{loc}.wav') + retreat
        foley[869*SPF:882*SPF] *= .17
        foley[869*SPF:882*SPF] += impact
        save(AUDIO/f'final-foley-{loc}.wav',foley)
        mix = foley + decode(AUDIO/'room.wav') + decode(AUDIO/'pulse.wav')
        if loc == 'cs':
            set_take(data[loc][9], 'cs-10.wav', 930, decode(AUDIO/'cs-10.wav'))
            for idx,start,selected in [(1,56,'pocket-cs-01'),(11,1370,'cs-11')]:
                name = f'performance/cs-{idx:02d}.wav'
                copyfile(ROOT/f'pilot/sound-pickups/{selected}-fit.wav', AUDIO/name)
                set_take(data[loc][idx-1],name,start,decode(AUDIO/name))
        subtitles = []
        for idx,cue in enumerate(data[loc],1):
            begin = cue['startFrame'] * SPF
            take = decode(AUDIO / cue['file'])
            mix[begin:begin+len(take)] += take
            subtitles.append(f"{idx}\n{stamp(cue['startMs'])} --> {stamp(cue['endMs'])}\n{cue['text']}\n")
        (ROOT/'out'/f'Fangs-{loc.upper()}.srt').write_text('\n'.join(subtitles),encoding='utf8')
        mix += decode(AUDIO/'music'/f'lift-{loc}.wav')
        save(ROOT/'out'/f'Fangs-{loc.upper()}-mix.wav',mix)
        print(loc, 'peak dBFS', round(20*np.log10(np.max(np.abs(mix))),2),
              [(q['startFrame'],q['endFrame']) for q in data[loc]])
    data_path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf8')


if __name__ == '__main__':
    main()
