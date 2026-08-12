"""Plot generator — NMR spectra, chromatograms, and kinetic curves.

Uses matplotlib with the Agg backend to render PNGs into a static folder
so they can be served to the UI. Falls back to JSON data when matplotlib
is unavailable.
"""

import io
import os
import json
import math
import logging

logger = logging.getLogger(__name__)

_AGG_CONFIGURED = False


def _ensure_agg():
    global _AGG_CONFIGURED
    if not _AGG_CONFIGURED:
        import matplotlib
        matplotlib.use("Agg")
        _AGG_CONFIGURED = True


class PlotGenerator:
    """Generate scientific plots for the UI."""

    def __init__(self, output_dir="static/plots"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self._plt = None
        try:
            _ensure_agg()
            import matplotlib.pyplot as plt
            self._plt = plt
        except Exception as exc:
            logger.warning("matplotlib unavailable: %s", exc)

    # --- NMR spectrum --------------------------------------------------
    def nmr_spectrum(self, peaks, title="Simulated 1H NMR"):
        """peaks: list of (shift_ppm, intensity, label)."""
        if self._plt is None:
            return {"data": peaks, "error": "matplotlib unavailable"}
        fig, ax = self._plt.subplots(figsize=(7, 4))
        x_min = max(12.0, max(p[0] for p in peaks) + 1) if peaks else 12.0
        xs = []
        for shift, intensity, *_ in peaks:
            xs += [shift - 0.02, shift, shift + 0.02]
        ys = []
        for shift, intensity, *_ in peaks:
            ys += [0, intensity, 0]
        ax.plot(xs, ys, color="#1f77b4")
        ax.invert_xaxis()
        ax.set_xlabel("Chemical shift (ppm)")
        ax.set_ylabel("Intensity")
        ax.set_title(title)
        for shift, intensity, *rest in peaks:
            label = rest[0] if rest else ""
            if label:
                ax.annotate(label, (shift, intensity), textcoords="offset points", xytext=(0, 5), ha="center", fontsize=8)
        path = os.path.join(self.output_dir, "nmr_spectrum.png")
        fig.tight_layout()
        fig.savefig(path, dpi=100)
        self._plt.close(fig)
        return {"image": path, "peaks": peaks}

    # --- Chromatogram --------------------------------------------------
    def chromatogram(self, peaks, title="Simulated HPLC Chromatogram"):
        """peaks: list of (retention_time_min, intensity, label)."""
        if self._plt is None:
            return {"data": peaks, "error": "matplotlib unavailable"}
        fig, ax = self._plt.subplots(figsize=(7, 4))
        xs = []
        ys = []
        for rt, intensity, *_ in peaks:
            for dx in (-0.1, -0.05, 0, 0.05, 0.1):
                xs.append(rt + dx)
                w = 0.05
                ys.append(intensity * math.exp(-(dx ** 2) / (2 * w ** 2)))
        ax.plot(xs, ys, color="#2ca02c")
        ax.set_xlabel("Retention time (min)")
        ax.set_ylabel("Absorbance")
        ax.set_title(title)
        for rt, intensity, *rest in peaks:
            label = rest[0] if rest else ""
            if label:
                ax.annotate(label, (rt, intensity), textcoords="offset points", xytext=(0, 5), ha="center", fontsize=8)
        path = os.path.join(self.output_dir, "chromatogram.png")
        fig.tight_layout()
        fig.savefig(path, dpi=100)
        self._plt.close(fig)
        return {"image": path, "peaks": peaks}

    # --- Kinetic curve -------------------------------------------------
    def kinetic_curve(self, times, concentrations, title="Kinetic Decay"):
        if self._plt is None:
            return {"data": {"times": times, "concentrations": concentrations}, "error": "matplotlib unavailable"}
        fig, ax = self._plt.subplots(figsize=(7, 4))
        ax.plot(times, concentrations, "o-", color="#d62728")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Concentration (M)")
        ax.set_title(title)
        path = os.path.join(self.output_dir, "kinetic_curve.png")
        fig.tight_layout()
        fig.savefig(path, dpi=100)
        self._plt.close(fig)
        return {"image": path}

    # --- Calibration curve --------------------------------------------
    def calibration_curve(self, x, y, title="Calibration Curve"):
        if self._plt is None or len(x) < 2:
            return {"data": {"x": x, "y": y}, "error": "matplotlib unavailable or insufficient data"}
        fig, ax = self._plt.subplots(figsize=(7, 4))
        ax.scatter(x, y, color="#9467bd")
        n = len(x)
        sx = sum(x); sy = sum(y)
        sxx = sum(xi * xi for xi in x); sxy = sum(xi * yi for xi, yi in zip(x, y))
        slope = (n * sxy - sx * sy) / (n * sxx - sx * sx)
        intercept = (sy - slope * sx) / n
        xr = [min(x), max(x)]
        yr = [slope * xi + intercept for xi in xr]
        ax.plot(xr, yr, color="#9467bd", linestyle="--")
        ax.set_xlabel("Concentration (M)")
        ax.set_ylabel("Absorbance")
        ax.set_title(title)
        path = os.path.join(self.output_dir, "calibration_curve.png")
        fig.tight_layout()
        fig.savefig(path, dpi=100)
        self._plt.close(fig)
        return {"image": path, "slope": slope, "intercept": intercept}
