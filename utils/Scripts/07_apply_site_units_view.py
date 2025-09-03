#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable


def read_jsonl(path: Path) -> Iterable[dict]:
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            s = line.strip()
            if s:
                yield json.loads(s)


def main() -> None:
    ap = argparse.ArgumentParser(description="Apply website site_units_view edits to lesson_units.json for iOS")
    ap.add_argument("--edited", default="utils/Scripts/outputs/site_units_view.edited.jsonl",
                    help="Exported JSONL from website after edits")
    ap.add_argument("--meta", default="utils/Scripts/Embeddings/ModelAssets/lessons_meta.json",
                    help="To determine the number of embedding indices")
    ap.add_argument("-o", "--out", default="utils/Scripts/outputs/lesson_units.json")
    args = ap.parse_args()

    meta = json.loads(Path(args.meta).read_text(encoding="utf-8"))
    count = int(meta.get("count") or len(meta.get("texts", [])))
    if not isinstance(count, int) or count <= 0:
        raise SystemExit("Invalid meta: missing count/texts")

    idx_to_units = {}
    for obj in read_jsonl(Path(args.edited)):
        idx = obj.get("cluster_id")
        if not isinstance(idx, int):
            continue
        cands = obj.get("candidates") or []
        units = []
        if cands:
            units = cands[0].get("units") or []
        # normalize and dedupe
        seen = set(); out_units = []
        for u in units:
            ch = int(u["chapter"]); st = int(u["start"]); en = int(u["end"])
            k = (ch, st, en)
            if k in seen:
                continue
            seen.add(k)
            out_units.append({"chapter": ch, "start": st, "end": en})
        idx_to_units[idx] = out_units

    mapping = []
    for i in range(count):
        mapping.append({
            "old_cluster_id": None,
            "units": idx_to_units.get(i, []),
        })

    Path(args.out).write_text(json.dumps(mapping, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"Wrote {len(mapping)} entries -> {args.out}")


if __name__ == "__main__":
    main()


