"""Biodegradable polymers and bacterial PHAs."""
from __future__ import annotations


BIOPLASTICS = {
    "PLA": {"name": "Polylactic acid", "monomer": "lactic acid",
            "tensile_mpa": 60, "degradation_months": 6, "source": "corn starch"},
    "PHA": {"name": "Polyhydroxyalkanoate", "monomer": "hydroxyalkanoic acids",
            "tensile_mpa": 40, "degradation_months": 12, "source": "bacterial fermentation"},
    "PHB": {"name": "Polyhydroxybutyrate", "monomer": "3-hydroxybutyric acid",
            "tensile_mpa": 43, "degradation_months": 24, "source": "bacteria (e.g. Ralstonia)"},
    "PBS": {"name": "Polybutylene succinate", "monomer": "succinic acid + 1,4-butanediol",
            "tensile_mpa": 35, "degradation_months": 3, "source": "petrochemical/bio-based"},
    "PLGA": {"name": "Poly(lactic-co-glycolic acid)", "monomer": "lactic + glycolic acid",
             "tensile_mpa": 50, "degradation_months": 2, "source": "synthetic copolymer"},
}


class BioplasticsDB:
    @staticmethod
    def lookup(name: str) -> dict:
        return BIOPLASTICS.get(name.upper(),
                               {"error": f"Unknown bioplastic '{name}'"})

    @staticmethod
    def list_all() -> list[str]:
        return sorted(BIOPLASTICS.keys())

    @staticmethod
    def pha_yield_bacteria(substrate_g: float, conversion_pct: float = 0.4) -> dict:
        """Theoretical PHA yield from carbon substrate (g/g)."""
        yield_g = substrate_g * conversion_pct
        return {"substrate_g": substrate_g, "conversion": conversion_pct,
                "pha_yield_g": round(yield_g, 2)}

    @staticmethod
    def recommend(application: str) -> list[str]:
        """Recommend polymers for an application."""
        app = application.lower()
        if "medical" in app or "implant" in app:
            return ["PLGA", "PLA"]
        if "packaging" in app:
            return ["PLA", "PBS"]
        if "biodegradable" in app:
            return ["PHA", "PHB", "PBS"]
        return sorted(BIOPLASTICS.keys())
