"""Quantum agent — executes ab initio electronic structure calculations."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from calculations.quantum_math import QuantumMath
from src.gemini_25_flash_engine import reason as gemini25_reason


class QuantumAgent:
    """Orchestrate electronic-structure calculations.

    Uses local QuantumMath helpers for analytic models and would dispatch
    to external engines (ORCA/Gaussian/PySCF) when configured. Simulations
    are presented on the UI.
    """

    BASIS_SETS = ["STO-3G", "3-21G", "6-31G*", "6-311G**", "cc-pVDZ", "cc-pVTZ", "def2-TZVP"]
    METHODS = ["HF", "B3LYP", "M06-2X", "MP2", "CCSD(T)", "PBE0", "wB97X-D"]

    def __init__(self, api_key=None):
        self.api_key = api_key
        self.math = QuantumMath()

    def handle(self, request):
        task = request.get("task", "")
        params = request.get("params", {}) or {}
        text = task.lower()
        if "hydrogen" in text or "h atom" in text:
            n = int(params.get("n", 1))
            return {"agent": "QuantumAgent", "capability": "hydrogen_atom",
                    "result": {"energy_n_eV": self.math.hydrogen_energy_n(n),
                               "bohr_radius_m": self.math.bohr_radius_n(n, params.get("Z", 1))}}
        if "particle in a box" in text:
            return {"agent": "QuantumAgent", "capability": "particle_in_box",
                    "result": {"energy_J": self.math.particle_in_box_energy(int(params.get("n", 1)),
                                                                            float(params.get("L_m", 1e-9)))}}
        if "harmonic" in text:
            return {"agent": "QuantumAgent", "capability": "harmonic_oscillator",
                    "result": {"energy_J": self.math.harmonic_oscillator_energy(int(params.get("n", 0)),
                                                                                 float(params.get("omega", 1e14)))}}
        # Default: Gaussian basis overlap
        return {"agent": "QuantumAgent", "capability": "basis_overlap",
                "result": {"overlap": self.math.gaussian_overlap(float(params.get("alpha", 0.5)),
                                                                  float(params.get("beta", 0.5)),
                                                                  float(params.get("R", 1.0)))},
                "available_methods": self.METHODS, "available_basis_sets": self.BASIS_SETS}

    def run_calculation(self, smiles_or_xyz, method="B3LYP", basis="6-31G*"):
        """Describe a computational job (actual execution requires external engine)."""
        job = {
            "agent": "QuantumAgent",
            "input": smiles_or_xyz,
            "method": method,
            "basis_set": basis,
            "status": "prepared (simulation)",
            "note": "Configure ORCA/Gaussian/PySCF path in config/paths.json for live execution.",
        }
        job["ai_enrichment"] = gemini25_reason(
            f"Propose what electronic properties to compute with {method}/{basis} for {smiles_or_xyz}.",
            api_key=self.api_key)
        return job
