"""Autoregression (ARIMA), Fourier analysis and spectral density."""

from __future__ import annotations

from typing import Any

import numpy as np


def autocorrelation(data: list[float], max_lag: int = 20) -> list[float]:
    arr = np.array(data, dtype=float)
    n = len(arr)
    arr = arr - arr.mean()
    out = []
    for k in range(max_lag + 1):
        if k == 0:
            out.append(1.0)
        else:
            c = np.sum(arr[:n - k] * arr[k:]) / np.sum(arr ** 2)
            out.append(float(c))
    return out


def ar_coefficients(data: list[float], p: int = 2) -> list[float]:
    """Estimate AR(p) coefficients via Yule-Walker."""
    arr = np.array(data, dtype=float)
    n = len(arr)
    r = autocorrelation(arr, p)
    # build Toeplitz system
    R = np.array([[r[abs(i - j)] for j in range(p)] for i in range(p)])
    phi = np.linalg.solve(R, np.array(r[1:p + 1]))
    return phi.tolist()


def arima_forecast(data: list[float], p: int = 1, d: int = 0, steps: int = 5) -> list[float]:
    """Forecast using an AR(p) model after differencing d times."""
    arr = np.array(data, dtype=float)
    for _ in range(d):
        arr = np.diff(arr)
    phi = np.array(ar_coefficients(arr.tolist(), p))
    preds = []
    for _ in range(steps):
        if len(arr) >= p:
            nxt = float(np.sum(phi * arr[-p:][::-1]))
        else:
            nxt = float(arr[-1])
        preds.append(nxt)
        arr = np.append(arr, nxt)
    return preds


def power_spectral_density(data: list[float], fs: float = 1.0) -> dict[str, np.ndarray]:
    """Periodogram-based PSD estimate."""
    arr = np.array(data, dtype=float)
    n = len(arr)
    freqs = np.fft.rfftfreq(n, d=1 / fs)
    fft = np.fft.rfft(arr)
    psd = (np.abs(fft) ** 2) / (fs * n)
    return {"frequencies": freqs, "psd": psd}


def fourier_decomposition(data: list[float], n_components: int = 5) -> dict[str, Any]:
    """Top-n Fourier components of a signal."""
    arr = np.array(data, dtype=float)
    n = len(arr)
    fft = np.fft.rfft(arr)
    mags = np.abs(fft)
    top_idx = np.argsort(mags)[-n_components:][::-1]
    return {
        "frequencies": (top_idx / n).tolist(),
        "amplitudes": (mags[top_idx] * 2 / n).tolist(),
        "phases": np.angle(fft[top_idx]).tolist(),
    }


def detrend(data: list[float]) -> list[float]:
    arr = np.array(data, dtype=float)
    x = np.arange(len(arr))
    coeffs = np.polyfit(x, arr, 1)
    trend = np.polyval(coeffs, x)
    return (arr - trend).tolist()


__all__ = [
    "autocorrelation", "ar_coefficients", "arima_forecast",
    "power_spectral_density", "fourier_decomposition", "detrend",
]
