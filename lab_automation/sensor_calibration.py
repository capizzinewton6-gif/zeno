"""Sensor calibration — pH meters, thermocouples, pressure transducers, conductivity probes."""


class SensorCalibration:
    """Calibrate laboratory sensors using linear fits."""

    @staticmethod
    def two_point_calibration(known_low, reading_low, known_high, reading_high):
        """Return slope and intercept mapping reading -> true value."""
        slope = (known_high - known_low) / (reading_high - reading_low)
        intercept = known_low - slope * reading_low
        return {"slope": slope, "intercept": intercept}

    @staticmethod
    def linear_fit(x, y):
        n = len(x)
        sx = sum(x); sy = sum(y)
        sxx = sum(xi ** 2 for xi in x); sxy = sum(xi * yi for xi, yi in zip(x, y))
        slope = (n * sxy - sx * sy) / (n * sxx - sx ** 2)
        intercept = (sy - slope * sx) / n
        return {"slope": slope, "intercept": intercept}

    @staticmethod
    def apply_calibration(reading, slope, intercept):
        return slope * reading + intercept

    @staticmethod
    def ph_calibration(ph4_reading, ph7_reading):
        return SensorCalibration.two_point_calibration(4.0, ph4_reading, 7.0, ph7_reading)

    @staticmethod
    def thermocouple_calibration(ice_reading, boil_reading):
        return SensorCalibration.two_point_calibration(0.0, ice_reading, 100.0, boil_reading)
