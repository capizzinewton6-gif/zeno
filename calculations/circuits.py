"""Circuit calculations: node analysis, filters, time constants."""

from __future__ import annotations

import math


class Circuits:
    def time_constant_rc(self, r: float, c: float) -> float:
        return r * c

    def time_constant_rl(self, r: float, l: float) -> float:
        return l / r

    def voltage_divider(self, v_in: float, r1: float, r2: float) -> float:
        return v_in * r2 / (r1 + r2)

    def current_divider(self, i_in: float, r1: float, r2: float) -> tuple[float, float]:
        total = 1 / r1 + 1 / r2
        return i_in * (1 / r1) / total, i_in * (1 / r2) / total

    def lowpass_cutoff(self, r: float, c: float) -> float:
        return 1 / (2 * math.pi * r * c)

    def highpass_cutoff(self, r: float, c: float) -> float:
        return 1 / (2 * math.pi * r * c)

    def gain_non_inverting(self, r1: float, r2: float) -> float:
        return 1 + r2 / r1

    def gain_inverting(self, r_in: float, r_f: float) -> float:
        return -r_f / r_in

    def wheatstone_balance(self, r1: float, r2: float, r3: float) -> float:
        """Rx for balanced bridge: R4 = R2*R3/R1."""
        return r2 * r3 / r1

    def power_dissipated(self, v: float, r: float) -> float:
        return v ** 2 / r
