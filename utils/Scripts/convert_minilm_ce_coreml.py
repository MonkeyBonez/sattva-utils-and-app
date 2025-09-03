#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
from pathlib import Path

import numpy as np
import torch
import coremltools as ct
from transformers import AutoTokenizer, AutoModelForSequenceClassification


MODEL_ID = "cross-encoder/ms-marco-MiniLM-L-6-v2"


class CEWrapper(torch.nn.Module):
    def __init__(self, base: torch.nn.Module):
        super().__init__()
        self.base = base

    def forward(self, input_ids: torch.Tensor, attention_mask: torch.Tensor, token_type_ids: torch.Tensor):
        out = self.base(input_ids=input_ids, attention_mask=attention_mask, token_type_ids=token_type_ids)
        # Expect logits shape [B, 1] or [B]
        logits = out.logits
        if logits.dim() == 2 and logits.size(-1) == 1:
            logits = logits[:, 0]
        return logits  # [B]


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert MiniLM cross-encoder to Core ML")
    parser.add_argument("--seq-len", type=int, default=160)
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("utils/Scripts/Embeddings/ModelAssets/CrossEncoder"),
        help="Output directory for .mlpackage and tokenizer assets",
    )
    parser.add_argument("--compute-precision", choices=["fp16", "fp32"], default="fp16")
    args = parser.parse_args()

    out_dir: Path = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    ml_out = out_dir / "MiniLML6CE.mlpackage"
    tok_out = out_dir / "MiniLML6CE_tokenizer"
    tok_out.mkdir(exist_ok=True)

    os.environ.setdefault("PYTHONHASHSEED", "42")
    torch.manual_seed(42)

    base = AutoModelForSequenceClassification.from_pretrained(MODEL_ID).eval()
    wrapper = CEWrapper(base).eval()

    ids = torch.zeros(1, args.seq_len, dtype=torch.long)
    mask = torch.ones(1, args.seq_len, dtype=torch.long)
    types = torch.zeros(1, args.seq_len, dtype=torch.long)

    ts = torch.jit.trace(wrapper, (ids, mask, types))
    precision = ct.precision.FLOAT16 if args.compute_precision == "fp16" else ct.precision.FLOAT32

    mlmodel = ct.convert(
        ts,
        convert_to="mlprogram",
        minimum_deployment_target=ct.target.iOS18,
        compute_units=ct.ComputeUnit.ALL,
        compute_precision=precision,
        inputs=[
            ct.TensorType(name="input_ids", shape=ids.shape, dtype=np.int32),
            ct.TensorType(name="attention_mask", shape=mask.shape, dtype=np.int32),
            ct.TensorType(name="token_type_ids", shape=types.shape, dtype=np.int32),
        ],
    )

    mlmodel.save(str(ml_out))

    tok = AutoTokenizer.from_pretrained(MODEL_ID)
    tok.save_pretrained(str(tok_out))

    print(f"Wrote Core ML model: {ml_out}")
    print(f"Wrote tokenizer assets: {tok_out}")


if __name__ == "__main__":
    main()

