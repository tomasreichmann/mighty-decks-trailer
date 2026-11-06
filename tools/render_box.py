"""Render the supplied box dieline into a transparent pack shot. Requires Pillow and NumPy."""

from pathlib import Path

import numpy as np
from PIL import Image, ImageEnhance

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "reference/krabice/box-v2_upscayl_2x_ultrasharp.png"
OUTPUT = ROOT / "reference/grafika/mighty-decks-krabice.png"

# Fold positions measured on a 3712 × 2748 preview of the print sheet.
TOP = (746, 750, 2973, 2001)
FRONT = (749, 2007, 2965, 2657)
RIGHT = (2979, 751, 3620, 2001)


def panel(source, bounds):
    sx, sy = source.width / 3712, source.height / 2748
    return source.crop(tuple(round(v * (sx if i % 2 == 0 else sy)) for i, v in enumerate(bounds)))


def camera():
    eye = np.array([0.94, -3.5, 3.8])
    forward = np.array([0.0, 0.0, 0.21]) - eye
    forward /= np.linalg.norm(forward)
    right = np.cross(forward, [0, 0, 1])
    right /= np.linalg.norm(right)
    up = np.cross(right, forward)

    def project(point):
        ray = np.array(point) - eye
        focal = 4700 / np.dot(ray, forward)
        return (1160 + focal * np.dot(ray, right), 810 - focal * np.dot(ray, up))

    return project


def composite_face(canvas, art, corners, exposure):
    art = ImageEnhance.Brightness(art).enhance(exposure)
    w, h = art.size
    system, values = [], []
    for (x, y), (u, v) in zip(corners, [(0, 0), (w, 0), (w, h), (0, h)]):
        system.extend([[x, y, 1, 0, 0, 0, -u*x, -u*y], [0, 0, 0, x, y, 1, -v*x, -v*y]])
        values.extend([u, v])
    coefficients = np.linalg.solve(system, values)
    surface = art.transform(canvas.size, Image.Transform.PERSPECTIVE, coefficients, Image.Resampling.BICUBIC)
    canvas.alpha_composite(surface)


def main():
    with Image.open(SOURCE) as source:
        top, front, side = [panel(source, bounds).convert("RGBA") for bounds in (TOP, FRONT, RIGHT)]
    # In the dieline, the right wall extends horizontally away from the lid fold.
    side = side.transpose(Image.Transpose.ROTATE_270)
    project = camera()
    back_left, back_right, front_right, front_left = [
        (x, y, .49) for x, y in [(-.89, .5), (.89, .5), (.89, -.5), (-.89, -.5)]
    ]
    floor = lambda p: (*p[:2], 0)
    canvas = Image.new("RGBA", (2320, 1620))
    composite_face(canvas, front, list(map(project, [front_left, front_right, floor(front_right), floor(front_left)])), .83)
    composite_face(canvas, side, list(map(project, [front_right, back_right, floor(back_right), floor(front_right)])), .76)
    composite_face(canvas, top, list(map(project, [back_left, back_right, front_right, front_left])), 1.0)
    canvas.crop(canvas.getbbox()).save(OUTPUT)


if __name__ == "__main__":
    main()

