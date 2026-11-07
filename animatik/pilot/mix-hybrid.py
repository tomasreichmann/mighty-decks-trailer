"""Mix the six-second cut. The source attack time is measured in the original pickup."""
import argparse
from pathlib import Path
import subprocess

import numpy as np
from scipy.io import wavfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("picture", type=Path)
    parser.add_argument("attack", type=float, help="Time of the first impact in h3-impact.wav, seconds")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    rate, pickup = wavfile.read(root / "media" / "h3-impact.wav")
    if np.issubdtype(pickup.dtype, np.integer):
        pickup = pickup.astype(float) / (float(np.iinfo(pickup.dtype).max) + 1)
    peak = np.max(np.abs(pickup[round(args.attack * rate):round((args.attack + .38) * rate)]))
    # Give the body of the hit headroom under the actress's last sentence.
    impact_gain = -14 - 20 * np.log10(peak)
    start = max(0, args.attack - .025)
    delay = round(1000 * (4 - args.attack + start))
    audio_filter = (
        "[1:a]aresample=48000,afade=t=out:st=4.80:d=0.09[voice];"
        f"[2:a]atrim=start={start}:duration=0.408,asetpts=PTS-STARTPTS,aresample=48000,"
        f"volume={impact_gain:.3f}dB,afade=t=in:d=0.008,afade=t=out:st=0.318:d=0.09,"
        f"adelay={delay}:all=1[hit];"
        "[3:a]atrim=start=29.4:duration=1.6,asetpts=PTS-STARTPTS,aresample=48000,"
        "afade=t=in:d=0.15,adelay=4400:all=1[room];"
        "[voice][hit][room]amix=inputs=3:normalize=0:duration=longest[mix]"
    )
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(args.picture), "-i",
                    str(root / "files" / "quiet-native.mp4"), "-i", str(root / "media" / "h3-impact.wav"),
                    "-i", str(root.parent / "public" / "audio" / "room.wav"),
                    "-filter_complex", audio_filter, "-map", "0:v:0", "-map", "[mix]", "-t", "6",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart",
                    str(root / "files" / "hybrid-zraneni.mp4")], check=True)
    print(f"Impact: source attack {args.attack:.3f}s placed at 4.000s, gain {impact_gain:+.2f} dB.")


if __name__ == "__main__":
    main()
