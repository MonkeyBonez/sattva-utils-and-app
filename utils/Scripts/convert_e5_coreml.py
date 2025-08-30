#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
from pathlib import Path

import numpy as np
import torch
from transformers import AutoModel, AutoTokenizer
import coremltools as ct


MODEL_ID = "intfloat/e5-small-v2"


class E5Wrapper(torch.nn.Module):
    def __init__(self, base: torch.nn.Module):
        super().__init__()
        self.base = base

    def forward(self, input_ids: torch.Tensor, attention_mask: torch.Tensor):
        out = self.base(input_ids=input_ids, attention_mask=attention_mask)
        last_hidden = out.last_hidden_state  # [B, S, H]
        mask = attention_mask.unsqueeze(-1).to(last_hidden.dtype)  # [B, S, 1]
        summed = (last_hidden * mask).sum(dim=1)  # [B, H]
        denom = mask.sum(dim=1).clamp(min=1e-6)  # [B, 1]
        mean = summed / denom  # [B, H]
        norm = mean / mean.norm(p=2, dim=1, keepdim=True).clamp(min=1e-6)
        return norm  # [B, 384]


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert E5 to Core ML with mean-pool+L2 baked in")
    parser.add_argument("--seq-len", type=int, default=128)
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("utils/Scripts/Embeddings/ModelAssets"),
        help="Output directory for .mlpackage and tokenizer assets",
    )
    parser.add_argument("--compute-precision", choices=["fp16", "fp32"], default="fp16")
    args = parser.parse_args()

    out_dir: Path = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    ml_out = out_dir / "E5SmallV2.mlpackage"
    tok_out = out_dir / "E5SmallV2_tokenizer"
    tok_out.mkdir(exist_ok=True)

    os.environ.setdefault("PYTHONHASHSEED", "42")
    torch.manual_seed(42)

    base = AutoModel.from_pretrained(MODEL_ID).eval()
    hidden_size = int(base.config.hidden_size)
    assert hidden_size == 384, f"Unexpected hidden size: {hidden_size}"

    wrapper = E5Wrapper(base).eval()

    ids = torch.zeros(1, args.seq_len, dtype=torch.long)
    mask = torch.ones(1, args.seq_len, dtype=torch.long)

    ts = torch.jit.trace(wrapper, (ids, mask))
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
        ],
    )

    mlmodel.save(str(ml_out))

    tok = AutoTokenizer.from_pretrained(MODEL_ID)
    tok.save_pretrained(str(tok_out))

    print(f"Wrote Core ML model: {ml_out}")
    print(f"Wrote tokenizer assets: {tok_out}")


if __name__ == "__main__":
    main()



