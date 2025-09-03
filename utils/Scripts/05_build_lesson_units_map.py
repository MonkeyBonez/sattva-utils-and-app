#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple


# ----------------------------
# Data models
# ----------------------------

@dataclass
class Unit:
    chapter: int
    start: int
    end: int


@dataclass
class HumanPassPt2Rec:
    cluster_id: Optional[int]
    old_cluster_id: Optional[int]
    text: Optional[str]
    member_ids: List[str]


# ----------------------------
# IO helpers
# ----------------------------

def read_jsonl(path: Path) -> Iterable[dict]:
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            yield json.loads(line)


def write_json(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, separators=(",", ":"))


# ----------------------------
# Load sources
# ----------------------------

def load_lessons_meta(meta_path: Path) -> Tuple[List[str], List[int]]:
    with meta_path.open("r", encoding="utf-8") as f:
        meta = json.load(f)
    texts: List[str] = list(meta.get("texts", []))
    ids: List[int] = list(meta.get("ids", []))
    if not texts:
        raise SystemExit(f"No texts in lessons_meta: {meta_path}")
    if not ids:
        # Fallback if not present; assume 0..N-1
        ids = list(range(len(texts)))
    if len(ids) != len(texts):
        raise SystemExit("lessons_meta malformed: ids/texts length mismatch")
    return texts, ids


def load_humanpass_pt2(path: Path) -> List[HumanPassPt2Rec]:
    recs: List[HumanPassPt2Rec] = []
    for obj in read_jsonl(path):
        recs.append(
            HumanPassPt2Rec(
                cluster_id=obj.get("cluster_id"),
                old_cluster_id=obj.get("old_cluster_id"),
                text=obj.get("text"),
                member_ids=list(obj.get("member_ids", [])),
            )
        )
    return recs


def load_clusters_humanpass1(path: Path) -> Dict[int, List[str]]:
    # cluster_id -> member_lesson_ids[]
    out: Dict[int, List[str]] = {}
    for obj in read_jsonl(path):
        cid = obj.get("cluster_id")
        if cid is None:
            continue
        ids = obj.get("member_lesson_ids") or []
        out[int(cid)] = list(ids)
    if not out:
        raise SystemExit(f"No clusters loaded from {path}")
    return out


def load_candidates(path: Path) -> Dict[str, List[Unit]]:
    # lesson_id -> [Unit]
    out: Dict[str, List[Unit]] = {}
    for obj in read_jsonl(path):
        lid = obj.get("lesson_id")
        unit = obj.get("unit")
        if not lid or not unit:
            # Skip malformed rows
            continue
        u = Unit(chapter=int(unit["chapter"]), start=int(unit["start"]), end=int(unit["end"]))
        out.setdefault(str(lid), []).append(u)
    if not out:
        raise SystemExit(f"No candidates with units found in {path}")
    return out


# ----------------------------
# Core mapping
# ----------------------------

def normalize_whitespace(s: str) -> str:
    return " ".join(str(s).strip().split())


def align_meta_to_humanpass(
    meta_texts: List[str], humanpass: List[HumanPassPt2Rec]
) -> List[HumanPassPt2Rec]:
    # Primary strategy: order alignment over non-null-text records
    hp_non_null: List[HumanPassPt2Rec] = [r for r in humanpass if r.text is not None]
    if len(meta_texts) != len(hp_non_null):
        # Attempt to sync by text matching as a fallback
        print(
            f"Warning: lessons_meta texts ({len(meta_texts)}) != non-null humanpass_pt2 rows ({len(hp_non_null)}). Trying text matching..."
        )
        # Build map text -> first rec (assume dedup already handled)
        text_to_rec: Dict[str, HumanPassPt2Rec] = {}
        for r in hp_non_null:
            key = normalize_whitespace(r.text or "")
            if key and key not in text_to_rec:
                text_to_rec[key] = r
        aligned: List[HumanPassPt2Rec] = []
        misses = 0
        for t in meta_texts:
            r = text_to_rec.get(normalize_whitespace(t))
            if r is None:
                misses += 1
                aligned.append(HumanPassPt2Rec(None, None, t, []))
            else:
                aligned.append(r)
        if misses:
            print(f"Warning: {misses} texts from lessons_meta not found in humanpass_pt2 by text.")
        return aligned
    # Fast path: lengths match → assume order preserved
    return hp_non_null


def dedupe_units(units: List[Unit]) -> List[Unit]:
    seen = set()
    out: List[Unit] = []
    for u in units:
        key = (u.chapter, u.start, u.end)
        if key in seen:
            continue
        seen.add(key)
        out.append(u)
    return out


def build_mapping(
    meta_texts: List[str],
    humanpass: List[HumanPassPt2Rec],
    clusters: Dict[int, List[str]],
    candidates: Dict[str, List[Unit]],
) -> List[dict]:
    aligned = align_meta_to_humanpass(meta_texts, humanpass)
    result: List[dict] = []

    for idx, r in enumerate(aligned):
        old_cid = r.old_cluster_id
        # Gather member_lesson_ids for this old cluster
        lesson_ids = clusters.get(int(old_cid)) if old_cid is not None else None
        units: List[Unit] = []

        if lesson_ids:
            for lid in lesson_ids:
                for u in candidates.get(lid, []):
                    units.append(u)
        else:
            # No cluster or no ids; leave units empty but keep structure
            pass

        units = dedupe_units(units)
        result.append(
            {
                "old_cluster_id": old_cid,
                "units": [
                    {"chapter": u.chapter, "start": u.start, "end": u.end} for u in units
                ],
            }
        )

    return result


# ----------------------------
# CLI
# ----------------------------

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Build mapping from embedding index to verse units")
    p.add_argument(
        "--meta",
        type=Path,
        default=Path(__file__).resolve().parent / "Embeddings" / "ModelAssets" / "lessons_meta.json",
        help="Path to lessons_meta.json",
    )
    p.add_argument(
        "--humanpass",
        type=Path,
        default=Path(__file__).resolve().parent / "outputs" / "humanpass_pt2.jsonl",
        help="Path to humanpass_pt2.jsonl",
    )
    p.add_argument(
        "--clusters",
        type=Path,
        default=Path(__file__).resolve().parent / "outputs" / "clusters_humanpass1.jsonl",
        help="Path to clusters_humanpass1.jsonl (Stage A clusters with member_lesson_ids)",
    )
    p.add_argument(
        "--candidates",
        type=Path,
        default=Path(__file__).resolve().parent / "outputs" / "candidates_1_4_8.jsonl",
        help="Path to candidates_1_4_8.jsonl (lesson_id -> unit)",
    )
    p.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path(__file__).resolve().parent / "outputs" / "lesson_units.json",
        help="Output JSON path (array aligned to embedding indices)",
    )
    return p.parse_args()


def main() -> None:
    args = parse_args()

    meta_texts, _ = load_lessons_meta(args.meta)
    humanpass = load_humanpass_pt2(args.humanpass)
    clusters = load_clusters_humanpass1(args.clusters)
    candidates = load_candidates(args.candidates)

    mapping = build_mapping(meta_texts, humanpass, clusters, candidates)

    # Basic validations
    if len(mapping) != len(meta_texts):
        print(
            f"Warning: mapping length {len(mapping)} != lessons_meta texts {len(meta_texts)}"
        )

    write_json(args.output, mapping)

    # Print a couple of samples for quick sanity check
    examples = [0, len(mapping) // 2, len(mapping) - 1]
    print(f"Wrote {len(mapping)} entries → {args.output}")
    for i in examples:
        if 0 <= i < len(mapping):
            m = mapping[i]
            print(
                f"idx={i} old_cluster_id={m.get('old_cluster_id')} units_count={len(m.get('units', []))}"
            )


if __name__ == "__main__":
    main()



