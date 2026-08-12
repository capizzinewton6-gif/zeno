"""Lipid bilayer permeability and vesicle formulation."""
from __future__ import annotations

import math


class MembraneProperties:
    @staticmethod
    def permeability(p_in: float, p_out: float, thickness_nm: float = 5) -> float:
        """Permeability (cm/s) via solubility-diffusion (illustrative)."""
        D = 1e-8  # cm^2/s
        K = (p_in + p_out) / 2 or 1e-6
        return round(D * K / max(thickness_nm * 1e-7, 1e-9), 6)

    @staticmethod
    def vesicle_radius_surface(volume_ml: float, surface_area_cm2: float) -> dict:
        """Estimate mean vesicle radius from total volume/surface."""
        if surface_area <= 0:
            return {"error": "Surface area must be > 0"}
        r_cm = 3 * volume_ml / surface_area  # rough
        return {"radius_cm": round(r_cm, 6),
                "diameter_nm": round(r_cm * 1e7, 2)}

    @staticmethod
    def nernst_potential(z_ion: int, conc_in: float, conc_out: float,
                         temp_c: float = 25) -> float:
        """Nernst equilibrium potential (mV)."""
        if conc_out <= 0 or conc_in <= 0:
            return 0.0
        R, F = 8.314, 96485
        return round((R * (temp_c + 273.15) / (z_ion * F)) * 1000 *
                     math.log(conc_out / conc_in), 3)

    @staticmethod
    def encapsulation_efficiency(loaded: float, total: float) -> float:
        if total == 0:
            return 0.0
        return round(100 * loaded / total, 2)
