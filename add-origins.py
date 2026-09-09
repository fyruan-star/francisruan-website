#!/usr/bin/env python3
"""Install the childhood photos: strip phone-screenshot letterboxing, crop square, save."""
import sys, pathlib, subprocess
import numpy as np
from PIL import Image, ImageOps

ROOT = pathlib.Path(__file__).parent
SRC  = pathlib.Path("/Users/francisruan/Desktop/baby photo")
OUT  = ROOT / "assets" / "photos"

# source, output, x-bias, y-bias   (0 = keep left/top edge, 1 = keep right/bottom)
JOBS = [
  ("IMG_8365.jpg", "origin-leadership.jpg",    0.50, 0.12),  # George Washington
  ("IMG_1003.jpg", "origin-engineer.jpg",      0.46, 0.50),  # screwdriver
  ("IMG_5235.jpg", "origin-relationships.jpg", 0.30, 0.50),  # writing, with the cat
  ("IMG_1001.PNG", "origin-curiosity.jpg",     0.50, 0.10),  # playground
  ("IMG_9972.JPG", "origin-fun.jpg",           0.28, 0.62),  # ninja suit
  ("IMG_1708.PNG", "awards.jpg",               0.50, 0.20),  # arms up on the blacktop
  ("IMG_1707.PNG", "barbershop.jpg",           0.28, 0.28),  # first haircut
]


def strip_letterbox(im, thresh=26):
    """Drop the near-black bars a phone screenshot puts above and below the frame."""
    a = np.asarray(im.convert("L"))
    rowmax = a.max(axis=1)
    keep = np.where(rowmax > thresh)[0]
    if keep.size == 0:
        return im
    top, bot = int(keep[0]), int(keep[-1]) + 1
    colmax = a.max(axis=0)
    kc = np.where(colmax > thresh)[0]
    left, right = (int(kc[0]), int(kc[-1]) + 1) if kc.size else (0, im.width)
    return im.crop((left, top, right, bot))


def square(im, xb, yb, size=900):
    w, h = im.size
    s = min(w, h)
    left = int(round((w - s) * xb))
    top  = int(round((h - s) * yb))
    return im.crop((left, top, left + s, top + s)).resize((size, size), Image.LANCZOS)


for src, dst, xb, yb in JOBS:
    p = SRC / src
    if not p.exists():
        print(f"  MISSING {src}")
        continue
    im = ImageOps.exif_transpose(Image.open(p)).convert("RGB")
    before = im.size
    im = strip_letterbox(im)
    out = square(im, xb, yb)
    out.save(OUT / dst, "JPEG", quality=88, optimize=True, progressive=True)
    print(f"  {src:16} {before[0]}x{before[1]} -> letterbox {im.size[0]}x{im.size[1]} -> {dst}")

subprocess.run([sys.executable, str(ROOT / "build-pages.py")], check=True, capture_output=True)
print("rebuilt")
