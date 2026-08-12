"""Electrical calculations: Ohm's law, power, impedance, networks."""

from __future__ import annotations

import cmath
import math


class Electricity:
    def ohms_law(self, v: float | None = None, i: float | None = None,
                 r: float | None = None) -> float:
        if v is None:
            return i * r  # type: ignore
        if i is None:
            return v / r  # type: ignore
        return v / i  # r

    def power_dc(self, v: float, i: float) -> float:
        return v * i

    def power_ac(self, v_rms: float, i_rms: float, pf: float = 1.0) -> float:
        return v_rms * i_rms * pf

    def resistance_series(self, resistors: list[float]) -> float:
        return sum(resistors)

    def resistance_parallel(self, resistors: list[float]) -> float:
        return 1.0 / sum(1.0 / r for r in resistors)

    def capacitance_series(self, caps: list[float]) -> float:
        return 1.0 / sum(1.0 / c for c in caps)

    def capacitance_parallel(self, caps: list[float]) -> float:
        return sum(caps)

    def impedance_rc(self, r: float, xc: float, f: float | None = None) -> complex:
        return complex(r, -xc)

    def impedance_rl(self, r: float, xl: float, f: float | None = None) -> complex:
        return complex(r, xl)

    def resonant_frequency(self, l: float, c: float) -> float:
        return 1.0 / (2 * math.pi * math.sqrt(l * c))

    def rms(self, peak: float) -> float:
        return peak / math.sqrt(2)

    def reactance_capacitive(self, c: float, f: float) -> float:
        return 1.0 / (2 * math.pi * f * c)

    def reactance_inductive(self, l: float, f: float) -> float:
        return 2 * math.pi * f * l
