"""Engineering formula engine: a library of common formulas."""

from __future__ import annotations

import math

FORMULAS = {
    "ohms_law": {"expr": "V = I * R", "params": ["V", "I", "R"],
                 "solve": {"V": lambda i, r: i * r,
                           "I": lambda v, r: v / r,
                           "R": lambda v, i: v / i}},
    "power_dc": {"expr": "P = V * I", "params": ["P", "V", "I"],
                 "solve": {"P": lambda v, i: v * i,
                           "V": lambda p, i: p / i,
                           "I": lambda p, v: p / v}},
    "kinetic_energy": {"expr": "KE = 0.5 * m * v^2", "params": ["KE", "m", "v"],
                       "solve": {"KE": lambda m, v: 0.5 * m * v ** 2,
                                 "m": lambda ke, v: 2 * ke / v ** 2,
                                 "v": lambda ke, m: math.sqrt(2 * ke / m)}},
    "pressure": {"expr": "P = F / A", "params": ["P", "F", "A"],
                 "solve": {"P": lambda f, a: f / a,
                           "F": lambda p, a: p * a,
                           "A": lambda f, p: f / p}},
    "torque": {"expr": "T = F * r", "params": ["T", "F", "r"],
               "solve": {"T": lambda f, r: f * r,
                         "F": lambda t, r: t / r,
                         "r": lambda t, f: t / f}},
    "area_circle": {"expr": "A = pi * r^2", "params": ["A", "r"],
                    "solve": {"A": lambda r: math.pi * r ** 2,
                              "r": lambda a: math.sqrt(a / math.pi)}},
    "carnot_efficiency": {"expr": "eta = 1 - Tc/Th", "params": ["eta", "Tc", "Th"],
                          "solve": {"eta": lambda tc, th: 1 - tc / th,
                                    "Tc": lambda e, th: th * (1 - e),
                                    "Th": lambda e, tc: tc / (1 - e)}},
}


class FormulaEngine:
    def __init__(self):
        self.formulas = dict(FORMULAS)

    def list(self) -> dict:
        return {k: v["expr"] for k, v in self.formulas.items()}

    def solve(self, name: str, solve_for: str, **values) -> float:
        if name not in self.formulas:
            raise KeyError(f"Unknown formula: {name}")
        solvers = self.formulas[name]["solve"]
        if solve_for not in solvers:
            raise KeyError(f"Cannot solve for {solve_for} in {name}")
        return solvers[solve_for](**values)

    def add(self, name: str, expr: str, params: list[str], solvers: dict):
        self.formulas[name] = {"expr": expr, "params": params, "solve": solvers}
