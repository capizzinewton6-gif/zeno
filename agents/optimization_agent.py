"""Optimization agent — optimizes reaction conditions, stoichiometry, purifications."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from calculations.stoichiometry import Stoichiometry
from calculations.kinetics import Kinetics
from calculations.thermodynamics import Thermodynamics
from synthesis.yield_predictor import YieldPredictor
from src.gemini_25_flash_engine import reason as gemini25_reason


class OptimizationAgent:
    """Optimize reaction conditions and stoichiometry."""

    def __init__(self, api_key=None):
        self.api_key = api_key
        self.stoich = Stoichiometry()
        self.kinetics = Kinetics()
        self.thermo = Thermodynamics()
        self.yield_pred = YieldPredictor()

    def handle(self, request):
        task = request.get("task", "")
        params = request.get("params", {}) or {}
        text = task.lower()
        if "stoichiom" in text or "limiting" in text or "mole" in text:
            reactants = params.get("reactants", [])
            if reactants:
                return {"agent": "OptimizationAgent", "capability": "limiting_reagent",
                        "result": self.stoich.limiting_reagent(reactants)}
            return {"agent": "OptimizationAgent", "capability": "stoichiometry",
                    "result": "Provide reactants list with moles and coefficients."}
        if "kinetic" in text or "rate" in text or "arrhenius" in text:
            return {"agent": "OptimizationAgent", "capability": "kinetics",
                    "result": self._kinetics(params)}
        if "thermo" in text or "enthalpy" in text or "gibbs" in text:
            return {"agent": "OptimizationAgent", "capability": "thermodynamics",
                    "result": self._thermo(params)}
        # Default: DOE / condition optimization
        return {"agent": "OptimizationAgent", "capability": "condition_optimization",
                "result": self._doe(params)}

    def _kinetics(self, params):
        if "A" in params and "Ea" in params and "T" in params:
            return {"arrhenius_k": self.kinetics.arrhenius_rate(params["A"], params["Ea"], params["T"])}
        return {"note": "Provide A, Ea (J/mol), T (K) for Arrhenius."}

    def _thermo(self, params):
        if "dH" in params and "dS" in params and "T" in params:
            return {"dG_kJ_mol": self.thermo.gibbs_free_energy(params["dH"], params["dS"], params["T"])}
        return {"note": "Provide dH (kJ), dS (kJ/K), T (K)."}

    def _doe(self, params):
        factors = params.get("factors", {"temperature": [25, 50, 80],
                                         "equiv": [1.0, 1.5, 2.0],
                                         "catalyst_loading": [0.01, 0.05, 0.1]})
        runs = 1
        for vals in factors.values():
            runs *= len(vals)
        return {
            "design": "full-factorial",
            "factors": factors,
            "total_runs": runs,
            "recommendation": "Run full factorial or fractional factorial; analyze via ANOVA.",
            "ai_enrichment": gemini25_reason(
                "Suggest a design-of-experiments plan to optimize a Suzuki coupling yield.",
                context={"factors": factors}, api_key=self.api_key),
        }
