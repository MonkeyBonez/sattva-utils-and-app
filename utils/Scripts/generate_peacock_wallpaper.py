#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
from typing import List, Tuple

try:
    from PIL import Image
except ImportError as e:
    raise SystemExit("Pillow is required. Install with: pip install pillow") from e


def parse_sizes(s: str) -> List[Tuple[int, int]]:
    sizes: List[Tuple[int, int]] = []
    for part in s.split(","):
        part = part.strip().lower()
        if not part:
            continue
        if "x" not in part:
            raise ValueError(f"Invalid size '{part}'. Use WIDTHxHEIGHT, e.g., 1290x2796")
        w_str, h_str = part.split("x", 1)
        w = int(w_str)
        h = int(h_str)
        if w <= 0 or h <= 0:
            raise ValueError(f"Invalid size '{part}'. Width/height must be > 0")
        sizes.append((w, h))
    if not sizes:
        raise ValueError("No valid sizes parsed")
    return sizes


def lerp(a: int, b: int, t: float) -> int:
    return max(0, min(255, int(round(a + (b - a) * t))))


def generate_vertical_gradient(width: int, height: int, top_rgb: Tuple[int, int, int], bottom_rgb: Tuple[int, int, int]) -> Image.Image:
    # Build a 1px-wide vertical gradient then resize horizontally for speed/quality
    col = Image.new("RGB", (1, height))
    px = col.load()
    r1, g1, b1 = top_rgb
    r2, g2, b2 = bottom_rgb
    if height == 1:
        for y in range(height):
            px[0, y] = (r1, g1, b1)
    else:
        for y in range(height):
            t = y / (height - 1)
            px[0, y] = (lerp(r1, r2, t), lerp(g1, g2, t), lerp(b1, b2, t))
    img = col.resize((width, height), Image.BILINEAR)
    return img


def main() -> None:
    ap = argparse.ArgumentParser(description="Generate peacock gradient wallpapers (vertical gradient, top->bottom)")
    ap.add_argument("--out-dir", type=Path, required=True, help="Output directory for wallpapers")
    ap.add_argument("--sizes", type=str, required=False,
                    help="Comma-separated sizes WIDTHxHEIGHT, e.g., '1290x2796,1170x2532'",
                    default="1290x2796,1170x2532,1242x2688,1125x2436,1080x2340")
    ap.add_argument("--format", type=str, choices=["png", "jpg", "jpeg"], default="png")
    ap.add_argument("--filename-prefix", type=str, default="peacock")
    # Colors from Shared/Resources/Colors.swift: greenPeacock (16,34,30) -> bluePeacock (16,34,34)
    ap.add_argument("--top", type=str, default="16,34,30", help="Top RGB, e.g., '16,34,30'")
    ap.add_argument("--bottom", type=str, default="16,34,34", help="Bottom RGB, e.g., '16,34,34'")
    args = ap.parse_args()

    def parse_rgb(s: str) -> Tuple[int, int, int]:
        parts = [int(p.strip()) for p in s.split(",")]
        if len(parts) != 3:
            raise ValueError("RGB must have 3 comma-separated ints")
        for v in parts:
            if v < 0 or v > 255:
                raise ValueError("RGB values must be 0..255")
        return parts[0], parts[1], parts[2]

    sizes = parse_sizes(args.sizes)
    top_rgb = parse_rgb(args.top)
    bottom_rgb = parse_rgb(args.bottom)

    out_dir: Path = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    for (w, h) in sizes:
        img = generate_vertical_gradient(w, h, top_rgb, bottom_rgb)
        fname = f"{args.filename_prefix}_{w}x{h}.{args.format}"
        out_path = out_dir / fname
        if args.format in ("jpg", "jpeg"):
            img = img.convert("RGB")
            img.save(out_path, quality=95, optimize=True)
        else:
            img.save(out_path)
        print(f"Saved {out_path}")


if __name__ == "__main__":
    main()



