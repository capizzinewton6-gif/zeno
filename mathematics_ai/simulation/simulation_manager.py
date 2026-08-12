"""Controls numerical solvers and arbitrary-precision settings across simulations."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import numpy as np


@dataclass
class SimulationConfig:
    precision: int = 50
    max_steps: int = 10000
    tolerance: float = 1e-8
    seed: int | None = None
    method: str = "RK45"
    output_format: str = "python"


class SimulationManager:
    """Tracks and controls a set of numerical simulations."""

    def __init__(self, config: SimulationConfig | None = None) -> None:
        self.config = config or SimulationConfig()
        self._results: dict[str, Any] = {}

    def run(self, name: str, fn, *args: Any, **kwargs: Any) -> Any:
        """Run a simulation function ``fn`` and store its result under ``name``."""
        if self.config.seed is not None:
            np.random.seed(self.config.seed)
        result = fn(*args, **kwargs)
        self._results[name] = result
        return result

    def get(self, name: str) -> Any:
        return self._results.get(name)

    def all(self) -> dict[str, Any]:
        return dict(self._results)

    def summary(self) -> dict[str, str]:
        return {name: type(r).__name__ for name, r in self._results.items()}

    def set_precision(self, digits: int) -> None:
        import mpmath
        mpmath.mp.dps = digits
        self.config.precision = digits


__all__ = ["SimulationConfig", "SimulationManager"]
