"""Blackbody radiation, atomic emission lines, and CMB power spectra."""

from __future__ import annotations

import numpy as np

from tools.plot_generator import PlotGenerator
from physics.thermodynamics import QuantumStatistics


class SpectrumVisualizer:
    """Render physical spectra."""

    def __init__(self, plotter: PlotGenerator | None = None):
        self.plot = plotter or PlotGenerator()

    def blackbody(self, ax, T: float = 5778.0, freq_max: float = 3e15):
        freq = np.linspace(1e12, freq_max, 500)
        B = QuantumStatistics.planck_spectrum(freq, T)
        ax.plot(freq, B, color="#e69f00")
        ax.set_xlabel("frequency (Hz)"); ax.set_ylabel("B_nu")
        ax.set_title(f"Blackbody spectrum (T={T:.0f} K)")

    def emission_lines(self, ax, lines: list[tuple[float, float]]):
        """lines: list of (wavelength_nm, intensity)."""
        for wl, intensity in lines:
            ax.plot([wl, wl], [0, intensity], color="#0072b2")
        ax.set_xlabel("wavelength (nm)"); ax.set_ylabel("intensity")
        ax.set_title("Atomic emission lines")

    def cmb_power_spectrum(self, ax, l: np.ndarray | None = None, cl: np.ndarray | None = None):
        """Schematic CMB TT power spectrum (illustrative)."""
        if l is None:
            l = np.arange(2, 1000)
            cl = 5000 * l ** -0.8 * np.exp(-(l / 220) ** 2 / 50) + 200 * l ** -1.5
        ax.plot(l, l * (l + 1) * cl / (2 * np.pi), color="#cc79a7")
        ax.set_xscale("log")
        ax.set_xlabel("multipole l"); ax.set_ylabel("l(l+1)C_l / 2pi")
        ax.set_title("CMB TT power spectrum (schematic)")
