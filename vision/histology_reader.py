"""Tissue section slide and pathology analysis."""
from __future__ import annotations

import numpy as np


STAINING_PROTOCOLS = {
    "H&E": {"target": "general tissue morphology", "nuclei": "blue (hematoxylin)", "cytoplasm": "pink (eosin)"},
    "IHC": {"target": "specific antigens", "signal": "brown (DAB) or red (AEC)"},
    "PAS": {"target": "glycogen, mucopolysaccharides", "signal": "magenta"},
    "Masson's trichrome": {"target": "collagen vs muscle", "collagen": "blue", "muscle": "red"},
    "Giemsa": {"target": "blood smears, parasites", "nuclei": "purple", "cytoplasm": "blue"},
}


class HistologyReader:
    @staticmethod
    def staining_lookup(stain: str) -> dict:
        return STAINING_PROTOCOLS.get(stain,
                                       {"error": f"Unknown stain '{stain}'"})

    @staticmethod
    def nuclear_density(dapi_image: np.ndarray, threshold: float = 0.3) -> dict:
        """Estimate nuclear density from a DAPI-like channel."""
        from scipy import ndimage
        if dapi_image.ndim == 3:
            dapi_image = dapi_image.mean(axis=2)
        norm = dapi_image / max(dapi_image.max(), 1e-9)
        binary = norm > threshold
        labeled, n = ndimage.label(binary)
        area = dapi_image.size
        return {"nuclei_count": int(n),
                "nuclei_per_unit_area": round(n / (area / 1e6), 3)}

    @staticmethod
    def tumor_grade(mitotic_count_per_hpf: float, necrosis_pct: float,
                    differentiation: str = "moderate") -> str:
        """A simple combined-score tumor grade (illustrative)."""
        score = 0
        if mitotic_count_per_hpf > 10:
            score += 2
        elif mitotic_count_per_hpf > 5:
            score += 1
        if necrosis_pct > 50:
            score += 2
        elif necrosis_pct > 20:
            score += 1
        if score >= 4:
            return "high grade"
        if score >= 2:
            return "intermediate grade"
        return "low grade"

    @staticmethod
    def area_fraction(image: np.ndarray, threshold: float = 0.5) -> float:
        if image.ndim == 3:
            image = image.mean(axis=2)
        norm = image / max(image.max(), 1e-9)
        return round(100.0 * float(np.sum(norm > threshold) / image.size), 2)
