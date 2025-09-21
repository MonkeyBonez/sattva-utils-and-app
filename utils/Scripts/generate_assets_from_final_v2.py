#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional


@dataclass
class Unit:
    chapter: int
    start: int
    end: int


def parse_verse_key(key: str) -> Optional[Tuple[int, int]]:
    try:
        ch, vv = key.split(":", 1)
        return int(ch), int(vv)
    except Exception:
        return None


def parse_range_key(key: str) -> Optional[Tuple[int, int, int]]:
    try:
        ch, rest = key.split(":", 1)
        if "-" in rest:
            s, e = rest.split("-", 1)
            return int(ch), int(s), int(e)
        else:
            v = int(rest)
            return int(ch), v, v
    except Exception:
        return None


def dedupe_units(units: List[Unit]) -> List[Unit]:
    seen = set()
    out: List[Unit] = []
    for u in units:
        k = (u.chapter, u.start, u.end)
        if k in seen:
            continue
        seen.add(k)
        out.append(u)
    return out


def build_from_final_v2(
    final_path: Path,
    out_lessons_txt: Path,
    out_units_json: Path,
) -> None:
    data = json.loads(final_path.read_text(encoding="utf-8"))
    # Expect an array of cluster objects with fields: cluster_id, text, verses[], bestVerseForUnit[] (optional), best_verse (optional)

    # Sort by cluster_id to define stable embedding indices 0..N-1
    items = sorted((x for x in data if isinstance(x, dict)), key=lambda o: int(o.get("cluster_id", 10**9)))

    # 1) lessons.txt
    out_lessons_txt.parent.mkdir(parents=True, exist_ok=True)
    with out_lessons_txt.open("w", encoding="utf-8") as ftxt:
        for obj in items:
            t = (obj.get("text") or "").strip()
            if not t:
                raise SystemExit("Encountered cluster with empty text; cannot build embeddings.")
            ftxt.write(t.replace("\n", " ") + "\n")

    # 2) lesson_units.json aligned to the same order
    mapping: List[Dict[str, Any]] = []
    for obj in items:
        units: List[Unit] = []

        # Insert anchor from bestVerseForUnit first if present
        anchor_list = obj.get("bestVerseForUnit") or []
        anchor_key: Optional[str] = None
        for key in anchor_list:
            if isinstance(key, str) and ":" in key:
                anchor_key = key
                break
        if anchor_key is None:
            # optional fallback to best_verse if provided
            bv = obj.get("best_verse")
            if isinstance(bv, str) and ":" in bv:
                anchor_key = bv

        if anchor_key:
            pv = parse_verse_key(anchor_key)
            if pv is not None:
                ch, vs = pv
                units.append(Unit(chapter=ch, start=vs, end=vs))

        # Add ranges from "verses" field
        verses = obj.get("verses") or []
        for vkey in verses:
            if not isinstance(vkey, str):
                continue
            pr = parse_range_key(vkey)
            if pr is None:
                continue
            ch, st, en = pr
            # normalize order
            if en < st:
                st, en = en, st
            units.append(Unit(chapter=ch, start=st, end=en))

        units = dedupe_units(units)

        # Drop old_cluster_id as requested by user; only emit units
        mapping.append({
            "units": [ {"chapter": u.chapter, "start": u.start, "end": u.end} for u in units ]
        })

    out_units_json.parent.mkdir(parents=True, exist_ok=True)
    out_units_json.write_text(json.dumps(mapping, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser(description="Build lessons.txt and lesson_units.json from finalClusters_FINAL_v2.json")
    ap.add_argument("final_json", type=Path, help="Path to finalClusters_FINAL_v2.json")
    ap.add_argument("--out-lessons", type=Path, default=Path("utils/Scripts/Embeddings/lessons.txt"))
    ap.add_argument("--out-units", type=Path, default=Path("utils/Scripts/outputs/lesson_units.json"))
    args = ap.parse_args()

    build_from_final_v2(args.final_json, args.out_lessons, args.out_units)
    print(f"Wrote lessons.txt -> {args.out_lessons}")
    print(f"Wrote lesson_units.json -> {args.out_units}")


if __name__ == "__main__":
    main()



