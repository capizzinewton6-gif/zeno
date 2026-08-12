"""Sensor manager: sensor selection and integration."""

from __future__ import annotations

from src.gemini_25_flash_engine import Gemini25FlashEngine

# Common sensor catalog.
SENSORS = [
    {"name": "DHT22", "type": "temperature_humidity", "range": "-40 to 80 C",
     "accuracy": "0.5 C", "interface": "digital"},
    {"name": "MPU6050", "type": "imu", "axes": "6",
     "interface": "I2C", "range": "±2g/±250dps"},
    {"name": "HC-SR04", "type": "ultrasonic_distance", "range": "2-400 cm",
     "interface": "digital"},
    {"name": "MPX5700AP", "type": "pressure", "range": "15-115 kPa",
     "interface": "analog"},
    {"name": "LDR", "type": "light", "interface": "analog"},
    {"name": "MQ-2", "type": "gas", "gases": "LPG, propane, methane",
     "interface": "analog"},
    {"name": "DS18B20", "type": "temperature", "range": "-55 to 125 C",
     "interface": "1-Wire"},
    {"name": "BME280", "type": "environmental", "params": "T/RH/P",
     "interface": "I2C/SPI"},
]


class SensorManager:
    def __init__(self, engine: Gemini25FlashEngine | None = None):
        self.engine = engine or Gemini25FlashEngine()
        self.sensors = list(SENSORS)

    def select(self, measurement: str) -> str:
        return self.engine.generate(
            f"Select suitable sensors to measure: {measurement}. Compare options.",
            system="You are a sensor selection engineer.")

    def integration_plan(self, sensor: str, mcu: str) -> str:
        return self.engine.generate(
            f"Design the interface and signal conditioning to connect {sensor} to {mcu}.",
            system="You are a sensor integration engineer.")

    def calibration_plan(self, sensor: str) -> str:
        return self.engine.generate(
            f"Design a calibration procedure for {sensor}.",
            system="You are a metrology engineer.")

    def search(self, stype: str) -> list[dict]:
        return [s for s in self.sensors if s["type"] == stype]
