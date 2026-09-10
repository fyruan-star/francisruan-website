#!/usr/bin/env python3
"""Install any photograph as one of the nine plates on the cover.

Crops to the 4:3 the belt frames use, writes it into assets/photos/, rebuilds
every page, and pushes. Called by "Set A Cover Photo.app"; also usable directly:

    python3 set-plate.py <image> <slug>
"""
import subprocess, sys, pathlib
from PIL import Image, ImageOps

ROOT = pathlib.Path(__file__).parent
PLATES = {
    "why": "my-why-title-sq.jpg",       "i": "who-am-i-wide.jpg",
    "fight on": "fight-on-sq.jpg",      "curiosity": "origin-curiosity.jpg",
    "leadership": "origin-leadership.jpg", "finance": "origin-relationships.jpg",
    "engineer": "origin-engineer.jpg",  "lucky": "awards.jpg",
    "the art of having fun": "origin-fun.jpg",
}

def install(src, slug):
    slug = slug.strip().lower()
    if slug not in PLATES:
        raise SystemExit(f"unknown plate {slug!r}. one of: {', '.join(PLATES)}")
    im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    w, h = im.size
    target = 4 / 3
    if w / h > target:                      # too wide, trim the sides
        nw = int(round(h * target)); left = (w - nw) // 2
        im = im.crop((left, 0, left + nw, h))
    elif w / h < target:                    # too tall, trim top and bottom
        nh = int(round(w / target)); top = (h - nh) // 2
        im = im.crop((0, top, w, top + nh))
    im = im.resize((1400, 1050), Image.LANCZOS)
    out = ROOT / "assets" / "photos" / PLATES[slug]
    im.save(out, quality=88, optimize=True)
    return out

def main():
    out = install(sys.argv[1], sys.argv[2])
    subprocess.run([sys.executable, "build-pages.py"], cwd=ROOT, check=True,
                   stdout=subprocess.DEVNULL)
    subprocess.run(["git", "add", "-A"], cwd=ROOT, check=True)
    subprocess.run(["git", "commit", "-q", "-m",
                    f"Replace the {sys.argv[2]} plate on the cover"], cwd=ROOT, check=True)
    subprocess.run(["git", "push", "-q", "origin", "main"], cwd=ROOT, check=True)
    print(f"installed {out.name} and pushed. live in about a minute.")

if __name__ == "__main__":
    main()
