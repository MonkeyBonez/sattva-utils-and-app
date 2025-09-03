#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import List, Dict, Tuple, Optional

import numpy as np
from sentence_transformers import SentenceTransformer


MODEL = "intfloat/e5-small-v2"


def load_emb_index(npz_path: Path) -> Tuple[np.ndarray, List[str]]:
    data = np.load(str(npz_path), allow_pickle=True)
    emb: np.ndarray = data["embeddings"].astype("float32")
    texts: List[str] = list(data["texts"])  # object array to list[str]
    return emb, texts


def load_units(units_path: Path) -> List[dict]:
    return json.loads(units_path.read_text(encoding="utf-8"))


def load_verse_map(map_path: Path) -> Dict[str, int]:
    return json.loads(map_path.read_text(encoding="utf-8"))


def encode_query(text: str, model: SentenceTransformer) -> np.ndarray:
    v = model.encode([f"query: {text}"], normalize_embeddings=True)[0]
    return np.asarray(v, dtype=np.float32)


def unit_key(ch: int, v: int) -> str:
    return f"{ch}:{v}"


def parse_iso8601(s: str) -> Optional[datetime]:
    try:
        # Support 'Z' and offsets
        if s.endswith('Z'):
            s = s[:-1] + '+00:00'
        return datetime.fromisoformat(s)
    except Exception:
        return None


def load_shown_filter(path: Optional[Path], horizon_days: float) -> Dict[int, datetime]:
    out: Dict[int, datetime] = {}
    if not path or not path.exists():
        return out
    try:
        arr = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return out
    cutoff = datetime.now(timezone.utc) - timedelta(days=horizon_days)
    for item in arr:
        idx = item.get("index")
        ts = item.get("ts")
        if idx is None or ts is None:
            continue
        dt = parse_iso8601(str(ts))
        if dt is None:
            continue
        dt = dt.astimezone(timezone.utc)
        if dt >= cutoff:
            out[int(idx)] = dt
    return out


def build_bookmark_lessons_with_weights(
    bookmarks: List[str],
    bookmarks_json: Optional[Path],
    verse_to_lesson: Dict[str, int],
    tau_days: float,
    w_min: float,
) -> Tuple[List[int], Dict[int, float]]:
    # Collect per-lesson most recent timestamp
    lesson_to_ts: Dict[int, datetime] = {}
    if bookmarks_json and bookmarks_json.exists():
        arr = json.loads(bookmarks_json.read_text(encoding="utf-8"))
        for item in arr:
            v = str(item.get("verse", ""))
            ts = item.get("ts")
            if v in verse_to_lesson and ts:
                dt = parse_iso8601(str(ts))
                if dt is None:
                    continue
                dt = dt.astimezone(timezone.utc)
                lid = int(verse_to_lesson[v])
                prev = lesson_to_ts.get(lid)
                if prev is None or dt > prev:
                    lesson_to_ts[lid] = dt
    else:
        # No timestamps provided; assign equal weights later
        for v in bookmarks:
            if v in verse_to_lesson:
                lid = int(verse_to_lesson[v])
                # Use a synthetic same-time for all to make weights equal
                lesson_to_ts[lid] = datetime.now(timezone.utc)

    # Build ordered unique lesson list preserving appearance order from CLI bookmarks (when provided)
    ordered: List[int] = []
    seen = set()
    # First honor CLI order
    for v in bookmarks:
        if v in verse_to_lesson:
            lid = int(verse_to_lesson[v])
            if lid not in seen:
                seen.add(lid); ordered.append(lid)
    # Then include any from JSON not already included
    for lid in lesson_to_ts.keys():
        if lid not in seen:
            seen.add(lid); ordered.append(lid)

    # Compute weights
    weights: Dict[int, float] = {}
    if not lesson_to_ts:
        return ordered, {lid: 1.0 for lid in ordered}
    now = max(lesson_to_ts.values())  # anchor to most recent bookmark timestamp
    tau = max(tau_days, 1e-3) * 86400.0  # seconds
    for lid, ts in lesson_to_ts.items():
        dt = max(0.0, (now - ts).total_seconds())
        w = float(np.exp(-dt / tau))
        if w_min is not None:
            w = max(w, float(w_min))
        weights[lid] = w
    # Normalize
    s = sum(weights.values())
    if s > 0:
        for lid in list(weights.keys()):
            weights[lid] = weights[lid] / s
    return ordered, weights


def recommend_from_bookmarks(
    bookmark_lessons: List[int],
    weights: Dict[int, float],
    emb: np.ndarray,
    texts: List[str],
    exclude_same: bool,
    min_cos: float,
    max_similar: float,
    topk_per_seed: int,
    overall_topk: int,
    combine: str = "max",
) -> List[Tuple[int, float]]:
    # Build centroid (or per-seed queries) and score
    # Strategy: gather candidates from each seed's topk, then filter by similarity to any seed > max_similar
    model = SentenceTransformer(MODEL)
    all_candidates: Dict[int, float] = {}
    for seed in bookmark_lessons:
        seed_text = texts[seed]
        q = encode_query(seed_text, model)
        scores = emb @ q
        order = np.argsort(-scores)
        taken = 0
        for idx in order:
            if exclude_same and int(idx) in bookmark_lessons:
                continue
            s = float(scores[idx])
            if s < min_cos:
                break
            w = float(weights.get(int(seed), 1.0))
            contrib = w * s
            if combine == "sum":
                all_candidates[int(idx)] = all_candidates.get(int(idx), 0.0) + contrib
            else:
                all_candidates[int(idx)] = max(all_candidates.get(int(idx), -1.0), contrib)
            taken += 1
            if taken >= topk_per_seed:
                break
    # Filter overly similar to any seed (use cosine between text embeddings already normalized)
    seeds = np.stack([emb[i] for i in bookmark_lessons], axis=0) if bookmark_lessons else np.zeros((0, emb.shape[1]), dtype=np.float32)
    filtered: List[Tuple[int, float]] = []
    for idx, s in all_candidates.items():
        if exclude_same and idx in bookmark_lessons:
            continue
        if seeds.shape[0] > 0:
            sims = seeds @ emb[int(idx)]
            if float(np.max(sims)) > max_similar:
                continue
        filtered.append((int(idx), float(s)))
    filtered.sort(key=lambda x: x[1], reverse=True)
    return filtered[:overall_topk]


def main() -> None:
    ap = argparse.ArgumentParser(description="Simulate next-lesson recommendations from bookmarks")
    ap.add_argument("--bookmarks", nargs="*", help="List of verse keys like '17:8'", default=[])
    ap.add_argument("--bookmarks-json", type=Path, help="Optional JSON file: [{verse:""C:V"", ts:""ISO8601""}] for recency weighting")
    ap.add_argument("--units", type=Path, default=Path("utils/Scripts/outputs/lesson_units.json"))
    ap.add_argument("--verse-map", type=Path, default=Path("utils/Scripts/outputs/verse_to_lesson.json"))
    ap.add_argument("--emb", type=Path, default=Path("utils/Scripts/Embeddings/lessons_e5_small_v2.npz"))
    ap.add_argument("--min-cos", type=float, default=0.25)
    ap.add_argument("--max-similar", type=float, default=0.90, help="Max cosine similarity to any seed to avoid near-duplicates")
    ap.add_argument("--topk-per-seed", type=int, default=50)
    ap.add_argument("--overall-topk", type=int, default=10)
    ap.add_argument("--exclude-same", action="store_true", default=True)
    ap.add_argument("--tau-days", type=float, default=7.0, help="Recency decay time constant in days")
    ap.add_argument("--w-min", type=float, default=0.2, help="Minimum weight floor per seed before normalization")
    ap.add_argument("--combine", choices=["max", "sum"], default="max", help="Combine contributions across seeds: max or sum")
    ap.add_argument("--random-pick-threshold", type=float, default=-1.0, help="If >0, randomly pick one cand with score >= threshold from the returned list")
    ap.add_argument("--random-seed", type=int, help="Optional RNG seed for reproducible random pick")
    # Goldilocks (single-candidate) mode using stored embeddings only (no model encoding)
    ap.add_argument("--one-goldilocks", action="store_true", help="Pick one candidate in a percentile band of max-to-seed similarity")
    ap.add_argument("--band-low-pct", type=float, default=70.0, help="Lower percentile for goldilocks band (0-100)")
    ap.add_argument("--band-high-pct", type=float, default=90.0, help="Upper percentile for goldilocks band (0-100)")
    ap.add_argument("--shown-json", type=Path, help="Optional JSON file of shown lessons [{index:int, ts:ISO8601}] to avoid repeats")
    ap.add_argument("--no-repeat-days", type=float, default=180.0, help="Do not repeat lessons shown within this many days")
    # Clustered mode
    ap.add_argument("--clustered-goldilocks", action="store_true", help="Cluster seed lessons (k=2–3) and pick one per cluster by Goldilocks band vs centroid")
    ap.add_argument("--k", type=int, default=2, help="Number of clusters for seeds (auto-capped to number of seeds)")
    ap.add_argument("--topm-per-cluster", type=int, default=200, help="Gather top-M nearest to centroid before banding")
    ap.add_argument("--json-out", type=Path, help="Optional JSON output file")
    args = ap.parse_args()

    emb, texts = load_emb_index(args.emb)
    verse_map = load_verse_map(args.verse_map)
    units = load_units(args.units)  # not directly used yet, but available for future tuning

    bookmark_lessons, weights = build_bookmark_lessons_with_weights(
        bookmarks=args.bookmarks,
        bookmarks_json=args.bookmarks_json,
        verse_to_lesson=verse_map,
        tau_days=args.tau_days,
        w_min=args.w_min,
    )
    recs: List[Tuple[int, float]]
    goldilocks_pick: Dict[str, object] | None = None
    if args.one_goldilocks:
        # Use stored lesson embeddings for seeds and candidates
        if not bookmark_lessons:
            print("No seeds from bookmarks. Exiting.")
            recs = []
        else:
            seeds_emb = np.stack([emb[i] for i in bookmark_lessons], axis=0)  # [S, D]
            # max-to-seed cosine for every candidate
            sims = seeds_emb @ emb.T  # [S, N]
            max_s = sims.max(axis=0)  # [N]
            mask = np.ones(emb.shape[0], dtype=bool)
            # Exclude seeds themselves if requested
            if args.exclude_same:
                mask[np.array(bookmark_lessons, dtype=int)] = False
            # Apply floor/ceiling
            if args.min_cos is not None:
                mask &= (max_s >= float(args.min_cos))
            if args.max_similar is not None and args.max_similar < 1.0:
                mask &= (max_s <= float(args.max_similar))
            # Exclude recently shown
            shown = load_shown_filter(args.shown_json, args.no_repeat_days)
            if shown:
                for shown_idx in shown.keys():
                    if 0 <= int(shown_idx) < mask.size:
                        mask[int(shown_idx)] = False
            cand_idx = np.nonzero(mask)[0]
            if cand_idx.size == 0:
                # If nothing after filters, pick any random candidate from all non-seeds
                pool_all = np.setdiff1d(np.arange(emb.shape[0]), np.array(bookmark_lessons, dtype=int), assume_unique=False)
                if pool_all.size > 0:
                    rng = np.random.default_rng(args.random_seed)
                    pick_pos = int(rng.integers(0, pool_all.size))
                    pick = int(pool_all[pick_pos])
                    goldilocks_pick = {"index": pick, "score": float(max_s[pick]), "text": texts[pick], "band": None, "fallback": "random_any"}
                    print(f"Goldilocks fallback(random any): {texts[pick]}  (score={max_s[pick]:+.4f})")
                    recs = [(pick, float(max_s[pick]))]
                else:
                    recs = []
            else:
                cand_scores = max_s[cand_idx]
                lo = float(np.percentile(cand_scores, args.band_low_pct))
                hi = float(np.percentile(cand_scores, args.band_high_pct))
                pool_mask = (cand_scores >= lo) & (cand_scores <= hi)
                pool_idx = cand_idx[pool_mask]
                if pool_idx.size == 0:
                    # fallback: pick uniformly at random from candidates that passed filters
                    rng = np.random.default_rng(args.random_seed)
                    pick_pos = int(rng.integers(0, cand_idx.size))
                    pick = int(cand_idx[pick_pos])
                    goldilocks_pick = {"index": pick, "score": float(max_s[pick]), "text": texts[pick], "band": [lo, hi], "fallback": "random_from_filtered"}
                    print(f"Goldilocks fallback(random filtered): {texts[pick]}  (score={max_s[pick]:+.4f}, band=[{lo:.4f}, {hi:.4f}])")
                    recs = [(int(i), float(max_s[i])) for i in cand_idx]
                    recs.sort(key=lambda x: x[1], reverse=True)
                    recs = recs[:args.overall_topk]
                else:
                    rng = np.random.default_rng(args.random_seed)
                    pick_pos = int(rng.integers(0, pool_idx.size))
                    pick = int(pool_idx[pick_pos])
                    goldilocks_pick = {"index": pick, "score": float(max_s[pick]), "text": texts[pick], "band": [lo, hi]}
                    print(f"Goldilocks pick: {texts[pick]}  (score={max_s[pick]:+.4f}, band=[{lo:.4f}, {hi:.4f}])")
                    # Output only candidates within the band, ranked by score desc
                    band_pairs = [(int(i), float(max_s[i])) for i in pool_idx]
                    band_pairs.sort(key=lambda x: x[1], reverse=True)
                    recs = band_pairs[:args.overall_topk]
                rng = np.random.default_rng(args.random_seed)
                pick_pos = int(rng.integers(0, pool_idx.size))
                pick = int(pool_idx[pick_pos])
                goldilocks_pick = {"index": pick, "score": float(max_s[pick]), "text": texts[pick], "band": [lo, hi]}
                print(f"Goldilocks pick: {texts[pick]}  (score={max_s[pick]:+.4f}, band=[{lo:.4f}, {hi:.4f}])")
                # Output only candidates within the band, ranked by score desc
                band_pairs = [(int(i), float(max_s[i])) for i in pool_idx]
                band_pairs.sort(key=lambda x: x[1], reverse=True)
                recs = band_pairs[:args.overall_topk]
    elif args.clustered_goldilocks:
        # Cluster seeds (k-means) in embedding space; build weighted centroids; goldilocks per cluster
        if not bookmark_lessons:
            print("No seeds from bookmarks. Exiting.")
            recs = []
        else:
            import math
            S = len(bookmark_lessons)
            # Auto-heuristic: k = max(1, min(3, round(sqrt(S)))) and <= S
            auto_k = max(1, min(3, int(round(math.sqrt(S)))))
            K = max(1, min(auto_k, S))
            seeds_emb = np.stack([emb[i] for i in bookmark_lessons], axis=0)  # [S,D]
            # Initialize centroids by picking K seeds evenly
            init_idx = np.linspace(0, S - 1, num=K, dtype=int)
            centroids = seeds_emb[init_idx].copy()
            # Lloyd iterations (few steps)
            for _ in range(5):
                # Assign
                dists = seeds_emb @ centroids.T  # cosine since normalized
                assign = np.argmax(dists, axis=1)
                # Recompute weighted centroid per cluster using recency weights
                for c in range(K):
                    members = np.where(assign == c)[0]
                    if members.size == 0:
                        continue
                    ws = np.array([weights.get(bookmark_lessons[m], 1.0) for m in members], dtype=np.float32)
                    vecs = seeds_emb[members]
                    centroid = (ws[:, None] * vecs).sum(axis=0)
                    # Normalize
                    norm = np.linalg.norm(centroid)
                    if norm > 1e-6:
                        centroid = centroid / norm
                    centroids[c] = centroid
            # For each centroid, gather top-M candidates, filter, band, pick
            shown = load_shown_filter(args.shown_json, args.no_repeat_days)
            rng = np.random.default_rng(args.random_seed)
            cluster_picks: List[Dict[str, object]] = []
            for c in range(K):
                q = centroids[c]
                scores = emb @ q
                order = np.argsort(-scores)
                pool = []
                for idx in order:
                    idx = int(idx)
                    if args.exclude_same and idx in bookmark_lessons:
                        continue
                    if shown and idx in shown:
                        continue
                    s = float(scores[idx])
                    if s < float(args.min_cos):
                        break
                    # Apply max_similar vs any seed in this cluster
                    members = np.where(assign == c)[0]
                    seed_ids = [bookmark_lessons[m] for m in members]
                    if seed_ids:
                        sim_to_seeds = seeds_emb[members] @ emb[idx]
                        if float(np.max(sim_to_seeds)) > float(args.max_similar):
                            continue
                    pool.append((idx, s))
                    if len(pool) >= int(args.topm_per_cluster):
                        break
                if not pool:
                    continue
                cand_scores = np.array([s for (_, s) in pool], dtype=np.float32)
                lo = float(np.percentile(cand_scores, args.band_low_pct))
                hi = float(np.percentile(cand_scores, args.band_high_pct))
                band = [(i, s) for (i, s) in pool if s >= lo and s <= hi]
                if band:
                    pick_pos = int(rng.integers(0, len(band)))
                    pick = band[pick_pos]
                    cluster_picks.append({"index": int(pick[0]), "score": float(pick[1]), "band": [lo, hi]})
                else:
                    # If no goldilocks picks, do not pick randomly from entire pool; skip the cluster
                    continue
            # Aggregate: if we have multiple cluster picks, choose one at random to return; and list all banded recs
            if cluster_picks:
                choice = cluster_picks[int(rng.integers(0, len(cluster_picks)))]
                goldilocks_pick = {"index": choice["index"], "score": choice["score"], "text": texts[int(choice["index"])], "band": choice["band"], "clustered": True}
                # For recs, merge banded items across clusters (top view)
                merged = sorted([(int(p["index"]), float(p["score"])) for p in cluster_picks], key=lambda x: x[1], reverse=True)
                recs = merged[:args.overall_topk]
            else:
                # No cluster picks at all; fallback: pick at random from all non-seed candidates
                pool_all = np.setdiff1d(np.arange(emb.shape[0]), np.array(bookmark_lessons, dtype=int), assume_unique=False)
                if pool_all.size > 0:
                    pick_pos = int(rng.integers(0, pool_all.size))
                    pick = int(pool_all[pick_pos])
                    goldilocks_pick = {"index": pick, "score": None, "text": texts[pick], "band": None, "clustered": True, "fallback": "random_any"}
                    recs = [(pick, float(emb[pick] @ centroids[0]))]
                else:
                    recs = []
    else:
        recs = recommend_from_bookmarks(
            bookmark_lessons=bookmark_lessons,
            weights=weights,
            emb=emb,
            texts=texts,
            exclude_same=args.exclude_same,
            min_cos=args.min_cos,
            max_similar=args.max_similar,
            topk_per_seed=args.topk_per_seed,
            overall_topk=args.overall_topk,
            combine=args.combine,
        )

    # Optional random pick among high-sim candidates
    random_pick: Dict[str, object] | None = None
    if (args.random_pick_threshold and args.random_pick_threshold > 0) and (not args.one_goldilocks):
        rng = np.random.default_rng(args.random_seed)
        pool = [(i, s) for (i, s) in recs if s >= float(args.random_pick_threshold)]
        if pool:
            idx = int(rng.integers(0, len(pool)))
            choice = pool[idx]
            random_pick = {"index": int(choice[0]), "score": float(choice[1]), "text": texts[int(choice[0])]}
            print("Random pick (>= %.2f): %s" % (args.random_pick_threshold, random_pick["text"]))

    # Print human-readable
    for rank, (idx, score) in enumerate(recs, start=1):
        print(f"{rank:>2}. {score:+.4f}  {texts[idx]}")

    if args.json_out:
        args.json_out.write_text(json.dumps({
            "bookmarks": args.bookmarks,
            "seed_lessons": bookmark_lessons,
            "weights": weights,
            "results": [{"index": i, "score": s, "text": texts[i]} for (i, s) in recs],
            "goldilocks_pick": goldilocks_pick,
            "random_pick": random_pick,
            "params": {
                "min_cos": args.min_cos,
                "max_similar": args.max_similar,
                "topk_per_seed": args.topk_per_seed,
                "overall_topk": args.overall_topk,
                "tau_days": args.tau_days,
                "w_min": args.w_min,
                "combine": args.combine,
                "random_pick_threshold": args.random_pick_threshold,
                "random_seed": args.random_seed,
            }
        }, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Wrote {args.json_out}")


if __name__ == "__main__":
    main()
