#!/usr/bin/env python3
"""
04_merge_clusters.py — Merge specified clusters in a clusters JSONL file.

Input format (per line):
  {
    "cluster_id": <int>,
    "candidates": [ { ... arbitrary candidate fields incl. text ... }, ... ]
  }

This script merges the clusters whose IDs you provide (one merge operation per
invocation), concatenating their candidates. You can optionally deduplicate by
candidate text and reindex cluster IDs to be contiguous after the merge.

Examples:
  # Merge clusters 12,37,45 into a single cluster (target becomes 12),
  # deduplicate by text (case/whitespace insensitive), and reindex 0..N-1
  python utils/Scripts/04_merge_clusters.py \
    -i utils/Scripts/outputs/clusters_B_recluster_st_th0p82.jsonl \
    -o utils/Scripts/outputs/clusters_B_recluster_st_th0p82_merged.jsonl \
    --merge 12,37,45 --dedupe --reindex

  # Merge clusters 100 and 108 into target cluster 200, without reindexing
  python utils/Scripts/04_merge_clusters.py \
    -i input.jsonl -o output.jsonl \
    --merge 100,108 --target-id 200 --dedupe
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List, Any, Tuple


def resolve_repo_root() -> Path:
    # utils/Scripts/ → parents[2] should be the workspace root
    return Path(__file__).resolve().parents[2]


def resolve_path(repo_root: Path, path_str: str) -> Path:
    p = Path(path_str)
    return p if p.is_absolute() else (repo_root / p).resolve()


def normalize_text(value: str) -> str:
    return " ".join((value or "").strip().lower().split())


def read_clusters(path: Path) -> Dict[int, List[Dict[str, Any]]]:
    clusters: Dict[int, List[Dict[str, Any]]] = {}
    with path.open("r", encoding="utf-8") as f:
        for idx, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            if "cluster_id" not in obj or "candidates" not in obj:
                raise ValueError(f"Line {idx}: missing cluster_id or candidates")
            cid = int(obj["cluster_id"])
            cands = obj.get("candidates", [])
            if not isinstance(cands, list):
                raise ValueError(f"Line {idx}: candidates must be a list")
            clusters[cid] = list(cands)
    return clusters


def write_clusters(path: Path, clusters: Dict[int, List[Dict[str, Any]]]) -> int:
    count = 0
    with path.open("w", encoding="utf-8") as f:
        for cid in sorted(clusters.keys()):
            row = {"cluster_id": cid, "candidates": clusters[cid]}
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
            count += 1
    return count


def merge_clusters(
    clusters: Dict[int, List[Dict[str, Any]]],
    merge_ids: List[int],
    *,
    target_id: int | None,
    dedupe: bool,
) -> Dict[int, List[Dict[str, Any]]]:
    if len(merge_ids) < 2:
        raise ValueError("Provide at least two cluster IDs to merge")
    missing = [cid for cid in merge_ids if cid not in clusters]
    if missing:
        raise KeyError(f"Cluster IDs not found: {missing}")

    # Choose target cluster id
    tgt = target_id if target_id is not None else min(merge_ids)

    # Concatenate candidates in order of cluster id ascending, preserving order within each
    merged: List[Dict[str, Any]] = []
    for cid in sorted(merge_ids):
        merged.extend(clusters[cid])

    if dedupe:
        seen: Dict[str, int] = {}
        unique: List[Dict[str, Any]] = []
        for cand in merged:
            text = cand.get("text")
            if isinstance(text, str):
                key = normalize_text(text)
                if key in seen:
                    continue
                seen[key] = 1
            unique.append(cand)
        merged = unique

    # Build new mapping
    out: Dict[int, List[Dict[str, Any]]] = {}
    for cid, cands in clusters.items():
        if cid in merge_ids:
            continue
        out[cid] = cands
    out[tgt] = merged
    return out


def reindex_clusters(clusters: Dict[int, List[Dict[str, Any]]]) -> Dict[int, List[Dict[str, Any]]]:
    mapping: List[Tuple[int, List[Dict[str, Any]]]] = sorted(clusters.items(), key=lambda kv: kv[0])
    reindexed: Dict[int, List[Dict[str, Any]]] = {}
    for new_id, (old_id, cands) in enumerate(mapping):
        reindexed[new_id] = cands
    return reindexed


def parse_args() -> argparse.Namespace:
    repo_root = resolve_repo_root()
    default_in = repo_root / "utils/Scripts/outputs/clusters_B_recluster_st_th0p82.jsonl"
    default_out = repo_root / "utils/Scripts/outputs/clusters_B_recluster_st_th0p82_merged.jsonl"

    p = argparse.ArgumentParser(description="Merge specified clusters in a JSONL file")
    p.add_argument("-i", "--in-file", default=str(default_in))
    p.add_argument("-o", "--out-file", default=str(default_out))
    p.add_argument(
        "--merge",
        required=True,
        help="Comma-separated cluster IDs to merge (e.g., 12,37,45)",
    )
    p.add_argument(
        "--target-id",
        type=int,
        default=None,
        help="Optional target cluster_id for the merged cluster (default: min of inputs)",
    )
    p.add_argument("--dedupe", action="store_true", help="Dedupe merged candidates by text")
    p.add_argument(
        "--reindex",
        action="store_true",
        help="Reindex cluster_ids to contiguous 0..N-1 after merge",
    )
    return p.parse_args()


def main() -> None:
    args = parse_args()
    repo_root = resolve_repo_root()
    in_path = resolve_path(repo_root, args.in_file)
    out_path = resolve_path(repo_root, args.out_file)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    clusters = read_clusters(in_path)
    merge_ids = [int(x.strip()) for x in str(args.merge).split(",") if x.strip()]
    merged = merge_clusters(clusters, merge_ids, target_id=args.target_id, dedupe=args.dedupe)
    if args.reindex:
        merged = reindex_clusters(merged)
    total = write_clusters(out_path, merged)
    print(f"✅ Wrote {total} clusters to {out_path}")


if __name__ == "__main__":
    main()




