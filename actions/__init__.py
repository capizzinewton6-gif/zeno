"""
actions package - 166+ individual tools.

Auto-registers every action module found in this directory so the orchestrator
can discover and invoke capabilities by name without manual imports.
"""

import importlib
import pkgutil
from typing import Any, Dict

from . import *  # noqa: F401,F403  - ensure all submodules import

_REGISTRY: Dict[str, Any] = {}


def _register(name: str, instance: Any) -> None:
    _REGISTRY[name] = instance


def get_actions() -> Dict[str, Any]:
    """Return a name -> instance map of all registered actions."""
    if not _REGISTRY:
        _autodiscover()
    return _REGISTRY


def get_action(name: str) -> Any:
    """Return a single registered action by name."""
    if not _REGISTRY:
        _autodiscover()
    return _REGISTRY.get(name)


def _autodiscover() -> None:
    """Import every sibling module and register its main class."""
    for finder, modname, ispkg in pkgutil.iter_modules(__path__):
        if ispkg or modname.startswith("_"):
            continue
        try:
            module = importlib.import_module(f"{__name__}.{modname}")
        except Exception as exc:  # pragma: no cover - keep loading siblings
            continue
        cls = _find_capability_class(module)
        if cls is None:
            continue
        try:
            instance = cls()
        except Exception:
            continue
        _register(instance.get_name() if hasattr(instance, "get_name") else modname, instance)


def _find_capability_class(module: Any) -> Any:
    """Pick the first user-defined class in a module that looks like a capability."""
    import inspect
    for _name, obj in inspect.getmembers(module, inspect.isclass):
        if obj.__module__ == module.__name__ and not _name.startswith("_"):
            return obj
    return None
