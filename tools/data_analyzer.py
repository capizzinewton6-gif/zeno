"""Data analyzer — LC-MS integration and multi-well plate kinetics."""

import math
import statistics


class DataAnalyzer:
    """Analyze chromatographic and kinetic datasets."""

    # --- Peak integration ---------------------------------------------
    @staticmethod
    def integrate_peak(times, signal, t_start, t_end):
        """Trapezoidal integration over a retention-time window."""
        pts = [(t, s) for t, s in zip(times, signal) if t_start <= t <= t_end]
        if len(pts) < 2:
            return 0.0
        area = 0.0
        for i in range(len(pts) - 1):
            area += (pts[i][1] + pts[i + 1][1]) / 2 * (pts[i + 1][0] - pts[i][0])
        return area

    @staticmethod
    def baseline_correct(signal, window=3):
        """Subtract rolling-minimum baseline."""
        n = len(signal)
        corrected = []
        for i in range(n):
            lo = max(0, i - window)
            hi = min(n, i + window + 1)
            baseline = min(signal[lo:hi])
            corrected.append(signal[i] - baseline)
        return corrected

    @staticmethod
    def snr(signal, noise_region):
        """Signal-to-noise ratio using std of a noise region."""
        peak = max(signal)
        noise = statistics.pstdev(noise_region) if noise_region else 1e-9
        return peak / noise if noise else float('inf')

    # --- Multi-well plate kinetics ------------------------------------
    @staticmethod
    def plate_kinetics(wells, time_points):
        """wells: dict well_id->list of absorbances. Returns slopes per well."""
        results = {}
        n = len(time_points)
        for well, abs_vals in wells.items():
            if len(abs_vals) != n:
                results[well] = {"error": "length mismatch"}
                continue
            slope = DataAnalyzer._linear_slope(time_points, abs_vals)
            results[well] = {"slope": slope, "max_abs": max(abs_vals)}
        return results

    @staticmethod
    def _linear_slope(x, y):
        n = len(x)
        sx = sum(x); sy = sum(y)
        sxx = sum(xi * xi for xi in x); sxy = sum(xi * yi for xi, yi in zip(x, y))
        denom = n * sxx - sx * sx
        return (n * sxy - sx * sy) / denom if denom else 0.0

    # --- Statistics ----------------------------------------------------
    @staticmethod
    def mean_std(values):
        if len(values) < 2:
            return {"mean": statistics.mean(values) if values else 0, "std": 0}
        return {"mean": statistics.mean(values), "std": statistics.stdev(values)}

    @staticmethod
    def rsd(values):
        """Relative standard deviation (%)."""
        if len(values) < 2:
            return 0.0
        m = statistics.mean(values)
        return (statistics.stdev(values) / m) * 100 if m else 0.0
