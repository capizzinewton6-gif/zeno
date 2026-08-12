"""Thermodynamics calculations."""

from __future__ import annotations

import math

R_UNIVERSAL = 8.314  # J/(mol K)


class Thermodynamics:
    def ideal_gas_pressure(self, n: float, t: float, v: float) -> float:
        return n * R_UNIVERSAL * t / v

    def carnot_efficiency(self, t_hot: float, t_cold: float) -> float:
        return 1 - t_cold / t_hot

    def heat_transfer_conduction(self, k: float, area: float, dt: float, dx: float) -> float:
        return k * area * dt / dx

    def heat_transfer_convection(self, h: float, area: float, dt: float) -> float:
        return h * area * dt

    def stefan_boltzmann(self, emissivity: float, area: float, t: float) -> float:
        sigma = 5.670374419e-8
        return emissivity * sigma * area * t ** 4

    def enthalpy_change(self, m: float, cp: float, dt: float) -> float:
        return m * cp * dt

    def rankine_efficiency(self, w_turbine: float, q_in: float) -> float:
        return w_turbine / q_in

    def cop_refrigerator(self, t_cold: float, t_hot: float) -> float:
        return t_cold / (t_hot - t_cold)

    def cop_heat_pump(self, t_cold: float, t_hot: float) -> float:
        return t_hot / (t_hot - t_cold)
