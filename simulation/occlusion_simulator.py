"""Occlusion simulator: artificial occlusions, light changes, lens noise."""

from __future__ import annotations

from typing import Optional, Tuple

import numpy as np


class OcclusionSimulator:
    """Inject synthetic occlusions, lighting changes, and sensor noise into frames."""

    def __init__(self, occlude_prob: float = 0.1, light_delta: int = 20,
                 noise_std: float = 5.0, seed: Optional[int] = None) -> None:
        self.occlude_prob = occlude_prob
        self.light_delta = light_delta
        self.noise_std = noise_std
        self._rng = np.random.default_rng(seed)

    def apply(self, image: np.ndarray) -> np.ndarray:
        out = image.astype(np.int16)
        if self._rng.random() < self.occlude_prob:
            out = self._add_occlusion(out)
        if self.light_delta:
            delta = int(self._rng.integers(-self.light_delta, self.light_delta + 1))
            out = out + delta
        if self.noise_std > 0:
            noise = self._rng.normal(0, self.noise_std, out.shape).astype(np.int16)
            out = out + noise
        return np.clip(out, 0, 255).astype(np.uint8)

    def _add_occlusion(self, image: np.ndarray) -> np.ndarray:
        h, w = image.shape[:2]
        bw = int(w * self._rng.uniform(0.1, 0.3))
        bh = int(h * self._rng.uniform(0.1, 0.3))
        x = int(self._rng.integers(0, max(1, w - bw)))
        y = int(self._rng.integers(0, max(1, h - bh)))
        image[y:y + bh, x:x + bw] = 0
        return image
