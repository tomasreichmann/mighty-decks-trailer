"""Recover the three approved face placements from the overhead storyboard insert."""
from pathlib import Path

import numpy as np
from PIL import Image

PROJECT = Path(__file__).resolve().parents[1]
BOARD = PROJECT / "storyboard"
SLOTS = [(712, 1083, "U2"), (1083, 1449, "C2"), (1449, 1822, "S1")]


def main():
    with Image.open(PROJECT / "reference/planches/over-shoulder.png") as plate:
        base = np.array(plate.convert("RGB"))
    for lang in ("cs", "en"):
        folder = BOARD / "overlays" / lang
        folder.mkdir(parents=True, exist_ok=True)
        with Image.open(BOARD / "screens" / lang / "04b-volba.png") as reference:
            target = np.array(reference.convert("RGB"))
        result = Image.fromarray(base)
        for x0, x1, card in SLOTS:
            y0, y1 = 437, 1014
            patch = target[y0:y1, x0:x1]
            changed = np.any(base[y0:y1, x0:x1] != patch, axis=2)
            face = Image.fromarray(patch).convert("RGBA")
            face.putalpha(Image.fromarray(np.uint8(changed)*255))
            full = Image.new("RGBA", result.size)
            full.paste(face, (x0,y0))
            full.save(folder / f"overhead-{card}.png")
            result.paste(full, mask=full.getchannel("A"))
        assert np.array_equal(np.asarray(result)[437:1014,712:1822],
                              target[437:1014,712:1822]), lang


if __name__ == "__main__":
    main()
