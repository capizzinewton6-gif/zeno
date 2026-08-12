"""Scale-up calculator — process chemistry scale-up, heat transfer, runaway risks."""

import math


class ScaleupCalculator:
    """Scale reaction from lab to pilot/plant with safety assessment."""

    def scale(self, lab_scale_g, target_scale_g, lab_yield_pct=80, delta_H_kJ_per_mol=None,
              moles_lab=None, molar_mass=100):
        scale_factor = target_scale_g / lab_scale_g
        heat_release = None
        if delta_H_kJ_per_mol and moles_lab:
            heat_release = delta_H_kJ_per_mol * moles_lab * scale_factor  # kJ
        # Heat transfer scales with surface area (L^2) while volume scales L^3
        cooling_ratio = 1.0 / scale_factor ** (1.0 / 3.0)
        runaway_risk = "low"
        if delta_H_kJ_per_mol and abs(delta_H_kJ_per_mol) > 100:
            runaway_risk = "moderate" if scale_factor < 100 else "high"
        return {
            "lab_scale_g": lab_scale_g,
            "target_scale_g": target_scale_g,
            "scale_factor": round(scale_factor, 2),
            "expected_yield_g": round(target_scale_g * lab_yield_pct / 100, 2),
            "heat_release_kJ": heat_release,
            "cooling_capacity_ratio": round(cooling_ratio, 3),
            "runaway_risk": runaway_risk,
            "recommendations": [
                "Use jacketed reactor for temperature control at scale." if scale_factor > 10 else None,
                "Consider semi-batch addition to manage exotherm." if runaway_risk in ("moderate", "high") else None,
                "Perform calorimetry (DSC/RC1) before scale-up." if runaway_risk == "high" else None,
                "Evaluate heat-transfer coefficient and cooling utility capacity.",
            ],
            "note": "Always validate with hazard assessment before scale-up.",
        }

    @staticmethod
    def heat_transfer_area(volume_L, aspect=1.0):
        """Approximate jacket heat-transfer area for a cylindrical vessel."""
        r = (volume_L / (1000 * math.pi * aspect)) ** (1.0 / 3.0)
        h = aspect * r
        area = 2 * math.pi * r * h + math.pi * r ** 2  # m^2
        return {"radius_m": round(r, 4), "height_m": round(h, 4), "area_m2": round(area, 4)}
