"""Cold-chain (-80C, liquid N2) and sample tracking."""
from __future__ import annotations

import time


STORAGE_CONDITIONS = {
    "4C": {"name": "refrigerator", "ttl_days": 7, "use": "short-term reagents, media"},
    "-20C": {"name": "freezer", "ttl_days": 365, "use": "enzymes, DNA, primers"},
    "-80C": {"name": "ultra-low freezer", "ttl_days": 3650, "use": "cell lines, tissue, proteins"},
    "liquid_N2": {"name": "cryogenic (vapor)", "ttl_days": 36500, "use": "cells, gametes, embryos"},
    "RT": {"name": "room temperature", "ttl_days": 30, "use": "chemicals, dried reagents"},
}


class BiohazardStorage:
    @staticmethod
    def assign_condition(sample_type: str) -> str:
        s = sample_type.lower()
        if "cell" in s or "line" in s:
            return "liquid_N2"
        if "protein" in s or "tissue" in s:
            return "-80C"
        if "dna" in s or "rna" in s or "primer" in s or "enzyme" in s:
            return "-20C"
        if "media" in s:
            return "4C"
        return "RT"

    @staticmethod
    def condition_info(condition: str) -> dict:
        return STORAGE_CONDITIONS.get(condition,
                                       {"error": f"Unknown condition {condition}"})

    @staticmethod
    def expiration(storage_date_iso: str, condition: str = "-20C") -> str:
        """Estimate expiration date from storage start and condition."""
        info = STORAGE_CONDITIONS.get(condition)
        if not info:
            return "unknown"
        from datetime import datetime, timedelta
        try:
            d = datetime.fromisoformat(storage_date_iso)
            expiry = d + timedelta(days=info["ttl_days"])
            return expiry.date().isoformat()
        except Exception:
            return "invalid date"

    @staticmethod
    def temperature_log_readings(readings: list[float], target: float,
                                 tolerance: float = 2.0) -> dict:
        excursions = [(i, r) for i, r in enumerate(readings)
                      if abs(r - target) > tolerance]
        return {"target": target, "n_readings": len(readings),
                "n_excursions": len(excursions),
                "excursions": excursions[:10],
                "status": "ok" if not excursions else "ALARM: temperature excursion"}


class SampleTracker:
    def __init__(self):
        self.samples: dict[str, dict] = {}

    def register(self, sample_id: str, sample_type: str, location: str) -> dict:
        self.samples[sample_id] = {
            "id": sample_id, "type": sample_type,
            "location": location,
            "registered_at": time.time(),
        }
        return self.samples[sample_id]

    def retrieve(self, sample_id: str) -> dict | None:
        return self.samples.get(sample_id)

    def move(self, sample_id: str, new_location: str) -> dict | None:
        s = self.samples.get(sample_id)
        if s:
            s["location"] = new_location
            s["last_moved"] = time.time()
        return s
