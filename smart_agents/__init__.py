"""
smart_agents package - 20 modules.

Auto-registers every module in this directory so the smart orchestrator can
discover capabilities by name without manual imports.
"""

import importlib
import inspect
import pkgutil
from typing import Any, Dict

from . import *  # noqa: F401,F403

_REGISTRY: Dict[str, Any] = {}


def get_modules() -> Dict[str, Any]:
    if not _REGISTRY:
        _autodiscover()
    return _REGISTRY


def get_module(name: str) -> Any:
    if not _REGISTRY:
        _autodiscover()
    return _REGISTRY.get(name)


def _autodiscover() -> None:
    for finder, modname, ispkg in pkgutil.iter_modules(__path__):
        if ispkg or modname.startswith("_"):
            continue
        try:
            module = importlib.import_module(f"{__name__}.{modname}")
        except Exception:
            continue
        for _name, obj in inspect.getmembers(module, inspect.isclass):
            if obj.__module__ == module.__name__ and not _name.startswith("_"):
                try:
                    instance = obj()
                except Exception:
                    continue
                key = instance.get_name() if hasattr(instance, "get_name") else modname
                _REGISTRY[key] = instance
                break
