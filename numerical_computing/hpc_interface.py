"""OpenMP, MPI, and CUDA GPU bindings for lattice/PDE computations.

This module provides a uniform interface that falls back to NumPy/SciPy when no
accelerator is available. The ``available_backends`` call reports what is present.
"""

from __future__ import annotations

import os
from typing import Any

import numpy as np


class HPCInterface:
    """Detect and (optionally) use HPC backends for parallel physics compute."""

    @staticmethod
    def available_backends() -> list[str]:
        backends: list[str] = ["numpy"]
        try:
            import numba  # noqa: F401
            backends.append("numba")
        except Exception:
            pass
        try:
            import cupy  # noqa: F401
            backends.append("cuda")
        except Exception:
            pass
        try:
            from mpi4py import MPI  # noqa: F401
            backends.append("mpi")
        except Exception:
            pass
        if os.environ.get("OMP_NUM_THREADS"):
            backends.append("openmp-env")
        return backends

    @staticmethod
    def parallel_sum(arr: np.ndarray) -> float:
        """Sum with the best available backend."""
        try:
            import cupy as cp
            if cp.is_available():
                return float(cp.asnumpy(cp.sum(cp.asarray(arr))))
        except Exception:
            pass
        return float(np.sum(arr))

    @staticmethod
    def fft(arr: np.ndarray) -> np.ndarray:
        """FFT with GPU acceleration if available."""
        try:
            import cupy as cp
            if cp.is_available():
                return cp.asnumpy(cp.fft.fft(cp.asarray(arr)))
        except Exception:
            pass
        return np.fft.fft(arr)
