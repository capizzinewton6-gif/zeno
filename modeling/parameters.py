"""Kinetic constants (Km, Vmax), mutation rates, and other biological parameters."""
from __future__ import annotations

# Representative enzyme kinetic parameters (literature values)
ENZYME_PARAMS = {
    "hexokinase": {"km_mM": 0.05, "vmax": 1.0, "substrate": "glucose"},
    "penicillinase": {"km_mM": 0.05, "vmax": 2000.0, "substrate": "penicillin"},
    "carbonic_anhydrase": {"km_mM": 8.0, "vmax": 600000.0, "substrate": "CO2"},
    "trypsin": {"km_mM": 0.1, "vmax": 100.0, "substrate": "casein"},
}

MUTATION_RATES = {
    "escherichia coli": 2.2e-10,  # per bp per generation
    "saccharomyces cerevisiae": 3.3e-10,
    "homo sapiens": 1.2e-8,  # per bp per generation (germline)
    "drosophila melanogaster": 3.5e-9,
}

POPULATION_SIZES = {
    "escherichia coli": 1e8,  # per mL in rich culture (rough)
    "human_ne": 10000,
}


class Parameters:
    @staticmethod
    def get_enzyme(name: str) -> dict:
        return ENZYME_PARAMS.get(name.lower(),
                                 {"error": f"No parameters for '{name}'"})

    @staticmethod
    def mutation_rate(organism: str) -> float | None:
        return MUTATION_RATES.get(organism.lower())

    @staticmethod
    def population_size(organism: str) -> float | None:
        return POPULATION_SIZES.get(organism.lower())

    @staticmethod
    def q10(rate_at_t1: float, t1: float, t2: float, q10: float = 2.0) -> float:
        """Adjust rate for a 10 C temperature change using Q10 factor."""
        import math
        return rate_at_t1 * q10 ** ((t2 - t1) / 10.0)

    @staticmethod
    def doubling_time_from_growth_rate(mu: float) -> float:
        import math
        if mu <= 0:
            raise ValueError("Growth rate must be > 0")
        return math.log(2) / mu
