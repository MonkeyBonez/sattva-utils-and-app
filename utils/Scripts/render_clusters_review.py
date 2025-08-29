#!/usr/bin/env python3
"""
Render clusters from a JSONL file into an easy-to-review grouped format.

Default output is Markdown grouped by cluster, de-duplicating identical texts
and summarizing counts and lesson_ids. You can also output CSV or plain text.

Usage examples:
  python Scripts/render_clusters_review.py \
    --input "/Users/snehal/Desktop/Software Projects/Gita Project/clusters_1_4_8.jsonl" \
    --output "/Users/snehal/Desktop/Software Projects/Gita Project/clusters_1_4_8_review.md"

  python Scripts/render_clusters_review.py --format csv --output clusters_review.csv
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


@dataclass(frozen=True)
class Candidate:
    lesson_id: str
    text: str


def read_clusters(jsonl_path: Path) -> Dict[int, List[Candidate]]:
    """Read clusters JSONL into a mapping: cluster_id -> list of Candidates."""
    clusters: Dict[int, List[Candidate]] = defaultdict(list)
    with jsonl_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            cluster_id = int(obj["cluster_id"])
            for cand in obj.get("candidates", []):
                clusters[cluster_id].append(Candidate(
                    lesson_id=str(cand.get("lesson_id", "")),
                    text=str(cand.get("text", "")),
                ))
    return clusters


def group_texts(candidates: Iterable[Candidate]) -> List[Tuple[str, List[str]]]:
    """Group identical texts and collect their lesson_ids.

    Returns a list of (text, [lesson_ids]) sorted by text.
    """
    text_to_lessons: Dict[str, List[str]] = defaultdict(list)
    for cand in candidates:
        text_to_lessons[cand.text].append(cand.lesson_id)
    # Sort by text for stable output
    return sorted(text_to_lessons.items(), key=lambda t: t[0].lower())


def render_markdown(clusters: Dict[int, List[Candidate]]) -> str:
    lines: List[str] = []
    lines.append("## Clusters Review")
    lines.append("")
    for cluster_id in sorted(clusters.keys()):
        candidates = clusters[cluster_id]
        grouped = group_texts(candidates)
        total = len(candidates)
        unique = len(grouped)
        lines.append(f"### Cluster {cluster_id} (unique texts: {unique}, total candidates: {total})")
        for text, lesson_ids in grouped:
            count = len(lesson_ids)
            count_str = f" (x{count})" if count > 1 else ""
            lines.append(f"- {text}{count_str}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_text(clusters: Dict[int, List[Candidate]]) -> str:
    lines: List[str] = []
    for cluster_id in sorted(clusters.keys()):
        candidates = clusters[cluster_id]
        grouped = group_texts(candidates)
        lines.append(f"Cluster {cluster_id}")
        for text, lesson_ids in grouped:
            count = len(lesson_ids)
            count_str = f" (x{count})" if count > 1 else ""
            lines.append(f"  - {text}{count_str}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def write_csv(clusters: Dict[int, List[Candidate]], out_path: Path) -> None:
    """Write CSV with columns: cluster_id, text, count, lesson_ids (semicolon-separated)."""
    with out_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["cluster_id", "text", "count", "lesson_ids"]) 
        for cluster_id in sorted(clusters.keys()):
            grouped = group_texts(clusters[cluster_id])
            for text, lesson_ids in grouped:
                writer.writerow([cluster_id, text, len(lesson_ids), ";".join(lesson_ids)])


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render clusters for review")
    default_input = Path(__file__).resolve().parents[1] / "clusters_1_4_8.jsonl"
    parser.add_argument(
        "--input",
        type=Path,
        default=default_input,
        help="Path to clusters JSONL (default: workspace clusters_1_4_8.jsonl)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output path. Defaults to same directory as input with _review.md/.txt/.csv",
    )
    parser.add_argument(
        "--format",
        choices=["md", "txt", "csv"],
        default="md",
        help="Output format (default: md)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_path: Path = args.input
    clusters = read_clusters(input_path)

    if args.output is None:
        suffix = {"md": "_review.md", "txt": "_review.txt", "csv": "_review.csv"}[args.format]
        out_path = input_path.with_name(input_path.stem + suffix)
    else:
        out_path = args.output

    out_path.parent.mkdir(parents=True, exist_ok=True)

    if args.format == "csv":
        write_csv(clusters, out_path)
        print(f"Wrote CSV: {out_path}")
        return

    if args.format == "md":
        content = render_markdown(clusters)
    else:
        content = render_text(clusters)

    with out_path.open("w", encoding="utf-8") as f:
        f.write(content)
    print(f"Wrote {args.format.upper()}: {out_path}")


if __name__ == "__main__":
    main()


