#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
-----------------
Load verses.json (array of {text, chapterNumber, verseNumber}),
build contiguous ranges up to K verses long, and save to units.jsonl.

This is deterministic, cheap, and only needs to be run once
unless your verse input changes.
"""

# ============================================================
# CONFIGURATION
# ============================================================

CONFIG = {
    "input_file": "Bhagavad-Gita-Verses-iOS-App/Shared/Resources/verses-formatted.json",   # Input: array JSON of verses - run from project root
    "out_file": "units.jsonl",     # Output: JSONL of contiguous verse ranges
    "max_range_len": 8             # K: maximum span length in verses
}

# ============================================================
# SCRIPT
# ============================================================

import json
from pathlib import Path
from collections import defaultdict

def load_verses(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    chapters = defaultdict(list)
    for row in data:
        ch = int(row["chapterNumber"])
        v = int(row["verseNumber"])
        txt = row["text"]
        chapters[ch].append((v, txt))
    for ch in chapters:
        chapters[ch] = sorted(chapters[ch], key=lambda x: x[0])
    return chapters

def build_units(chapters, K):
    """Generate all contiguous verse spans up to length K."""
    units = []
    for ch, verses in chapters.items():
        n = len(verses)
        for L in range(1, K+1):
            for i in range(0, n-L+1):
                start = verses[i][0]
                end = verses[i+L-1][0]
                txt = "\n".join(t for (_, t) in verses[i:i+L])
                units.append({
                    "chapter": ch,
                    "start": start,
                    "end": end,
                    "text": txt
                })
    return units
def main(cfg):
    repo_root = Path(__file__).resolve().parents[1]
    input_path = repo_root / cfg["input_file"]
    output_path = repo_root / cfg["out_file"]

    chapters = load_verses(str(input_path))
    units = build_units(chapters, cfg["max_range_len"])
    with open(str(output_path), "w", encoding="utf-8") as f:
        for u in units:
            f.write(json.dumps(u, ensure_ascii=False) + "\n")
    print(f"✅ Wrote {len(units)} units to {cfg['out_file']}")

if __name__ == "__main__":
    main(CONFIG)
