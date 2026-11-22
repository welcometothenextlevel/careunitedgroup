#!/usr/bin/env python3
"""Swap the licence-free stand-ins for the client's licensed Adobe Stock images.

1. Put each licensed file (the full download after purchase, NOT the watermarked
   preview) in _build/adobe/, named by its Adobe Stock ID, e.g.
       _build/adobe/1238389313.jpg
   (.jpg, .jpeg, .png or .webp all work; you can swap one or all five).
2. Run:  python3 _build/swap_adobe.py
   It writes the site's WebP sizes over the stand-in images and records the swap in
   _build/adobe/licensed.json.
3. Run:  python3 _build/build.py   (updates alt text and removes the stand-in TODOs)

The licensed originals themselves are git-ignored so they are never published raw.
"""
import json
import pathlib
import sys

from PIL import Image, ImageOps

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
from build import IMAGES, STANDINS  # noqa: E402

ADOBE_DIR = HERE / "adobe"
RECORD = ADOBE_DIR / "licensed.json"

# Where to centre the crop on each original (x, y as 0..1).
FOCUS = {"greeting": (.6, .55), "paper-chain": (.5, .5), "nurse": (.55, .5), "park": (.6, .55)}


def crop(im, ar, fx, fy):
    w, h = im.size
    nw, nh = (int(h * ar), h) if w / h > ar else (w, int(w / ar))
    x = min(max(int(fx * w - nw / 2), 0), w - nw)
    y = min(max(int(fy * h - nh / 2), 0), h - nh)
    return im.crop((x, y, x + nw, y + nh))


def main():
    done = json.loads(RECORD.read_text()) if RECORD.exists() else {}
    for name, adobe_id in STANDINS.items():
        src = next((p for ext in ("jpg", "jpeg", "png", "webp") for p in [ADOBE_DIR / f"{adobe_id}.{ext}"] if p.exists()), None)
        if not src:
            print(f"skip  {name:12} (no _build/adobe/{adobe_id}.jpg)")
            continue
        widths, (rw, rh) = IMAGES[name]
        im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
        if im.width < 1400:
            print(f"WARN  {name:12} {src.name} is only {im.width}px wide: is this the watermarked preview? Use the licensed download.")
        im = crop(im, rw / rh, *FOCUS[name])
        for wd in widths:
            out = ROOT / "images" / f"{name}-{wd}.webp"
            r = im.resize((wd, round(wd * rh / rw)), Image.LANCZOS) if im.width > wd else im
            r.save(out, "WEBP", quality=70, method=6)
            print(f"wrote {out.relative_to(ROOT)} {r.size} {out.stat().st_size // 1024} KB")
        done[name] = adobe_id
    RECORD.write_text(json.dumps(done, indent=2) + "\n")
    print(f"\nlicensed so far: {sorted(done) or 'none'}. Now run: python3 _build/build.py")


if __name__ == "__main__":
    main()
