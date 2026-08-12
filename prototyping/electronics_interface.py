"""Thermoelectric coolers and incubator controls."""
from __future__ import annotations


class ElectronicsInterface:
    @staticmethod
    def thermoelectric_pid(setpoint_c: float, measured_c: float,
                            kp: float = 0.5, ki: float = 0.01,
                            integral: float = 0.0, dt: float = 1.0) -> dict:
        error = setpoint_c - measured_c
        integral += error * dt
        output = kp * error + ki * integral
        return {"error": round(error, 3), "integral": round(integral, 3),
                "pid_output": round(output, 3),
                "heating": output > 0, "cooling": output < 0}

    @staticmethod
    def incubator_profile(setpoint_c: float = 37.0, co2_pct: float = 5.0,
                          humidity_pct: float = 95.0) -> dict:
        return {"temperature_setpoint": setpoint_c, "co2_setpoint": co2_pct,
                "humidity_setpoint": humidity_pct}

    @staticmethod
    def pwm_duty_cycle(error: float, max_duty: float = 100.0) -> float:
        return round(min(max(abs(error) * 5, 0), max_duty), 2)
