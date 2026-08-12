"""Context manager — reaction context (pH, temperature, solvent environment)."""

import copy


class ContextManager:
    """Maintains the chemical context of the current session."""

    def __init__(self):
        self._context = {
            "temperature_C": 25.0,
            "pressure_atm": 1.0,
            "solvent": None,
            "pH": None,
            "atmosphere": "air",
            "concentration_M": None,
            "last_task": None,
        }

    def set(self, key, value):
        self._context[key] = value
        return self._context[key]

    def get(self, key, default=None):
        return self._context.get(key, default)

    def update(self, mapping):
        self._context.update(mapping)

    def snapshot(self):
        return copy.deepcopy(self._context)

    def set_last_task(self, task):
        self._context["last_task"] = task

    def reset(self):
        self.__init__()
