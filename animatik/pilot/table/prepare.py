"""Split the three tabletop cards, keep their perspective, and verify both locales."""
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
ROOT = PROJECT.parent
LAYERS = ROOT / "storyboard/vrstvy/table"
OUTPUT = PROJECT / "public/pilot/table"
REG = json.loads((HERE / "registration.json").read_text(encoding="utf-8"))


def box(bounds):
    x, y, width, height = bounds
    return x, y, x + width, y + height


def fill_wood(room, masks):
    # The visible grain runs across the table. Continue each scanline from the
    # unoccluded wood on its two sides, then borrow fine grain from below it.
    pixels = np.asarray(room.convert("RGB"), dtype=np.float32)
    grain = pixels - np.asarray(room.convert("RGB").filter(ImageFilter.GaussianBlur(5)))
    clean = pixels.copy()
    for mask in masks.values():
        alpha = np.asarray(mask)
        _, top, _, bottom = mask.getbbox()
        for y in range(top, bottom):
            columns = np.flatnonzero(alpha[y])
            left, right = columns[0], columns[-1]
            t = ((columns - left + 1) / (right - left + 2))[:, None]
            light_left = np.median(pixels[y, left - 5:left], axis=0)
            light_right = np.median(pixels[y, right + 1:right + 6], axis=0)
            base = (1 - t) * light_left + t * light_right
            clean[y, columns] = base + .5 * np.sin(np.pi * t) * grain[y + 74, columns]
    return Image.fromarray(np.clip(clean, 0, 255).astype(np.uint8))


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    room = Image.open(LAYERS / "00-pozadi.png").convert("RGBA")
    narrator = Image.open(LAYERS / "01-vypravec.png").convert("RGBA")
    actress = Image.open(LAYERS / "02-hracka.png").convert("RGBA")
    source = Image.open(ROOT / "reference/planches/table.png").convert("RGBA")

    # The scan already contains three outlined cards with a contact shadow. Strip
    # those footprints so a moving card never exposes its former unlocalized face.
    masks = {}
    union = Image.new("L", room.size)
    for card, data in REG["cards"].items():
        shape = Image.new("L", room.size)
        ImageDraw.Draw(shape).polygon([tuple(p) for p in data["outline"]], fill=255)
        masks[card] = shape
        union = ImageChops.lighter(union, shape)
    wood_box = box(REG["wood"])
    wood = fill_wood(room, masks).crop(wood_box)
    wood.putalpha(union.crop(wood_box))
    wood.save(OUTPUT / "wood.png", optimize=True)
    wood_xy = tuple(REG["wood"][:2])

    for locale in ("cs", "en"):
        folder = OUTPUT / locale
        folder.mkdir(exist_ok=True)
        faces = Image.open(ROOT / f"storyboard/overlays/{locale}/table-faces.png").convert("RGBA")
        if ImageChops.subtract(faces.getchannel("A"), union).getbbox():
            raise ValueError(f"{locale}: a localized face is outside its physical card")
        expected = Image.alpha_composite(source, faces)
        assembled = Image.alpha_composite(Image.alpha_composite(room, narrator), actress)
        assembled.alpha_composite(wood, dest=wood_xy)
        for card, shape in masks.items():
            bounds = REG["cards"][card]["bounds"]
            # Antialias only OUTSIDE the opaque mask. At rest, the entire modified
            # wood patch is covered by the exact localized pixels from the source.
            alpha = ImageChops.lighter(shape, shape.filter(ImageFilter.GaussianBlur(0.55)))
            piece = expected.crop(box(bounds))
            piece.putalpha(alpha.crop(box(bounds)))
            path = folder / f"{card}.png"
            piece.save(path, optimize=True)
            with Image.open(path) as saved:
                assembled.alpha_composite(saved, dest=tuple(bounds[:2]))
        delta = np.abs(np.asarray(assembled, dtype=np.int16) - np.asarray(expected, dtype=np.int16))
        print(f"{locale}: max delta {delta.max()}, changed pixels {np.count_nonzero(delta.max(axis=2))}")
        if delta.max() != 0:
            raise ValueError("Registered card/character assembly differs from approved source")


if __name__ == "__main__":
    main()
