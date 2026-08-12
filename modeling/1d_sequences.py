"""DNA/RNA/Protein primary sequence analysis."""
from __future__ import annotations

from collections import Counter

from biology.molecular import MolecularModule


class Sequence1D:
    @staticmethod
    def composition(sequence: str) -> dict:
        c = Counter(sequence.upper())
        total = sum(c.values())
        return {k: round(v / total, 4) for k, v in c.items()} if total else {}

    @staticmethod
    def dinucleotide_frequency(sequence: str) -> dict:
        seq = sequence.upper()
        c = Counter(seq[i:i + 2] for i in range(len(seq) - 1))
        total = sum(c.values()) or 1
        return {k: round(v / total, 4) for k, v in sorted(c.items())}

    @staticmethod
    def find_motif(sequence: str, motif: str) -> list[int]:
        positions = []
        start = 0
        while True:
            idx = sequence.upper().find(motif.upper(), start)
            if idx == -1:
                break
            positions.append(idx)
            start = idx + 1
        return positions

    @staticmethod
    def orf_scan(sequence: str, min_aa: int = 30) -> list[dict]:
        from genetic_engineering.construct_refinement import ConstructRefinement
        return ConstructRefinement().find_orfs(sequence, min_aa)

    @staticmethod
    def translate(sequence: str) -> str:
        prot, _ = MolecularModule.translate(sequence)
        return prot

    @staticmethod
    def gc_content(sequence: str) -> float:
        return MolecularModule.gc_content(sequence)
