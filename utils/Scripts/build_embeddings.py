#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path
from typing import List, Tuple

import numpy as np
from sentence_transformers import SentenceTransformer
from tqdm import tqdm


MODEL_NAME = "intfloat/e5-small-v2"


def read_lessons(path: Path) -> List[str]:
    lines: List[str] = []
    with path.open("r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            lines.append(line)
    if not lines:
        raise SystemExit("Empty lessons file after cleaning.")
    return lines


def compute_hash(lines: List[str]) -> str:
    h = hashlib.sha256()
    for line in lines:
        h.update(line.encode("utf-8"))
        h.update(b"\n")
    return h.hexdigest()


def maybe_load_existing(npz_path: Path) -> Tuple[dict, bool]:
    if not npz_path.exists():
        return {}, False
    data = dict(np.load(npz_path, allow_pickle=True))
    return data, True


def main() -> None:
    parser = argparse.ArgumentParser(description="Build embeddings for lessons using E5")
    parser.add_argument("lessons_path", type=Path, help="Path to lessons.txt (one lesson per line)")
    parser.add_argument(
        "--emb-path",
        type=Path,
        default=Path(__file__).resolve().parent / "Embeddings" / "lessons_e5_small_v2.npz",
        help="Output .npz path (default: utils/Scripts/Embeddings/lessons_e5_small_v2.npz)",
    )
    parser.add_argument("--batch-size", type=int, default=64)
    parser.add_argument("--skip-if-unchanged", action="store_true", help="Skip rebuild if lessons hash matches")
    args = parser.parse_args()

    lessons = read_lessons(args.lessons_path)
    lessons_hash = compute_hash(lessons)

    npz_path: Path = args.emb_path
    npz_path.parent.mkdir(parents=True, exist_ok=True)

    existing, exists = maybe_load_existing(npz_path)
    if args.skip_if_unchanged and exists:
        old_texts = list(existing.get("texts", []))
        if old_texts and compute_hash(list(old_texts)) == lessons_hash:
            print(f"Unchanged lessons; skipping rebuild. ({npz_path})")
            return

    # Determinism
    os.environ.setdefault("PYTHONHASHSEED", "42")
    try:
        import random
        random.seed(42)
        import numpy
        numpy.random.seed(42)
        import torch
        torch.manual_seed(42)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(42)
    except Exception:
        pass

    # Load model
    model = SentenceTransformer(MODEL_NAME)

    # Prefix per E5
    passages = [f"passage: {t}" for t in lessons]

    emb = model.encode(
        passages,
        normalize_embeddings=True,
        batch_size=args.batch_size,
        show_progress_bar=True,
    )

    if emb.dtype != np.float32:
        emb = emb.astype(np.float32)

    # IDs: sequential indices 0..N-1 (stable across unchanged order)
    ids = np.arange(len(lessons), dtype=np.int32)

    avg_norm = float(np.linalg.norm(emb, axis=1).mean())

    np.savez(
        npz_path,
        embeddings=emb,
        ids=ids,
        texts=np.array(lessons, dtype=object),
        model=MODEL_NAME,
        source=str(args.lessons_path),
        hash=lessons_hash,
    )

    print(f"Embedded {len(lessons)} lessons → {npz_path}")
    print(f"Avg embedding norm (should be ~1.0): {avg_norm:.4f}")


if __name__ == "__main__":
    main()


