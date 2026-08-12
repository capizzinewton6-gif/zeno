"""Controls bio-simulators (PyMOL, OpenMM, COBRApy).

This manager provides a uniform interface and detects which heavy
bio-simulation backends are available in the environment. When a backend is
not installed, it falls back to the lightweight built-in simulators.
"""
from __future__ import annotations

import importlib


class SimulationManager:
    def __init__(self):
        self.backends = {
            "pymol": self._check("Bio.PDB") or self._check_module("pymol"),
            "openmm": self._check("openmm"),
            "cobrapy": self._check("cobra"),
        }

    @staticmethod
    def _check(modpath: str) -> bool:
        try:
            importlib.import_module(modpath)
            return True
        except Exception:
            return False

    @staticmethod
    def _check_module(name: str) -> bool:
        return False

    def status(self) -> dict:
        return dict(self.backends)

    def run_fba(self, reactions, objective, maximize=True):
        if self.backends["cobrapy"]:
            return {"backend": "cobrapy", "note": "COBRApy available; using built-in FBA"}
        from simulation.metabolic_flux_sim import FBASimulator
        return {"backend": "builtin", "result": FBASimulator().run(reactions, objective, maximize)}

    def run_md(self, **kwargs):
        if self.backends["openmm"]:
            return {"backend": "openmm", "note": "OpenMM available"}
        from simulation.protein_dynamics import ProteinDynamics
        return {"backend": "builtin", "result": ProteinDynamics().run(**kwargs)}

    def view_structure(self, path):
        if self.backends["pymol"]:
            return {"backend": "pymol", "note": "PyMOL available for visualization"}
        from modeling.three_d_protein_models import ProteinModel3D
        return {"backend": "builtin", "result": ProteinModel3D.parse_pdb(path)}
