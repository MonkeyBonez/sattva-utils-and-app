#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List, Tuple


def load_lesson_units(path: Path) -> List[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise SystemExit("lesson_units.json must be a JSON array")
    return data


def build_verse_to_lesson(units: List[dict]) -> Tuple[Dict[str, int], Dict[str, List[int]]]:
    primary: Dict[str, int] = {}
    all_hits: Dict[str, List[int]] = {}
    for lesson_idx, entry in enumerate(units):
        for u in entry.get("units", []):
            ch = int(u["chapter"])
            st = int(u["start"])
            en = int(u["end"]) if int(u["end"]) >= int(u["start"]) else int(u["start"])  # safety
            for v in range(st, en + 1):
                key = f"{ch}:{v}"
                # Record full hit list
                all_hits.setdefault(key, []).append(lesson_idx)
                # Primary mapping: keep the first (lowest lesson index) to ensure determinism
                if key not in primary:
                    primary[key] = lesson_idx
    return primary, all_hits


def main() -> None:
    p = argparse.ArgumentParser(description="Build O(1) verse->lesson map for iOS from lesson_units.json")
    p.add_argument(
        "--units",
        type=Path,
        default=Path("utils/Scripts/outputs/lesson_units.json"),
        help="Path to lesson_units.json (aligned to embedding indices)",
    )
    p.add_argument(
        "--out",
        type=Path,
        default=Path("utils/Scripts/outputs/verse_to_lesson.json"),
        help="Output JSON path for primary verse->lesson map",
    )
    p.add_argument(
        "--out-all",
        type=Path,
        default=Path("utils/Scripts/outputs/verse_to_lessons_all.json"),
        help="Optional JSON path for verse->all matching lesson indices",
    )
    args = p.parse_args()

    units = load_lesson_units(args.units)
    primary, all_hits = build_verse_to_lesson(units)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(primary, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    if args.out_all:
        args.out_all.write_text(json.dumps(all_hits, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote primary map: {args.out} ({len(primary)} verse keys)")
    if args.out_all:
        print(f"Wrote all-hits map: {args.out_all} ({len(all_hits)} verse keys)")


if __name__ == "__main__":
    main()


