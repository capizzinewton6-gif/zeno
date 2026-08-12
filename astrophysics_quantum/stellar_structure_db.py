"""Polytrope models, Lane-Emden equations, and EOS tables."""

from __future__ import annotations

import numpy as np

from physics.astrophysics_cosmology import StellarStructure
from tools.constant_engine import CONSTANTS


G = CONSTANTS.value("G")


class StellarStructureDB:
    """Polytropic stellar models (Lane-Emden)."""

    lane_emden = staticmethod(StellarStructure.lane_emden_solve)

    @staticmethod
    def polytrope(n: float, K: float, rho_c: float, xi1: float | None = None) -> dict:
        """Compute radius and mass of a polytrope of index n.

        R = a xi_1,  a = sqrt((n+1) K rho_c^{(1-n)/n} / (4 pi G)).
        """
        # common first-zero values of the Lane-Emden function
        xi_table = {0: 1.0, 0.5: 2.7528, 1.0: np.pi, 1.5: 3.6538, 3.0: 6.8968, 5.0: np.inf}
        if xi1 is None:
            xi1 = xi_table.get(n, 6.9)
        a = np.sqrt((n + 1) * K * rho_c ** ((1 - n) / n) / (4 * np.pi * G))
        R = a * xi1
        M = 4 * np.pi * a ** 3 * rho_c * abs(xi1 ** 2 * (-1))  # use |theta' (xi1)|
        return {"polytropic_index": n, "scale_a": float(a), "radius": float(R),
                "note": "mass requires |theta'(xi1)| from Lane-Emden solution."}

    @staticmethod
    def stellar_types() -> dict:
        return {
            "main_sequence_O": {"M_solar": 16, "T_eff": 30000, "R_solar": 6.6},
            "main_sequence_G": {"M_solar": 1.0, "T_eff": 5778, "R_solar": 1.0},
            "white_dwarf": {"M_solar": 0.6, "T_eff": 10000, "R_solar": 0.008},
            "neutron_star": {"M_solar": 1.4, "T_eff": 1e6, "R_solar": 1e-5},
        }
