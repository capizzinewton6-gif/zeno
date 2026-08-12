"""Instrument interface — connect to GC-MS, HPLC, NMR, and spectrophotometers.

Provides a uniform simulation interface; real drivers would implement these
methods against vendor SDKs.
"""

import time


class InstrumentInterface:
    """Simulated instrument control interface."""

    INSTRUMENTS = ["GC-MS", "HPLC", "NMR", "UV-Vis", "FT-IR", "ICP-MS"]

    def __init__(self):
        self.connections = {}

    def connect(self, instrument, address="sim"):
        if instrument not in self.INSTRUMENTS:
            return {"error": f"Unknown instrument {instrument}"}
        self.connections[instrument] = {"address": address, "connected": True, "since": time.time()}
        return {"instrument": instrument, "status": "connected", "address": address}

    def disconnect(self, instrument):
        if instrument in self.connections:
            self.connections[instrument]["connected"] = False
            return {"instrument": instrument, "status": "disconnected"}
        return {"error": "not connected"}

    def run_acquisition(self, instrument, method="default", sample="unknown"):
        if instrument not in self.connections or not self.connections[instrument]["connected"]:
            return {"error": f"{instrument} not connected"}
        result = {
            "instrument": instrument,
            "method": method,
            "sample": sample,
            "status": "complete",
            "timestamp": time.time(),
            "data": self._simulate(instrument),
        }
        return result

    def _simulate(self, instrument):
        if instrument == "GC-MS":
            return {"peaks": [{"rt_min": 5.2, "mz": 91, "area": 1.2e6},
                              {"rt_min": 8.7, "mz": 130, "area": 3.4e6}]}
        if instrument == "HPLC":
            return {"peaks": [{"rt_min": 3.1, "area": 2.1e5, "purity_pct": 98.5}]}
        if instrument == "NMR":
            return {"peaks": [{"shift_ppm": 7.26, "intensity": 1.0, "mult": "s"},
                              {"shift_ppm": 2.1, "intensity": 3.0, "mult": "s"}]}
        if instrument == "UV-Vis":
            return {"lambda_max_nm": 280, "absorbance": 0.74}
        if instrument == "FT-IR":
            return {"peaks_cm1": [3300, 1720, 1600, 1200]}
        if instrument == "ICP-MS":
            return {"elements_ppm": {"Fe": 1.2, "Cu": 0.3}}
        return {}

    def list_connections(self):
        return self.connections
