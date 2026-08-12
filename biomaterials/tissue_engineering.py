"""Scaffold properties and cell seeding density."""
from __future__ import annotations

import math


class TissueEngineering:
    @staticmethod
    def porosity(solid_volume: float, total_volume: float) -> float:
        if total_volume == 0:
            return 0.0
        return round(1 - solid_volume / total_volume, 4)

    @staticmethod
    def cell_seeding_density(cell_count: int, scaffold_volume_ml: float) -> float:
        if scaffold_volume_ml == 0:
            return 0.0
        return round(cell_count / scaffold_volume_ml, 2)

    @staticmethod
    def youngs_modulus(force_n: float, area_m2: float, strain: float) -> float:
        if area_m2 == 0 or strain == 0:
            return 0.0
        return round(force_n / (area_m2 * strain), 4)

    @staticmethod
    def degradation_rate(initial_mass: float, mass_at_time: float, days: float) -> float:
        if initial_mass <= 0 or days <= 0:
            return 0.0
        return round((initial_mass - mass_at_time) / (initial_mass * days), 5)

    @staticmethod
    def oxygen_diffusion(consumption_rate: float, diffusion_coef: float,
                         cell_density: float) -> float:
        """Maximum penetration depth of oxygen in a tissue construct."""
        if consumption_rate * cell_density <= 0:
            return 0.0
        return round(math.sqrt(2 * diffusion_coef /
                               (consumption_rate * cell_density)), 5)
