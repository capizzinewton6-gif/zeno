"""RNA secondary structure and protein folding (SS)."""
from __future__ import annotations

# Simple Nussinov-style max pairing prediction (small RNAs only).
PAIRING = {"AU", "UA", "GC", "CG", "GU", "UG"}


class SecondaryStructure:
    @staticmethod
    def nussinov(rna: str) -> dict:
        seq = rna.upper().replace("T", "U")
        n = len(seq)
        if n == 0:
            return {"structure": "", "pairs": 0, "mfe": 0.0}
        dp = [[0] * n for _ in range(n)]
        for length in range(1, n):
            for i in range(n - length):
                j = i + length
                best = dp[i + 1][j]
                if seq[i] + seq[j] in PAIRING:
                    best = max(best, dp[i + 1][j - 1] + 1)
                for k in range(i, j):
                    best = max(best, dp[i][k] + dp[k + 1][j])
                dp[i][j] = best
        # traceback (simplified)
        structure = ["."] * n
        pairs = []

        def trace(i, j):
            if i >= j:
                return
            if dp[i][j] == dp[i + 1][j]:
                trace(i + 1, j)
                return
            if seq[i] + seq[j] in PAIRING and dp[i][j] == dp[i + 1][j - 1] + 1:
                structure[i] = "("
                structure[j] = ")"
                pairs.append((i, j))
                trace(i + 1, j - 1)
                return
            for k in range(i, j):
                if dp[i][j] == dp[i][k] + dp[k + 1][j]:
                    trace(i, k)
                    trace(k + 1, j)
                    return

        trace(0, n - 1)
        mfe = -1.5 * len(pairs)  # rough kcal/mol
        return {"structure": "".join(structure), "pairs": len(pairs),
                "mfe_kcal_mol": round(mfe, 2), "pair_list": pairs}

    @staticmethod
    def protein_secondary_structure(sequence: str) -> dict:
        """Chou-Fasman heuristic for alpha-helix / beta-sheet propensity."""
        helix_prop = {"A": 1.42, "E": 1.51, "L": 1.21, "M": 1.45, "K": 1.16,
                      "R": 0.98, "H": 1.00, "Q": 1.11}
        sheet_prop = {"V": 1.70, "I": 1.60, "Y": 1.47, "F": 1.38, "W": 1.37,
                      "T": 1.20, "C": 1.19}
        seq = sequence.upper()
        helix = sum(helix_prop.get(a, 1.0) for a in seq) / max(len(seq), 1)
        sheet = sum(sheet_prop.get(a, 1.0) for a in seq) / max(len(seq), 1)
        if helix > sheet:
            pred = "alpha-helix"
        elif sheet > helix:
            pred = "beta-sheet"
        else:
            pred = "coil/mixed"
        return {"mean_helix_propensity": round(helix, 3),
                "mean_sheet_propensity": round(sheet, 3),
                "prediction": pred}
