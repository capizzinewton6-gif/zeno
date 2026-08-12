"""Select hydrogels, matrices, and growth factors."""
from __future__ import annotations


HYDROGELS = {
    "alginate": {"modulus_kpa": 10, "gelation": "Ca2+ crosslinking",
                 "biodegradable": True, "cell_adhesive": False},
    "collagen": {"modulus_kpa": 0.5, "gelation": "temperature/pH",
                 "biodegradable": True, "cell_adhesive": True},
    "matrigel": {"modulus_kpa": 0.5, "gelation": "temperature (37C)",
                 "biodegradable": True, "cell_adhesive": True},
    "peg": {"modulus_kpa": 50, "gelation": "photo/chemical crosslinking",
            "biodegradable": False, "cell_adhesive": False},
    "gelatin_methacryloyl": {"modulus_kpa": 20, "gelation": "photocrosslinking",
                            "biodegradable": True, "cell_adhesive": True},
}

GROWTH_FACTORS = {
    "EGF": {"target": "epithelial cells", "role": "proliferation"},
    "FGF": {"target": "fibroblasts, stem cells", "role": "proliferation/differentiation"},
    "VEGF": {"target": "endothelial cells", "role": "angiogenesis"},
    "BMP-2": {"target": "osteoblasts", "role": "bone formation"},
    "TGF-beta": {"target": "fibroblasts", "role": "ECM production"},
}


class BiomaterialSelector:
    @staticmethod
    def select_hydrogel(application: str, target_modulus_kpa: float = 0,
                        cell_adhesive: bool = True) -> list[str]:
        recs = []
        for name, props in HYDROGELS.items():
            if props["cell_adhesive"] != cell_adhesive:
                continue
            if target_modulus_kpa > 0 and abs(props["modulus_kpa"] - target_modulus_kpa) > 50:
                continue
            recs.append(name)
        app = application.lower()
        if "bone" in app:
            recs = [h for h in recs if h in ("gelatin_methacryloyl", "collagen", "peg")]
        if not recs:
            recs = list(HYDROGELS.keys())
        return recs

    @staticmethod
    def growth_factor_for_cell_type(cell_type: str) -> list[str]:
        ct = cell_type.lower()
        matches = []
        for gf, info in GROWTH_FACTORS.items():
            if ct in info["target"].lower():
                matches.append(gf)
        return matches or list(GROWTH_FACTORS.keys())

    @staticmethod
    def matrix_recommendation(application: str) -> dict:
        return {
            "application": application,
            "hydrogels": BiomaterialSelector.select_hydrogel(application),
            "growth_factors": [gf for gf, info in GROWTH_FACTORS.items()],
        }
