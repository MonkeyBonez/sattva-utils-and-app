#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, Iterable, List


def read_jsonl(path: Path) -> Iterable[dict]:
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            s = line.strip()
            if s:
                yield json.loads(s)


def load_lessons_meta(meta_path: Path) -> List[str]:
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    texts = list(meta.get("texts", []))
    if not texts:
        raise SystemExit(f"No texts in lessons_meta: {meta_path}")
    return texts


def normalize_whitespace(s: str) -> str:
    return " ".join(str(s).strip().split())


def main() -> None:
    ap = argparse.ArgumentParser(description="Build website-friendly units view (one row per embedding index)")
    ap.add_argument("--meta", default="utils/Scripts/Embeddings/ModelAssets/lessons_meta.json")
    ap.add_argument("--humanpass", default="utils/Scripts/outputs/humanpass_pt2.jsonl")
    ap.add_argument("--clusters", default="utils/Scripts/outputs/clusters_humanpass1.jsonl")
    ap.add_argument("--candidates", default="utils/Scripts/outputs/candidates_1_4_8.jsonl")
    ap.add_argument("-o", "--out", default="utils/Scripts/outputs/site_units_view.jsonl")
    args = ap.parse_args()

    texts = load_lessons_meta(Path(args.meta))

    # Align humanpass_pt2 reps to texts by content (ignoring null rows)
    hp_non_null: Dict[str, dict] = {}
    for obj in read_jsonl(Path(args.humanpass)):
        t = obj.get("text")
        if not t:
            continue
        key = normalize_whitespace(t)
        if key not in hp_non_null:
            hp_non_null[key] = obj

    # clusters: cluster_id -> member lesson ids
    clusters_map: Dict[int, List[str]] = {}
    for obj in read_jsonl(Path(args.clusters)):
        cid = obj.get("cluster_id")
        if cid is None:
            continue
        clusters_map[int(cid)] = list(obj.get("member_lesson_ids") or [])

    # candidates: lesson_id -> [units]
    lesson_to_units: Dict[str, List[dict]] = {}
    for obj in read_jsonl(Path(args.candidates)):
        lid = obj.get("lesson_id")
        unit = obj.get("unit")
        if not lid or not unit:
            continue
        lesson_to_units.setdefault(lid, []).append(
            {"chapter": int(unit["chapter"]), "start": int(unit["start"]), "end": int(unit["end"]) }
        )

    with Path(args.out).open("w", encoding="utf-8") as out:
        for idx, t in enumerate(texts):
            rec = hp_non_null.get(normalize_whitespace(t))
            old_cid = rec.get("old_cluster_id") if rec else None
            units: List[dict] = []
            if old_cid is not None:
                for lid in clusters_map.get(int(old_cid), []):
                    for u in lesson_to_units.get(lid, []):
                        units.append(u)
            # dedupe units
            seen = set(); dedup: List[dict] = []
            for u in units:
                k = (u["chapter"], u["start"], u["end"])
                if k in seen:
                    continue
                seen.add(k)
                dedup.append(u)

            row = {
                "cluster_id": idx,
                "candidates": [{
                    "old_cluster_id": old_cid,
                    "text": t,
                    "units": dedup,
                }],
            }
            out.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(f"Wrote {len(texts)} lines -> {args.out}")


if __name__ == "__main__":
    main()


