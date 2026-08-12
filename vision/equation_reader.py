"""OCR for physics derivations and LaTeX.

Without external OCR engine access this module returns structured guidance and a
regex-based LaTeX expression extractor so the rest of the pipeline keeps working.
"""

from __future__ import annotations

import re


class EquationReader:
    """Extract physics expressions from text / (simulated) OCR output."""

    LATEX_PATTERN = re.compile(r"\\[a-zA-Z]+(?:\{[^{}]*\})*|\$[^$]*\$|[a-zA-Z]\w*")
    GREEK = {"alpha", "beta", "gamma", "delta", "epsilon", "zeta", "eta", "theta",
             "iota", "kappa", "lambda", "mu", "nu", "xi", "pi", "rho", "sigma",
             "tau", "upsilon", "phi", "chi", "psi", "omega", "Delta", "Sigma", "Omega"}

    @staticmethod
    def extract_symbols(text: str) -> list[str]:
        return sorted(set(EquationReader.LATEX_PATTERN.findall(text)))

    @staticmethod
    def detect_greek(text: str) -> list[str]:
        found = []
        for g in EquationReader.GREEK:
            if g.lower() in text.lower() or f"\\{g}" in text:
                found.append(g)
        return found

    @staticmethod
    def parse_equation(text: str) -> dict:
        """Heuristically split an equation string at '='."""
        if "=" in text:
            lhs, rhs = text.split("=", 1)
            return {"lhs": lhs.strip(), "rhs": rhs.strip(), "symbols": EquationReader.extract_symbols(text)}
        return {"expression": text, "symbols": EquationReader.extract_symbols(text)}
