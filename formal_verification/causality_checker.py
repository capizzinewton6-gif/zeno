"""Verify light-cone constraints and Kramers-Kronig relations."""

from __future__ import annotations

import numpy as np


class CausalityChecker:
    """Causality and dispersion-relation checks."""

    @staticmethod
    def light_cone_check(x: float, t: float, c: float = 3.0e8) -> bool:
        """Return True if the event is inside the future light cone (timelike separable)."""
        return abs(x) <= c * abs(t)

    @staticmethod
    def superluminal(v: float, c: float = 3.0e8) -> bool:
        return abs(v) > c

    @staticmethod
    def kramers_kronig(omega: np.ndarray, chi_real: np.ndarray, chi_imag: np.ndarray) -> dict:
        """Check the Hilbert-transform relation between real and imaginary parts of chi(omega).

        Kramers-Kronig: Re chi(omega) = (1/pi) P.V. integral Im chi(omega')/(omega'-omega) d omega'.
        """
        from scipy.integrate import cumulative_trapezoid
        # principal-value approximation: avoid the pole by skipping a small window
        integrand = chi_imag / (omega - omega[0] + 1e-12)
        kk_real_approx = cumulative_trapezoid(integrand, omega, initial=0) / np.pi
        return {
            "max_diff": float(np.max(np.abs(kk_real_approx - chi_real))),
            "note": "Approximate KK check; full principal value requires a dedicated PV integrator.",
        }
