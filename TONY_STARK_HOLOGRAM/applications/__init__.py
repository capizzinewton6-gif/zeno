"""applications package - auto-registers its capability modules."""

from typing import Any, Dict, List

# Per-module imports (kept explicit so a failing import does not break
# the whole package).
from .holographic_browser import HolographicBrowser
from .holographic_communication import HolographicCommunication
from .holographic_control import HolographicControl
from .holographic_files import HolographicFiles
from .holographic_maps import HolographicMaps
from .holographic_terminal import HolographicTerminal
from .holographic_workspace import HolographicWorkspace


def list_modules() -> List[str]:
    """Return the capability names registered in this package."""
    return [
        "holographic_browser",
        "holographic_communication",
        "holographic_control",
        "holographic_files",
        "holographic_maps",
        "holographic_terminal",
        "holographic_workspace",
    ]


def instantiate_all(config: Dict[str, Any] = None) -> Dict[str, Any]:
    """Instantiate every module in this package and return name->instance."""
    return {
        name: cls(config=config)
        for name, cls in (
            ("holographic_browser", HolographicBrowser),
            ("holographic_communication", HolographicCommunication),
            ("holographic_control", HolographicControl),
            ("holographic_files", HolographicFiles),
            ("holographic_maps", HolographicMaps),
            ("holographic_terminal", HolographicTerminal),
            ("holographic_workspace", HolographicWorkspace),
        )
    }


__all__ = ["list_modules", "instantiate_all", "HolographicBrowser", "HolographicCommunication", "HolographicControl", "HolographicFiles", "HolographicMaps", "HolographicTerminal", "HolographicWorkspace"]
