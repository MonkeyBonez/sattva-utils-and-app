#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import coremltools as ct
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer


MODEL_ID = "intfloat/e5-small-v2"


def coreml_embed(mlp: ct.models.MLModel, tok, text: str, max_len: int) -> np.ndarray:
    enc = tok(text, max_length=max_len, truncation=True, padding="max_length", return_tensors="np")
    feed = {
        "input_ids": enc["input_ids"].astype(np.int32),
        "attention_mask": enc["attention_mask"].astype(np.int32),
    }
    out = mlp.predict(feed)
    # Expect single output [1,384]
    arr = next(iter(out.values()))
    return np.asarray(arr, dtype=np.float32)[0]


def main() -> None:
    p = argparse.ArgumentParser(description="Parity check: SentenceTransformers vs Core ML cosine")
    p.add_argument(
        "--mlpackage",
        type=Path,
        default=Path("utils/Scripts/Embeddings/ModelAssets/E5SmallV2.mlpackage"),
    )
    p.add_argument("--max-len", type=int, default=128)
    args = p.parse_args()

    st = SentenceTransformer(MODEL_ID)
    tok = AutoTokenizer.from_pretrained(MODEL_ID)
    ml = ct.models.MLModel(str(args.mlpackage))

    q = "query: I feel anxious before a big meeting"
    psg = "passage: Act with courage in the face of fear."

    a_st = st.encode([q], normalize_embeddings=True)[0].astype(np.float32)
    b_st = st.encode([psg], normalize_embeddings=True)[0].astype(np.float32)
    cos_st = float(a_st @ b_st)

    a_ml = coreml_embed(ml, tok, q, args.max_len)
    b_ml = coreml_embed(ml, tok, psg, args.max_len)
    cos_ml = float(a_ml @ b_ml)

    print(f"ST cosine:  {cos_st:+.6f}")
    print(f"CoreML cos: {cos_ml:+.6f}")
    print(f"abs diff:   {abs(cos_st - cos_ml):.6f} (expect ≤ ~1e-2)")


if __name__ == "__main__":
    main()



