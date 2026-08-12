"""Holographic workspace - the interactive command surface."""

from __future__ import annotations

import importlib
from typing import Any, Dict, Optional

from core.arc_reactor import ArcReactor
from core.hologram_grid import HologramGrid
from core.telemetry_dashboard import TelemetryDashboard


class HolographicWorkspace:
    """Central brain that routes holographic commands to capability packages."""

    PACKAGES = [
        "holographic_display",
        "gesture_control",
        "spatial_computing",
        "interaction",
        "holographic_objects",
        "visualization",
        "scientific_visualization",
        "engineering",
        "telepresence",
        "hardware",
        "rendering",
        "security",
        "applications",
        "ai_bridge",
        "persistence",
        "safety",
    ]

    def __init__(self, ui=None):
        self.ui = ui
        self.reactor = ArcReactor(ui=None)
        self.reactor.online = True
        self.grid = HologramGrid(ui=None)
        self.dashboard = TelemetryDashboard(ui=ui)
        self.registry: Dict[str, Any] = {}
        self._load_packages()

    def _load_packages(self):
        for pkg in self.PACKAGES:
            try:
                mod = importlib.import_module(pkg)
                instances = mod.instantiate_all(config={})
                for name, inst in instances.items():
                    self.registry[f"{pkg}.{name}"] = inst
            except Exception as exc:
                if self.ui:
                    self.ui.warn(f"package {pkg} failed to load: {exc}")

    def help(self) -> dict:
        return {
            "commands": "help | status | list | scan | dashboard | arc | grid | <package.module> <task>",
            "packages": ", ".join(self.PACKAGES),
            "modules": len(self.registry),
        }

    def execute(self, command: str, context: Optional[Dict[str, Any]] = None) -> Any:
        cmd = command.strip()
        low = cmd.lower()

        # Built-ins.
        if low in ("help", "?"):
            return self.help()
        if low in ("status",):
            return {
                "reactor": self.reactor.status(),
                "grid": self.grid.status(),
                "modules_loaded": len(self.registry),
            }
        if low in ("list", "modules"):
            return {"modules": sorted(self.registry.keys())}
        if low in ("scan",):
            if self.ui:
                self.ui.progress("Scanning spatial environment", total=100, sleep=0.01)
            self.grid.raise_grid()
            return {"scan": "complete", "grid": self.grid.status()}
        if low in ("dashboard", "telemetry"):
            return self.dashboard.materialise()
        if low in ("arc", "reactor"):
            return self.reactor.status()
        if low in ("grid",):
            return self.grid.status()

        # Route "<package.module> <task>" or "<module> <task>".
        parts = cmd.split(maxsplit=1)
        target = parts[0]
        task = parts[1] if len(parts) > 1 else "execute"
        inst = self.registry.get(target)
        if inst is None:
            # try matching by suffix
            matches = [k for k in self.registry if k.endswith("." + target) or k.split(".")[-1] == target]
            if len(matches) == 1:
                inst = self.registry[matches[0]]
            elif matches:
                return {"ambiguity": matches}
        if inst is not None:
            try:
                result = inst.execute(task, context)
                self.dashboard.add_hologram(1)
                return result
            except Exception as exc:
                return {"error": str(exc), "module": target}

        return {
            "error": "unknown command",
            "command": cmd,
            "hint": "type 'help' for available commands, 'list' for modules",
        }

    def tick_safety(self):
        """Daemon safety tick - placeholder for safety package polling."""
        safety = self.registry.get("safety.emergency_shutdown")
        if safety is not None:
            try:
                safety.execute("tick")
            except Exception:
                pass
