"""Solves instrumentation, measurement, and experimental error problems."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Iterable

import numpy as np

from tools.constant_engine import CONSTANTS
from calculations.dimensional_analysis import DimensionalAnalysis


@dataclass
class ErrorAnalysis:
    value: float
    uncertainty: float
    relative: float

    def render(self) -> str:
        return (f"value = {self.value:.6g} +/- {self.uncertainty:.3g} "
                f"(relative {self.relative * 100:.2f}%)")


class ExperimentalAgent:
    """Instrumentation, measurement, and error-propagation utilities."""

    @staticmethod
    def propagate(value: float, uncertainties: Iterable[tuple[float, float]]) -> ErrorAnalysis:
        """Gaussian uncertainty propagation: sum of (partial, sigma) contributions squared.

        Each entry is (df/dx_i, sigma_i); total sigma = sqrt(sum (partial_i * sigma_i)^2).
        """
        total = sum((p * s) ** 2 for p, s in uncertainties)
        sigma = math.sqrt(total)
        rel = sigma / abs(value) if value != 0 else float("inf")
        return ErrorAnalysis(value, sigma, rel)

    @staticmethod
    def covariance_propagate(jacobian: np.ndarray, cov: np.ndarray) -> float:
        """sigma^2 = J Cov J^T for a vector of measured quantities."""
        return float(jacobian @ cov @ jacobian.T)

    @staticmethod
    def significance(signal: float, background: float, sigma_b: float) -> float:
        """Discovery significance in sigma: S / sqrt(B + sigma_b^2)."""
        denom = math.sqrt(max(background + sigma_b ** 2, 1e-30))
        return signal / denom

    @staticmethod
    def chisq(observed: np.ndarray, expected: np.ndarray, errors: np.ndarray) -> float:
        return float(np.sum(((observed - expected) / errors) ** 2))

    @staticmethod
    def reduced_chisq(observed: np.ndarray, expected: np.ndarray, errors: np.ndarray, n_params: int) -> float:
        dof = len(observed) - n_params
        return ExperimentalAgent.chisq(observed, expected, errors) / max(dof, 1)

    @staticmethod
    def lock_in_amplitude(signal: np.ndarray, reference: np.ndarray, dt: float) -> dict:
        """Simulate a lock-in amplifier: multiply by reference, low-pass via mean."""
        mixed = signal * reference
        R = np.mean(mixed)
        Q = np.mean(signal * np.roll(reference, len(reference) // 4))
        amplitude = 2 * math.sqrt(R ** 2 + Q ** 2)
        phase = math.atan2(Q, R)
        return {"amplitude": amplitude, "phase": phase, "R": R, "Q": Q}
