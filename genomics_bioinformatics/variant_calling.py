"""SNP and indel identification pipeline."""
from __future__ import annotations

from collections import Counter


class VariantCaller:
    @staticmethod
    def call_snps(reference: str, read: str) -> list[dict]:
        n = min(len(reference), len(read))
        snps = []
        for i in range(n):
            if reference[i] != read[i] and reference[i] in "ACGT" and read[i] in "ACGT":
                snps.append({
                    "position": i, "ref": reference[i], "alt": read[i],
                    "type": "SNP",
                    "transition": VariantCaller._is_transition(reference[i], read[i]),
                })
        return snps

    @staticmethod
    def call_indels(reference: str, read: str) -> list[dict]:
        """Simple gap-free detection via alignment offset."""
        from calculations.sequence_alignment import needleman_wunsch
        _, a1, a2 = needleman_wunsch(reference, read)
        indels = []
        pos = 0
        for ref_c, read_c in zip(a1, a2):
            if ref_c == "-":
                indels.append({"position": pos, "type": "insertion",
                               "inserted_base": read_c})
            elif read_c == "-":
                indels.append({"position": pos, "type": "deletion",
                               "deleted_base": ref_c})
                pos += 1
            else:
                pos += 1
        return indels

    @staticmethod
    def variant_frequency(reads: list[str]) -> dict:
        counts = Counter(reads)
        total = sum(counts.values())
        return {k: round(v / total, 4) for k, v in counts.items()} if total else {}

    @staticmethod
    def _is_transition(a, b):
        return {a, b} in ({"A", "G"}, {"C", "T"})
