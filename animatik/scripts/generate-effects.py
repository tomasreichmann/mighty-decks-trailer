"""Working room, pulse and foley stems. Python 3, numpy and scipy."""
from pathlib import Path

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, chirp, resample_poly, sosfilt


RATE = 24000
FPS = 30
DEST = Path(__file__).resolve().parents[1] / "public" / "audio"
RNG = np.random.default_rng(516)


def silence():
    return np.zeros(50 * RATE)


def axis(seconds):
    return np.arange(round(seconds * RATE)) / RATE


def add(stem, frame, signal):
    start = round(frame * RATE / FPS)
    size = min(len(stem) - start, len(signal))
    stem[start:start + size] += signal[:size]


def bandnoise(t, low, high):
    filt = butter(2, [low, high], btype="bandpass", fs=RATE, output="sos")
    noise = sosfilt(filt, RNG.standard_normal(len(t)))
    return noise / max(1e-6, np.max(np.abs(noise)))


def envelope(t, attack, release):
    return np.minimum(t / attack, 1) * np.exp(-t / release)


def clang(stem, frame, freq, sec, level):
    # Several inharmonic decays leave a pitched metallic tail behind the knock.
    t = axis(sec)
    clangs = sum(weight * np.sin(2 * np.pi * freq * ratio * t)
                 * np.exp(-t / (sec * decay)) for ratio, weight, decay in
                 [(1, .50, .27), (1.48, .27, .16), (2.71, .15, .12), (4.1, .09, .07)])
    attack = .3 * bandnoise(t, 340, 5500) * np.exp(-t / .012)
    add(stem, frame, level * (clangs + attack) * np.minimum(t / .002, 1))


def rub(stem, frame, sec, low, high, level, attack=.009):
    t = axis(sec)
    add(stem, frame, level * bandnoise(t, low, high) * envelope(t, attack, sec / 4))


def room_and_pulse():
    room = silence()
    pulse = silence()
    for first, last, freq, level in [(0, 420, 56, .021), (420, 750, 73, .025),
                                     (750, 870, 110, .004), (870, 1080, 56, .023),
                                     (1080, 1230, 88, .007), (1350, 1500, 110, .004)]:
        t = axis((last - first) / FPS)
        edges = np.minimum(t / .1, 1) * np.minimum((len(t) / RATE - t) / .1, 1)
        air = bandnoise(t, 95, 1400) + .24 * np.sin(2 * np.pi * freq * t)
        add(room, first, level * air * edges)
    for frame in range(193, 660, 25):
        t = axis(.56)
        accent = .040 if frame % 50 == 43 else .028
        if frame < 270 or 500 <= frame <= 556:
            accent *= .55
        add(pulse, frame, accent * np.sin(2 * np.pi * (70 * t + .9 * (1 - np.exp(-t*16))))
            * envelope(t, .018, .11))
    return room, pulse


def effects():
    fx = silence()
    # The third radio burst opens into speech. Paper slides have little low end.
    for frame, level in [(12, .15), (32, .19), (55, .21), (165, .09)]:
        rub(fx, frame, .15, 1300, 8100, level)
    for frame in [270, 390, 480, 624, 840, 920, 944, 1044, 1266, 1270, 1276]:
        rub(fx, frame, .15, 1300, 6600, .105, .019)
    for frame, freq in [(330, 930), (334, 1370)]:
        clang(fx, frame, freq, .13, .16)
    for frame, freq, sec, level in [(363, 440, .12, .22), (378, 78, .44, .26),
                                   (420, 124, .62, .14), (534, 116, .29, .33),
                                   (635, 94, .52, .27), (660, 358, .52, .40),
                                   (684, 158, .69, .26), (870, 79, .48, .45),
                                   (984, 463, .13, .18), (1092, 604, .17, .24),
                                   (1170, 1720, .44, .19)]:
        clang(fx, frame, freq, sec, level)
    rub(fx, 376, .86, 95, 2100, .18, .15)   # sliding hatch
    rub(fx, 534, .23, 1600, 7200, .31)       # sleeve against the claw
    for frame in (568, 578, 593, 609, 621):
        clang(fx, frame, 72, .17, .12)
    rub(fx, 635, .58, 245, 2600, .17, .05)   # shutter
    rub(fx, 660, .61, 540, 4900, .23, .016)
    rub(fx, 870, .12, 1600, 7800, .20)       # physical card against wood
    rub(fx, 900, .30, 810, 4200, .20, .02)   # slide across torn edge
    rub(fx, 918, .36, 270, 1450, .15, .05)
    for frame in (1180, 1206):                 # kit breath by the buckle
        rub(fx, frame, .48, 310, 1540, .095, .09)
    return fx


def save(name, track):
    assert np.max(np.abs(track)) < .98 and np.isfinite(track).all()
    wavfile.write(DEST / f"{name}.wav", RATE, np.round(track * 32767).astype("<i2"))


def main():
    DEST.mkdir(parents=True, exist_ok=True)
    room, pulse = room_and_pulse()
    save("room", room)
    save("pulse", pulse)
    common = effects()
    # Make room for the spoken coordinates and replace the original broad
    # scratch with the timed stock contact, cloth rip and animal performance.
    frames = np.arange(len(common)) * FPS / RATE
    common *= np.interp(frames, [329, 330, 337, 339, 531, 533, 537.5, 541, 545],
                        [1, .58, .58, 1, 1, .19, .19, .44, 1])
    rate, fight = wavfile.read(DEST / "hangar-impact.wav")
    assert rate == 48000 and fight.shape == (9 * rate,) and fight.dtype == np.int16
    add(common, 390, resample_poly(fight.astype(float) / 32768, 1, 2))
    t = axis(2.38)
    jet = (.33 * bandnoise(t, 120, 2900) + .09 * chirp(t, f0=170, f1=48, t1=t[-1]))
    jet *= np.minimum((t[-1] - t) / .2, 1) * envelope(t, .16, .84)
    for locale in ("cs", "en"):
        fx = common.copy()
        # English keeps its soft ignition on 984 and opens the jet after 990.
        opening = np.interp(t, [0, .20, .35], [.09, .12, 1]) if locale == "en" else 1
        add(fx, 984, jet * opening)
        save(f"foley-{locale}", fx)


if __name__ == "__main__":
    main()
