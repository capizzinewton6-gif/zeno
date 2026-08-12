"""ai_bridge package - auto-registers its capability modules."""

from typing import Any, Dict, List

# Per-module imports (kept explicit so a failing import does not break
# the whole package).
from .api_client import ApiClient
from .capability_interface import CapabilityInterface
from .command_router import CommandRouter
from .event_bridge import EventBridge
from .response_handler import ResponseHandler


def list_modules() -> List[str]:
    """Return the capability names registered in this package."""
    return [
        "api_client",
        "capability_interface",
        "command_router",
        "event_bridge",
        "response_handler",
    ]


def instantiate_all(config: Dict[str, Any] = None) -> Dict[str, Any]:
    """Instantiate every module in this package and return name->instance."""
    return {
        name: cls(config=config)
        for name, cls in (
            ("api_client", ApiClient),
            ("capability_interface", CapabilityInterface),
            ("command_router", CommandRouter),
            ("event_bridge", EventBridge),
            ("response_handler", ResponseHandler),
        )
    }


__all__ = ["list_modules", "instantiate_all", "ApiClient", "CapabilityInterface", "CommandRouter", "EventBridge", "ResponseHandler"]
