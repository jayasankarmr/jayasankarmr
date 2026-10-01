"""Crop and resize full-size photos into the small JPEGs that build_assets.py embeds.

Run this once, locally, whenever a source photo changes, and commit what it writes to
assets/src/. The originals (5–23 MB each) stay out of the repo, and CI never needs an
image library because build_assets.py only base64-encodes these files.

    python scripts/prepare_photos.py hero ~/Pictures/embers.jpg

Uses `sips`, which ships with macOS.
"""
import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "assets" / "src"

# name → (output width, output height, focal x, focal y, byte budget)
# 1.5x the hero's display size: 2x does not fit, because the embers compress badly and
# the SVG must stay under 200 KB after base64 (+33%).
SPECS = {
    "hero": (797, 600, 0.50, 0.55, 140_000),
}
QUALITIES = range(82, 39, -4)


def sips(*args):
    subprocess.run(["sips", *map(str, args)], check=True, stdout=subprocess.DEVNULL)


def size_of(path):
    out = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", str(path)],
                         check=True, capture_output=True, text=True).stdout
    vals = [int(line.split(":")[1]) for line in out.splitlines() if "pixel" in line]
    return vals[0], vals[1]


def strip_metadata(data):
    """Drop EXIF/XMP (APP1), Photoshop (APP13) and comment segments from a JPEG.
    sips keeps them, and Lightroom XMP alone can be tens of KB. ICC (APP2) stays."""
    if data[:2] != b"\xff\xd8":
        raise ValueError("not a JPEG")
    out, i = bytearray(data[:2]), 2
    while i < len(data):
        if data[i] != 0xFF:
            raise ValueError(f"bad JPEG marker at {i}")
        marker = data[i + 1]
        if marker == 0xDA:  # start of scan: the rest is image data
            out += data[i:]
            break
        length = int.from_bytes(data[i + 2:i + 4], "big")
        if marker not in (0xE1, 0xED, 0xFE):
            out += data[i:i + 2 + length]
        i += 2 + length
    return bytes(out)


def crop_box(sw, sh, ow, oh, fx, fy):
    """Largest box of aspect ow:oh inside sw×sh, centred on the focal point and clamped."""
    if sw / sh > ow / oh:
        ch, cw = sh, round(sh * ow / oh)
    else:
        cw, ch = sw, round(sw * oh / ow)
    x = min(max(round(fx * sw - cw / 2), 0), sw - cw)
    y = min(max(round(fy * sh - ch / 2), 0), sh - ch)
    return x, y, cw, ch


def prepare(name, source):
    ow, oh, fx, fy, budget = SPECS[name]
    sw, sh = size_of(source)
    x, y, cw, ch = crop_box(sw, sh, ow, oh, fx, fy)
    out = SRC / f"{name}.jpg"
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp) / "work.jpg"
        shutil.copy(source, work)
        sips("-c", ch, cw, "--cropOffset", y, x, work)
        sips("-z", oh, ow, work)
        for q in QUALITIES:
            trial = Path(tmp) / f"q{q}.jpg"
            sips("-s", "format", "jpeg", "-s", "formatOptions", q, work, "--out", trial)
            data = strip_metadata(trial.read_bytes())
            if len(data) <= budget:
                SRC.mkdir(parents=True, exist_ok=True)
                out.write_bytes(data)
                print(f"{out.relative_to(ROOT)}  {ow}×{oh}  q{q}  {len(data) // 1024} KB  "
                      f"(crop {cw}×{ch} at {x},{y})")
                return
    sys.exit(f"{name}: no quality down to {QUALITIES[-1]} fits {budget // 1024} KB")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("name", choices=sorted(SPECS))
    ap.add_argument("source", type=Path)
    args = ap.parse_args()
    if not shutil.which("sips"):
        sys.exit("sips not found: this script needs macOS")
    prepare(args.name, args.source)


if __name__ == "__main__":
    main()
