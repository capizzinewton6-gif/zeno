"""External integrations."""

from __future__ import annotations

import json
import logging
import urllib.parse
import urllib.request
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


class ExternalTools:
    """Integrations with external services and tools."""

    def http_get(self, url: str, headers: Optional[Dict[str, str]] = None,
                 timeout: int = 10) -> Dict[str, Any]:
        try:
            req = urllib.request.Request(url, headers=headers or {})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                body = resp.read().decode("utf-8", errors="replace")
                return {
                    "status": resp.status,
                    "headers": dict(resp.headers),
                    "body": body,
                }
        except Exception as exc:
            logger.warning("HTTP GET %s failed: %s", url, exc)
            return {"status": 0, "error": str(exc)}

    def http_post(self, url: str, data: Dict[str, Any],
                  headers: Optional[Dict[str, str]] = None,
                  timeout: int = 10) -> Dict[str, Any]:
        try:
            payload = json.dumps(data).encode("utf-8")
            hdrs = {"Content-Type": "application/json"}
            if headers:
                hdrs.update(headers)
            req = urllib.request.Request(url, data=payload, headers=hdrs, method="POST")
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                body = resp.read().decode("utf-8", errors="replace")
                return {"status": resp.status, "body": body}
        except Exception as exc:
            logger.warning("HTTP POST %s failed: %s", url, exc)
            return {"status": 0, "error": str(exc)}

    def webhook(self, url: str, payload: Dict[str, Any]) -> bool:
        result = self.http_post(url, payload)
        return 200 <= result.get("status", 0) < 300

    def open_webhook_url(self, url: str) -> bool:
        from integrations.operating_system import OperatingSystem
        return OperatingSystem().open_url(url)

    def run_shell(self, command: str, timeout: int = 30) -> Dict[str, Any]:
        import subprocess
        try:
            result = subprocess.run(
                command, shell=True, capture_output=True, text=True, timeout=timeout, check=False,
            )
            return {
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
            }
        except Exception as exc:
            return {"returncode": -1, "stdout": "", "stderr": str(exc)}
