"""First-principles reasoning and asymptotic scaling analysis."""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ReasoningStep:
    title: str
    detail: str
    result: str = ""


@dataclass
class ReasoningTrace:
    question: str
    steps: list[ReasoningStep] = field(default_factory=list)
    conclusion: str = ""

    def add(self, title: str, detail: str, result: str = "") -> "ReasoningTrace":
        self.steps.append(ReasoningStep(title, detail, result))
        return self

    def as_text(self) -> str:
        lines = [f"Problem: {self.question}", ""]
        for i, s in enumerate(self.steps, 1):
            lines.append(f"{i}. {s.title}")
            lines.append(f"   {s.detail}")
            if s.result:
                lines.append(f"   -> {s.result}")
        lines.append("")
        lines.append(f"Conclusion: {self.conclusion}")
        return "\n".join(lines)


class ReasoningEngine:
    """Structured first-principles decomposition for physics problems."""

    # Registry of regimes the engine knows how to classify.
    REGIMES = {
        "classical": ["newton", "lagrangian", "hamiltonian", "rigid body", "oscillator"],
        "electromagnetic": ["maxwell", "wave", "circuit", "antenna", "relativistic ed"],
        "quantum": ["wavefunction", "operator", "spin", "tunneling", "perturbation"],
        "thermal": ["heat", "entropy", "statistical", "phase", "kinetic theory"],
        "relativistic": ["lorentz", "four-vector", "e=mc^2", "geodesic", "metric"],
        "field_theory": ["feynman", "s-matrix", "gauge", "qed", "qcd"],
        "astro": ["stellar", "orbit", "cosmology", "dark energy", "cmb"],
        "condensed": ["band", "lattice", "phonon", "superconductor"],
    }

    def classify_regime(self, problem: str) -> list[str]:
        p = problem.lower()
        hits: list[str] = []
        for regime, keywords in self.REGIMES.items():
            if any(k in p for k in keywords):
                hits.append(regime)
        return hits or ["classical"]

    def identify_dofs(self, regime: str, problem: str) -> list[str]:
        """Heuristic identification of relevant degrees of freedom."""
        p = problem.lower()
        if regime == "classical":
            if "pendulum" in p or "oscillator" in p:
                return ["generalized coordinate q(t)", "conjugate momentum p(t)"]
            if "rigid body" in p or "rotation" in p:
                return ["Euler angles (theta, phi, psi)", "angular momentum L"]
            return ["position r(t)", "velocity v(t)"]
        if regime == "quantum":
            return ["wavefunction psi(x,t)", "energy eigenvalues E_n"]
        if regime == "thermal":
            return ["temperature T", "partition function Z", "entropy S"]
        if regime == "relativistic":
            return ["four-momentum p^mu", "proper time tau"]
        if regime == "field_theory":
            return ["field phi(x)", "coupling constants g", "S-matrix elements"]
        if regime == "astro":
            return ["orbital elements", "Hubble parameter H(z)"]
        if regime == "condensed":
            return ["crystal momentum k", "band energies E_n(k)"]
        return ["system state variables"]

    def governing_equations(self, regime: str) -> list[str]:
        return {
            "classical": ["F = m a", "L = T - V  ->  d/dt(dL/dqdot) = dL/dq", "H = p qdot - L"],
            "electromagnetic": ["Maxwell: div E = rho/eps0, curl B = mu0 J + mu0 eps0 dE/dt", "wave eq: box E = 0"],
            "quantum": ["i hbar dpsi/dt = H psi", "H psi = E psi  (eigenvalue)", "<H> integral"],
            "thermal": ["dS = dQ/T", "Z = sum exp(-beta E)", "F = -kT ln Z"],
            "relativistic": ["p^mu p_mu = -m^2 c^2", "E^2 = (pc)^2 + (mc^2)^2", "ds^2 = g_ab dx^a dx^b"],
            "field_theory": ["Euler-Lagrange on L", "S-matrix unitarity", "Ward identities"],
            "astro": ["dr/dt = v", "F = -G M m / r^2", "H^2 = (8pi G/3) rho"],
            "condensed": ["Bloch: psi_k(r) = u_k(r) e^{ik.r}", "Born-von Karman BCs"],
        }.get(regime, ["Apply the relevant equations of motion"])

    def asymptotic_scaling(self, expression: str, small_param: str = "x") -> str:
        """Report leading scaling of an expression as small_param -> 0."""
        expr = expression.replace(" ", "")
        # Very small symbolic heuristic: detect common leading powers.
        rules = {
            "sin(x)": f"~ {small_param}   (leading order of sin)",
            "cos(x)": "~ 1 - x^2/2",
            "tan(x)": f"~ {small_param}",
            "exp(x)": "~ 1 + x",
            "ln(1+x)": f"~ {small_param}",
            "1/(1+x)": f"~ 1 - {small_param}",
        }
        for pat, scaling in rules.items():
            if pat.replace("x", small_param) in expr:
                return scaling
        return f"Expand in powers of {small_param}; leading term is constant/linear unless otherwise indicated."

    def decompose(self, problem: str) -> ReasoningTrace:
        trace = ReasoningTrace(question=problem)
        regimes = self.classify_regime(problem)
        regime = regimes[0]
        trace.add("Regime identification",
                  f"The problem keywords map to the {regime} regime" +
                  (f" (also touches {', '.join(regimes[1:])})" if len(regimes) > 1 else ""),
                  regime)
        dofs = self.identify_dofs(regime, problem)
        trace.add("Degrees of freedom",
                  "Identify the independent variables that describe the system state.",
                  ", ".join(dofs))
        eqns = self.governing_equations(regime)
        trace.add("Governing equations",
                  "Select the principle that generates the equations of motion.",
                  "; ".join(eqns))
        trace.add("Boundary/initial conditions",
                  "Specify the state at the reference time/surface to fix integration constants.",
                  "Apply physically motivated constraints")
        trace.add("Solve and verify",
                  "Solve exactly where possible, else numerically with stated tolerance. "
                  "Check dimensions, conservation, and limits.",
                  "Compute, then verify")
        trace.conclusion = (
            f"Approach: formulate in the {regime} framework using "
            f"({', '.join(dofs[:2])}) and the equations {eqns[0]}.")
        return trace


REASONING = ReasoningEngine()
