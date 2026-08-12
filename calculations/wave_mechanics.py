"""Fourier optics, dispersion relations, and the scattering matrix (S-matrix)."""

from __future__ import annotations

import math

import numpy as np
from numpy.fft import fft, fftfreq, ifft


class WaveMechanics:
    """Fourier-domain wave and scattering utilities."""

    @staticmethod
    def fourier_transform(signal: np.ndarray, dt: float = 1.0) -> tuple[np.ndarray, np.ndarray]:
        """Return (frequencies, spectrum) of a real time-series."""
        n = len(signal)
        spectrum = fft(signal)
        freqs = fftfreq(n, d=dt)
        return freqs, spectrum

    @staticmethod
    def inverse_transform(spectrum: np.ndarray) -> np.ndarray:
        return np.real(ifft(spectrum))

    @staticmethod
    def power_spectrum(signal: np.ndarray, dt: float = 1.0) -> tuple[np.ndarray, np.ndarray]:
        freqs, spec = WaveMechanics.fourier_transform(signal, dt)
        return freqs, np.abs(spec) ** 2

    @staticmethod
    def dispersion_wave(k: np.ndarray, depth: float, g: float = 9.80665) -> np.ndarray:
        """Deep/shallow water gravity-wave dispersion: omega^2 = g k tanh(k h)."""
        return np.sqrt(g * k * np.tanh(k * depth))

    @staticmethod
    def group_velocity(omega: np.ndarray, k: np.ndarray) -> np.ndarray:
        """d omega / d k via finite differences."""
        return np.gradient(omega, k)

    @staticmethod
    def scattering_matrix(transmission: float, reflection: float, n: int = 1) -> np.ndarray:
        """Build a 2-port S-matrix from T and R (lossless if T+R=1)."""
        r = math.sqrt(max(reflection, 0.0))
        t = math.sqrt(max(transmission, 0.0))
        return np.array([[r, t], [t, r]], dtype=complex)


WAVE = WaveMechanics()
