"""Analyzes bioreactor and lab apparatus images."""
from __future__ import annotations

import numpy as np


APPARATUS_TYPES = {
    "bioreactor": {"key_features": ["vessel", "impeller", "probe ports", "gas sparger"],
                   "typical_volume_l": "1-10000"},
    "shaker_flask": {"key_features": ["erlenmeyer", "baffled", " vent cap"],
                     "typical_volume_ml": "50-3000"},
    "microplate": {"key_features": ["96/384 wells", "rectangular grid"],
                   "typical_volume_ul": "50-200"},
    "fermenter": {"key_features": ["jacketed vessel", "sterile sampling", "harvest valve"],
                  "typical_volume_l": "1-500"},
}


class ApparatusAnalyzer:
    @staticmethod
    def identify(apparatus_type: str) -> dict:
        return APPARATUS_TYPES.get(apparatus_type.lower(),
                                    {"error": f"Unknown apparatus '{apparatus_type}'"})

    @staticmethod
    def foam_level(image: np.ndarray, liquid_threshold: float = 0.5) -> dict:
        """Estimate foam vs liquid fraction from a side-view image column."""
        if image.ndim == 3:
            image = image.mean(axis=2)
        norm = image / max(image.max(), 1e-9)
        col_mean = norm.mean(axis=1)
        liquid_rows = np.sum(col_mean < liquid_threshold)
        foam_rows = len(col_mean) - liquid_rows
        return {"liquid_fraction": round(float(liquid_rows / len(col_mean)), 3),
                "foam_fraction": round(float(foam_rows / len(col_mean)), 3),
                "foam_present": foam_rows > 0.1 * len(col_mean)}

    @staticmethod
    def fill_level(image: np.ndarray) -> float:
        """Estimate fill fraction of a vessel from side-view intensity."""
        if image.ndim == 3:
            image = image.mean(axis=2)
        col_mean = image.mean(axis=1)
        threshold = col_mean.mean()
        filled = np.sum(col_mean < threshold)
        return round(float(filled / len(col_mean)), 3)
