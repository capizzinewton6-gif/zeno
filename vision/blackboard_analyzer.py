"""Read whiteboard/blackboard physical proofs and tensor indices."""

from __future__ import annotations

import re

from vision.equation_reader import EquationReader


class BlackboardAnalyzer:
    """Parse proof / derivation text blocks into structured steps."""

    STEP_SPLIT = re.compile(r"(?:^|\n)\s*(?:\d+\.|Step \d+:|[\-=]+)")

    @staticmethod
    def parse_proof(text: str) -> list[dict]:
        raw_steps = BlackboardAnalyzer.STEP_SPLIT.split(text)
        steps = []
        for i, step in enumerate(s.strip() for s in raw_steps):
            if not step:
                continue
            parsed = EquationReader.parse_equation(step)
            parsed["step"] = i
            steps.append(parsed)
        return steps

    @staticmethod
    def index_contractions(expr: str) -> list[str]:
        """Find repeated (contracted) indices in expressions like T^{mu}_{nu} S_{mu}."""
        return re.findall(r"\b([a-z])\b", expr)
