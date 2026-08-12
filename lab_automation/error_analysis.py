"""Technical replicates and pipetting error bounds."""
from __future__ import annotations

import math


class ErrorAnalysis:
    @staticmethod
    def mean_std(replicates: list[float]) -> dict:
        n = len(replicates)
        if n == 0:
            return {"mean": 0.0, "std": 0.0, "sem": 0.0}
        mean = sum(replicates) / n
        if n > 1:
            var = sum((x - mean) ** 2 for x in replicates) / (n - 1)
            std = math.sqrt(var)
            sem = std / math.sqrt(n)
        else:
            std = sem = 0.0
        return {"mean": round(mean, 5), "std": round(std, 5),
                "sem": round(sem, 5), "n": n}

    @staticmethod
    def cv(replicates: list[float]) -> float:
        stats = ErrorAnalysis.mean_std(replicates)
        if stats["mean"] == 0:
            return 0.0
        return round(100.0 * stats["std"] / stats["mean"], 3)

    @staticmethod
    def pipetting_error(volume_ul: float, manufacturer_cv: float = 0.005) -> dict:
        std = volume_ul * manufacturer_cv
        return {"volume_ul": volume_ul, "std_ul": round(std, 4),
                "upper_95": round(volume_ul + 1.96 * std, 4),
                "lower_95": round(volume_ul - 1.96 * std, 4)}

    @staticmethod
    def confidence_interval(mean: float, sem: float, z: float = 1.96) -> dict:
        return {"lower": round(mean - z * sem, 5),
                "upper": round(mean + z * sem, 5),
                "confidence_level": f"{round(100 * (1 - 2 * (1 - 0.975)) if z==1.96 else 0)}%"}

    @staticmethod
    def propagate_division(a: float, sa: float, b: float, sb: float) -> float:
        """Relative uncertainty of a/b."""
        if a == 0 or b == 0:
            return 0.0
        return round(math.sqrt((sa / a) ** 2 + (sb / b) ** 2), 5)
