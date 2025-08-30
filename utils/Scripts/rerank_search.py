#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import List, Tuple

import numpy as np
from sentence_transformers import CrossEncoder, SentenceTransformer


def load_index(npz_path: Path):
    data = np.load(str(npz_path), allow_pickle=True)
    emb: np.ndarray = data["embeddings"].astype("float32")
    ids: np.ndarray = data["ids"].astype("int32")
    texts = list(data["texts"])  # object array → list[str]
    model = str(data["model"]) if "model" in data.files else "intfloat/e5-small-v2"
    return emb, ids, texts, model


def retrieve_e5(query: str, emb: np.ndarray, model_name: str, topk: int) -> List[Tuple[int, float]]:
    # E5 asymmetric: prefix query and ensure L2 norm
    st = SentenceTransformer(model_name)
    q_vec = st.encode(["query: " + query], normalize_embeddings=True)[0].astype("float32")
    # emb assumed already normalized → cosine = dot
    scores = emb @ q_vec
    # argsort desc
    idx = np.argsort(-scores)[:topk]
    return [(int(i), float(scores[i])) for i in idx]


def rerank_pairs(query: str, candidates: List[str], ce_model: str, batch_size: int = 64) -> List[float]:
    ce = CrossEncoder(ce_model)
    pairs = [[query, c] for c in candidates]
    scores = ce.predict(pairs, batch_size=batch_size)
    return [float(s) for s in scores]


def main() -> None:
    p = argparse.ArgumentParser(description="Retrieve with E5 and rerank with CrossEncoder")
    p.add_argument("--query", required=True, help="User query text")
    p.add_argument("--emb", type=Path, default=Path("utils/Scripts/Embeddings/lessons_e5_small_v2.npz"))
    p.add_argument("--topk", type=int, default=200, help="Top-k to retrieve with E5")
    p.add_argument("--rerank", type=int, default=10, help="How many of retrieved to rerank")
    p.add_argument("--output", type=Path, help="Optional JSON output path for results")
    p.add_argument("--ce", default="cross-encoder/ms-marco-MiniLM-L-6-v2", help="CrossEncoder model id")
    args = p.parse_args()

    emb, ids, texts, model = load_index(args.emb)
    if emb.shape[0] != len(texts):
        raise SystemExit(f"embeddings count ({emb.shape[0]}) != texts count ({len(texts)})")

    # Retrieve
    hits = retrieve_e5(args.query, emb, model_name=model, topk=min(args.topk, emb.shape[0]))
    # Truncate to rerank N
    to_rr = hits[: min(args.rerank, len(hits))]
    cand_indices = [i for (i, _cos) in to_rr]
    cand_texts = [texts[i] for i in cand_indices]

    # Rerank
    ce_scores = rerank_pairs(args.query, cand_texts, ce_model=args.ce)
    combined = [
        {
            "rank_ce": None,  # to be assigned after sorting
            "rank_cos": r + 1,
            "id": int(ids[i]),
            "text": texts[i],
            "cosine": float(cos),
            "ce": float(ce_scores[r]),
        }
        for r, ((i, cos)) in enumerate(to_rr)
    ]
    # Sort by CE desc
    combined.sort(key=lambda x: x["ce"], reverse=True)
    for r, item in enumerate(combined, start=1):
        item["rank_ce"] = r

    # Print
    for item in combined:
        print(f"{item['rank_ce']:>2}. CE={item['ce']:+.4f}  cos={item['cosine']:+.4f}  {item['text']}")

    # Optional JSON output
    if args.output:
        args.output.write_text(json.dumps({
            "query": args.query,
            "model_retrieval": model,
            "model_rerank": args.ce,
            "results": combined,
        }, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
