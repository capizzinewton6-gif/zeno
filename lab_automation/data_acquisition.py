"""Data acquisition — real-time temperature, pressure, absorbance acquisition."""

import time
import random


class DataAcquisition:
    """Simulate real-time data acquisition streams."""

    def __init__(self, sampling_rate_hz=1.0):
        self.sampling_rate_hz = sampling_rate_hz
        self.buffer = []

    def acquire(self, sensor, duration_s, base_value=25.0, noise=0.1):
        n_points = int(duration_s * self.sampling_rate_hz)
        data = []
        for i in range(n_points):
            t = i / self.sampling_rate_hz
            value = base_value + random.gauss(0, noise)
            data.append({"t": round(t, 3), sensor: round(value, 4)})
        self.buffer.extend(data)
        return data

    def stream(self, sensor, n=10, base_value=25.0, noise=0.1):
        """Generate a simulated stream of n readings."""
        return [{"t": round(i / self.sampling_rate_hz, 3),
                 sensor: round(base_value + random.gauss(0, noise), 4)} for i in range(n)]

    def clear(self):
        self.buffer = []

    def summary(self):
        if not self.buffer:
            return {"n": 0}
        return {"n": len(self.buffer), "first": self.buffer[0], "last": self.buffer[-1]}
