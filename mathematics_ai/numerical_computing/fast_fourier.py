"""FFT, wavelet and spectral transforms."""

from __future__ import annotations

from typing import Any

import numpy as np


def fft(signal: list[complex | float]) -> list[complex]:
    return np.fft.fft(np.array(signal, dtype=complex)).tolist()


def ifft(spectrum: list[complex]) -> list[complex]:
    return np.fft.ifft(np.array(spectrum, dtype=complex)).tolist()


def fftfreq(n: int, d: float = 1.0) -> list[float]:
    return np.fft.fftfreq(n, d=d).tolist()


def power_spectrum(signal: list[float]) -> list[float]:
    sp = np.fft.fft(np.array(signal, dtype=float))
    return (np.abs(sp) ** 2).tolist()


def stft(signal: list[float], window_size: int = 256, hop: int = 64) -> list[list[complex]]:
    """Short-time Fourier transform using a Hann window."""
    s = np.array(signal, dtype=float)
    n = len(s)
    window = np.hanning(window_size)
    out = []
    for start in range(0, n - window_size + 1, hop):
        frame = s[start:start + window_size] * window
        out.append(np.fft.fft(frame).tolist())
    return out


def haar_wavelet(signal: list[float], level: int = 1) -> dict[str, list]:
    """Simple Haar wavelet transform (discrete)."""
    a = np.array(signal, dtype=float)
    approx = []
    detail = []
    for _ in range(level):
        n = len(a)
        if n % 2:
            n -= 1
        a_pairs = a[:n].reshape(-1, 2)
        approx = ((a_pairs[:, 0] + a_pairs[:, 1]) / np.sqrt(2)).tolist()
        detail = ((a_pairs[:, 0] - a_pairs[:, 1]) / np.sqrt(2)).tolist()
        a = np.array(approx)
    return {"approx": approx, "detail": detail}


def dct(signal: list[float]) -> list[float]:
    """Discrete cosine transform (type II)."""
    return np.fft.dct(np.array(signal, dtype=float)).tolist()


def dst(signal: list[float]) -> list[float]:
    """Discrete sine transform."""
    return np.fft.dst(np.array(signal, dtype=float)).tolist()


__all__ = ["fft", "ifft", "fftfreq", "power_spectrum", "stft", "haar_wavelet", "dct", "dst"]
