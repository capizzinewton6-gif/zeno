"""Control systems: classical and modern control design."""

from __future__ import annotations

import math

from src.gemini_25_flash_engine import Gemini25FlashEngine


class ControlSystem:
    def __init__(self, engine: Gemini25FlashEngine | None = None):
        self.engine = engine or Gemini25FlashEngine()

    def design(self, plant: str, requirements: str) -> str:
        return self.engine.generate(
            f"Design a controller for plant '{plant}' meeting: {requirements}. "
            f"Choose PID/state-space/LQR/MPC and provide gains and stability analysis.",
            system="You are a control systems engineer.")

    def pid_tune(self, plant: str, method: str = "Ziegler-Nichols") -> str:
        return self.engine.generate(
            f"Tune a PID controller for '{plant}' using {method}.",
            system="You are a PID tuning engineer.")

    def stability_margin(self, gain: float, phase_margin_deg: float) -> dict:
        return {"gain_margin_db": 20 * math.log10(gain) if gain > 0 else None,
                "phase_margin_deg": phase_margin_deg}

    def closed_loop_2nd_order(self, wn: float, zeta: float) -> dict:
        """Step-response metrics for a second-order system."""
        ts = 4.0 / (zeta * wn) if zeta > 0 else float("inf")
        tr = (math.pi - math.acos(zeta)) / (wn * math.sqrt(1 - zeta ** 2)) if zeta < 1 else float("inf")
        overshoot = 100 * math.exp(-math.pi * zeta / math.sqrt(1 - zeta ** 2)) if zeta < 1 else 0
        return {"settling_time": ts, "rise_time": tr,
                "percent_overshoot": overshoot, "damping_ratio": zeta,
                "natural_frequency": wn}
