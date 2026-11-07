"""Audit delivery files with FFprobe, OpenCV and Pillow. Run from any directory."""
from pathlib import Path
import json
import re
import subprocess

import cv2
import numpy as np
from PIL import Image


OUT = Path(__file__).resolve().parents[1] / "out"
TARGET = "https://board-game-prototypes.netlify.app/mighty-decks"


def verify_video(locale):
    path = OUT / f"Fangs-{locale}.mp4"
    streams = json.loads(subprocess.check_output([
        "ffprobe", "-v", "error", "-count_frames", "-show_streams",
        "-print_format", "json", str(path),
    ]))["streams"]
    video, = (s for s in streams if s["codec_type"] == "video")
    audio, = (s for s in streams if s["codec_type"] == "audio")
    assert (video["width"], video["height"], video["avg_frame_rate"],
            int(video["nb_read_frames"]), float(video["duration"])) == (
                1920, 1080, "30/1", 1500, 50.0), video
    assert abs(float(audio["duration"]) - 50) < 0.05, audio
    cues = (OUT / f"Fangs-{locale}.srt").read_text(encoding="utf-8-sig")
    assert len(re.findall(r" --> ", cues)) == 11
    assert ("Beru zranění." if locale == "CS" else "We take the injury.") in cues
    detector = cv2.QRCodeDetector()
    cap = cv2.VideoCapture(str(path))
    for frame in (1350, 1425, 1499):
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame)
        ok, image = cap.read()
        assert ok, (path, frame)
        small = np.asarray(Image.fromarray(image).resize((390, 219), Image.Resampling.LANCZOS))
        for sample in (image, small):
            value, _, _ = detector.detectAndDecode(sample)
            assert value == TARGET, (path, frame, sample.shape[1], value)
            print(f"{locale} f{frame} {sample.shape[1]}px QR OK")
    cap.release()
    print(f"{locale} 1920x1080, 30 fps, 1500 frames, 50 s, {audio['codec_name']}, 11 cues")


if __name__ == "__main__":
    for language in ("CS", "EN"):
        verify_video(language)
