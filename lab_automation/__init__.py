"""lab_automation package — automated synthesis, sensors, instruments, acquisition, errors, safety."""

from .synthesis_robot import SynthesisRobot
from .sensor_calibration import SensorCalibration
from .instrument_interface import InstrumentInterface
from .data_acquisition import DataAcquisition
from .error_analysis import ErrorAnalysis
from .safety_interlocks import SafetyInterlocks

__all__ = [
    "SynthesisRobot", "SensorCalibration", "InstrumentInterface",
    "DataAcquisition", "ErrorAnalysis", "SafetyInterlocks",
]
