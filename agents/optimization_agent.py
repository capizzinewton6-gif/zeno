"""Optimization agent: inference latency, frame dropping, resolution scaling."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from modeling.parameters import Parameters


@dataclass
class OptimizationDecision:
    target_fps: int
    input_size: tuple
    skip_frames: int
    jpeg_quality: int
    reason: str


class OptimizationAgent:
    """Dynamically tune pipeline parameters to hit a latency budget."""

    def __init__(self, target_latency_ms: float = 50.0,
                 min_size: int = 320, max_size: int = 1280) -> None:
        self.target_latency_ms = target_latency_ms
        self.min_size = min_size
        self.max_size = max_size
        self._ema_latency = 0.0

    def observe(self, latency_ms: float) -> None:
        self._ema_latency = 0.8 * self._ema_latency + 0.2 * latency_ms if self._ema_latency else latency_ms

    def decide(self, current: Parameters) -> OptimizationDecision:
        size = current.input_size[0]
        skip = 0
        reason = "within_budget"
        if self._ema_latency > self.target_latency_ms * 1.2:
            size = max(self.min_size, int(size * 0.85))
            skip = 1
            reason = "downscale_to_reduce_latency"
        elif self._ema_latency < self.target_latency_ms * 0.5:
            size = min(self.max_size, int(size * 1.1))
            reason = "upscale_for_quality"
        return OptimizationDecision(
            target_fps=current.target_fps,
            input_size=(size, size),
            skip_frames=skip,
            jpeg_quality=current.jpeg_quality,
            reason=reason)
