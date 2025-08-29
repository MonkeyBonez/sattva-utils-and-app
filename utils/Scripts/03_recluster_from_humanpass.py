#!/usr/bin/env python3
"""
03_recluster_from_humanpass.py — recluster curated reps by their text

Input: JSONL where each row is the human-curated representative per cluster:
  {"cluster_id": <int>, "lesson_id": <str>, "text": <str>, ...}

This script ignores prior cluster_ids and re-clusters FROM SCRATCH based on
the "text" field only. Output mirrors 02_cluster_duplicates.py format:

  {"cluster_id": <int>, "candidates": [{"lesson_id": <str>, "text": <str>}, ...]}

Notes:
- Deterministic greedy single-linkage by cosine similarity, given input order
- Embeddings: mock (MD5-hash-based) by default; sentence-transformers optional
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional


def resolve_repo_root() -> Path:
    # utils/Scripts/ → parents[2] should be the workspace root
    return Path(__file__).resolve().parents[2]


def resolve_path(repo_root: Path, path_str: str) -> Path:
    p = Path(path_str)
    return p if p.is_absolute() else (repo_root / p).resolve()


def l2_normalize(vec: List[float]) -> List[float]:
    s = math.sqrt(sum(v * v for v in vec))
    return [v / s for v in vec] if s > 0 else vec


def cos_sim(a: List[float], b: List[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


def hash_to_vec(text: str, dim: int = 384) -> List[float]:
    digest = hashlib.md5(text.strip().lower().encode("utf-8")).digest()
    vec: List[float] = []
    seed_bytes = digest
    while len(vec) < dim:
        seed_bytes = hashlib.md5(seed_bytes).digest()
        for b in seed_bytes:
            vec.append((b / 255.0) - 0.5)
            if len(vec) == dim:
                break
    return l2_normalize(vec)


@dataclass
class Candidate:
    old_cluster_id: int
    text: str


def load_rows(path: Path) -> List[Candidate]:
    rows: List[Candidate] = []
    with path.open("r", encoding="utf-8") as f:
        for idx, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            # Expect at least cluster_id + text; ignore any prior lesson_id for output
            if "cluster_id" not in obj or "text" not in obj:
                raise ValueError(f"Line {idx}: missing cluster_id/text")
            old_cid = int(obj["cluster_id"]) if isinstance(obj["cluster_id"], (int, str)) else None
            if old_cid is None:
                raise ValueError(f"Line {idx}: invalid cluster_id")
            text = str(obj["text"]) or ""
            if not text:
                raise ValueError(f"Line {idx}: empty text")
            rows.append(Candidate(old_cluster_id=int(old_cid), text=text))
    return rows


def embed_texts(texts: List[str], *, model_name: str, mock: bool) -> List[List[float]]:
    if mock:
        return [hash_to_vec(t) for t in texts]
    try:
        from sentence_transformers import SentenceTransformer  # type: ignore
    except Exception as e:
        raise RuntimeError(
            "sentence-transformers not available. Install it or pass --mock"
        ) from e
    model = SentenceTransformer(model_name)
    emb = model.encode(texts, normalize_embeddings=True, show_progress_bar=False)
    return [list(map(float, v)) for v in emb]


def greedy_single_linkage(embeddings: List[List[float]], threshold: float) -> List[List[int]]:
    clusters: List[List[int]] = []
    for i, emb in enumerate(embeddings):
        placed = False
        for cluster in clusters:
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
                    {"old_cluster_id": candidates[i].old_cluster_id, "text": candidates[i].text}
                    for i in idxs
                ],
            }
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
            count += 1
    return count


def parse_args() -> argparse.Namespace:
    repo_root = resolve_repo_root()
    default_in = repo_root / "utils/Scripts/outputs/clusters_humanpass1.jsonl"
    default_out = repo_root / "utils/Scripts/outputs/clusters_B_recluster.jsonl"

    p = argparse.ArgumentParser(description="Recluster curated reps by text from scratch")
    p.add_argument("-i", "--in-file", default=str(default_in))
    p.add_argument("-o", "--out-file", default=str(default_out))
    p.add_argument("--model-name", default="all-mpnet-base-v2")
    p.add_argument("--threshold", type=float, default=0.83)
    p.add_argument("--mock", action="store_true", help="Use deterministic mock embeddings")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    repo_root = resolve_repo_root()
    in_path = resolve_path(repo_root, args.in_file)
    out_path = resolve_path(repo_root, args.out_file)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    candidates = load_rows(in_path)
    if not candidates:
        print("No rows found in input.")
        return

    texts = [c.text for c in candidates]
    embeddings = embed_texts(texts, model_name=args.model_name, mock=args.mock)
    clusters = greedy_single_linkage(embeddings, threshold=args.threshold)
    total = write_clusters(out_path, candidates, clusters)
    print(f"✅ Wrote {total} clusters to {out_path}")


if __name__ == "__main__":
    main()


