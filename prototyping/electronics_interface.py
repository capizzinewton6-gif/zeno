"""Electronics interface — mass flow controllers and heating mantle integration."""


class ElectronicsInterface:
    """Simulate control of MFCs and heating elements."""

    def __init__(self):
        self.mfcs = {}
        self.heaters = {}

    def add_mfc(self, channel, gas, max_sccm=1000):
        self.mfcs[channel] = {"gas": gas, "max_sccm": max_sccm, "setpoint_sccm": 0}
        return self.mfcs[channel]

    def set_flow(self, channel, sccm):
        if channel not in self.mfcs:
            return {"error": "unknown MFC"}
        mfc = self.mfcs[channel]
        if sccm > mfc["max_sccm"]:
            return {"error": "exceeds max flow", "max_sccm": mfc["max_sccm"]}
        mfc["setpoint_sccm"] = sccm
        return {"channel": channel, "setpoint_sccm": sccm}

    def add_heater(self, channel, max_C=400):
        self.heaters[channel] = {"max_C": max_C, "setpoint_C": 25}
        return self.heaters[channel]

    def set_temperature(self, channel, target_C):
        if channel not in self.heaters:
            return {"error": "unknown heater"}
        h = self.heaters[channel]
        if target_C > h["max_C"]:
            return {"error": "exceeds max temp", "max_C": h["max_C"]}
        h["setpoint_C"] = target_C
        return {"channel": channel, "setpoint_C": target_C}

    def status(self):
        return {"mfcs": self.mfcs, "heaters": self.heaters}
