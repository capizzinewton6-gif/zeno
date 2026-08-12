"""Noise filtering, lock-in amplifier simulation, and wavelet analysis."""

from __future__ import annotations

import numpy as np
from scipy import signal as sps

from numerical_computing.fast_fourier import FastFourier


class SignalProcessing:
    """Filtering and analysis of experimental signals."""

    @staticmethod
    def lowpass(signal_: np.ndarray, fs: float, cutoff: float, order: int = 4) -> np.ndarray:
        nyq = 0.5 * fs
        b, a = sps.butter(order, cutoff / nyq, btype="low")
        return sps.filtfilt(b, a, signal_)

    @staticmethod
    def highpass(signal_: np.ndarray, fs: float, cutoff: float, order: int = 4) -> np.ndarray:
        nyq = 0.5 * fs
        b, a = sps.butter(order, cutoff / nyq, btype="high")
        return sps.filtfilt(b, a, signal_)

    @staticmethod
    def notch(signal_: np.ndarray, fs: float, freq: float, Q: float = 30.0) -> np.ndarray:
        b, a = sps.iirnotch(freq, Q, fs=fs)
        return sps.filtfilt(b, a, signal_)

    @staticmethod
    def lock_in(signal_: np.ndarray, reference: np.ndarray) -> dict:
        """Simulate a lock-in: R = 2<signal*reference>, Q = 2<signal*reference_90deg>."""
        R = 2 * np.mean(signal_ * reference)
        shifted = np.roll(reference, len(reference) // 4)
        Q = 2 * np.mean(signal_ * shifted)
        return {"amplitude": float(np.hypot(R, Q)), "phase": float(np.arctan2(Q, R))}

    @staticmethod
    def wavelet_cwt(signal_: np.ndarray, widths: np.ndarray, dt: float = 1.0) -> np.ndarray:
        return sps.cwt(signal_, sps.ricker, widths) * dt
