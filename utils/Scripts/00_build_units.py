#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
00_build_units.py — deterministically enumerate contiguous Bhagavad Gita verse spans.

Input: JSON array of { text, chapterNumber, verseNumber }
Output: JSONL lines like {"chapter":2, "start":47, "end":49, "text":"..."}

Defaults are set for this repository layout, but all parameters are configurable via CLI.
"""

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Tuple


def resolve_repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def resolve_path(repo_root: Path, path_str: str) -> Path:
    candidate = Path(path_str)
    if candidate.is_absolute():
        return candidate
    return (repo_root / candidate).resolve()


def load_verses(path: Path) -> Dict[int, List[Tuple[int, str]]]:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    chapters: Dict[int, List[Tuple[int, str]]] = defaultdict(list)
    for row in data:
        chapter_number = int(row["chapterNumber"])  # type: ignore[arg-type]
        verse_number = int(row["verseNumber"])      # type: ignore[arg-type]
        text: str = row["text"]
        chapters[chapter_number].append((verse_number, text))
    # Sort verses within each chapter by verse_number
    for chapter in list(chapters.keys()):
        chapters[chapter] = sorted(chapters[chapter], key=lambda item: item[0])
    return chapters


def build_units(
    chapters: Dict[int, List[Tuple[int, str]]], span_lengths: List[int]
) -> List[Dict[str, object]]:
    units: List[Dict[str, object]] = []
    # Deterministic iteration: chapters ascending
    for chapter, verses in sorted(chapters.items(), key=lambda kv: kv[0]):
        num_verses = len(verses)
        # For each requested span length
        for span_len in sorted({l for l in span_lengths if l > 0}):
            # Sliding window over verses
            for start_idx in range(0, max(0, num_verses - span_len + 1)):
                start_verse = verses[start_idx][0]
                end_verse = verses[start_idx + span_len - 1][0]
                text = "\n".join(v_text for (_v_num, v_text) in verses[start_idx:start_idx + span_len])
                units.append({
                    "chapter": chapter,
                    "start": start_verse,
                    "end": end_verse,
                    "text": text,
                })
    return units


def write_jsonl(units: List[Dict[str, object]], output_path: Path) -> int:
    count = 0
    with output_path.open("w", encoding="utf-8") as f:
        for unit in units:
            f.write(json.dumps(unit, ensure_ascii=False) + "\n")
            count += 1
    return count


def parse_args() -> argparse.Namespace:
    repo_root = resolve_repo_root()
    default_input = (
        repo_root
        / "Bhagavad-Gita-Verses-iOS-App/Shared/Resources/verses-formatted.json"
    )
    default_output = repo_root / "units.jsonl"

    parser = argparse.ArgumentParser(description="Enumerate contiguous verse spans into units.jsonl")
    parser.add_argument(
        "-i",
        "--input",
        default=str(default_input),
        help="Path to verses JSON array (default: repository verses-formatted.json)",
    )
    parser.add_argument(
        "-o",
        "--output",
        default=str(default_output),
        help="Output JSONL path (default: units.jsonl at repo root)",
    )
    parser.add_argument(
        "-k",
        "--max-range-len",
        type=int,
        default=8,
        help="Maximum contiguous span length K (default: 8) — ignored if --span-lengths is provided",
    )
    parser.add_argument(
        "--span-lengths",
        type=str,
        default="1,4,8",
        help="Comma-separated span lengths to generate (default: 1,4,8)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    repo_root = resolve_repo_root()

    input_path = resolve_path(repo_root, args.input)
    output_path = resolve_path(repo_root, args.output)

    # Determine span lengths
    if args.span_lengths:
        try:
            span_lengths = [int(x.strip()) for x in str(args.span_lengths).split(",") if x.strip()]
        except ValueError:
            raise SystemExit("--span-lengths must be comma-separated integers (e.g., 1,4,8)")
    else:
        if args.max_range_len <= 0:
            raise SystemExit("--max-range-len must be a positive integer")
        span_lengths = list(range(1, args.max_range_len + 1))

    chapters = load_verses(input_path)
    units = build_units(chapters, span_lengths)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    total = write_jsonl(units, output_path)
    print(f"✅ Wrote {total} units to {output_path}")


if __name__ == "__main__":
    main()


