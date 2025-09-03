#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Iterable, List


def normalize_whitespace(text: str) -> str:
    text = text.strip()
    # Collapse internal whitespace to single spaces
    text = re.sub(r"\s+", " ", text)
    return text


def extract_texts(jsonl_path: Path) -> List[str]:
    texts: List[str] = []
    with jsonl_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            text = obj.get("text")
            if text is None:
                continue
            norm = normalize_whitespace(str(text))
            if norm:
                texts.append(norm)
    return texts


def write_lines(lines: Iterable[str], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        for line in lines:
            if not line or line.startswith("#"):
                # skip comments/blank safety
                continue
            f.write(line.rstrip() + "\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Make lessons.txt from human-pass JSONL")
    parser.add_argument("input", type=Path, help="Path to human-pass JSONL (cluster_id/text per line)")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path(__file__).resolve().parent / "Embeddings" / "lessons.txt",
        help="Output lessons.txt path (default: utils/Scripts/Embeddings/lessons.txt)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    texts = extract_texts(args.input)
    if not texts:
        raise SystemExit("No lessons found (non-null text). Aborting.")
    write_lines(texts, args.output)
    print(f"Wrote lessons: {len(texts)} → {args.output}")


if __name__ == "__main__":
    main()




