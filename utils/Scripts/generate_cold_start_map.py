#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple


def parse_verse_key(key: str) -> Optional[Tuple[int, int]]:
    try:
        ch, vv = key.split(":", 1)
        return int(ch), int(vv)
    except Exception:
        return None


def build_cluster_index_map(final_path: Path) -> Dict[int, int]:
    data = json.loads(final_path.read_text(encoding="utf-8"))
    items = sorted((x for x in data if isinstance(x, dict)), key=lambda o: int(o.get("cluster_id", 10**9)))
    m: Dict[int, int] = {}
    for i, obj in enumerate(items):
        cid = obj.get("cluster_id")
        if isinstance(cid, int):
            m[cid] = i
    return m


def main() -> None:
    ap = argparse.ArgumentParser(description="Generate cold_start_map.json from final_v2 clusters and curated cold-start list")
    ap.add_argument("final_json", type=Path, help="Path to finalClusters_FINAL_v2.json")
    ap.add_argument("curated_json", type=Path, help="Path to cold_start_lessons_from_final_v2.json")
    ap.add_argument("--out", type=Path, default=Path("utils/Scripts/outputs/cold_start_map.json"))
    args = ap.parse_args()

    cid_to_idx = build_cluster_index_map(args.final_json)
    curated = json.loads(args.curated_json.read_text(encoding="utf-8"))
    lessons = curated.get("lessons") or []
    out: List[dict] = []
    for obj in lessons:
        cid = obj.get("cluster_id")
        if not isinstance(cid, int):
            continue
        idx = cid_to_idx.get(cid)
        if idx is None:
            continue
        # Prefer first bestVerseForUnit; fallback to best_verse
        best_list = obj.get("bestVerseForUnit") or []
        anchor = None
        for k in best_list:
            if isinstance(k, str) and ":" in k:
                anchor = k
                break
        if anchor is None:
            bv = obj.get("best_verse")
            if isinstance(bv, str) and ":" in bv:
                anchor = bv
        ch, vs = 1, 1
        if anchor:
            pv = parse_verse_key(anchor)
            if pv is not None:
                ch, vs = pv
        pos = obj.get("position")
        out.append({
            "index": idx,
            "chapter": ch,
            "verse": vs,
            "position": int(pos) if isinstance(pos, int) else None
        })

    # sort by position if provided
    out.sort(key=lambda x: (x.get("position") is None, x.get("position") or 0))

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps({"lessons": out}, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"Wrote cold_start_map.json -> {args.out} ({len(out)} entries)")


if __name__ == "__main__":
    main()



