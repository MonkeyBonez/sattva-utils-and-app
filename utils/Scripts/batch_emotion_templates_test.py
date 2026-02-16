#!/usr/bin/env python3
"""
Query-rewriting comparison: run all 72 emotion wheel leaf queries through multiple
query templates (no model/corpus changes) and output side-by-side analysis.

Templates:
  - Current:  "I feel Sad because I feel Lonely, because I feel Isolated"
  - Option A: "I feel lonely and isolated, how do I find peace and overcome sadness"
  - Option B: "overcome loneliness and isolation" (drop "I feel" entirely)
  - Option C: Category-aware (negative → overcome/cope, positive → cultivate/deepen)

Outputs to Scripts/outputs/:
  - template_comparison_results.json — full results per template
  - template_comparison_analysis.md  — category summaries, side-by-side tables, agreement

Usage:
    python batch_emotion_templates_test.py
    python batch_emotion_templates_test.py --topk 10 --rerank 5
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import List, Tuple, Dict

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

# ---------- Negative vs positive roots ----------
NEGATIVE_ROOTS = {"Sad", "Mad", "Scared"}
POSITIVE_ROOTS = {"Joyful", "Powerful", "Peaceful"}

# ---------- Query templates (query rewriting only; no model/corpus changes) ----------

def template_current(root: str, mid: str, leaf: str) -> str:
    """Current – iOS app format: I feel X because I feel Y, because I feel Z."""
    return f"I feel {root} because I feel {mid}, because I feel {leaf}"

def template_option_a(root: str, mid: str, leaf: str) -> str:
    """Option A – Bridge to solution: I feel X and Y, how do I find peace and overcome Z."""
    return f"I feel {leaf.lower()} and {mid.lower()}, how do I find peace and overcome {root.lower()}"

def template_option_b(root: str, mid: str, leaf: str) -> str:
    """Option B – Drop 'I feel': solution phrase only (overcome X and Y)."""
    return f"overcome {mid.lower()} and {leaf.lower()}"

def template_option_c(root: str, mid: str, leaf: str) -> str:
    """Option C – Category-aware: negative → overcome/cope, positive → cultivate/deepen."""
    if root in NEGATIVE_ROOTS:
        return f"overcome {mid.lower()} and {leaf.lower()}, cope with {root.lower()}"
    else:
        return f"cultivate {mid.lower()} and {leaf.lower()}, deepen {root.lower()}"

TEMPLATES = {
    "Current": template_current,
    "Option_A": template_option_a,
    "Option_B": template_option_b,
    "Option_C": template_option_c,
}


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


def run_query(query: str, emb, ids, texts, st, ce, topk: int, rerank: int, lesson_units: list) -> dict:
    hits = retrieve_e5(query, emb, st, topk=topk)
    to_rr = hits[:min(rerank, len(hits))]
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

    results.sort(key=lambda x: x["ce_score"], reverse=True)
    for r, item in enumerate(results):
        item["rank_ce"] = r + 1

    return {
        "query": query,
        "top_cosine": round(hits[0][1], 4) if hits else None,
        "top_ce": round(results[0]["ce_score"], 4) if results else None,
        "top_lesson": results[0]["lesson_text"] if results else None,
        "top_lesson_id": results[0]["lesson_id"] if results else None,
        "results": results,
    }


def main() -> None:
    p = argparse.ArgumentParser(description="Compare query templates for emotion wheel")
    p.add_argument("--emb", type=Path,
                    default=Path(__file__).resolve().parent / "Embeddings" / "lessons_e5_small_v2.npz")
    p.add_argument("--topk", type=int, default=10)
    p.add_argument("--rerank", type=int, default=5)
    p.add_argument("--ce", default="cross-encoder/ms-marco-MiniLM-L-6-v2")
    p.add_argument("--out-dir", type=Path,
                    default=Path(__file__).resolve().parent / "outputs")
    args = p.parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)
    json_out = args.out_dir / "template_comparison_results.json"
    md_out = args.out_dir / "template_comparison_analysis.md"

    print("Loading models...")
    emb, ids, texts, model_name = load_index(args.emb)
    st = SentenceTransformer(model_name)
    ce = CrossEncoder(args.ce)

    units_path = Path(__file__).resolve().parent.parent.parent / \
        "Bhagavad-Gita-Verses-iOS-App" / "Shared" / "Inference" / "swift" / "lesson_units.json"
    lesson_units = []
    if units_path.exists():
        with open(units_path) as f:
            lesson_units = json.load(f)

    total_queries = len(EMOTIONS) * len(TEMPLATES)
    print(f"Running {len(EMOTIONS)} emotions x {len(TEMPLATES)} templates = {total_queries} queries...\n")

    # {template_name: {category: [top_ce_scores]}}
    cat_scores: Dict[str, Dict[str, list]] = {t: {} for t in TEMPLATES}
    # Full per-emotion results
    all_data: Dict[str, list] = {t: [] for t in TEMPLATES}
    counter = 0

    for root, mid, leaf in EMOTIONS:
        label = f"{root} > {mid} > {leaf}"
        for tname, tfunc in TEMPLATES.items():
            counter += 1
            query = tfunc(root, mid, leaf)
            result = run_query(query, emb, ids, texts, st, ce, args.topk, args.rerank, lesson_units)
            result["emotion_path"] = label
            result["root"] = root
            result["template"] = tname
            all_data[tname].append(result)

            if root not in cat_scores[tname]:
                cat_scores[tname][root] = []
            if result["top_ce"] is not None:
                cat_scores[tname][root].append(result["top_ce"])

        print(f"  [{counter // len(TEMPLATES):>2}/{len(EMOTIONS)}] {label}")

    # ---------- Write JSON ----------
    with open(json_out, "w") as f:
        json.dump({"config": {"topk": args.topk, "rerank": args.rerank},
                    "templates": {k: v.__doc__.strip() for k, v in TEMPLATES.items()},
                    "results_by_template": all_data}, f, indent=2, ensure_ascii=False)
    print(f"\nJSON: {json_out}")

    # ---------- Write Markdown ----------
    cats_order = ["Sad", "Mad", "Scared", "Joyful", "Powerful", "Peaceful"]
    tmpl_order = list(TEMPLATES.keys())

    with open(md_out, "w") as f:
        f.write("# Query Template Comparison: Emotion Wheel\n\n")
        f.write(f"**{len(EMOTIONS)} emotions x {len(TEMPLATES)} templates = {total_queries} queries**\n\n")

        # Template descriptions
        f.write("## Templates Tested\n\n")
        f.write("| ID | Description | Example (Sad > Lonely > Isolated) |\n")
        f.write("|----|-------------|-----------------------------------|\n")
        for tname, tfunc in TEMPLATES.items():
            example = tfunc("Sad", "Lonely", "Isolated")
            f.write(f"| {tname} | {tfunc.__doc__.strip()} | `{example}` |\n")
        f.write("\n---\n\n")

        # Category x Template summary
        f.write("## Category Summary: Avg Top CE Score by Template\n\n")
        f.write("Higher (less negative) = better match confidence.\n\n")
        header = "| Category | " + " | ".join(tmpl_order) + " | Best |\n"
        sep = "|----------|" + "|".join(["------" for _ in tmpl_order]) + "|------|\n"
        f.write(header)
        f.write(sep)
        for cat in cats_order:
            row = f"| **{cat}** |"
            avgs = {}
            for t in tmpl_order:
                scores = cat_scores[t].get(cat, [])
                avg = np.mean(scores) if scores else float("-inf")
                avgs[t] = avg
                row += f" {avg:.2f} |"
            best = max(avgs, key=lambda k: avgs[k])
            row += f" **{best}** |\n"
            f.write(row)

        # Overall average
        f.write("| **OVERALL** |")
        overall_avgs = {}
        for t in tmpl_order:
            all_scores = []
            for cat in cats_order:
                all_scores.extend(cat_scores[t].get(cat, []))
            avg = np.mean(all_scores) if all_scores else float("-inf")
            overall_avgs[t] = avg
            f.write(f" {avg:.2f} |")
        best_overall = max(overall_avgs, key=lambda k: overall_avgs[k])
        f.write(f" **{best_overall}** |\n")

        # Negative-only average
        f.write("| **NEG ONLY** |")
        neg_avgs = {}
        for t in tmpl_order:
            neg_scores = []
            for cat in NEGATIVE_ROOTS:
                neg_scores.extend(cat_scores[t].get(cat, []))
            avg = np.mean(neg_scores) if neg_scores else float("-inf")
            neg_avgs[t] = avg
            f.write(f" {avg:.2f} |")
        best_neg = max(neg_avgs, key=lambda k: neg_avgs[k])
        f.write(f" **{best_neg}** |\n")
        f.write("\n---\n\n")

        # Duplicate counts per template
        f.write("## Differentiation: Duplicate Top-Lesson Count per Template\n\n")
        f.write("Lower = more variety across emotions.\n\n")
        f.write("| Template | Unique Top Lessons | Duplicate Pairs |\n")
        f.write("|----------|-------------------|----------------|\n")
        for t in tmpl_order:
            seen = {}
            dupe_count = 0
            for entry in all_data[t]:
                if entry["top_lesson_id"] is not None:
                    lid = entry["top_lesson_id"]
                    if lid in seen:
                        dupe_count += 1
                    else:
                        seen[lid] = True
            f.write(f"| {t} | {len(seen)} | {dupe_count} |\n")
        f.write("\n---\n\n")

        # Template agreement: same top lesson across templates
        f.write("## Template Agreement: Same Top Lesson\n\n")
        f.write("For each emotion, how often do templates pick the same #1 lesson? "
                "Rows = emotions; checkmarks = template pair agrees.\n\n")
        # Build per-emotion list of (label, [lid_current, lid_a, lid_b, lid_c])
        emotion_labels = [f"{r} > {m} > {l}" for (r, m, l) in EMOTIONS]
        agree_all = 0
        for i, label in enumerate(emotion_labels):
            lids = []
            for t in tmpl_order:
                entry = next(e for e in all_data[t] if e["emotion_path"] == label)
                lids.append(entry.get("top_lesson_id"))
            if len(set(lids) - {None}) <= 1:
                agree_all += 1
        f.write(f"**Emotions where all 4 templates share the same top lesson:** {agree_all} / {len(EMOTIONS)}\n\n")
        # Pairwise agreement counts
        f.write("| Template A | Template B | Same top lesson (count) |\n")
        f.write("|------------|------------|--------------------------|\n")
        for ia, ta in enumerate(tmpl_order):
            for ib, tb in enumerate(tmpl_order):
                if ia >= ib:
                    continue
                count = 0
                for label in emotion_labels:
                    ea = next(e for e in all_data[ta] if e["emotion_path"] == label)
                    eb = next(e for e in all_data[tb] if e["emotion_path"] == label)
                    if ea.get("top_lesson_id") == eb.get("top_lesson_id") and ea.get("top_lesson_id") is not None:
                        count += 1
                f.write(f"| {ta} | {tb} | {count} |\n")
        f.write("\n---\n\n")

        # Compact side-by-side: every emotion, CE score per template
        f.write("## Side-by-Side: All Emotions (Top CE Score per Template)\n\n")
        f.write("| Emotion | " + " | ".join(tmpl_order) + " | Best |\n")
        f.write("|---------|" + "|".join(["--------" for _ in tmpl_order]) + "|------|\n")
        for label in emotion_labels:
            row = f"| {label} |"
            best_ce = float("-inf")
            best_t = None
            for t in tmpl_order:
                entry = next(e for e in all_data[t] if e["emotion_path"] == label)
                ce = entry["top_ce"]
                if ce is not None and ce > best_ce:
                    best_ce = ce
                    best_t = t
                row += f" {ce:+.2f} |" if ce is not None else " — |"
            row += f" **{best_t}** |\n" if best_t else " — |\n"
            f.write(row)
        f.write("\n---\n\n")

        # Per-emotion comparison: show all templates side by side for negative emotions
        f.write("## Head-to-Head: Negative Emotions (Top Lesson per Template)\n\n")
        f.write("Showing the #1 CE-ranked lesson for each template, for all Sad/Mad/Scared emotions.\n\n")
        for root, mid, leaf in EMOTIONS:
            if root not in NEGATIVE_ROOTS:
                continue
            label = f"{root} > {mid} > {leaf}"
            f.write(f"### {label}\n\n")
            f.write("| Template | CE Score | Query | Top Lesson |\n")
            f.write("|----------|---------|-------|------------|\n")
            for t in tmpl_order:
                entry = next(e for e in all_data[t] if e["emotion_path"] == label)
                f.write(f"| {t} | {entry['top_ce']:+.2f} | `{entry['query'][:60]}` | "
                        f"{entry['top_lesson'][:70]} |\n")
            f.write("\n")

        f.write("---\n\n")
        f.write("## Recommendation\n\n")
        f.write("Compare the avg CE scores above to decide which template to ship.\n")
        f.write("Key questions:\n")
        f.write("1. Which template has the best **negative emotion** scores (Sad/Mad/Scared)?\n")
        f.write("2. Does the winning template hurt positive emotion scores?\n")
        f.write("3. Does the winning template produce more differentiated (unique) top lessons?\n")
        f.write("4. Do the actual top lessons for negative emotions feel more relevant?\n")

    print(f"Markdown: {md_out}")
    print("\nDone!")


if __name__ == "__main__":
    main()
