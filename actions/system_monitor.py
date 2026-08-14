"""
actions - system_monitor
=========================
Monitor CPU, RAM, GPU, temperature and battery.

Independent actions module for the Autonomous Computer AI Assistant.
Implements the standard execute(task, context) capability contract.
"""

import os
import platform
import time
from typing import Any, Dict, Optional

from core.capability import Capability

try:
    import psutil  # type: ignore
    _HAS_PSUTIL = True
except ImportError:  # pragma: no cover
    _HAS_PSUTIL = False


class SystemMonitor(Capability):
    """Monitor CPU, RAM, GPU, temperature and battery."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.name = "system_monitor"
        self.description = "Monitor CPU, RAM, GPU, temperature and battery."

    def execute(self, task: str, context: Optional[Dict[str, Any]] = None) -> Any:
        if not _HAS_PSUTIL:
            return self.error("psutil is not installed. Run: pip install psutil")
        low = task.lower()
        if "disk" in low or "storage" in low or "space" in low:
            return self._disk()
        if "battery" in low or "power" in low:
            return self._battery()
        if "network" in low or "net" in low:
            return self._network()
        return self._overview()

    def _overview(self) -> Any:
        vm = psutil.virtual_memory()
        sm = psutil.swap_memory()
        cpu_percent = psutil.cpu_percent(interval=0.5)
        load = os.getloadavg() if hasattr(os, "getloadavg") else ()
        boot = psutil.boot_time()
        uptime = int(time.time() - boot)
        lines = [
            f"System: {platform.system()} {platform.release()} ({platform.machine()})",
            f"Hostname: {platform.node()}",
            f"Uptime: {uptime // 3600}h {(uptime % 3600) // 60}m",
            f"CPU usage: {cpu_percent}% ({psutil.cpu_count()} cores)",
        ]
        if load:
            lines.append(f"Load avg: {', '.join(f'{x:.2f}' for x in load)}")
        lines.extend([
            f"Memory: {vm.percent}% used ({vm.used // (1024**2)} / {vm.total // (1024**2)} MB)",
            f"Swap: {sm.percent}% used ({sm.used // (1024**2)} / {sm.total // (1024**2)} MB)",
        ])
        batt = self._battery_raw()
        if batt:
            lines.append(f"Battery: {batt.percent}% {'(charging)' if batt.power_plugged else '(on battery)'}")
        return self.ok("\n".join(lines))

    def _disk(self) -> Any:
        lines = []
        for part in psutil.disk_partitions(all=False):
            try:
                usage = psutil.disk_usage(part.mountpoint)
            except (PermissionError, OSError):
                continue
            lines.append(
                f"{part.mountpoint} ({part.device}): "
                f"{usage.percent}% used ({usage.used // (1024**3)} / {usage.total // (1024**3)} GB)"
            )
        if not lines:
            return self.error("No accessible disk partitions.")
        io = psutil.disk_io_counters()
        extra = f"\nDisk I/O: read={io.read_bytes // (1024**2)}MB write={io.write_bytes // (1024**2)}MB" if io else ""
        return self.ok("\n".join(lines) + extra)

    def _battery(self) -> Any:
        batt = self._battery_raw()
        if not batt:
            return self.error("No battery detected (desktop system).")
        return self.ok(
            f"Battery: {batt.percent}% {'(charging)' if batt.power_plugged else '(on battery)'}"
            + (f", {batt.secsleft // 60} min remaining" if batt.secsleft and batt.secsleft > 0 else "")
        )

    def _network(self) -> Any:
        io = psutil.net_io_counters()
        lines = [
            f"Bytes sent: {io.bytes_sent // (1024**2)} MB",
            f"Bytes recv: {io.bytes_recv // (1024**2)} MB",
            f"Packets sent: {io.packets_sent}",
            f"Packets recv: {io.packets_recv}",
        ]
        return self.ok("\n".join(lines))

    @staticmethod
    def _battery_raw():
        try:
            return psutil.sensors_battery()
        except Exception:
            return None
