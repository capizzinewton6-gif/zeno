"""MOF frameworks — pore volumes and surface area (BET)."""


class MOFFrameworks:
    """Metal-organic framework property helpers."""

    MOFS = {
        "MOF-5": {"surface_area_m2_g": 2900, "pore_volume_cm3_g": 1.18, "linker": "BDC", "metal": "Zn4O"},
        "HKUST-1": {"surface_area_m2_g": 1500, "pore_volume_cm3_g": 0.62, "linker": "BTC", "metal": "Cu2"},
        "ZIF-8": {"surface_area_m2_g": 1630, "pore_volume_cm3_g": 0.66, "linker": "2-methylimidazole", "metal": "Zn"},
        "UiO-66": {"surface_area_m2_g": 1180, "pore_volume_cm3_g": 0.49, "linker": "BDC", "metal": "Zr6O4(OH)4"},
        "MIL-101(Cr)": {"surface_area_m2_g": 4100, "pore_volume_cm3_g": 2.0, "linker": "BDC", "metal": "Cr3"},
    }

    @staticmethod
    def bet_surface_area(p_rel, adsorbed_volumes):
        """BET surface area from a few (p/p0, v) points.

        Returns specific surface area (m^2/g) assuming N2 at 77 K.
        """
        x = [p for p in p_rel]
        y = [(p / (v * (1 - p))) for p, v in zip(p_rel, adsorbed_volumes)]
        n = len(x)
        sx = sum(x); sy = sum(y)
        sxx = sum(xi ** 2 for xi in x); sxy = sum(xi * yi for xi, yi in zip(x, y))
        denom = n * sxx - sx ** 2
        if denom == 0:
            return {"error": "insufficient data"}
        slope = (n * sxy - sx * sy) / denom
        intercept = (sy - slope * sx) / n
        vm = 1.0 / (slope + intercept)
        na = 6.022e23
        cross_section = 0.162e-18  # m^2 N2 molecule
        area_m2 = vm * na * cross_section
        return {"BET_surface_area_m2_g": round(area_m2, 1), "monolayer_volume_cm3_g": round(vm, 4)}

    def lookup(self, name):
        return self.MOFS.get(name, None)

    def list_mofs(self):
        return list(self.MOFS.keys())
