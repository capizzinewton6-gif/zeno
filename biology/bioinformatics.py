"""Sequence alignment, genomics, and structural biology."""
from __future__ import annotations

from biology._shared import safe_ai_reason
from calculations.sequence_alignment import needleman_wunsch, smith_waterman


class BioinformaticsModule:
    def handle(self, command: str, query: str, ctx) -> str:
        return safe_ai_reason(query, ctx)

    @staticmethod
    def global_align(seq1: str, seq2: str, match=2, mismatch=-1, gap=-2) -> dict:
        score, a1, a2 = needleman_wunsch(seq1, seq2, match, mismatch, gap)
        return {"score": score, "alignment1": a1, "alignment2": a2}

    @staticmethod
    def local_align(seq1: str, seq2: str, match=2, mismatch=-1, gap=-2) -> dict:
        score, a1, a2 = smith_waterman(seq1, seq2, match, mismatch, gap)
        return {"score": score, "alignment1": a1, "alignment2": a2}

    @staticmethod
    def hamming_distance(seq1: str, seq2: str) -> int:
        if len(seq1) != len(seq2):
            raise ValueError("Sequences must be equal length for Hamming distance")
        return sum(a != b for a, b in zip(seq1, seq2))

    @staticmethod
    def percent_identity(seq1: str, seq2: str) -> float:
        if not seq1 or not seq2:
            return 0.0
        matches = sum(a == b for a, b in zip(seq1, seq2))
        return 100.0 * matches / min(len(seq1), len(seq2))
