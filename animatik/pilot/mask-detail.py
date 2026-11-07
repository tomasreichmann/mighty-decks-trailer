"""Compare two full-resolution Remotion frame sequences of the same spoken line."""
import argparse
from pathlib import Path
import subprocess

from PIL import Image, ImageDraw, ImageFont


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("before", type=Path)
    parser.add_argument("after", type=Path)
    parser.add_argument("--output", type=Path, help="Write the encoded comparison to this MP4")
    args = parser.parse_args()
    sequences = [sorted(path.glob("element-*.png"))[:66] for path in (args.before, args.after)]
    if any(len(seq) != 66 for seq in sequences):
        raise ValueError("Both directories must contain the full 66-frame spoken shot")
    files = Path(__file__).resolve().parent / "files"
    with subprocess.Popen([
        "ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pixel_format", "rgb24",
        "-video_size", "896x556", "-framerate", "30", "-i", "-",
        "-i", str(files / "hybrid-zraneni.mp4"), "-map", "0:v", "-map", "1:a",
        "-t", "2.2", "-c:v", "libx264", "-crf", "15", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-movflags", "+faststart", str(args.output or files / "detail-masky-sam.mp4"),
    ], stdin=subprocess.PIPE) as encoder:
        font = ImageFont.truetype("segoeuib.ttf", 22)
        for pair in zip(*sequences):
            board = Image.new("RGB", (896, 556), "#151c20")
            draw = ImageDraw.Draw(board)
            for col, (frame, label) in enumerate(zip(pair, ("Původní maska", "Segment Anything"))):
                x = 448 * col
                draw.text((x + 15, 6), label, fill="#f2e6d1", font=font)
                with Image.open(frame) as source:
                    if source.size != (1920, 1080):
                        raise ValueError("These registered crops require 1920 × 1080 input frames")
                    board.paste(source.crop((328, 156, 776, 462)), (x, 36))
                    board.paste(source.crop((352, 565, 800, 777)), (x, 344))
            encoder.stdin.write(board.tobytes())
        encoder.stdin.close()
        if encoder.wait():
            raise RuntimeError("Could not encode the mask comparison")


if __name__ == "__main__":
    main()
