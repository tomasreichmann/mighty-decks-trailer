"""Typeset the table shot and assemble the colour review boards."""

import json
from pathlib import Path
from os import environ
from tempfile import NamedTemporaryFile
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[1] / "storyboard"
FONTS = Path(environ["WINDIR"]) / "Fonts"


def save_png(im, path):
    with NamedTemporaryFile(suffix=".png", dir=path.parent, delete=False) as f:
        tmp = Path(f.name)
    try:
        im.save(tmp)
        tmp.replace(path)
    finally:
        tmp.unlink(missing_ok=True)


def font(size, bold=False):
    return ImageFont.truetype(str(FONTS / ("segoeuib.ttf" if bold else "segoeui.ttf")), size)


# All panels and board copy follow the same edit decision list as the animatic.
def read_panels():
    cut = json.loads((ROOT / "strih.json").read_text(encoding="utf-8"))
    fps = cut["fps"]
    return [(f"{s['in']/fps:g}–{s['out']/fps:g}", s["id"], s["cs"]["action"],
             s["cs"]["caption"], s["en"]["action"], s["en"]["caption"]) for s in cut["shots"]]


PANELS = read_panels()


def table_faces(reference, loc):
    # Same physical hand as the next overhead shot. Coordinates are on the clean
    # 1920x1080 plate. Retain the artist's outer edges, thickness and shadows.
    quads = [
        ((587,730), (663,729), (649,769), (566,769)),
        ((695,730), (774,728), (780,767), (692,769)),
        ((807,727), (884,726), (901,765), (816,768)),
    ]
    overlay = Image.new("RGBA", (1920,1080))
    for stem, quad in zip(("success", "partial-success", "fumble"), quads):
        with Image.open(reference / "karty/ruka" / loc / (stem+".png")) as src:
            face = ImageOps.grayscale(src.crop(src.getbbox())).rotate(180)
        # In the wide shot only markings should register. Match the amber lamp
        # and shallow focus, retaining actual face data rather than invented art.
        face = ImageOps.colorize(face, "#8e5c32", "#e9b777")
        w,h = face.size
        mat, dest = [], []
        for (x,y),(u,v) in zip(quad, ((0,0),(w,0),(w,h),(0,h))):
            mat += [[x,y,1,0,0,0,-x*u,-y*u],[0,0,0,x,y,1,-x*v,-y*v]]
            dest += [u,v]
        coeff = np.linalg.solve(mat,dest)
        warped = face.transform(overlay.size, Image.Transform.PERSPECTIVE, coeff,
                                Image.Resampling.BICUBIC).filter(ImageFilter.GaussianBlur(0.7))
        mask = Image.new("L",overlay.size)
        ImageDraw.Draw(mask).polygon(quad, fill=255)
        warped.putalpha(mask.filter(ImageFilter.GaussianBlur(0.4)))
        overlay.alpha_composite(warped)
    return overlay


def compose_table(loc, folder):
    # Preserve the original portrait frame used throughout the existing gallery.
    pos = (40, 812, 264, 1038)
    with Image.open(folder / "04b-volba.png") as ref:
        portrait = ref.crop(pos)
    reference = ROOT.parent / "reference"
    with Image.open(reference / "planches/table.png") as plate:
        table = plate.convert("RGB")
    faces = table_faces(reference, loc)
    overlays = ROOT / "overlays" / loc
    overlays.mkdir(parents=True, exist_ok=True)
    save_png(faces, overlays / "table-faces.png")
    table.paste(faces, (0,0), faces)
    with Image.open(reference / "grafika/mighty_decks_logo.png") as src:
        logo = src.crop(src.getbbox())
        logo.thumbnail((154, 154), Image.Resampling.LANCZOS)
    table.paste(logo, (1920 - 77 - logo.width, 43), logo)
    table.paste(portrait, pos)
    draw = ImageDraw.Draw(table)
    for y, size, label, color in [
        (912, 35, "HRÁČKA" if loc == "cs" else "PLAYER", "#efd9bb"),
        (962, 68, PANELS[4][3 if loc == "cs" else 5], "white"),
    ]:
        draw.text((286, y), label, font=font(size, True), anchor="lt", fill=color,
                  stroke_fill="#121b23", stroke_width=4)
    save_png(table, folder / "04b-stul-celek.png")
    save_png(table, reference / "vyber" / f"stul-kompozice-{loc}.png")


def board(loc, rows, name, title, cols):
    folder = ROOT / "screens" / loc
    margin, gutter, w, h, rowh = 40, 24, 640, 360, 491
    im = Image.new("RGB", (2*margin + cols*w + (cols-1)*gutter,
                           128 + rowh*((len(rows)+cols-1)//cols)), "#f5f1e8")
    d = ImageDraw.Draw(im)
    d.text((margin, 18), title, font=font(42, True), fill="#121b23")
    d.text((margin, 78), "Mighty Decks   /   Fangs in the Sun   /   50 s   /   30 fps   /   " + loc.upper(),
           font=font(22), fill="#575348")
    for i, (time, stem, cs, line_cs, en, line_en) in enumerate(rows):
        x = margin + i % cols*(w+gutter)
        y = 128 + i//cols*rowh
        d.text((x,y), time.replace(".", ",") + " s" if loc == "cs" else time + " s",
               font=font(22, True), fill="#865622")
        with Image.open(folder / (stem + ".png")) as frame:
            im.paste(frame.convert("RGB").resize((w,h), Image.Resampling.LANCZOS), (x,y+34))
        d.text((x,y+400), cs if loc == "cs" else en, font=font(26,True), fill="#121b23")
        d.text((x,y+440), line_cs if loc == "cs" else line_en, font=font(22), fill="#454642")
    save_png(im, ROOT / name)


if __name__ == "__main__":
    for loc, name, title in [("cs", "storyboard-v5.png", "Očima hráčky"), ("en", "storyboard-en.png", "Through the player’s eyes")]:
        compose_table(loc, ROOT / "screens" / loc)
        board(loc, PANELS, name, title, 3)
    board("cs", PANELS[3:9], "rampa-volba-dopad.png", "Volba na rampě a její cena", 3)
