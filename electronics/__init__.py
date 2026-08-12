"""Electronics capabilities (One Capability = One Module)."""

from .circuit_designer import CircuitDesigner
from .component_database import ComponentDatabase, COMPONENTS
from .microcontroller import MicrocontrollerProject
from .pcb_designer import PCBDesigner
from .sensor_manager import SensorManager, SENSORS
from .power_systems import PowerSystems

__all__ = [
    "CircuitDesigner", "ComponentDatabase", "COMPONENTS",
    "MicrocontrollerProject", "PCBDesigner", "SensorManager", "SENSORS", "PowerSystems",
]
