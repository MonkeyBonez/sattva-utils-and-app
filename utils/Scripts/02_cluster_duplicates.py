#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
02_cluster_duplicates.py — group semantically similar candidate lessons.

Input: candidates.jsonl (rows: { lesson_id, unit, raw })
Output: clusters.jsonl with clusters of near-duplicate paraphrases.

By default uses a mock embedding backend (deterministic hash-based vectors).
Optionally supports sentence-transformers if installed.
"""

import argparse
import json
import math
import os
import sys
import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple, Dict, Iterable, Optional


def resolve_repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def resolve_path(repo_root: Path, path_str: str) -> Path:
    p = Path(path_str)
    return p if p.is_absolute() else (repo_root / p).resolve()


def l2_normalize(vec: List[float]) -> List[float]:
    s = math.sqrt(sum(v * v for v in vec))
    return [v / s for v in vec] if s > 0 else vec


def cos_sim(a: List[float], b: List[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


def hash_to_vec(text: str, dim: int = 384) -> List[float]:
    """Deterministic pseudo-embedding from text via repeated MD5 hashing.

    Produces a vector in R^dim, then L2-normalizes.
    """
    digest = hashlib.md5(text.strip().lower().encode("utf-8")).digest()
    vec: List[float] = []
    seed_bytes = digest
    while len(vec) < dim:
        # Extend by hashing the previous digest to create more bytes
        seed_bytes = hashlib.md5(seed_bytes).digest()
        for b in seed_bytes:
            # Map byte [0,255] → [-0.5, 0.5]
            vec.append((b / 255.0) - 0.5)
            if len(vec) == dim:
                break
    return l2_normalize(vec)


@dataclass
class Candidate:
    lesson_id: str
    text: str


def load_candidates(path: Path, limit: Optional[int]) -> List[Candidate]:
    items: List[Candidate] = []
    with path.open("r", encoding="utf-8") as f:
        for idx, line in enumerate(f):
            if limit is not None and idx >= limit:
                break
            if not line.strip():
                continue
            row = json.loads(line)
            items.append(Candidate(lesson_id=row["lesson_id"], text=row["raw"].strip()))
    return items


def embed_texts(texts: List[str], model_name: str, mock: bool) -> List[List[float]]:
    if mock:
        return [hash_to_vec(t) for t in texts]

    try:
        # Lazy import to avoid mandatory dependency
        from sentence_transformers import SentenceTransformer  # type: ignore
    except Exception as e:
        raise RuntimeError(
            "sentence-transformers not available. Install it or pass --mock"
        ) from e

    model = SentenceTransformer(model_name)
    emb = model.encode(texts, normalize_embeddings=True, show_progress_bar=False)
    return [list(map(float, v)) for v in emb]


def cluster_candidates(candidates: List[Candidate], embeddings: List[List[float]], threshold: float) -> List[List[int]]:
    """Greedy single-linkage: assign item to first cluster with any member ≥ threshold.
    Returns list of clusters as lists of indices into `candidates`.
    Deterministic given input order.
    """
    clusters: List[List[int]] = []
    for i, emb in enumerate(embeddings):
        placed = False
        for cluster in clusters:
            # compute max sim vs cluster members
            sim = max(cos_sim(emb, embeddings[j]) for j in cluster)
            if sim >= threshold:
                cluster.append(i)
                placed = True
                break
        if not placed:
            clusters.append([i])
    return clusters


def write_clusters(path: Path, candidates: List[Candidate], clusters: List[List[int]]) -> int:
    count = 0
    with path.open("w", encoding="utf-8") as f:
        for cid, idxs in enumerate(clusters):
            row = {
                "cluster_id": cid,
                "candidates": [
                    {"lesson_id": candidates[i].lesson_id, "text": candidates[i].text}
                    for i in idxs
                ],
            }
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
            count += 1
    return count


def main() -> None:
    repo_root = resolve_repo_root()

    parser = argparse.ArgumentParser(description="Cluster near-duplicate lessons by cosine similarity")
    parser.add_argument("-i", "--in-file", default=str(repo_root / "candidates.jsonl"))
    parser.add_argument("-o", "--out-file", default=str(repo_root / "clusters.jsonl"))
    parser.add_argument("--model-name", default="all-mpnet-base-v2")
    parser.add_argument("--threshold", type=float, default=0.88)
    parser.add_argument("--limit", type=int, default=None, help="Process only first N candidates")
    parser.add_argument("--mock", action="store_true", help="Use deterministic mock embeddings")
    args = parser.parse_args()

    in_path = resolve_path(repo_root, args.in_file)
    out_path = resolve_path(repo_root, args.out_file)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    candidates = load_candidates(in_path, args.limit)
    if not candidates:
        print("No candidates to cluster.")
        return

    texts = [c.text for c in candidates]
    embeddings = embed_texts(texts, args.model_name, args.mock)
    clusters = cluster_candidates(candidates, embeddings, args.threshold)
    total = write_clusters(out_path, candidates, clusters)
    print(f"✅ Wrote {total} clusters to {out_path}")


if __name__ == "__main__":
    main()



