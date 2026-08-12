"""Analytical agent — interprets spectroscopy, chromatography, titration, MS data."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from calculations.spectroscopy_math import SpectroscopyMath
from calculations.equilibrium import Equilibrium
from tools.plot_generator import PlotGenerator
from tools.data_analyzer import DataAnalyzer
from src.gemini_25_flash_engine import reason as gemini25_reason


class AnalyticalAgent:
    """Interpret analytical data."""

    def __init__(self, api_key=None):
        self.api_key = api_key
        self.spec = SpectroscopyMath()
        self.eq = Equilibrium()
        self.plotter = PlotGenerator()
        self.analyzer = DataAnalyzer()

    def handle(self, request):
        task = request.get("task", "")
        params = request.get("params", {}) or {}
        # Coerce common numeric params from strings (UI may send strings)
        for k in ("A", "epsilon", "eps", "path_length", "C", "ka", "kb", "pka",
                  "base_conc", "acid_conc", "mass", "charge", "Hz", "MHz", "nm"):
            if k in params and params[k] not in (None, ""):
                try:
                    params[k] = float(params[k])
                except (TypeError, ValueError):
                    pass
        text = task.lower()
        if "beer" in text or "absorbance" in text or "concentration" in text:
            A = params.get("A")
            eps = params.get("epsilon", params.get("eps"))
            b = params.get("path_length", 1.0)
            if A is not None and eps:
                return {"agent": "AnalyticalAgent", "capability": "beer_lambert",
                        "result": {"concentration_M": self.spec.beer_lambert_concentration(A, eps, b)}}
            c = params.get("C")
            if c is not None and eps:
                return {"agent": "AnalyticalAgent", "capability": "beer_lambert",
                        "result": {"absorbance": self.spec.beer_lambert_absorbance(c, eps, b)}}
        if "nmr" in text:
            peaks = params.get("peaks", [(7.26, 1.0, "solvent"), (2.1, 3.0, "CH3")])
            return {"agent": "AnalyticalAgent", "capability": "nmr_simulation",
                    "result": self.plotter.nmr_spectrum(peaks)}
        if "chromat" in text or "hplc" in text:
            peaks = params.get("peaks", [(3.1, 2.1e5, "product"), (5.2, 0.4e5, "impurity")])
            return {"agent": "AnalyticalAgent", "capability": "chromatogram",
                    "result": self.plotter.chromatogram(peaks)}
        if "ph" in text or "acid" in text or "buffer" in text:
            ka = params.get("ka")
            c = params.get("C")
            # Try to extract concentration & known Ka from natural language
            import re
            if c is None:
                m = re.search(r"([\d.eE+-]+)\s*M\b", task)
                if m:
                    c = float(m.group(1))
            if ka is None:
                known_ka = {"acetic": 1.8e-5, "acetate": 1.8e-5, "formic": 1.78e-4,
                            "benzoic": 6.3e-5, "hydrofluoric": 6.6e-4, "hf": 6.6e-4,
                            "nitrous": 4.5e-4, "chloroacetic": 1.4e-3, "ammonium": 5.6e-10,
                            "cyanic": 3.5e-4, "lactic": 1.38e-4, "carbonic": 4.3e-7}
                for name, k in known_ka.items():
                    if name in text:
                        ka = k
                        break
            if ka and c:
                return {"agent": "AnalyticalAgent", "capability": "weak_acid_pH",
                        "result": {"pH": self.eq.weak_acid_ph(ka, c),
                                   "ka": ka, "concentration_M": c}}
            pka = params.get("pka")
            base = params.get("base_conc")
            acid = params.get("acid_conc")
            if pka and base and acid:
                return {"agent": "AnalyticalAgent", "capability": "buffer",
                        "result": {"pH": self.eq.henderson_hasselbalch(pka, base, acid)}}
        if "ms" in text or "mass spec" in text:
            mass = params.get("mass", 130.0651)
            charge = params.get("charge", 1)
            return {"agent": "AnalyticalAgent", "capability": "mass_spec",
                    "result": {"mz": self.spec.mass_to_charge(mass, charge)}}
        # Default: general interpretation via AI
        return {"agent": "AnalyticalAgent", "capability": "interpretation",
                "result": gemini25_reason(task, context=params, api_key=self.api_key)}
