"""Surface plasmon resonance (SPR) and dissociation constants (Kd)."""
from __future__ import annotations

import math


class BiomoleculeAffinity:
    @staticmethod
    def kd_from_conc(bound: float, free: float) -> float:
        """Kd = [free][bound-or-not]/[bound] simplified as [free]/(bound)."""
        if bound == 0:
            return float("inf")
        return round(free / bound, 6)

    @staticmethod
    def kd_to_ki(ic50: float, substrate: float, km: float) -> float:
        """Cheng-Prusoff: Ki = IC50 / (1 + [S]/Km)."""
        if km <= 0:
            return ic50
        return round(ic50 / (1 + substrate / km), 6)

    @staticmethod
    def binding_fraction(ligand: float, kd: float) -> float:
        if kd <= 0:
            return 1.0
        return round(ligand / (ligand + kd), 4)

    @staticmethod
    def hill_coefficient(conc_series: list[float], response_series: list[float]) -> float:
        """Estimate Hill coefficient from log-logit slope."""
        import numpy as np
        valid = [(c, r) for c, r in zip(conc_series, response_series)
                 if c > 0 and 0 < r < 1]
        if len(valid) < 2:
            return 1.0
        log_c = np.log([c for c, _ in valid])
        logit = np.log([r / (1 - r) for _, r in valid])
        slope, _ = np.polyfit(log_c, logit, 1)
        return round(float(slope), 3)

    @staticmethod
    def spr_kinetics(ka: float, kd: float, rmax: float,
                     conc: float) -> dict:
        """1:1 Langmuir binding R(t) steady state."""
        req = (rmax * conc) / (conc + (kd / max(ka, 1e-12)))
        return {"ka": ka, "kd": kd, "kd_value": round(kd / max(ka, 1e-12), 6),
                "rmax": rmax, "req_steady": round(req, 3)}
