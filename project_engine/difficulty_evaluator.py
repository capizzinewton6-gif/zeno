"""Evaluates code complexity and matches appropriate projects."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from calculations.complexity_metrics import ComplexityMetrics
from modeling.neural_backbones import NeuralBackbone, get_backbone


@dataclass
class DifficultyAssessment:
    level: str  # beginner, intermediate, advanced
    score: float  # 0..100
    reasons: list[str]


class DifficultyEvaluator:
    """Maps code complexity to a developer/project difficulty level."""

    def __init__(self, backbone: NeuralBackbone | None = None,
                 metrics: ComplexityMetrics | None = None) -> None:
        self.backbone = backbone or get_backbone()
        self.metrics = metrics or ComplexityMetrics()

    def evaluate_code(self, source: str, language: str = "python") -> DifficultyAssessment:
        m = self.metrics.cyclomatic_complexity(source, language)
        halstead = self.metrics.halstead(source, language)
        score = min(100.0, m * 8 + halstead.get("volume", 0) / 50.0)
        level, reasons = self._classify(score, m, halstead)
        return DifficultyAssessment(level=level, score=round(score, 1), reasons=reasons)

    def match_project(self, skill_level: str, candidate_levels: list[str]) -> str | None:
        """Pick the best-fitting project difficulty for a developer level."""
        order = {"beginner": 0, "intermediate": 1, "advanced": 2}
        target = order.get(skill_level, 1)
        ranked = sorted(candidate_levels, key=lambda l: abs(order.get(l, 1) - target))
        return ranked[0] if ranked else None

    def _classify(self, score: float, cyclo: float,
                  halstead: dict[str, float]) -> tuple[str, list[str]]:
        reasons: list[str] = []
        if cyclo > 10:
            reasons.append(f"High cyclomatic complexity ({cyclo:.1f})")
        if halstead.get("volume", 0) > 1000:
            reasons.append(f"High Halstead volume ({halstead['volume']:.0f})")
        if score < 33:
            return "beginner", reasons or ["Low complexity"]
        if score < 66:
            return "intermediate", reasons or ["Moderate complexity"]
        return "advanced", reasons or ["High complexity"]
