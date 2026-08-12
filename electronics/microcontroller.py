"""Microcontroller project builder."""

from __future__ import annotations

from src.gemini_25_flash_engine import Gemini25FlashEngine


class MicrocontrollerProject:
    def __init__(self, engine: Gemini25FlashEngine | None = None):
        self.engine = engine or Gemini25FlashEngine()

    def select_mcu(self, requirements: str) -> str:
        return self.engine.generate(
            f"Select a microcontroller for: {requirements}. Justify choice "
            f"(cores, peripherals, memory, power, cost).",
            system="You are an embedded systems architect.")

    def pinout(self, mcu: str, peripherals: str) -> str:
        return self.engine.generate(
            f"Design a pinout for {mcu} using: {peripherals}.",
            system="You are a firmware engineer.")

    def firmware_outline(self, mcu: str, function: str) -> str:
        return self.engine.generate(
            f"Write a firmware outline for {mcu} implementing: {function}. "
            f"Use the appropriate HAL/framework.",
            system="You are an embedded firmware engineer.")

    def peripheral_config(self, mcu: str, peripheral: str) -> str:
        return self.engine.generate(
            f"Configure {peripheral} on {mcu} with register-level detail.",
            system="You are an embedded peripherals engineer.")
