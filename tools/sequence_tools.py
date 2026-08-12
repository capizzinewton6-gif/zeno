"""Biopython alignment and translation tools (thin wrappers)."""
from __future__ import annotations

from biology.molecular import MolecularModule
from calculations.sequence_alignment import needleman_wunsch, smith_waterman


class SequenceTools:
    @staticmethod
    def align(seq1: str, seq2: str, local: bool = False) -> dict:
        if local:
            score, a1, a2 = smith_waterman(seq1, seq2)
        else:
            score, a1, a2 = needleman_wunsch(seq1, seq2)
        matches = sum(1 for x, y in zip(a1, a2) if x == y and x != "-")
        length = max(len(a1), len(a2))
        pid = 100 * matches / length if length else 0.0
        return {"score": score, "alignment1": a1, "alignment2": a2,
                "matches": matches, "percent_identity": round(pid, 2)}

    @staticmethod
    def translate(seq: str) -> str:
        prot, _ = MolecularModule.translate(seq)
        return prot

    @staticmethod
    def reverse_complement(seq: str) -> str:
        return MolecularModule.reverse_complement(seq)

    @staticmethod
    def transcribe(seq: str) -> str:
        return MolecularModule.transcribe(seq)

    @staticmethod
    def gc_content(seq: str) -> float:
        return MolecularModule.gc_content(seq)

    @staticmethod
    def molecular_weight(seq: str, seq_type: str = "dna") -> float:
        # average base weights (g/mol)
        weights = {
            "dna": {"A": 331.2, "T": 322.2, "G": 347.2, "C": 307.2},
            "rna": {"A": 347.2, "U": 324.2, "G": 363.2, "C": 323.2},
            "protein": {"A": 89.1, "R": 174.2, "N": 132.1, "D": 133.1,
                        "C": 121.2, "E": 147.1, "Q": 146.2, "G": 75.0,
                        "H": 155.2, "I": 131.2, "L": 131.2, "K": 146.2,
                        "M": 149.2, "F": 165.2, "P": 115.1, "S": 105.1,
                        "T": 119.1, "W": 204.2, "Y": 181.2, "V": 117.1},
        }
        table = weights.get(seq_type.lower(), weights["dna"])
        seq = seq.upper()
        return round(sum(table.get(b, 0.0) for b in seq), 2)
