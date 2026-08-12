"""Local model quantization specifications (GGUF, AWQ, EXL2).

Documents the supported quantization formats and their trade-offs so the
research layer and backbone can reason about on-device deployment. This is a
specification module; it does not perform actual quantization.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

QuantFormat = Literal["gguf", "awq", "exl2", "gptq", "fp16", "fp32"]


@dataclass(frozen=True)
class QuantSpec:
    format: QuantFormat
    bits: int
    memory_reduction: float  # vs fp16, e.g. 0.5 = half the memory
    speed: str               # "fast", "medium", "slow"
    quality: str             # "high", "medium", "low"
    recommended_for: str
    notes: str


QUANTIZATION_SPECS: dict[str, QuantSpec] = {
    "gguf-q4_k_m": QuantSpec(
        "gguf", 4, 0.25, "fast", "medium",
        "CPU inference, llama.cpp",
        "Best general-purpose 4-bit format; broad hardware support.",
    ),
    "gguf-q8_0": QuantSpec(
        "gguf", 8, 0.5, "medium", "high",
        "CPU/GPU hybrid",
        "Near-lossless 8-bit; good when VRAM permits.",
    ),
    "awq-4bit": QuantSpec(
        "awq", 4, 0.25, "fast", "high",
        "GPU serving, vLLM",
        "Activation-aware weighting preserves quality well at 4-bit.",
    ),
    "exl2-6.0": QuantSpec(
        "exl2", 6, 0.38, "fast", "high",
        "ExLlamaV2 single-GPU",
        "Variable bitrate; excellent quality/speed balance.",
    ),
    "gptq-4bit": QuantSpec(
        "gptq", 4, 0.25, "medium", "medium",
        "Legacy GPU serving",
        "Older format; superseded by AWQ/EXL2.",
    ),
    "fp16": QuantSpec(
        "fp16", 16, 1.0, "fast", "high",
        "Server GPUs",
        "Unquantized baseline; maximum quality.",
    ),
}


def recommend(target: str = "gpu") -> QuantSpec:
    """Recommend a quantization spec for a deployment target."""
    if target == "cpu":
        return QUANTIZATION_SPECS["gguf-q4_k_m"]
    if target == "single_gpu":
        return QUANTIZATION_SPECS["exl2-6.0"]
    return QUANTIZATION_SPECS["awq-4bit"]
