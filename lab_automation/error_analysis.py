"""Error analysis — instrumental drift, calibration curves, signal-to-noise ratio."""

import math
import statistics


class ErrorAnalysis:
    """Quantify measurement uncertainty and error."""

    @staticmethod
    def standard_deviation(values):
        if len(values) < 2:
            return 0.0
        return statistics.stdev(values)

    @staticmethod
    def standard_error(values):
        n = len(values)
        if n < 2:
            return 0.0
        return statistics.stdev(values) / math.sqrt(n)

    @staticmethod
    def confidence_interval(values, confidence=0.95):
        if len(values) < 2:
            return {"mean": statistics.mean(values) if values else 0, "ci": 0}
        m = statistics.mean(values)
        se = ErrorAnalysis.standard_error(values)
        z = {0.90: 1.645, 0.95: 1.96, 0.99: 2.576}.get(confidence, 1.96)
        return {"mean": m, "margin": z * se, "lower": m - z * se, "upper": m + z * se}

    @staticmethod
    def instrumental_drift(readings, times):
        """Linear drift slope of readings vs time."""
        n = len(readings)
        if n < 2:
            return {"drift_per_unit_time": 0}
        sx = sum(times); sy = sum(readings)
        sxx = sum(t ** 2 for t in times); sxy = sum(t * r for t, r in zip(times, readings))
        denom = n * sxx - sx ** 2
        slope = (n * sxy - sx * sy) / denom if denom else 0
        return {"drift_per_unit_time": slope}

    @staticmethod
    def snr(signal_max, noise_std):
        return signal_max / noise_std if noise_std else float('inf')

    @staticmethod
    def propagation_relative(errors):
        """Relative error propagation for product/quotient: sqrt(sum(e_i^2))."""
        return math.sqrt(sum(e ** 2 for e in errors))

    @staticmethod
    def lod_loq(slope, noise_std):
        """Limit of detection / quantitation from calibration slope and blank noise."""
        lod = 3 * noise_std / slope if slope else 0
        loq = 10 * noise_std / slope if slope else 0
        return {"LOD": lod, "LOQ": loq}
