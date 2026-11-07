"""Build a self-contained, file:// compatible viewer; PNGs stay in the layer pack."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "storyboard/vrstvy"


def build():
    data = json.loads((PACK / "manifest.json").read_text(encoding="utf-8-sig"))
    for shot in data["shots"]:
        files = [shot["source"], *(layer["file"] for layer in shot["layers"])]
        for file in files:
            if not (PACK / file).is_file():
                raise FileNotFoundError(f'{shot["id"]}: {file}')
    src = Path(__file__).with_name("layer_preview.html").read_text(encoding="utf-8")
    encoded = json.dumps(data, ensure_ascii=False).replace("<", r"\u003c")
    (PACK / "index.html").write_text(src.replace("__MANIFEST__", encoded), encoding="utf-8")


if __name__ == "__main__":
    build()
