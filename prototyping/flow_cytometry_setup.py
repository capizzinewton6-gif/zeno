"""Gating strategy and fluorophore channel planning."""
from __future__ import annotations

FLUOROPHORES = {
    "FITC": {"excitation": 494, "emission": 521, "laser": "488", "channel": "BL1"},
    "PE": {"excitation": 496, "emission": 575, "laser": "488", "channel": "YL2"},
    "APC": {"excitation": 650, "emission": 660, "laser": "638", "channel": "RL1"},
    "PerCP-Cy5.5": {"excitation": 482, "emission": 695, "laser": "488", "channel": "RL2"},
    "Pacific Blue": {"excitation": 405, "emission": 455, "laser": "405", "channel": "VL1"},
}


class FlowCytometrySetup:
    @staticmethod
    def gating_strategy(markers: list[str]) -> list[dict]:
        return [{"gate": f"{markers[i]}+", "parent": "singlets" if i == 0 else f"{markers[i-1]}+",
                 "population": f"{markers[i]}-positive"} for i in range(len(markers))]

    @staticmethod
    def panel_design(fluorophores: list[str]) -> dict:
        panel = {}
        for f in fluorophores:
            info = FLUOROPHORES.get(f)
            if info:
                panel[f] = info
        # spectral overlap warning (heuristic)
        warnings = []
        for i, f1 in enumerate(fluorophores):
            for f2 in fluorophores[i + 1:]:
                if f1 in FLUOROPHORES and f2 in FLUOROPHORES:
                    if FLUOROPHORES[f1]["emission"] - 5 < FLUOROPHORES[f2]["emission"] < \
                       FLUOROPHORES[f1]["emission"] + 5:
                        warnings.append(f"Possible spectral overlap: {f1} & {f2}")
        return {"panel": panel, "warnings": warnings}

    @staticmethod
    def compensation_matrix(fluorophores: list[str]) -> list[list[float]]:
        """Identity compensation matrix placeholder with small off-diagonal."""
        n = len(fluorophores)
        mat = [[0.0] * n for _ in range(n)]
        for i in range(n):
            mat[i][i] = 1.0
        return mat
