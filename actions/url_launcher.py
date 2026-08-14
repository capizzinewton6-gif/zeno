"""
actions - url_launcher
=======================
Open URLs in the browser.

Independent actions module for the Autonomous Computer AI Assistant.
Implements the standard execute(task, context) capability contract.
"""

import re
import webbrowser
from typing import Any, Dict, Optional

from core.capability import Capability


class UrlLauncher(Capability):
    """Open URLs in the browser."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.name = "url_launcher"
        self.description = "Open URLs in the browser."

    def execute(self, task: str, context: Optional[Dict[str, Any]] = None) -> Any:
        url = self._extract_url(task)
        if not url:
            return self.error("No URL found in task.")
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        try:
            opened = webbrowser.open(url)
        except Exception as exc:
            return self.error(str(exc), url=url)
        if opened:
            return self.ok(f"Opened {url} in the default browser.", url=url)
        return self.ok(f"Browser open requested for {url} (no GUI browser may be available).", url=url)

    def _extract_url(self, task: str) -> str:
        task = task.strip()
        for prefix in ("open url:", "open website:", "open link:", "go to:", "navigate to:", "open "):
            if task.lower().startswith(prefix):
                task = task[len(prefix):].strip()
        match = re.search(r"https?://[^\s\"']+", task)
        if match:
            return match.group(0)
        match = re.search(r"[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}([/?]\S*)?", task)
        return match.group(0).strip("\"'") if match else task.strip("\"'")
