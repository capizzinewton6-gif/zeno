"""CODATA fundamental physical constants with unit tracking.

Values are the CODATA 2018 recommended values (the basis of the 2019 SI redefinition),
expressed in SI base units. Each constant carries its symbol, value, uncertainty, and
SI dimensions so that the dimensional validator can reason about them.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict


@dataclass(frozen=True)
class PhysicalConstant:
    name: str
    symbol: str
    value: float
    unit: str
    uncertainty: float
    dimensions: Dict[str, int]  # {length:1, mass:1, time:-1, ...} exponents in SI base

    def __repr__(self) -> str:  # pragma: no cover - cosmetic
        return f"{self.symbol} = {self.value} {self.unit}"


# SI base dimension exponents: length L, mass M, time T, current I,
# temperature theta, amount N, luminous intensity J.
def _dims(L=0, M=0, T=0, I=0, theta=0, N=0, J=0) -> Dict[str, int]:
    return {"L": L, "M": M, "T": T, "I": I, "theta": theta, "N": N, "J": J}


_CONSTANTS: Dict[str, PhysicalConstant] = {
    "c": PhysicalConstant("speed of light in vacuum", "c", 299_792_458.0, "m/s", 0.0, _dims(L=1, T=-1)),
    "h": PhysicalConstant("Planck constant", "h", 6.62607015e-34, "J*s", 0.0, _dims(L=2, M=1, T=-1)),
    "hbar": PhysicalConstant("reduced Planck constant", "hbar", 1.054571817e-34, "J*s", 0.0, _dims(L=2, M=1, T=-1)),
    "G": PhysicalConstant("Newtonian constant of gravitation", "G", 6.67430e-11, "m^3 kg^-1 s^-2", 2.2e-15, _dims(L=3, M=-1, T=-2)),
    "kB": PhysicalConstant("Boltzmann constant", "kB", 1.380649e-23, "J/K", 0.0, _dims(L=2, M=1, T=-2, theta=-1)),
    "e": PhysicalConstant("elementary charge", "e", 1.602176634e-19, "C", 0.0, _dims(T=1, I=1)),
    "eps0": PhysicalConstant("vacuum electric permittivity", "eps0", 8.8541878128e-12, "F/m", 1.3e-21, _dims(L=-3, M=-1, T=4, I=2)),
    "mu0": PhysicalConstant("vacuum magnetic permeability", "mu0", 1.25663706212e-6, "N/A^2", 1.9e-17, _dims(L=1, M=1, T=-2, I=-2)),
    "NA": PhysicalConstant("Avogadro number", "NA", 6.02214076e23, "1/mol", 0.0, _dims(N=-1)),
    "R": PhysicalConstant("molar gas constant", "R", 8.31446261815324, "J/(mol*K)", 0.0, _dims(L=2, M=1, T=-2, theta=-1, N=-1)),
    "sigma": PhysicalConstant("Stefan-Boltzmann constant", "sigma", 5.670374419e-8, "W/(m^2 K^4)", 0.0, _dims(L=0, M=1, T=-3, theta=-4)),
    "a0": PhysicalConstant("Bohr radius", "a0", 5.29177210903e-11, "m", 8e-21, _dims(L=1)),
    "alpha": PhysicalConstant("fine-structure constant", "alpha", 7.2973525693e-3, "dimensionless", 1.1e-12, _dims()),
    "me": PhysicalConstant("electron mass", "me", 9.1093837015e-31, "kg", 2.8e-40, _dims(M=1)),
    "mp": PhysicalConstant("proton mass", "mp", 1.67262192369e-27, "kg", 5.1e-37, _dims(M=1)),
    "mn": PhysicalConstant("neutron mass", "mn", 1.67492749804e-27, "kg", 9.5e-37, _dims(M=1)),
    "eV": PhysicalConstant("electronvolt", "eV", 1.602176634e-19, "J", 0.0, _dims(L=2, M=1, T=-2)),
    "g": PhysicalConstant("standard acceleration of gravity", "g", 9.80665, "m/s^2", 0.0, _dims(L=1, T=-2)),
    "kB_eV": PhysicalConstant("Boltzmann constant (eV/K)", "kB_eV", 8.617333262e-5, "eV/K", 0.0, _dims(theta=-1)),
}


class ConstantEngine:
    """Lookup and natural-unit conversions for fundamental constants."""

    def __init__(self, constants: Dict[str, PhysicalConstant] | None = None):
        self._c = dict(constants if constants is not None else _CONSTANTS)

    def get(self, symbol: str) -> PhysicalConstant:
        try:
            return self._c[symbol]
        except KeyError as exc:  # pragma: no cover
            raise KeyError(f"Unknown physical constant: {symbol}") from exc

    def value(self, symbol: str) -> float:
        return self.get(symbol).value

    def all(self) -> Dict[str, PhysicalConstant]:
        return dict(self._c)

    def as_dict(self) -> Dict[str, float]:
        """symbol -> numerical value, for quick substitution."""
        return {k: v.value for k, v in self._c.items()}

    def natural_units(self, c=1, hbar=1, kB=1):
        """Return a dict of conversion factors for natural units (c=hbar=kB=1)."""
        out = {"c": c, "hbar": hbar, "kB": kB}
        out["eV_to_J"] = self.value("eV")
        out["eV_to_inverse_meters"] = self.value("eV") / (self.value("hbar") * self.value("c"))
        out["eV_to_seconds"] = self.value("hbar") / self.value("eV")
        out["eV_to_kelvin"] = self.value("eV") / (kB if kB != 1 else self.value("kB"))
        return out

    def planck_units(self) -> Dict[str, float]:
        c = self.value("c")
        hbar = self.value("hbar")
        G = self.value("G")
        kB = self.value("kB")
        return {
            "planck_length": (hbar * G / c ** 3) ** 0.5,
            "planck_time": (hbar * G / c ** 5) ** 0.5,
            "planck_mass": (hbar * c / G) ** 0.5,
            "planck_temperature": (hbar * c ** 5 / (G * kB ** 2)) ** 0.5,
            "planck_energy": (hbar * c ** 5 / G) ** 0.5,
        }


CONSTANTS = ConstantEngine()
