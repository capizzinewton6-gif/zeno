"""Molecular weight and sequence statistics evaluator."""
from __future__ import annotations

from collections import Counter

from biology.molecular import MolecularModule


class FormulaEngine:
    @staticmethod
    def molecular_weight(seq: str, seq_type: str = "dna") -> float:
        return _SequenceTools().molecular_weight(seq, seq_type)  # delegated

    @staticmethod
    def sequence_stats(sequence: str) -> dict:
        seq = sequence.upper()
        counts = Counter(seq)
        return {
            "length": len(seq),
            "composition": dict(counts),
            "gc_content": MolecularModule.gc_content(seq),
            "melting_temp_wallace": _TmHelpers.wallace(seq),
        }

    @staticmethod
    def extinction_coefficient(protein: str) -> float:
        """Estimate protein extinction coefficient at 280 nm (M^-1 cm^-1)."""
        prot = protein.upper()
        n_trp, n_tyr, n_cys = prot.count("W"), prot.count("Y"), prot.count("C")
        # Pace's method (approximate)
        return 5500 * n_trp + 1490 * n_tyr + 125 * (n_cys // 2)

    @staticmethod
    def isoelectric_point(protein: str) -> float:
        """Very rough pI estimate from charged residue balance."""
        prot = protein.upper()
        charge = prot.count("K") + prot.count("R") - prot.count("D") - prot.count("E")
        return round(7.0 - 0.1 * charge, 2)


# Local imports to avoid a circular import with tools.sequence_tools
def _SequenceTools():
    from tools.sequence_tools import SequenceTools
    return SequenceTools


class _TmHelpers:
    @staticmethod
    def wallace(seq):
        from calculations.thermodynamic_calc import tm_wallace
        return tm_wallace(seq)
