#!/usr/bin/env python3
"""
Batch test: run all 72 emotion wheel leaf queries through E5 retrieval + CE rerank.
Outputs a JSON file with full results and a markdown summary for LLM analysis.

Usage:
    python batch_emotion_test.py
    python batch_emotion_test.py --topk 10 --rerank 5
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import List, Tuple

import numpy as np
from sentence_transformers import CrossEncoder, SentenceTransformer

# ---------- Emotion wheel: all 72 leaf nodes ----------

EMOTIONS = [
    # SAD
    ("Sad", "Lonely", "Isolated"),
    ("Sad", "Lonely", "Abandoned"),
    ("Sad", "Vulnerable", "Fragile"),
    ("Sad", "Vulnerable", "Victimized"),
    ("Sad", "Despair", "Powerless"),
    ("Sad", "Despair", "Grief"),
    ("Sad", "Guilty", "Remorse"),
    ("Sad", "Guilty", "Ashamed"),
    ("Sad", "Depressed", "Empty"),
    ("Sad", "Depressed", "Inferior"),
    ("Sad", "Hurt", "Let down"),
    ("Sad", "Hurt", "Agonized"),
    # MAD
    ("Mad", "Critical", "Skeptical"),
    ("Mad", "Critical", "Judging"),
    ("Mad", "Distant", "Withdrawn"),
    ("Mad", "Distant", "Numb"),
    ("Mad", "Frustrated", "Annoyed"),
    ("Mad", "Frustrated", "Bitter"),
    ("Mad", "Aggressive", "Hostile"),
    ("Mad", "Aggressive", "Furious"),
    ("Mad", "Hateful", "Rage"),
    ("Mad", "Hateful", "Violated"),
    ("Mad", "Hurt", "Jealous"),
    ("Mad", "Hurt", "Bashful"),
    # SCARED
    ("Scared", "Anxious", "Worried"),
    ("Scared", "Anxious", "Afraid"),
    ("Scared", "Insecure", "Inadequate"),
    ("Scared", "Insecure", "Inferior"),
    ("Scared", "Swamped", "Helpless"),
    ("Scared", "Swamped", "Small"),
    ("Scared", "Rejected", "Weak"),
    ("Scared", "Rejected", "Submissive"),
    ("Scared", "Confused", "Baffled"),
    ("Scared", "Confused", "Discouraged"),
    ("Scared", "Embarrassed", "Foolish"),
    ("Scared", "Embarrassed", "Shy"),
    # JOYFUL
    ("Joyful", "Playful", "Amused"),
    ("Joyful", "Playful", "Spirited"),
    ("Joyful", "Content", "Peaceful"),
    ("Joyful", "Content", "Pleasant"),
    ("Joyful", "Interested", "Curious"),
    ("Joyful", "Interested", "Inquisitive"),
    ("Joyful", "Proud", "Achieved"),
    ("Joyful", "Proud", "Confident"),
    ("Joyful", "Excited", "Eager"),
    ("Joyful", "Excited", "Energetic"),
    ("Joyful", "Cheerful", "Delightful"),
    ("Joyful", "Cheerful", "Optimistic"),
    # POWERFUL
    ("Powerful", "Respected", "Valuable"),
    ("Powerful", "Respected", "Valued"),
    ("Powerful", "Courageous", "Daring"),
    ("Powerful", "Courageous", "Bold"),
    ("Powerful", "Proud", "Achieved"),
    ("Powerful", "Proud", "Important"),
    ("Powerful", "Creative", "Ingenious"),
    ("Powerful", "Creative", "Versatile"),
    ("Powerful", "Aware", "Present"),
    ("Powerful", "Aware", "Focused"),
    ("Powerful", "Confident", "Capable"),
    ("Powerful", "Confident", "Secure"),
    # PEACEFUL
    ("Peaceful", "Thankful", "Grateful"),
    ("Peaceful", "Thankful", "Blessed"),
    ("Peaceful", "Loving", "Tender"),
    ("Peaceful", "Loving", "Empathic"),
    ("Peaceful", "Trusting", "Receptive"),
    ("Peaceful", "Trusting", "Patient"),
    ("Peaceful", "Nurturing", "Supportive"),
    ("Peaceful", "Nurturing", "Caring"),
    ("Peaceful", "Serene", "Calm"),
    ("Peaceful", "Serene", "Content"),
    ("Peaceful", "Hopeful", "Optimistic"),
    ("Peaceful", "Hopeful", "Inspired"),
]


def build_query(root: str, mid: str, leaf: str) -> str:
    """Build the same query string the iOS app sends."""
    return f"I feel {root} because I feel {mid}, because I feel {leaf}"


def load_index(npz_path: Path):
    data = np.load(str(npz_path), allow_pickle=True)
    emb = data["embeddings"].astype("float32")
    ids = data["ids"].astype("int32")
    texts = list(data["texts"])
    model = str(data["model"]) if "model" in data.files else "intfloat/e5-small-v2"
    return emb, ids, texts, model


def retrieve_e5(query: str, emb: np.ndarray, st_model: SentenceTransformer, topk: int) -> List[Tuple[int, float]]:
    q_vec = st_model.encode(["query: " + query], normalize_embeddings=True)[0].astype("float32")
    scores = emb @ q_vec
    idx = np.argsort(-scores)[:topk]
    return [(int(i), float(scores[i])) for i in idx]


def rerank_pairs(query: str, candidates: List[str], ce: CrossEncoder) -> List[float]:
    pairs = [[query, c] for c in candidates]
    scores = ce.predict(pairs, batch_size=64)
    return [float(s) for s in scores]


def main() -> None:
    p = argparse.ArgumentParser(description="Batch emotion wheel test")
    p.add_argument("--emb", type=Path,
                    default=Path(__file__).resolve().parent / "Embeddings" / "lessons_e5_small_v2.npz")
    p.add_argument("--topk", type=int, default=10, help="E5 retrieval top-k")
    p.add_argument("--rerank", type=int, default=5, help="How many to rerank with CE")
    p.add_argument("--ce", default="cross-encoder/ms-marco-MiniLM-L-6-v2", help="CrossEncoder model")
    p.add_argument("--out-dir", type=Path,
                    default=Path(__file__).resolve().parent / "outputs")
    args = p.parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)
    json_out = args.out_dir / "emotion_test_results.json"
    md_out = args.out_dir / "emotion_test_analysis.md"

    # Load models once
    print("Loading embedding index...")
    emb, ids, texts, model_name = load_index(args.emb)
    print(f"  {emb.shape[0]} lessons, dim={emb.shape[1]}, model={model_name}")

    print("Loading E5 retriever...")
    st = SentenceTransformer(model_name)

    print("Loading CrossEncoder reranker...")
    ce = CrossEncoder(args.ce)

    # Load lesson_units.json for verse mapping context
    units_path = Path(__file__).resolve().parent.parent.parent / \
        "Bhagavad-Gita-Verses-iOS-App" / "Shared" / "Inference" / "swift" / "lesson_units.json"
    lesson_units = []
    if units_path.exists():
        with open(units_path) as f:
            lesson_units = json.load(f)
        print(f"  Loaded {len(lesson_units)} lesson unit mappings")

    all_results = []
    category_scores = {}

    print(f"\nRunning {len(EMOTIONS)} emotion queries (topk={args.topk}, rerank={args.rerank})...\n")

    for i, (root, mid, leaf) in enumerate(EMOTIONS):
        query = build_query(root, mid, leaf)
        label = f"{root} > {mid} > {leaf}"
        print(f"  [{i+1:>2}/{len(EMOTIONS)}] {label}")

        # Retrieve
        hits = retrieve_e5(query, emb, st, topk=args.topk)

        # Rerank top N
        to_rr = hits[:min(args.rerank, len(hits))]
        cand_indices = [idx for (idx, _) in to_rr]
        cand_texts = [texts[idx] for idx in cand_indices]
        ce_scores = rerank_pairs(query, cand_texts, ce)

        results = []
        for r, ((idx, cos), ce_s) in enumerate(zip(to_rr, ce_scores)):
            units = []
            if idx < len(lesson_units):
                units = lesson_units[idx].get("units", [])
            results.append({
                "lesson_id": int(ids[idx]),
                "lesson_text": texts[idx],
                "cosine": round(cos, 4),
                "ce_score": round(ce_s, 4),
                "verse_units": units,
            })

        # Sort by CE score
        results.sort(key=lambda x: x["ce_score"], reverse=True)
        for r, item in enumerate(results):
            item["rank_ce"] = r + 1

        entry = {
            "emotion_path": label,
            "root": root,
            "mid": mid,
            "leaf": leaf,
            "query": query,
            "top_cosine": round(hits[0][1], 4) if hits else None,
            "top_ce": round(results[0]["ce_score"], 4) if results else None,
            "results": results,
        }
        all_results.append(entry)

        # Track per-category
        if root not in category_scores:
            category_scores[root] = {"cos": [], "ce": []}
        if hits:
            category_scores[root]["cos"].append(hits[0][1])
        if results:
            category_scores[root]["ce"].append(results[0]["ce_score"])

    # ---------- Write JSON ----------
    with open(json_out, "w") as f:
        json.dump({"config": {"topk": args.topk, "rerank": args.rerank,
                               "retrieval_model": model_name, "rerank_model": args.ce},
                    "results": all_results}, f, indent=2, ensure_ascii=False)
    print(f"\nJSON results: {json_out}")

    # ---------- Write Markdown ----------
    with open(md_out, "w") as f:
        f.write("# Emotion Wheel → Lesson Search: Test Results\n\n")
        f.write(f"**Config:** E5 top-{args.topk} retrieval → CE rerank top-{args.rerank}\n\n")
        f.write(f"**Models:** `{model_name}` (retrieval) + `{args.ce}` (rerank)\n\n")
        f.write(f"**Corpus:** {emb.shape[0]} lesson texts\n\n")
        f.write("---\n\n")

        # Category summary
        f.write("## Category Summary\n\n")
        f.write("| Category | Avg Top Cosine | Avg Top CE | Min CE | Max CE | Count |\n")
        f.write("|----------|---------------|-----------|--------|--------|-------|\n")
        for cat in ["Sad", "Mad", "Scared", "Joyful", "Powerful", "Peaceful"]:
            if cat in category_scores:
                cs = category_scores[cat]
                avg_cos = np.mean(cs["cos"]) if cs["cos"] else 0
                avg_ce = np.mean(cs["ce"]) if cs["ce"] else 0
                min_ce = min(cs["ce"]) if cs["ce"] else 0
                max_ce = max(cs["ce"]) if cs["ce"] else 0
                f.write(f"| {cat} | {avg_cos:.4f} | {avg_ce:.4f} | {min_ce:.4f} | {max_ce:.4f} | {len(cs['ce'])} |\n")
        f.write("\n---\n\n")

        # Per-emotion details
        f.write("## Per-Emotion Results\n\n")
        current_root = None
        for entry in all_results:
            if entry["root"] != current_root:
                current_root = entry["root"]
                f.write(f"### {current_root.upper()}\n\n")

            f.write(f"#### {entry['emotion_path']}\n")
            f.write(f"**Query:** `{entry['query']}`\n\n")
            f.write(f"**Top cosine:** {entry['top_cosine']}  |  **Top CE:** {entry['top_ce']}\n\n")
            f.write("| Rank (CE) | CE Score | Cosine | Lesson | Verses |\n")
            f.write("|-----------|---------|--------|--------|--------|\n")
            for r in entry["results"]:
                units_str = ", ".join(
                    f"{u['chapter']}:{u['start']}-{u['end']}" for u in r["verse_units"]
                ) if r["verse_units"] else "—"
                f.write(f"| {r['rank_ce']} | {r['ce_score']:+.4f} | {r['cosine']:.4f} | "
                        f"{r['lesson_text'][:80]} | {units_str} |\n")
            f.write("\n")

        # Duplicate detection
        f.write("---\n\n## Differentiation Analysis\n\n")
        f.write("Emotion pairs where the #1 CE-ranked lesson is identical:\n\n")
        seen = {}
        dupes = []
        for entry in all_results:
            if entry["results"]:
                top_id = entry["results"][0]["lesson_id"]
                if top_id in seen:
                    dupes.append((seen[top_id], entry["emotion_path"], top_id,
                                  entry["results"][0]["lesson_text"]))
                else:
                    seen[top_id] = entry["emotion_path"]

        if dupes:
            f.write("| Emotion A | Emotion B | Shared Lesson ID | Lesson Text |\n")
            f.write("|-----------|-----------|-----------------|-------------|\n")
            for a, b, lid, ltxt in dupes:
                f.write(f"| {a} | {b} | {lid} | {ltxt[:60]} |\n")
        else:
            f.write("No duplicates found — all emotions map to different top lessons.\n")

        f.write("\n---\n\n")
        f.write("## Notes for LLM Analysis\n\n")
        f.write("When reviewing these results, consider:\n")
        f.write("1. **Relevance:** Does the top lesson make sense for someone feeling this emotion?\n")
        f.write("2. **Differentiation:** Do similar emotions (e.g., Isolated vs Abandoned) get meaningfully different lessons?\n")
        f.write("3. **Positive vs Negative:** Do positive emotions (Joyful, Peaceful) get affirming lessons vs corrective ones?\n")
        f.write("4. **Score gaps:** Large CE score drops from #1 to #2 suggest strong matches; flat scores suggest ambiguity.\n")
        f.write("5. **Query format:** The query is `I feel X because I feel Y, because I feel Z` — consider if this phrasing helps or hurts semantic matching.\n")

    print(f"Markdown summary: {md_out}")
    print("\nDone! Feed the markdown file to an LLM for qualitative analysis.")


if __name__ == "__main__":
    main()
