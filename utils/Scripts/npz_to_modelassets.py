#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np


def main() -> None:
    ap = argparse.ArgumentParser(description="Convert lessons_e5_small_v2.npz to lessons_meta.json + lessons_f32.bin")
    ap.add_argument("npz_path", type=Path, help="Path to lessons_e5_small_v2.npz")
    ap.add_argument("--out-dir", type=Path, default=Path("utils/Scripts/Embeddings/ModelAssets"))
    args = ap.parse_args()

    data = dict(np.load(args.npz_path, allow_pickle=True))
    emb = np.asarray(data["embeddings"], dtype=np.float32)
    texts = [str(t) for t in data.get("texts", [])]
    if emb.ndim != 2:
        raise SystemExit(f"embeddings is not 2D: {emb.shape}")
    if len(texts) != emb.shape[0]:
        raise SystemExit("texts length does not match embeddings rows")

    ids = list(range(emb.shape[0]))
    model = str(data.get("model", "intfloat/e5-small-v2"))
    source = str(data.get("source", "utils/Scripts/Embeddings/lessons.txt"))

    args.out_dir.mkdir(parents=True, exist_ok=True)
    meta = {
        "count": int(emb.shape[0]),
        "dim": int(emb.shape[1]),
        "ids": ids,
        "texts": texts,
        "model": model,
        "source": source,
    }
    (args.out_dir / "lessons_meta.json").write_text(json.dumps(meta, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    emb.tofile(args.out_dir / "lessons_f32.bin")
    print(f"Wrote {(args.out_dir / 'lessons_meta.json')} and {(args.out_dir / 'lessons_f32.bin')}")


if __name__ == "__main__":
    main()



