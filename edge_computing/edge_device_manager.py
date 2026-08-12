"""Edge device manager: CPU/GPU usage, thermal throttling, power modes."""

from __future__ import annotations

import os
import time
from dataclasses import dataclass
from typing import Optional


@dataclass
class DeviceMetrics:
    cpu_percent: float
    memory_percent: float
    gpu_percent: float
    gpu_temp_c: float
    power_mode: str


class EdgeDeviceManager:
    """Collect device telemetry and manage power modes (NVIDIA Jetson-aware)."""

    def __init__(self, jetson: bool = False) -> None:
        self.jetson = jetson

    def metrics(self) -> DeviceMetrics:
        cpu = self._cpu_percent()
        mem = self._memory_percent()
        gpu, temp = self._gpu_stats()
        return DeviceMetrics(cpu_percent=cpu, memory_percent=mem,
                             gpu_percent=gpu, gpu_temp_c=temp,
                             power_mode=self.power_mode())

    def _cpu_percent(self) -> float:
        try:
            import psutil  # type: ignore
            return float(psutil.cpu_percent(interval=0.1))
        except Exception:
            return 0.0

    def _memory_percent(self) -> float:
        try:
            import psutil  # type: ignore
            return float(psutil.virtual_memory().percent)
        except Exception:
            return 0.0

    def _gpu_stats(self):
        try:
            import pynvml  # type: ignore
            pynvml.nvmlInit()
            handle = pynvml.nvmlDeviceGetHandleByIndex(0)
            util = pynvml.nvmlDeviceGetUtilizationRates(handle)
            temp = pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU)
            return float(util.gpu), float(temp)
        except Exception:
            return 0.0, 0.0

    def power_mode(self) -> str:
        if self.jetson and os.path.exists("/etc/nvpmodel.conf"):
            try:
                with open("/sys/devices/17000000.gv10b/nvpmodel/nvpmodel_turbomode") as f:
                    return "turbo" if "1" in f.read() else "normal"
            except Exception:
                pass
        return "default"

    def set_power_mode(self, mode: str) -> bool:
        if not self.jetson:
            return False
        try:
            import subprocess
            subprocess.run(["sudo", "nvpmodel", "-m", mode], check=True)
            return True
        except Exception:
            return False
