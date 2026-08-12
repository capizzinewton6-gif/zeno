"""Data size, time duration, and memory unit conversions."""
from __future__ import annotations

_BYTE_UNITS = ("B", "KB", "MB", "GB", "TB", "PB")
_TIME_UNITS = ("ns", "us", "ms", "s", "min", "h", "d")


def human_bytes(n: float) -> str:
    """Convert bytes to a human-readable string."""
    n = float(n)
    for unit in _BYTE_UNITS:
        if abs(n) < 1024.0 or unit == _BYTE_UNITS[-1]:
            return f"{n:.1f} {unit}"
        n /= 1024.0
    return f"{n:.1f} {unit}"


def parse_bytes(text: str) -> int:
    """Parse a human-readable byte string (e.g. '1.5GB') into bytes."""
    import re
    m = re.match(r"^\s*([\d.]+)\s*([KMGTPE]?B?)\s*$", text, re.IGNORECASE)
    if not m:
        return 0
    value = float(m.group(1))
    unit = m.group(2).upper()
    multipliers = {"": 1, "B": 1, "KB": 1024, "MB": 1024**2,
                   "GB": 1024**3, "TB": 1024**4, "PB": 1024**5}
    return int(value * multipliers.get(unit, 1))


def human_duration(seconds: float) -> str:
    """Convert seconds to a human-readable duration."""
    if seconds < 1e-6:
        return f"{seconds * 1e9:.0f} ns"
    if seconds < 1e-3:
        return f"{seconds * 1e6:.0f} us"
    if seconds < 1:
        return f"{seconds * 1e3:.1f} ms"
    if seconds < 60:
        return f"{seconds:.1f} s"
    if seconds < 3600:
        return f"{seconds / 60:.1f} min"
    if seconds < 86400:
        return f"{seconds / 3600:.1f} h"
    return f"{seconds / 86400:.1f} d"


def parse_duration(text: str) -> float:
    """Parse a human-readable duration string into seconds."""
    import re
    m = re.match(r"^\s*([\d.]+)\s*(ns|us|ms|s|min|h|d)?\s*$", text, re.IGNORECASE)
    if not m:
        return 0.0
    value = float(m.group(1))
    unit = (m.group(2) or "s").lower()
    factors = {"ns": 1e-9, "us": 1e-6, "ms": 1e-3, "s": 1,
               "min": 60, "h": 3600, "d": 86400}
    return value * factors.get(unit, 1.0)


class UnitConverter:
    """Convenience wrapper for unit conversions."""

    human_bytes = staticmethod(human_bytes)
    parse_bytes = staticmethod(parse_bytes)
    human_duration = staticmethod(human_duration)
    parse_duration = staticmethod(parse_duration)
