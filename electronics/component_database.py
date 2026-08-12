"""Electronic component database with common parts."""

from __future__ import annotations

import json
import os
from typing import Any, Dict, List

# A small built-in catalog of common components.
COMPONENTS: List[Dict[str, Any]] = [
    {"part": "1k_resistor", "type": "resistor", "value": 1000, "unit": "ohm",
     "tolerance": "1%", "package": "0805", "power": 0.125},
    {"part": "10k_resistor", "type": "resistor", "value": 10000, "unit": "ohm",
     "tolerance": "1%", "package": "0805", "power": 0.125},
    {"part": "100nF_cap", "type": "capacitor", "value": 100e-9, "unit": "F",
     "tolerance": "10%", "package": "0805", "voltage": 50},
    {"part": "10uF_cap", "type": "capacitor", "value": 10e-6, "unit": "F",
     "tolerance": "20%", "package": "0805", "voltage": 16},
    {"part": "LM7805", "type": "regulator", "voltage_out": 5.0, "package": "TO-220",
     "max_current": 1.0},
    {"part": "ESP32", "type": "microcontroller", "core": "Xtensa LX6", "flash": "4MB",
     "wifi": True, "bluetooth": True, "package": "module"},
    {"part": "ATmega328P", "type": "microcontroller", "core": "AVR", "flash": "32KB",
     "package": "DIP-28"},
    {"part": "NPN_2N2222", "type": "transistor", "polarity": "NPN",
     "ic_max": 0.8, "package": "TO-92"},
    {"part": "1N4148", "type": "diode", "vrrm": 100, "if_avg": 0.3, "package": "DO-35"},
    {"part": "PC817", "type": "optocoupler", "ctr": 0.5, "package": "DIP-4"},
]


class ComponentDatabase:
    def __init__(self, db_path: str | None = None):
        self.db_path = db_path or os.path.join(
            os.path.dirname(__file__), "..", "database", "components.db")
        self.components = list(COMPONENTS)

    def search(self, **filters) -> List[Dict[str, Any]]:
        results = self.components
        for key, value in filters.items():
            results = [c for c in results if c.get(key) == value]
        return results

    def by_type(self, ctype: str) -> List[Dict[str, Any]]:
        return [c for c in self.components if c.get("type") == ctype]

    def get(self, part: str) -> Dict[str, Any] | None:
        for c in self.components:
            if c["part"].lower() == part.lower():
                return c
        return None

    def add(self, component: Dict[str, Any]):
        self.components.append(component)

    def all(self) -> List[Dict[str, Any]]:
        return list(self.components)
