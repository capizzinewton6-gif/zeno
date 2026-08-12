"""Power systems: supply design, battery, and regulation."""

from __future__ import annotations

import math

from src.gemini_25_flash_engine import Gemini25FlashEngine


class PowerSystems:
    def __init__(self, engine: Gemini25FlashEngine | None = None):
        self.engine = engine or Gemini25FlashEngine()

    def regulator_design(self, vin: float, vout: float, iout: float) -> str:
        power = vout * iout
        return self.engine.generate(
            f"Design a regulator: Vin={vin}V, Vout={vout}V, Iout={iout}A "
            f"(Pout={power}W). Choose LDO vs switcher, compute losses and thermal.",
            system="You are a power electronics engineer.")

    def battery_life(self, capacity_mah: float, current_ma: float,
                     efficiency: float = 1.0) -> float:
        """Return estimated battery life in hours."""
        return capacity_mah * efficiency / current_ma if current_ma > 0 else float("inf")

    def solar_sizing(self, load_wh_per_day: float, peak_sun_hours: float,
                     system_efficiency: float = 0.75) -> float:
        """Required panel wattage."""
        return load_wh_per_day / (peak_sun_hours * system_efficiency)

    def power_budget(self, components: list[dict]) -> dict:
        """Sum current/power of components [{name, voltage, current}]."""
        total_power = sum(c["voltage"] * c["current"] for c in components)
        total_current = {v: sum(c["current"] for c in components if c["voltage"] == v)
                          for v in {c["voltage"] for c in components}}
        return {"total_power_W": total_power, "by_voltage": total_current}

    def ups_design(self, load_w: float, backup_hours: float,
                   battery_voltage: float) -> dict:
        """Battery capacity needed for a UPS."""
        energy = load_w * backup_hours  # Wh
        ah = energy / battery_voltage
        return {"required_Wh": energy, "battery_Ah": ah,
                "battery_voltage": battery_voltage}
