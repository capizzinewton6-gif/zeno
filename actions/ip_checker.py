"""
actions - ip_checker
=====================
Public IP information.

Independent actions module for the Autonomous Computer AI Assistant.
Implements the standard execute(task, context) capability contract.
"""

import json
from typing import Any, Dict, Optional

from core.capability import Capability

try:
    import requests  # type: ignore
    _HAS_REQUESTS = True
except ImportError:  # pragma: no cover
    _HAS_REQUESTS = False


class IpChecker(Capability):
    """Public IP information."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.name = "ip_checker"
        self.description = "Public IP information."
        self.timeout = int(self.config.get("timeout", 8))

    def execute(self, task: str, context: Optional[Dict[str, Any]] = None) -> Any:
        if not _HAS_REQUESTS:
            return self.error("requests is not installed. Run: pip install requests")
        try:
            resp = requests.get("https://ipinfo.io/json", timeout=self.timeout)
            resp.raise_for_status()
            data = resp.json()
        except Exception as exc:
            return self.error(str(exc))
        lines = [
            f"IP: {data.get('ip', 'unknown')}",
            f"City: {data.get('city', 'unknown')}",
            f"Region: {data.get('region', 'unknown')}",
            f"Country: {data.get('country', 'unknown')}",
            f"Org: {data.get('org', 'unknown')}",
            f"Location: {data.get('loc', 'unknown')}",
        ]
        return self.ok("\n".join(lines), ip=data.get("ip"), raw=data)
