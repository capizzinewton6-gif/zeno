"""Mechanical engineering capability: machine design, mechanisms,
stress/strain analysis, and mechanical system synthesis."""

from __future__ import annotations

from ai_core.knowledge_engine import KnowledgeEngine


class MechanicalEngineering:
    def __init__(self, knowledge: KnowledgeEngine | None = None):
        self.knowledge = knowledge or KnowledgeEngine()

    def design_mechanism(self, spec: str) -> str:
        return self.knowledge.engine.generate(
            f"Design a mechanism satisfying: {spec}. Include kinematics, linkages, "
            f"and actuation.",
            system="You are a mechanical design engineer.")

    def stress_analysis(self, part: str, loads: str) -> str:
        return self.knowledge.engine.generate(
            f"Perform stress/strain analysis for part '{part}' under loads: {loads}. "
            f"State governing equations and safety factors.",
            system="You are a stress analysis engineer.")

    def gear_design(self, ratio: float, torque: float) -> str:
        return self.knowledge.engine.generate(
            f"Design a gear train with ratio {ratio} handling torque {torque} Nm. "
            f"Specify module, teeth, materials.",
            system="You are a gear design specialist.")

    def bearing_selection(self, load: float, rpm: float, life_hours: float) -> str:
        return self.knowledge.engine.generate(
            f"Select a bearing for load {load} N at {rpm} rpm, L10 life {life_hours} h.",
            system="You are a bearing selection engineer.")

    def heat_treatment(self, material: str, application: str) -> str:
        return self.knowledge.engine.generate(
            f"Recommend heat treatment for {material} in {application}.",
            system="You are a metallurgy engineer.")
