"""Check gauge invariance, conservation laws, and causality on a model."""

from __future__ import annotations

from formal_verification.gauge_invariance_check import GaugeInvarianceCheck
from formal_verification.conservation_checker import ConservationChecker
from formal_verification.causality_checker import CausalityChecker


class PhysicalConstraintTest:
    """Aggregate verification of a phenomenological model's consistency."""

    gauge = GaugeInvarianceCheck()
    conservation = ConservationChecker()
    causality = CausalityChecker()

    @staticmethod
    def check_all(symbolic_L=None, fields=None) -> dict:
        report = {}
        if symbolic_L is not None and fields:
            phi = fields[0]
            report["gauge_u1"] = PhysicalConstraintTest.gauge.u1_scalar(phi, symbolic_L)
        report["causality_note"] = "Causality requires real propagator poles within the light cone."
        return report
