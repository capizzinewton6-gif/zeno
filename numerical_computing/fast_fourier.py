"""Spatial FFTs, momentum-space transforms, and power-spectrum estimation."""

from __future__ import annotations

import numpy as np
from numpy.fft import fft, fft2, fftfreq, fftshift, ifft, ifft2


class FastFourier:
    """FFT helpers tuned for physics (real-space <-> momentum-space)."""

    @staticmethod
    def fft1d(signal: np.ndarray, dt: float = 1.0) -> tuple[np.ndarray, np.ndarray]:
        freqs = fftfreq(len(signal), d=dt)
        return fftshift(freqs), fftshift(fft(signal))

    @staticmethod
    def ifft1d(spectrum: np.ndarray) -> np.ndarray:
        return np.real(ifft(fftshift(spectrum)))

    @staticmethod
    def fft2d(field: np.ndarray, dx: float = 1.0, dy: float = 1.0) -> tuple[np.ndarray, np.ndarray]:
        nx, ny = field.shape
        kx = fftshift(fftfreq(nx, d=dx))
        ky = fftshift(fftfreq(ny, d=dy))
        KX, KY = np.meshgrid(kx, ky, indexing="ij")
        return np.sqrt(KX ** 2 + KY ** 2), fftshift(fft2(field))

    @staticmethod
    def power_spectrum_1d(signal: np.ndarray, dt: float = 1.0) -> tuple[np.ndarray, np.ndarray]:
        freqs, spec = FastFourier.fft1d(signal, dt)
        return freqs, np.abs(spec) ** 2

    @staticmethod
    def power_spectrum_2d(field: np.ndarray, dx: float = 1.0, dy: float = 1.0) -> np.ndarray:
        _, spec = FastFourier.fft2d(field, dx, dy)
        return np.abs(spec) ** 2
