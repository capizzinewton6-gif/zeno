"""Unphysical-state detection layer.

Catches results that violate basic physical principles before they are presented
to the user, e.g. negative mass, superluminal signalling, non-unitary evolution.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from tools.constant_engine import CONSTANTS


@dataclass
class SafetyViolation:
    rule: str
    detail: str
    severity: str = "high"  # high | medium | low


@dataclass
class SafetyReport:
    violations: list[SafetyViolation] = field(default_factory=list)
    ok: bool = True

    def add(self, v: SafetyViolation) -> None:
        self.violations.append(v)
        self.ok = False

    def summary(self) -> str:
        if self.ok:
            return "No unphysical states detected. All checks passed."
        lines = [f"[{v.severity.upper()}] {v.rule}: {v.detail}" for v in self.violations]
        return "\n".join(lines)


class SafetyLayer:
    """Rule-based checks against common unphysical results."""

    C = CONSTANTS.value("c")

    def check_mass(self, m: float) -> SafetyReport:
        rep = SafetyReport()
        if m < 0:
            rep.add(SafetyViolation("No negative mass", f"mass = {m} kg is negative"))
        return rep

    def check_speed(self, v: float) -> SafetyReport:
        rep = SafetyReport()
        if abs(v) > self.C:
            rep.add(SafetyViolation("No superluminal signalling", f"v = {v} m/s exceeds c = {self.C} m/s"))
        return rep

    def check_temperature(self, T: float) -> SafetyReport:
        rep = SafetyReport()
        if T < 0:
            rep.add(SafetyViolation("No negative absolute temperature", f"T = {T} K is below absolute zero"))
        return rep

    def check_probability(self, p: float) -> SafetyReport:
        rep = SafetyReport()
        if not (0.0 <= p <= 1.0 + 1e-9):
            rep.add(SafetyViolation("Probability bounded in [0,1]", f"p = {p} is outside [0,1]"))
        return rep

    def check_unitarity(self, matrix, tol: float = 1e-6) -> SafetyReport:
        import numpy as np
        rep = SafetyReport()
        M = np.asarray(matrix, dtype=complex)
        if M.ndim != 2 or M.shape[0] != M.shape[1]:
            rep.add(SafetyViolation("Unitarity requires a square matrix", f"shape {M.shape}"))
            return rep
        ident = M.conj().T @ M
        if not np.allclose(ident, np.eye(M.shape[0]), atol=tol):
            rep.add(SafetyViolation("S-matrix / evolution must be unitary", "M^dagger M != I"))
        return rep

    def check_energy(self, E: float) -> SafetyReport:
        rep = SafetyReport()
        if E < 0:
            rep.add(SafetyViolation("No negative total energy for a bound ground state", f"E = {E} J"))
        return rep

    def full_check(self, **values: Any) -> SafetyReport:
        rep = SafetyReport()
        for key, val in values.items():
            sub: SafetyReport | None = None
            if key == "mass":
                sub = self.check_mass(val)
            elif key == "speed":
                sub = self.check_speed(val)
            elif key == "temperature":
                sub = self.check_temperature(val)
            elif key == "probability":
                sub = self.check_probability(val)
            elif key == "energy":
                sub = self.check_energy(val)
            if sub is not None:
                for v in sub.violations:
                    rep.add(v)
        return rep


SAFETY = SafetyLayer()
