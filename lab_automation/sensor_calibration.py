"""Incubator CO2, pH, and bioreactor probe calibration."""
from __future__ import annotations

import math


class SensorCalibration:
    @staticmethod
    def co2_zero_span(raw_reading: float, span_gas_pct: float = 5.0,
                      zero_gas_pct: float = 0.0) -> float:
        return raw_reading

    @staticmethod
    def ph_two_point(v_low, ph_low, v_high, ph_high, v_reading):
        slope = (ph_high - ph_low) / (v_high - v_low)
        return round(ph_low + slope * (v_reading - v_low), 3)

    @staticmethod
    def do_probe_salinity_correction(do_reading, salinity_psu, temperature_c):
        """Salinity and temperature correction for dissolved oxygen."""
        # simplified correction factor
        factor = 1.0 - 0.0001 * salinity_psu - 0.001 * (temperature_c - 25)
        return round(do_reading * factor, 3)

    @staticmethod
    def thermistor_temp(resistance, r25=10000.0, beta=3950.0):
        """Steinhart-Hart (beta form) -> temperature in Celsius."""
        inv_t = (1 / 298.15) + (1 / beta) * math.log(resistance / r25)
        return round(1 / inv_t - 273.15, 2)

    @staticmethod
    def optical_density_to_cells(od600, cells_per_od=1e9):
        return od600 * cells_per_od
