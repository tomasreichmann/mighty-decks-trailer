"""Build the 390–659 encounter from native H3 animal takes and contact foley.

The silent tail gives the 635 shutter to the existing foley. Mix the resulting
48 kHz mono WAV at unity, aligned at 390. The former stock/tear can be faded
locally on its own bus. Its linear-gain points (absolute frame, gain) are
(531, 1), (533, .19), (537.5, .19), (541, .44), (545, 1).
"""
from pathlib import Path
import subprocess

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt


RATE = 48_000
FPS = 30
FIRST = 390
PROJECT = Path(__file__).resolve().parents[1]
DEST = PROJECT / "public" / "audio" / "hangar-impact.wav"
NATIVE = PROJECT / "pilot" / "foley-hangar"
RNG = np.random.default_rng(534)


def times(seconds):
    return np.arange(round(RATE * seconds)) / RATE


def band_noise(t, low, high):
    filt = butter(3, [low, high], btype="bandpass", fs=RATE, output="sos")
    signal = sosfilt(filt, RNG.standard_normal(t.size))
    return signal / np.sqrt(np.mean(signal ** 2))


def peak(signal, amplitude):
    return signal * (amplitude / np.max(np.abs(signal)))


def put(track, frame, sound, delay=0.0):
    start = round(((frame - FIRST) / FPS + delay) * RATE)
    assert 0 <= start < start + len(sound) <= len(track)
    track[start:start+len(sound)] += sound


def edges(t, enter, leave):
    return np.clip(t / enter, 0, 1) * np.clip((t[-1] - t) / leave, 0, 1)


def recording(path):
    cmd = ["ffmpeg","-v","error","-i",str(path),"-ar",str(RATE),"-ac","1","-f","f32le","-"]
    data = np.frombuffer(subprocess.check_output(cmd), dtype="<f4").astype(float)
    return sosfilt(butter(2, 46, btype="highpass", fs=RATE, output="sos"), data)


def take(source, start, stop, attack=.012, release=.055):
    clip = source[round(start*RATE):round(stop*RATE)].copy()
    return clip * edges(np.arange(clip.size)/RATE, attack, release)


def animal_performance(track):
    charge = recording(NATIVE / "charge.flac")
    throat = recording(NATIVE / "throat.flac")

    # The steel hatch carries both of this take's short chest calls. Preserve
    # a little upper grunt so the J-cut remains audible on a phone speaker.
    warning = take(throat,3.13,4.30,attack=.045,release=.12)
    door = sosfilt(butter(2, 485, fs=RATE, output="sos"), warning)
    door += .18 * sosfilt(butter(2,[600,1190],btype="bandpass",fs=RATE,output="sos"), warning)
    put(track,390,peak(door,.30))

    # The second performance has an audible inhale between its two roars.
    # Its short first phrase crosses the opening cut. The next, full growl
    # arrives with the lunge. Air reflections disappear at the weapon.
    voice = take(charge,.26,2.46,attack=.025,release=.20)
    t = np.arange(voice.size)/RATE
    frame = 417 + t*FPS
    close = np.interp(frame,[417,420,426,437,456,460,464,474,483],
                      [.22,.62,.87,.96,1,.70,.88,.82,.38])
    dry = peak(voice,.78)
    put(track,417,dry*close)
    wall = sosfilt(butter(2,2300,fs=RATE,output="sos"), dry)
    wall *= np.interp(frame,[417,422,438,458,483],[.06,.20,.17,.036,.02])
    put(track,417,wall,delay=.082)
    put(track,417,wall*.43,delay=.157)

    # The original takes have two different residual vocal gestures; keep a
    # last close snort in the bite and a longer answering roar after the cut.
    snort = take(throat,3.22,3.68,attack=.005,release=.09)
    put(track,478,peak(snort,.39))
    rasp = take(charge,.13,.40,attack=.040,release=.06)
    put(track,522,peak(rasp,.025))
    answer = take(throat,3.72,4.31,attack=.012,release=.09)
    put(track,550,peak(answer,.47))


def heavy_landing():
    # A short, low-passed part of the recorded H3 wood/steel shock conveys the
    # weight borne by the stock. The little resonant receiver sits above it.
    impact = recording(PROJECT / "pilot" / "media" / "h3-impact.wav")
    timber = take(impact,.962,1.156,attack=.001,release=.075)
    timber = sosfilt(butter(3,540,fs=RATE,output="sos"), timber)
    out = peak(stock_contact(),.30)
    out[:timber.size] += peak(timber,.29)
    return out


def stock_contact():
    """Short damped, irregular bending modes of the wood and receiver."""
    t = times(.26)
    body = np.zeros_like(t)
    for hz, decay, weight in [(196, .060, .61), (337, .041, .53), (488, .026, .31),
                              (710, .016, .20), (1138, .009, .18), (2161, .005, .13)]:
        body += weight * np.sin(2*np.pi*hz*t) * np.exp(-t/decay)
    body += .12 * band_noise(t, 900, 3950) * np.exp(-t/.006)
    return body * edges(t, .0022, .035)


def grain(seconds, low, high, rise, fall):
    t = times(seconds)
    return band_noise(t, low, high) * edges(t, rise, .008) * np.exp(-t/fall)


def ripping_canvas():
    # Catch, tension, then closely spaced bundles failing at different sizes.
    # The first fibre sits under the line. The longest pull clears its last vowel.
    t = times(.53)
    rub = band_noise(t, 690, 3680)
    release = np.interp(t,[0,.040,.075,.125,.200,.28,.38,.51],[0,.16,.24,.10,.65,1,.60,0])
    weight = .78 + .22 * np.sin(2*np.pi*(23*t + 27*t*t))
    result = .14 * rub * release * weight
    cursor = .005
    while cursor < .435:
        sec = RNG.uniform(.009,.028)
        burst = grain(sec, RNG.uniform(900,1400), RNG.uniform(3500,6400), .0016, sec*.33)
        amplitude = .09 + .62*np.interp(cursor,t,release)
        index = round(cursor*RATE)
        result[index:index+len(burst)] += amplitude * burst
        cursor += RNG.uniform(.009,.030)
    return result * edges(t,.001,.024)


def main():
    track = np.zeros(9 * RATE)
    animal_performance(track)
    # The open room lasts 40 frames before the body drives into the carbine.
    for frame, level in [(427,.095),(438,.145),(450,.19)]:
        foot = peak(stock_contact(),level)
        put(track,frame,sosfilt(butter(2,750,fs=RATE,output="sos"),foot))
        put(track,frame,peak(grain(.094,570,2760,.004,.027),level*.37),delay=.023)
    put(track,460,heavy_landing())
    put(track,462,peak(grain(.175,780,2460,.015,.065),.17))
    put(track,468,peak(grain(.13,940,2820,.010,.048),.092))
    # A single fast intake precedes the command; leave the syllables clear.
    put(track, 489, peak(grain(.30, 320, 1970, .09, .15), .126))
    t = times(.117)
    swipe = band_noise(t, 620, 1920) * np.sin(np.pi*t/t[-1]) ** 2
    put(track, 534, peak(swipe, .068), delay=-.117)
    put(track, 534, peak(stock_contact(), .132))
    put(track, 534, peak(grain(.065, 1170, 3040, .0017, .011), .040), delay=.016)
    tear = peak(ripping_canvas(), .305)
    tear_time = np.arange(tear.size) / RATE
    # A few strands start breaking on the card resolve. The body of the tear
    # opens only after the end of the Exile's Czech consonants on f542.
    tear *= np.interp(tear_time,[0,4/FPS,7/FPS,9/FPS],[.42,.46,.75,1])
    put(track, 536, tear)
    put(track, 553, peak(grain(.305, 330, 1940, .062, .122), .103))
    # Wet boot skid and crate straps continue below the original marked footfalls.
    put(track, 567, peak(grain(.15, 180, 1500, .018, .06), .080))
    put(track, 608, peak(grain(.24, 210, 1720, .035, .077), .082))
    put(track, 622, peak(grain(.165, 640, 2310, .033, .054), .063))
    assert np.isfinite(track).all() and np.max(np.abs(track)) < .98
    DEST.parent.mkdir(parents=True, exist_ok=True)
    wavfile.write(DEST, RATE, np.round(track*32767).astype("<i2"))


if __name__ == "__main__":
    main()
