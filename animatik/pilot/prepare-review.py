"""Prepare a five-second, level-matched audition from the 25–30 s Czech edit."""
import json
import math
import os
from pathlib import Path
import re
import subprocess
import argparse

PILOT = Path(__file__).resolve().parent
FILES = PILOT / "files"
DURATION = "5"
TAKES = {"quiet": "A · Tiché rozhodnutí", "urgent": "B · Pod tlakem"}


def ffmpeg(*args):
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *map(str, args)], check=True)


def levels(path):
    cmd = ["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-t", DURATION,
           "-vn", "-af", "loudnorm=print_format=json", "-f", "null", "-"]
    log = subprocess.run(cmd, capture_output=True, check=True).stderr.decode(errors="replace")
    data = json.loads(re.search(r'\{[^{}]*"input_i"[^{}]*\}', log).group())
    return float(data["input_i"]), float(data["input_tp"])


def audio_hash(path):
    return subprocess.check_output(["ffmpeg", "-loglevel", "error", "-i", str(path),
                                    "-map", "0:a:0", "-c", "copy", "-f", "md5", "-"])


def prepare_takes():
    FILES.mkdir(exist_ok=True)
    original = PILOT.parent / "out" / "Fangs-CS.mp4"
    baseline = FILES / "baseline.mp4"
    ffmpeg("-ss", "25", "-i", original, "-t", DURATION, "-vf", "scale=640:360:flags=lanczos",
           "-c:v", "libx264", "-preset", "fast", "-crf", "17", "-c:a", "aac", "-b:a", "192k",
           "-movflags", "+faststart", baseline)
    reference, _ = levels(baseline)
    for name in TAKES:
        raw = PILOT / "media" / f"h3-{name}.mp4"
        if not raw.exists():
            continue
        loudness, peak = levels(raw)
        if not math.isfinite(loudness):
            raise ValueError(f"Silent candidate: {raw.name}")
        # A single gain preserves performance dynamics. Leave headroom for AAC.
        gain = min(reference - loudness, -1.5 - peak)
        native = FILES / f"{name}-native.mp4"
        dub = FILES / f"{name}-2d.mp4"
        ffmpeg("-i", raw, "-t", DURATION, "-map", "0:v:0", "-map", "0:a:0",
               "-af", f"volume={gain:.2f}dB", "-vf", "scale=640:360:force_original_aspect_ratio=decrease,pad=640:360:(ow-iw)/2:(oh-ih)/2",
               "-c:v", "libx264", "-crf", "17", "-preset", "fast", "-c:a", "aac", "-b:a", "192k",
               "-movflags", "+faststart", native)
        ffmpeg("-i", baseline, "-i", native, "-map", "0:v:0", "-map", "1:a:0", "-t", DURATION,
               "-c", "copy", "-movflags", "+faststart", dub)
        if audio_hash(native) != audio_hash(dub):
            raise ValueError(f"Soundtrack differs across {name} views")
        print(f"{name}: {gain:+.2f} dB, identical audio packets in both cuts.")


def publish():
    config = {"baseline": {"src": "files/baseline.mp4", "label": "Původní 2D s pracovním hlasem"}, "takes": []}
    for name, label in TAKES.items():
        if all((FILES / f"{name}-{cut}.mp4").is_file() for cut in ("native", "2d")):
            config["takes"].append({"id": name, "label": label, "native": f"files/{name}-native.mp4",
                                    "dub": f"files/{name}-2d.mp4"})
    if (FILES / "hybrid-sam.mp4").is_file():
        config["edits"] = [{"id": "hybrid", "label": "C · Rozšířené masky SAM", "src": "files/hybrid-sam.mp4"},
                           {"id": "pred-sam", "label": "C · Původní masky", "src": "files/hybrid-vrstvy.mp4"}]
    elif (FILES / "hybrid-vrstvy.mp4").is_file():
        config["edits"] = [{"id": "hybrid", "label": "C · 2D scéna a pohyb hráčky",
                            "src": "files/hybrid-vrstvy.mp4"}]
    elif (FILES / "hybrid-zraneni.mp4").is_file():
        config["edits"] = [{"id": "hybrid", "label": "C · H3 + 2D se Zraněním",
                            "src": "files/hybrid-zraneni.mp4"}]
    related = [
        ("detail-masky-sam.mp4", "Detail masek před a po"),
        ("dohoda-hangar-selma-pohyb-cs.mp4", "Příchod šelmy · pohyb tlap a hlavy · CS"),
        ("dohoda-hangar-selma-cs.mp4", "Příchod šelmy · 2D póza · CS"),
        ("dohoda-hangar-selma-bez-hlasu.mp4", "Příchod šelmy · obraz a ruchy"),
        ("dohoda-hangar-selma-en.mp4", "Dohoda a hangár · příchod šelmy · EN"),
        ("dohoda-hangar-zasah-cs.mp4", "Dohoda a hangár · CS · nové hlasy a zásah"),
        ("dohoda-hangar-zasah-bez-hlasu.mp4", "Dohoda a hangár · CS · titulky a ruchy"),
        ("dohoda-hangar-zasah-en.mp4", "Dohoda a hangár · EN · nový zásah"),
        ("dohoda-hangar-cs.mp4", "Dohoda a hangár · CS"),
        ("dohoda-hangar-en.mp4", "Dohoda a hangár · EN"),
    ]
    config["related"] = [{"src": "files/" + file, "label": label}
                         for file, label in related if (FILES / file).is_file()]
    # A selected cut keeps its ID across revisions. Its media URL must change
    # so an already-open comparison actually reloads the updated picture.
    for item in config.get("edits", []) + config["related"]:
        version = (PILOT / item["src"]).stat().st_mtime_ns
        item["src"] += f"?v={version}"
    temporary = PILOT / "variants.next.json"
    temporary.write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf8")
    os.replace(temporary, PILOT / "variants.json")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--publish-only", action="store_true", help="Publish already rendered comparisons")
    if not parser.parse_args().publish_only:
        prepare_takes()
    publish()
