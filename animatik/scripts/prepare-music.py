"""Build 50-second music stems and mux them with the existing locked picture."""
import argparse
import json
from pathlib import Path
import subprocess

import numpy as np
from scipy.io import wavfile

ROOT = Path(__file__).resolve().parents[1]
AUDIO = ROOT / 'public/audio'
OUT = ROOT / 'out'
RATE = 24000
SPF = RATE // 30
TRACKS = {
    'lift': ('The Lift', 69, 'USUAN1500066'),
    'constancy': ('Constancy Part One', 14, 'USUAN1100775'),
    'getaway': ('Mistake the Getaway', 0, 'USUAN1100699'),
}


def read(path):
    sr, data = wavfile.read(path)
    assert sr == RATE and data.dtype == np.int16 and data.ndim == 1, path
    return data.astype(float) / 32768


def rms(samples):
    return np.sqrt(np.mean(samples ** 2))


def render(key, title, offset, isrc, sources, locale, cues):
    audio = subprocess.check_output([
        'ffmpeg', '-v', 'error', '-ss', str(offset), '-i', str(sources / (title + '.mp3')),
        '-t', '50', '-af', 'equalizer=f=2000:t=o:w=1.6:g=-3', '-ar', str(RATE),
        '-ac', '1', '-f', 'f32le', '-'])
    music = np.frombuffer(audio, '<f4').astype(float)
    assert len(music) == RATE * 50
    t = np.arange(len(music)) / RATE
    # Lift on the hangar cut and engine burn. Leave the latch and kit breathing exposed.
    level = np.interp(t, [0,.5,12,14,21,22,30,31,33,35.5,36,40.7,41.3,44.7,45.2,48,49.6],
                      [-90,-25,-25,-20,-20,-25,-25,-22,-19,-19,-43,-43,-24,-24,-31,-31,-90])
    music *= 10 ** (level / 20) / rms(music)
    duck = np.zeros(len(t))
    mix = sum(read(AUDIO / name) for name in ['room.wav','pulse.wav',f'final-foley-{locale}.wav'])
    margins = []
    for cue in cues:
        voice = read(AUDIO / cue['file'])
        a = cue['startFrame'] * SPF
        b = a + len(voice)
        mix[a:b] += voice
        # The crate impact under the injury line already takes up much of the mix.
        margin = 32 if 860 <= cue['startFrame'] <= 880 else 16
        drop = min(-6, 20*np.log10(rms(voice)/rms(music[a:b])) - margin)
        duck = np.minimum(duck, np.interp(t, [t[a]-.18,t[a],t[b],t[b]+.5], [0,drop,drop,0]))
    music *= 10 ** (duck / 20)
    for cue in cues:
        voice = read(AUDIO / cue['file'])
        a = cue['startFrame'] * SPF
        margins.append(20*np.log10(rms(voice)/rms(music[a:a+len(voice)])))
    assert min(margins) >= 15.99
    stem = AUDIO / 'music' / f'{key}-{locale}.wav'
    wavfile.write(stem, RATE, np.rint(music * 32767).astype('<i2'))
    mix += read(stem)
    assert np.max(np.abs(mix)) < .98
    base = OUT / f'Fangs-{locale.upper()}.mp4'
    dest = OUT / f'Fangs-{locale.upper()}-{key}.mp4'
    credit = (f'{title} by Kevin MacLeod, https://incompetech.com/music/royalty-free/'
              f'index.html?isrc={isrc} | CC BY 4.0 https://creativecommons.org/licenses/by/4.0/ '
              '| Excerpt, EQ, fades and dialogue ducking.')
    subprocess.run(['ffmpeg','-v','error','-y','-i',str(base),'-f','f32le','-ar',str(RATE),
                    '-ac','1','-i','pipe:0','-map','0:v:0','-map','1:a:0','-c:v','copy',
                    '-c:a','aac','-b:a','144k','-metadata','comment='+credit,'-movflags','+faststart',
                    str(dest)],input=mix.astype('<f4').tobytes(),check=True)
    if key == 'lift':
        dest.replace(base)
        wavfile.write(base.with_name(base.stem+'-mix.wav'),RATE,np.rint(mix*32767).astype('<i2'))
    print(locale, key, 'minimum dialogue/music RMS difference', round(min(margins),1),'dB')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('sources', type=Path, help='Folder containing the three original MP3s')
    args = parser.parse_args()
    dialogue = json.loads((ROOT/'src/dialogue.json').read_text(encoding='utf8'))
    for key, (title, offset, isrc) in TRACKS.items():
        for locale,cues in dialogue.items():
            render(key,title,offset,isrc,args.sources,locale,cues)
