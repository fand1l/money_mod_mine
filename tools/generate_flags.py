#!/usr/bin/env python3
"""Generate placeholder flag TGAs for the Random World custom countries.

HOI4 expects, per country tag, uncompressed 32-bit TGA flags in 3 sizes:
    gfx/flags/TAG.tga           82 x 52   (also TAG_<ideology>.tga)
    gfx/flags/medium/...        41 x 26
    gfx/flags/small/...         10 x 7

Design: each country has a two-band base flag; each ideology variant adds a
colored vertical stripe on the hoist (left) side so ideology flips are
visible in-game. Replace these TGAs with real art any time - just keep the
file names and sizes.

Run from the repository root:  python3 tools/generate_flags.py
"""
import os
import struct

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "random_world", "gfx", "flags")

SIZES = [("", 82, 52), ("medium", 41, 26), ("small", 10, 7)]

# Base flag: (top band RGB, bottom band RGB)
COUNTRIES = {
    "NES": ((45, 110, 210), (242, 195, 48)),   # blue over yellow (Podillia)
    "KAM": ((150, 30, 45), (240, 240, 240)),   # crimson over white
    "KHA": ((35, 125, 60), (30, 30, 30)),      # green over dark
}

# Hoist stripe color per ideology variant (None = plain base flag)
VARIANTS = {
    "": None,
    "_neutrality": (140, 140, 140),
    "_fascism": (100, 60, 40),
    "_communism": (190, 30, 30),
    "_democratic": (30, 80, 170),
}


def tga_bytes(width, height, pixel_rgb):
    """Uncompressed 32-bit BGRA TGA, top-left origin."""
    header = struct.pack(
        "<BBBHHBHHHHBB",
        0, 0, 2,        # no id field, no color map, uncompressed true-color
        0, 0, 0,        # color map spec (unused)
        0, 0,           # x, y origin
        width, height,
        32, 0x20,       # 32 bits/pixel, top-left origin
    )
    body = bytearray()
    for y in range(height):
        for x in range(width):
            r, g, b = pixel_rgb(x, y, width, height)
            body += bytes((b, g, r, 255))
    return header + bytes(body)


def make_pixel_fn(top, bottom, stripe):
    def pixel(x, y, w, h):
        if stripe is not None and x < max(1, w // 4):
            return stripe
        return top if y < h // 2 else bottom
    return pixel


def main():
    count = 0
    for subdir, w, h in SIZES:
        outdir = os.path.join(ROOT, subdir) if subdir else ROOT
        os.makedirs(outdir, exist_ok=True)
        for tag, (top, bottom) in COUNTRIES.items():
            for suffix, stripe in VARIANTS.items():
                data = tga_bytes(w, h, make_pixel_fn(top, bottom, stripe))
                path = os.path.join(outdir, f"{tag}{suffix}.tga")
                with open(path, "wb") as f:
                    f.write(data)
                count += 1
    print(f"Wrote {count} flag files under {ROOT}")


if __name__ == "__main__":
    main()
