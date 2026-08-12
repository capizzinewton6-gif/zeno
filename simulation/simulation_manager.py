"""Simulation manager: orchestrates and logs simulation runs."""

from __future__ import annotations

import json
import os
from typing import Any

from .physics_simulator import PhysicsSimulator
from .circuit_simulator import CircuitSimulator
from .mechanical_simulator import MechanicalSimulator
from .thermal_simulator import ThermalSimulator
from .fluid_simulator import FluidSimulator
from .robotics_simulator import RobotSimulator


class SimulationManager:
    def __init__(self):
        self.physics = PhysicsSimulator()
        self.circuit = CircuitSimulator()
        self.mechanical = MechanicalSimulator()
        self.thermal = ThermalSimulator()
        self.fluid = FluidSimulator()
        self.robotics = RobotSimulator()
        self._log: list[dict] = []

    def run(self, name: str, fn, *args, **kwargs) -> Any:
        result = fn(*args, **kwargs)
        entry = {"name": name, "status": "completed"}
        self._log.append(entry)
        return result

    def save_log(self, path: str) -> str:
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self._log, f, indent=2)
        return path

    @property
    def log(self) -> list[dict]:
        return list(self._log)
