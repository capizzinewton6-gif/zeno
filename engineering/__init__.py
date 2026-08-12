"""Engineering discipline capabilities (One Capability = One Module)."""

from .mechanical import MechanicalEngineering
from .electrical import ElectricalEngineering
from .electronics import ElectronicsEngineering
from .civil import CivilEngineering
from .chemical import ChemicalEngineering
from .aerospace import AerospaceEngineering
from .robotics import RoboticsEngineering
from .automotive import AutomotiveEngineering
from .mechatronics import MechatronicsEngineering

__all__ = [
    "MechanicalEngineering", "ElectricalEngineering", "ElectronicsEngineering",
    "CivilEngineering", "ChemicalEngineering", "AerospaceEngineering",
    "RoboticsEngineering", "AutomotiveEngineering", "MechatronicsEngineering",
]
