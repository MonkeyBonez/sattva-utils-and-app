#!/usr/bin/env python3
"""
Compare two clusters JSONL files and report where they differ.

Outputs a Markdown summary including:
  - Cluster IDs only in A or only in B (by presence of cluster_id)
  - For cluster_ids present in both: texts added/removed
  - Texts that moved clusters (text -> cluster_id sets differ between files)

Usage:
  python utils/Scripts/compare_clusters.py \
    --a "/Users/snehal/Desktop/Software Projects/Gita Project/clusters_1_4_8.jsonl" \
    --b "/Users/snehal/Desktop/Software Projects/Gita Project/clusters_1_4_8v2.jsonl" \
    --out "/Users/snehal/Desktop/Software Projects/Gita Project/utils/Scripts/outputs/clusters_compare.md"
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Set, Tuple


@dataclass(frozen=True)
class Candidate:
    lesson_id: str
    text: str


def read_clusters(jsonl_path: Path) -> Dict[int, List[Candidate]]:
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


def texts_by_cluster(clusters: Dict[int, List[Candidate]]) -> Dict[int, Set[str]]:
    return {cid: {c.text for c in cands} for cid, cands in clusters.items()}


def clusters_by_text(clusters: Dict[int, List[Candidate]]) -> Dict[str, Set[int]]:
    mapping: Dict[str, Set[int]] = defaultdict(set)
    for cid, cands in clusters.items():
        for c in cands:
            mapping[c.text].add(cid)
    return mapping


def render_markdown(
    name_a: str,
    name_b: str,
    clusters_a: Dict[int, List[Candidate]],
    clusters_b: Dict[int, List[Candidate]],
    limit_per_section: int = 50,
) -> str:
    texts_a = texts_by_cluster(clusters_a)
    texts_b = texts_by_cluster(clusters_b)

    cids_a = set(texts_a.keys())
    cids_b = set(texts_b.keys())

    only_a = sorted(cids_a - cids_b)
    only_b = sorted(cids_b - cids_a)
    both = sorted(cids_a & cids_b)

    # Per-cluster text diffs for clusters present in both
    cluster_diffs: List[Tuple[int, List[str], List[str]]] = []
    total_added = 0
    total_removed = 0
    for cid in both:
        removed = sorted(texts_a[cid] - texts_b[cid])
        added = sorted(texts_b[cid] - texts_a[cid])
        if removed or added:
            cluster_diffs.append((cid, removed, added))
            total_removed += len(removed)
            total_added += len(added)

    # Text movement (cluster assignments differ)
    a_by_text = clusters_by_text(clusters_a)
    b_by_text = clusters_by_text(clusters_b)
    texts_all = set(a_by_text.keys()) | set(b_by_text.keys())
    moved: List[Tuple[str, List[int], List[int]]] = []
    for t in sorted(texts_all):
        a_c = sorted(a_by_text.get(t, set()))
        b_c = sorted(b_by_text.get(t, set()))
        if a_c != b_c:
            moved.append((t, a_c, b_c))

    lines: List[str] = []
    lines.append("## Cluster Comparison")
    lines.append("")
    lines.append(f"- Comparing: {name_a} (A) vs {name_b} (B)")
    lines.append(f"- Total clusters: A={len(cids_a)}, B={len(cids_b)}, both={len(both)}")
    lines.append(f"- Cluster IDs only in A: {len(only_a)}; only in B: {len(only_b)}")
    lines.append(f"- Clusters (in both) with text diffs: {len(cluster_diffs)} (added={total_added}, removed={total_removed})")
    lines.append(f"- Texts with different cluster assignments: {len(moved)}")
    lines.append("")

    if only_a:
        lines.append(f"### Cluster IDs only in A ({len(only_a)})")
        for cid in only_a[:limit_per_section]:
            lines.append(f"- {cid}")
        if len(only_a) > limit_per_section:
            lines.append(f"- ... and {len(only_a) - limit_per_section} more")
        lines.append("")

    if only_b:
        lines.append(f"### Cluster IDs only in B ({len(only_b)})")
        for cid in only_b[:limit_per_section]:
            lines.append(f"- {cid}")
        if len(only_b) > limit_per_section:
            lines.append(f"- ... and {len(only_b) - limit_per_section} more")
        lines.append("")

    if cluster_diffs:
        lines.append(f"### Clusters present in both with added/removed texts ({len(cluster_diffs)})")
        for cid, removed, added in cluster_diffs[:limit_per_section]:
            lines.append(f"- Cluster {cid}")
            if removed:
                lines.append(f"  - removed ({len(removed)}):")
                for t in removed[:10]:
                    lines.append(f"    - {t}")
                if len(removed) > 10:
                    lines.append(f"    - ... and {len(removed) - 10} more")
            if added:
                lines.append(f"  - added ({len(added)}):")
                for t in added[:10]:
                    lines.append(f"    - {t}")
                if len(added) > 10:
                    lines.append(f"    - ... and {len(added) - 10} more")
        if len(cluster_diffs) > limit_per_section:
            lines.append(f"- ... and {len(cluster_diffs) - limit_per_section} more clusters with diffs")
        lines.append("")

    if moved:
        lines.append(f"### Texts with different cluster assignments ({len(moved)})")
        for t, a_c, b_c in moved[:limit_per_section]:
            lines.append(f"- {t}")
            lines.append(f"  - A clusters: {a_c if a_c else '—'}")
            lines.append(f"  - B clusters: {b_c if b_c else '—'}")
        if len(moved) > limit_per_section:
            lines.append(f"- ... and {len(moved) - limit_per_section} more texts moved")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compare two clusters JSONL files")
    parser.add_argument("--a", type=Path, required=True, help="Path to first (baseline) clusters JSONL")
    parser.add_argument("--b", type=Path, required=True, help="Path to second clusters JSONL")
    parser.add_argument("--out", type=Path, default=None, help="Output markdown file path")
    parser.add_argument("--limit", type=int, default=50, help="Max items to list per section")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    path_a: Path = args.a
    path_b: Path = args.b

    clusters_a = read_clusters(path_a)
    clusters_b = read_clusters(path_b)

    name_a = path_a.name
    name_b = path_b.name

    content = render_markdown(name_a, name_b, clusters_a, clusters_b, limit_per_section=args.limit)

    if args.out is None:
        out_path = path_b.with_name(f"compare_{path_a.stem}_vs_{path_b.stem}.md")
    else:
        out_path = args.out

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(content, encoding="utf-8")
    print(f"Wrote comparison report: {out_path}")


if __name__ == "__main__":
    main()


