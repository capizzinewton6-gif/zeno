"""Optimization agent: solves constrained and unconstrained optimization problems."""

from __future__ import annotations

from typing import Any, Callable

from mathematics_ai.agents.base import BaseAgent, AgentResult
from mathematics_ai.numerical_computing import optimization_solver


class OptimizationAgent(BaseAgent):
    """Dispatches optimization problems to the appropriate solver."""

    name = "optimization_agent"

    def minimize(self, f: Callable, x0: list[float], method: str = "BFGS") -> AgentResult:
        res = optimization_solver.minimize_nonlinear(f, x0, method=method)
        return self.result(res, steps=[{"method": method, "x0": x0}], objective_value=res["fun"])

    def linear_program(self, c: list[float], A_ub=None, b_ub=None, A_eq=None, b_eq=None) -> AgentResult:
        res = optimization_solver.linear_program(c, A_ub, b_ub, A_eq, b_eq)
        return self.result(res, steps=[{"type": "linear_program"}])

    def curve_fit(self, f: Callable, xdata: list[float], ydata: list[float], p0=None) -> AgentResult:
        res = optimization_solver.least_squares_curve_fit(f, xdata, ydata, p0)
        return self.result(res, steps=[{"type": "curve_fit"}])

    def quadratic_program(self, H: list[list[float]], f: list[float]) -> AgentResult:
        res = optimization_solver.quadratic_program(H, f)
        return self.result(res, steps=[{"type": "quadratic_program"}])

    def integer_program(self, c: list[float], bounds: list[tuple[int, int]]) -> AgentResult:
        res = optimization_solver.integer_program(c, bounds)
        return self.result(res, steps=[{"type": "integer_program"}])

    def constrained(self, f: Callable, bounds: list[tuple[float, float]], x0: list[float]) -> AgentResult:
        res = optimization_solver.convex_constrained(f, bounds, x0)
        return self.result(res, steps=[{"type": "constrained"}])
