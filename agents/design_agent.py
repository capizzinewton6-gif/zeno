"""Design agent: creates and analyzes designs."""

from __future__ import annotations

from ai_core.ai_engine import AIEngine
from design import CADManager, Design2D, Design3D, TechnicalDrawing
from design.dimensioning import Dimensioning
from design.design_rules import DesignRules


class DesignAgent:
    def __init__(self, engine: AIEngine | None = None):
        self.engine = engine or AIEngine()
        self.cad = CADManager(self.engine.primary)
        self.d2 = Design2D()
        self.d3 = Design3D()
        self.drawing = TechnicalDrawing(self.engine.primary)
        self.dimensioning = Dimensioning(self.engine.primary)
        self.rules = DesignRules(self.engine.primary)

    def design(self, spec: str) -> str:
        return self.engine.reason(
            f"Create a complete engineering design for: {spec}. Include "
            f"geometry, dimensions, tolerances, and materials.",
            system="You are a senior design engineer.")

    def analyze(self, design: str) -> str:
        return self.engine.reason(
            f"Analyze this design for correctness, manufacturability, and "
            f"compliance with engineering rules: {design}",
            system="You are a design analyst.")

    def generate_views(self, design: str) -> str:
        return self.engine.reason(
            f"Specify the 2D and 3D views (front, top, side, iso, section) "
            f"required to fully document: {design}",
            system="You are a CAD drafter.")

    def check_rules(self, design: str) -> str:
        return self.rules.check(design)
