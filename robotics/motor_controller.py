"""Motor controller: motor selection and drive design."""

from __future__ import annotations

import math

from src.gemini_25_flash_engine import Gemini25FlashEngine


class MotorController:
    def __init__(self, engine: Gemini25FlashEngine | None = None):
        self.engine = engine or Gemini25FlashEngine()

    def select(self, load: str, speed_rpm: float, torque_nm: float) -> str:
        power = torque_nm * 2 * math.pi * speed_rpm / 60
        return self.engine.generate(
            f"Select a motor for {load}: {speed_rpm} rpm, {torque_nm} Nm "
            f"(~{power:.1f} W). Include type, driver, feedback.",
            system="You are a motor selection engineer.")

    def driver_design(self, motor: str, control: str) -> str:
        return self.engine.generate(
            f"Design a motor driver for {motor} with {control} control. "
            f"Include power stage, gate driver, protection.",
            system="You are a motor drive engineer.")

    def speed_torque_curve(self, no_load_rpm: float, stall_torque: float,
                           n: int = 10) -> list[dict]:
        pts = []
        for i in range(n + 1):
            t = stall_torque * i / n
            rpm = no_load_rpm * (1 - i / n)
            pts.append({"torque_nm": t, "speed_rpm": rpm,
                        "power_w": t * 2 * math.pi * rpm / 60})
        return pts
