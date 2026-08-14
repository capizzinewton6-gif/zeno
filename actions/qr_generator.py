"""
actions - qr_generator
=======================
Generate QR codes.

Independent actions module for the Autonomous Computer AI Assistant.
Implements the standard execute(task, context) capability contract.
"""

import re
import urllib.parse
from typing import Any, Dict, Optional

from core.capability import Capability

try:
    import requests  # type: ignore
    _HAS_REQUESTS = True
except ImportError:  # pragma: no cover
    _HAS_REQUESTS = False


class QrGenerator(Capability):
    """Generate QR codes."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.name = "qr_generator"
        self.description = "Generate QR codes."
        self.timeout = int(self.config.get("timeout", 10))

    def execute(self, task: str, context: Optional[Dict[str, Any]] = None) -> Any:
        data = self._extract_data(task)
        if not data:
            return self.error("No data to encode found in task.")
        url = "https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=" + urllib.parse.quote(data)
        if _HAS_REQUESTS:
            try:
                resp = requests.get(url, timeout=self.timeout)
                if resp.status_code == 200:
                    return self.ok(f"QR code generated for: {data}\nImage URL: {url}", url=url, data=data)
                return self.error(f"QR service returned status {resp.status_code}", url=url)
            except Exception as exc:
                return self.error(str(exc), url=url)
        return self.ok(f"QR code URL: {url}", url=url, data=data)

    def _extract_data(self, task: str) -> str:
        task = task.strip()
        for prefix in ("generate qr:", "qr code:", "qr:", "encode:"):
            if task.lower().startswith(prefix):
                return task[len(prefix):].strip().strip("\"\'")
                break
        # Word-prefixes without colon: "generate qr ...", "make qr ..."
        low = task.lower()
        for word, n in (("generate qr", 11), ("make qr", 7), ("qr code", 7)):
            if low.startswith(word):
                return task[n:].strip().strip("\"\'")
        # Otherwise pull the first quoted string, else use the whole task.
        m = re.search(r'["\']([^"\']+)["\']', task)
        return m.group(1) if m else task.strip().strip("\"\'")

    def get_name(self) -> str:
        return self.name

    def get_description(self) -> str:
        return self.description
