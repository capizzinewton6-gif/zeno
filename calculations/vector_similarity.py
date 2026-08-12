"""Semantic similarity scoring for code snippet retrieval.

Computes cosine similarity over simple bag-of-vectors representations when no
embedding model is available, with hooks for vector DB embeddings.
"""
from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass
from typing import Any

try:  # pragma: no cover - optional
    import numpy as np  # type: ignore
    _NP = True
except Exception:  # pragma: no cover
    _NP = False


@dataclass
class SimilarityScore:
    a: str
    b: str
    score: float  # 0..1
    method: str


class VectorSimilarity:
    """Cosine similarity for code snippets via token vectors."""

    def cosine(self, a: str, b: str) -> SimilarityScore:
        tokens_a = self._tokens(a)
        tokens_b = self._tokens(b)
        if not tokens_a or not tokens_b:
            return SimilarityScore(a[:40], b[:40], 0.0, "cosine")
        if _NP:
            score = self._np_cosine(tokens_a, tokens_b)
        else:
            score = self._pure_cosine(tokens_a, tokens_b)
        return SimilarityScore(a[:40], b[:40], round(score, 4), "cosine")

    def jaccard(self, a: str, b: str) -> SimilarityScore:
        sa, sb = set(self._tokens(a)), set(self._tokens(b))
        union = sa | sb
        if not union:
            return SimilarityScore(a[:40], b[:40], 0.0, "jaccard")
        return SimilarityScore(a[:40], b[:40], round(len(sa & sb) / len(union), 4), "jaccard")

    def most_similar(self, query: str, candidates: list[str], top: int = 5) -> list[tuple[str, float]]:
        scored = [(c, self.cosine(query, c).score) for c in candidates]
        return sorted(scored, key=lambda x: -x[1])[:top]

    def _tokens(self, text: str) -> list[str]:
        return re.findall(r"[A-Za-z_]\w*|[^\s\w]", text.lower())

    def _pure_cosine(self, a: list[str], b: list[str]) -> float:
        ca, cb = Counter(a), Counter(b)
        keys = set(ca) | set(cb)
        dot = sum(ca[k] * cb[k] for k in keys)
        na = math.sqrt(sum(v * v for v in ca.values()))
        nb = math.sqrt(sum(v * v for v in cb.values()))
        return dot / (na * nb) if na and nb else 0.0

    def _np_cosine(self, a: list[str], b: list[str]) -> float:  # pragma: no cover
        ca, cb = Counter(a), Counter(b)
        keys = sorted(set(ca) | set(cb))
        va = np.array([ca[k] for k in keys], dtype=float)
        vb = np.array([cb[k] for k in keys], dtype=float)
        denom = (np.linalg.norm(va) * np.linalg.norm(vb))
        return float(np.dot(va, vb) / denom) if denom else 0.0
