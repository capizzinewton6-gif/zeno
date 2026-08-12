"""Synthesis robot — automated liquid/solid handling and flow-chemistry control.

Simulates an automated synthesis platform. All simulations run on the UI.
"""

import time


class SynthesisRobot:
    """Simulate automated synthesis module operations."""

    def __init__(self):
        self.syringes = {"A": None, "B": None, "C": None, "D": None}
        self.temperature_C = 25.0
        self.stir_rpm = 0
        self.log = []

    def load_syringe(self, port, reagent, volume_mL):
        if port not in self.syringes:
            return {"error": f"Unknown port {port}"}
        self.syringes[port] = {"reagent": reagent, "volume_mL": volume_mL}
        self._log(f"Loaded {reagent} ({volume_mL} mL) into port {port}")
        return self.syringes[port]

    def dispense(self, port, volume_mL, rate_mL_min=1.0):
        if port not in self.syringes or not self.syringes[port]:
            return {"error": f"Port {port} empty"}
        if self.syringes[port]["volume_mL"] < volume_mL:
            return {"error": "Insufficient volume"}
        self.syringes[port]["volume_mL"] -= volume_mL
        duration_min = volume_mL / rate_mL_min
        self._log(f"Dispensed {volume_mL} mL from {port} at {rate_mL_min} mL/min ({duration_min:.2f} min)")
        return {"dispensed_mL": volume_mL, "duration_min": round(duration_min, 2)}

    def set_temperature(self, target_C, ramp_C_min=5.0):
        delta = target_C - self.temperature_C
        ramp_time = abs(delta) / ramp_C_min if ramp_C_min else 0
        self.temperature_C = target_C
        self._log(f"Set temperature to {target_C} C (ramp {ramp_time:.1f} min)")
        return {"target_C": target_C, "ramp_time_min": round(ramp_time, 2)}

    def stir(self, rpm):
        self.stir_rpm = rpm
        self._log(f"Stirring at {rpm} rpm")
        return {"rpm": rpm}

    def run_flow(self, flow_rate_mL_min, residence_time_min, volume_mL):
        reactor_volume = flow_rate_mL_min * residence_time_min
        self._log(f"Flow: {flow_rate_mL_min} mL/min, residence {residence_time_min} min, "
                  f"reactor vol {reactor_volume:.2f} mL")
        return {
            "flow_rate_mL_min": flow_rate_mL_min,
            "residence_time_min": residence_time_min,
            "reactor_volume_mL": round(reactor_volume, 2),
            "collection_time_min": round(volume_mL / flow_rate_mL_min, 2),
        }

    def status(self):
        return {
            "syringes": self.syringes,
            "temperature_C": self.temperature_C,
            "stir_rpm": self.stir_rpm,
        }

    def get_log(self):
        return list(self.log)

    def _log(self, msg):
        self.log.append({"t": time.time(), "msg": msg})
