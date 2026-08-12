"""Robotic sensor systems: perception and state estimation."""

from __future__ import annotations

from src.gemini_25_flash_engine import Gemini25FlashEngine


class SensorSystem:
    def __init__(self, engine: Gemini25FlashEngine | None = None):
        self.engine = engine or Gemini25FlashEngine()

    def perception_stack(self, robot: str) -> str:
        return self.engine.generate(
            f"Design a perception stack (sensors, fusion, localization) for: {robot}.",
            system="You are a robotics perception engineer.")

    def state_estimation(self, sensors: str) -> str:
        return self.engine.generate(
            f"Design state estimation (Kalman/particle filter) fusing: {sensors}.",
            system="You are a state estimation specialist.")

    def sensor_placement(self, robot: str) -> str:
        return self.engine.generate(
            f"Recommend sensor placement and coverage for: {robot}.",
            system="You are a sensor placement engineer.")
