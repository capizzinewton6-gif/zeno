"""Engineering unit converter."""

from __future__ import annotations

import math

# Conversion factors to SI base units.
LENGTH = {
    "m": 1.0, "km": 1000.0, "cm": 0.01, "mm": 0.001, "um": 1e-6,
    "in": 0.0254, "ft": 0.3048, "yd": 0.9144, "mi": 1609.344,
}
MASS = {
    "kg": 1.0, "g": 1e-3, "mg": 1e-6, "t": 1000.0,
    "lb": 0.45359237, "oz": 0.028349523125,
}
FORCE = {"N": 1.0, "kN": 1000.0, "lbf": 4.4482216152605, "kgf": 9.80665}
PRESSURE = {"Pa": 1.0, "kPa": 1000.0, "MPa": 1e6, "bar": 1e5,
            "psi": 6894.757293168, "atm": 101325.0}
ENERGY = {"J": 1.0, "kJ": 1000.0, "MJ": 1e6, "cal": 4.184,
          "kcal": 4184.0, "Wh": 3600.0, "kWh": 3.6e6, "BTU": 1055.05585262}
POWER = {"W": 1.0, "kW": 1000.0, "MW": 1e6, "hp": 745.699871582}
TEMP_OFFSET = {"C": 0.0, "K": -273.15, "F": -32.0}
ANGLE = {"deg": 1.0, "rad": 180.0 / math.pi, "grad": 0.9}


class UnitConverter:
    def convert(self, value: float, from_unit: str, to_unit: str,
                category: str = "auto") -> float:
        if category == "auto":
            category = self._detect_category(from_unit, to_unit)
        if category == "temperature":
            return self._temperature(value, from_unit, to_unit)
        table = self._table(category)
        if from_unit not in table or to_unit not in table:
            raise ValueError(f"Units {from_unit}/{to_unit} not in category {category}")
        return value * table[from_unit] / table[to_unit]

    def _table(self, category: str) -> dict:
        tables = {"length": LENGTH, "mass": MASS, "force": FORCE,
                  "pressure": PRESSURE, "energy": ENERGY, "power": POWER,
                  "angle": ANGLE}
        if category not in tables:
            raise ValueError(f"Unknown category {category}")
        return tables[category]

    def _detect_category(self, u1: str, u2: str) -> str:
        for cat, table in [("length", LENGTH), ("mass", MASS), ("force", FORCE),
                           ("pressure", PRESSURE), ("energy", ENERGY),
                           ("power", POWER), ("angle", ANGLE)]:
            if u1 in table and u2 in table:
                return cat
        if u1 in TEMP_OFFSET and u2 in TEMP_OFFSET:
            return "temperature"
        raise ValueError(f"Cannot detect category for {u1} -> {u2}")

    def _temperature(self, value: float, frm: str, to: str) -> float:
        # to Celsius first
        if frm == "C":
            c = value
        elif frm == "K":
            c = value - 273.15
        elif frm == "F":
            c = (value - 32) * 5 / 9
        else:
            raise ValueError(f"Unknown temp unit {frm}")
        if to == "C":
            return c
        if to == "K":
            return c + 273.15
        if to == "F":
            return c * 9 / 5 + 32
        raise ValueError(f"Unknown temp unit {to}")
