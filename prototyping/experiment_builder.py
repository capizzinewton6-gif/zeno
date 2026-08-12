"""Wet-lab protocol and assay design."""
from __future__ import annotations


class ExperimentBuilder:
    def build_protocol(self, title: str, objective: str, steps: list[dict],
                       controls: list[str] | None = None) -> dict:
        return {
            "title": title,
            "objective": objective,
            "steps": steps,
            "positive_control": controls[0] if controls else None,
            "negative_control": controls[1] if controls and len(controls) > 1 else None,
            "n_steps": len(steps),
        }

    def build_assay(self, assay_type: str, samples: list[str],
                    replicates: int = 3, readout: str = "absorbance") -> dict:
        return {"assay_type": assay_type, "samples": samples,
                "n_replicates": replicates, "readout": readout,
                "total_wells": len(samples) * replicates + 2}  # +2 controls

    @staticmethod
    def power_analysis(effect_size: float, alpha: float = 0.05,
                       power: float = 0.8) -> int:
        """Rough sample size estimate (normal approximation)."""
        import math
        z_alpha = 1.96  # two-sided alpha=0.05
        z_beta = 0.84    # power=0.80
        if effect_size == 0:
            return -1
        return int(math.ceil(((z_alpha + z_beta) / effect_size) ** 2))
