"""Quantization: FP16 / INT8 helpers and TensorRT engine serialization helpers.

These are pure-Python configuration/serialization descriptors. The actual
runtime conversion (torch AMP, TensorRT build) is handled by edge_computing when
the optional backends are present.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class QuantizationConfig:
    precision: str = "fp32"  # fp32 | fp16 | int8
    int8_calib_images: int = 100
    workspace_size_mb: int = 2048
    dynamic_shapes: bool = False

    def validate(self) -> None:
        if self.precision not in {"fp32", "fp16", "int8"}:
            raise ValueError(f"Unsupported precision: {self.precision}")

    def to_dict(self) -> dict:
        return asdict(self)


def serialize_plan(config: QuantizationConfig, out_path: str) -> str:
    """Write a quantization plan JSON (used by edge_computing to build engines)."""
    config.validate()
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(config.to_dict(), f, indent=2)
    return out_path


def load_plan(path: str) -> QuantizationConfig:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return QuantizationConfig(**data)
