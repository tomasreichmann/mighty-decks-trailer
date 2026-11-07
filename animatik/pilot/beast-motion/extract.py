"""Key the lossless H3 output onto transparent, registered 512px cels."""
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw


HERE = Path(__file__).resolve().parent


def chroma_key(rgb):
    rgb = np.asarray(rgb, dtype=np.float32)
    key = np.median(np.concatenate([rgb[:8], rgb[-8:]]).reshape(-1, 3), axis=0)
    green = rgb[:, :, 1] - np.maximum(rgb[:, :, 0], rgb[:, :, 2])
    dominance = key[1] - max(key[0], key[2])
    alpha = 1 - np.clip((green - 2) / max(dominance - 5, 1), 0, 1)
    alpha[(green > .87 * dominance) | (alpha < .045)] = 0
    alpha[green < 2] = 1
    # Unmix the sampled matte at antialiased fur edges. Warm ink and midtones
    # are opaque and keep their native values.
    a = alpha[:, :, None]
    color = np.clip((rgb - key * (1 - a)) / np.maximum(a, .01), 0, 255)
    edge = (alpha > 0) & (alpha < 1)
    color[:, :, 1] = np.where(edge, np.minimum(color[:, :, 1],
        np.maximum(color[:, :, 0], color[:, :, 2]) + 1), color[:, :, 1])
    color[alpha == 0] = 0
    return Image.fromarray(np.dstack((color, alpha * 255)).round().astype(np.uint8))


def main():
    source = Image.open(HERE / "h3-lossless.webp")
    frames = HERE / "frames"
    frames.mkdir(exist_ok=True)
    report = []
    board = Image.new("RGB", (3 * 340, 368), "#29343c")
    for i in range(29):
        native = round(i * (source.n_frames - 1) / 28)
        source.seek(native)
        out = chroma_key(source.convert("RGB"))
        # Keep the original registered (32,32) inset throughout. The action
        # may extend into the green margin, so the player expands its canvas.
        alpha = np.asarray(out.getchannel("A")).astype(np.float32)
        outside = max(0, 1 - alpha[32:480,32:480].sum() / alpha.sum())
        if i == 0:
            # Exact approved stance on the first frame, before the generated flex.
            original = Image.open(HERE.parents[1] / "public/hangar/approach.png").convert("RGBA")
            out = Image.new("RGBA", (512, 512))
            out.alpha_composite(original.resize((448,448), Image.Resampling.LANCZOS), (32,32))
        out.save(frames / f"{i:03}.webp", lossless=True, method=3)
        report.append((i, native, round(float(outside) * 100, 3)))
        if i in (0, 14, 28):
            col = i // 14
            view = out.resize((340,340), Image.Resampling.LANCZOS)
            board.paste(view, (col*340,0), view)
            ImageDraw.Draw(board).text((col*340+12,343), f"f{431+i}", fill="white")
    board.save(HERE / "poses.jpg", quality=93)
    print(f"{source.n_frames} native frames; 29 registered 512×512 RGBA WebP")
    print("Timeline offset, native frame, alpha mass outside registered square (%):", report)


if __name__ == "__main__":
    main()
