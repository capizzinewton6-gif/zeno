"""Mendelian, population, and quantitative genetics."""
from __future__ import annotations

import itertools

from biology._shared import safe_ai_reason


class GeneticsModule:
    def handle(self, command: str, query: str, ctx) -> str:
        q = query.lower()
        if "punnett" in q or "cross" in q or "mendel" in q:
            return "Use punnett_cross('Aa', 'Aa') for a 2x2 cross; results below."
        if "hardy" in q or "weinberg" in q or "allele freq" in q:
            return safe_ai_reason(query, ctx)
        return safe_ai_reason(query, ctx)

    @staticmethod
    def punnett_cross(parent1: str, parent2: str) -> dict:
        p1, p2 = parent1.upper(), parent2.upper()
        if len(p1) != len(p2) or len(p1) % 2 != 0:
            raise ValueError("Parents must have equal, even allele lengths")
        genotypes = {}
        for g1 in GeneticsModule._all_gametes(p1):
            for g2 in GeneticsModule._all_gametes(p2):
                child = "".join(sorted(a + b) for a, b in zip(g1, g2))
                genotypes[child] = genotypes.get(child, 0) + 1
        total = sum(genotypes.values())
        ratios = {k: round(v / total, 4) for k, v in sorted(genotypes.items())}
        return {"parent1": p1, "parent2": p2, "genotype_ratios": ratios}

    @staticmethod
    def _all_gametes(genotype: str):
        # genotype like "AaBb" -> cartesian product of each locus's alleles
        loci = [genotype[i:i + 2] for i in range(0, len(genotype), 2)]
        return {"".join(g) for g in itertools.product(*loci)}

    @staticmethod
    def hardy_weinberg(p: float, q: float = None) -> dict:
        if q is None:
            q = 1 - p
        if not abs(p + q - 1.0) < 1e-6:
            raise ValueError("Allele frequencies must sum to 1")
        return {
            "p": p, "q": q,
            "freq_AA": round(p ** 2, 6),
            "freq_Aa": round(2 * p * q, 6),
            "freq_aa": round(q ** 2, 6),
        }

    @staticmethod
    def narrow_sense_heritability(v_a: float, v_p: float) -> float:
        if v_p == 0:
            raise ValueError("Phenotypic variance must be > 0")
        return v_a / v_p
