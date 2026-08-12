"""Robot designer: morphology and subsystem design."""

from __future__ import annotations

from src.gemini_25_flash_engine import Gemini25FlashEngine


class RobotDesigner:
    def __init__(self, engine: Gemini25FlashEngine | None = None):
        self.engine = engine or Gemini25FlashEngine()

    def design(self, spec: str) -> str:
        return self.engine.generate(
            f"Design a robot: {spec}. Cover morphology, locomotion, manipulator, "
            f"sensors, compute, power.",
            system="You are a robot systems architect.")

    def morphology(self, task: str) -> str:
        return self.engine.generate(
            f"Recommend robot morphology (wheeled/legged/flying/ARM) for task: {task}.",
            system="You are a robot morphology specialist.")

    def dof_analysis(self, task: str) -> str:
        return self.engine.generate(
            f"Determine required degrees of freedom and workspace for: {task}.",
            system="You are a kinematics architect.")
