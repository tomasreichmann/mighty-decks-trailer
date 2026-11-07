"""Publish verified masters on the existing loopback pilot server."""
from pathlib import Path
import shutil

root = Path(__file__).resolve().parents[1]
for language in ("CS", "EN"):
    for ext in ("mp4", "srt"):
        src = root / "out" / f"Fangs-{language}.{ext}"
        dest = root / "pilot" / "files" / src.name
        temp = dest.with_suffix(dest.suffix + ".next")
        shutil.copyfile(src, temp)
        temp.replace(dest)
        print(f"http://127.0.0.1:3118/files/{dest.name}")
