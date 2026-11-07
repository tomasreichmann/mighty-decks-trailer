"""Pack a finished local ComfyUI SAM2 job's two reference and 136 tracked mattes."""
import argparse
import io
import json
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen

import numpy as np
from PIL import Image


def collect(url, job_id):
    with urlopen(f"{url}/history/{job_id}", timeout=10) as response:
        job = json.load(response).get(job_id)
    if not job or job["status"]["status_str"] != "success":
        raise RuntimeError(f"Job {job_id} has not finished successfully")
    mattes = {}
    graph = json.loads(Path(__file__).with_name("sam2-graph.json").read_text(encoding="utf8"))
    for take, length in (("art", 1), ("tracked", 68)):
        for part in ("face", "hand"):
            key = f"{take}-{part}"
            crop = graph[key + "-crop"]["inputs"]
            x, y, w, h = (crop[field] for field in ("x", "y", "width", "height"))
            items = job["outputs"][key + "-save"]["images"]
            if len(items) != length:
                raise ValueError(f"{key}: expected {length} frames, got {len(items)}")
            stack = []
            for item in items:
                with urlopen(url + "/view?" + urlencode(item), timeout=10) as response:
                    with Image.open(io.BytesIO(response.read())) as im:
                        mask = np.array(im.convert("L")) > 127
                if mask.shape != (h, w) or not mask.any():
                    raise ValueError(f"{key}: empty or incorrectly sized segmentation")
                canvas = np.zeros((416, 448), dtype=bool)
                canvas[y:y+h, x:x+w] = mask
                stack.append(np.packbits(canvas, axis=1))
            mattes[key] = np.stack(stack)
    np.savez_compressed(Path(__file__).with_name("sam2-mattes.npz"), **mattes)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("job_id")
    parser.add_argument("--url", default="http://127.0.0.1:7821")
    args = parser.parse_args()
    collect(args.url, args.job_id)
