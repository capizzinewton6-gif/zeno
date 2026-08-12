"""Bacteria, viruses, fungi, and culture methods."""
from __future__ import annotations

from biology._shared import safe_ai_reason

GRAM_POSITIVE = {"staphylococcus", "streptococcus", "bacillus", "lactobacillus",
                 "clostridium", "enterococcus", "micrococcus"}
GRAM_NEGATIVE = {"escherichia", "salmonella", "pseudomonas", "klebsiella",
                 "neisseria", "helicobacter", "vibrio", "shigella"}


class MicrobiologyModule:
    def handle(self, command: str, query: str, ctx) -> str:
        q = query.lower()
        if "gram" in q:
            genus = self._extract_genus(q)
            result = self.gram_stain(genus)
            return f"{genus}: {result}" if result else "Provide a genus name to classify Gram reaction."
        if "doubling" in q or "growth" in q or "doubling time" in q:
            return safe_ai_reason(query, ctx)
        return safe_ai_reason(query, ctx)

    @staticmethod
    def _extract_genus(text: str) -> str:
        for w in text.replace(",", " ").split():
            if w in GRAM_POSITIVE or w in GRAM_NEGATIVE:
                return w
        for w in text.split():
            if w.endswith("us") or w.endswith("a") or w.endswith("um"):
                return w.strip(".,")
        return ""

    @staticmethod
    def gram_stain(genus: str) -> str | None:
        g = genus.lower()
        if g in GRAM_POSITIVE:
            return "Gram positive"
        if g in GRAM_NEGATIVE:
            return "Gram negative"
        return None

    @staticmethod
    def doubling_time(n0: float, n_t: float, t_hours: float) -> float:
        """Compute doubling time from growth data."""
        import math
        if n0 <= 0 or n_t <= 0 or t_hours <= 0:
            raise ValueError("All inputs must be positive")
        return t_hours * math.log(2) / math.log(n_t / n0)
