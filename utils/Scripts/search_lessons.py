#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer


MODEL_NAME = "intfloat/e5-small-v2"


def load_index(path: Path) -> dict:
    if not path.exists():
        raise SystemExit(f"Index not found: {path}")
    data = dict(np.load(path, allow_pickle=True))
    required = {"embeddings", "ids", "texts", "model"}
    missing = required - set(data.keys())
    if missing:
        raise SystemExit(f"Index missing keys: {sorted(missing)}")
    if data["model"].item() != MODEL_NAME:
        raise SystemExit(
            f"Model mismatch: index has {data['model'].item()}, expected {MODEL_NAME}. Rebuild.")
    emb = data["embeddings"]
    if emb.ndim != 2 or emb.shape[1] != 384:
        raise SystemExit(f"Unexpected embedding shape: {emb.shape}")
    return data


def main() -> None:
    parser = argparse.ArgumentParser(description="Search lessons with E5 embeddings")
    parser.add_argument("query", type=str, help="User query text")
    parser.add_argument(
        "--emb-path",
        type=Path,
        default=Path(__file__).resolve().parent / "Embeddings" / "lessons_e5_small_v2.npz",
        help="Embeddings .npz path (default: utils/Scripts/Embeddings/lessons_e5_small_v2.npz)",
    )
    parser.add_argument("--topk", type=int, default=10)
    args = parser.parse_args()

    index = load_index(args.emb_path)
    emb = np.asarray(index["embeddings"], dtype=np.float32)
    texts = list(index["texts"])  # object array

    model = SentenceTransformer(MODEL_NAME)
    query_vec = model.encode([f"query: {args.query}"], normalize_embeddings=True)
    query_vec = np.asarray(query_vec, dtype=np.float32)[0]  # (384,)

    scores = emb @ query_vec  # cosine because pre-normalized
    order = np.argsort(-scores)[: args.topk]

    for rank, idx in enumerate(order, start=1):
        print(f"{rank:>2}. {scores[idx]:+.4f}  {texts[idx][:120]}")


if __name__ == "__main__":
    main()




