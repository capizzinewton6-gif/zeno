"""Browser interaction."""

from __future__ import annotations

import logging
import subprocess
import time
from typing import Any, Dict, Optional

from integrations.operating_system import OperatingSystem

logger = logging.getLogger(__name__)


class BrowserControl:
    """Open and interact with web browsers."""

    def __init__(self) -> None:
        self.os = OperatingSystem()

    def open_url(self, url: str) -> bool:
        return self.os.open_url(url)

    def open_url_in_browser(self, url: str, browser: Optional[str] = None) -> bool:
        if browser:
            try:
                if self.os.is_windows:
                    subprocess.Popen(["cmd", "/c", "start", browser, url])
                elif self.os.is_macos:
                    subprocess.Popen(["open", "-a", browser, url])
                else:
                    subprocess.Popen([browser, url])
                return True
            except Exception as exc:
                logger.warning("open_url_in_browser failed: %s", exc)
                return False
        return self.open_url(url)

    def search(self, query: str, engine: str = "google") -> bool:
        engines = {
            "google": "https://www.google.com/search?q=",
            "bing": "https://www.bing.com/search?q=",
            "duckduckgo": "https://duckduckgo.com/?q=",
        }
        base = engines.get(engine.lower(), engines["google"])
        return self.open_url(base + query.replace(" ", "+"))

    def keyboard_shortcut(self, *keys) -> bool:
        from automation.keyboard_controller import KeyboardController
        return KeyboardController().hotkey(*keys)

    def new_tab(self) -> bool:
        return self.keyboard_shortcut("ctrl", "t")

    def close_tab(self) -> bool:
        return self.keyboard_shortcut("ctrl", "w")

    def reload(self) -> bool:
        return self.keyboard_shortcut("ctrl", "r")

    def focus_address_bar(self) -> bool:
        return self.keyboard_shortcut("ctrl", "l")

    def navigate_back(self) -> bool:
        from automation.keyboard_controller import KeyboardController
        return KeyboardController().hotkey("alt", "left")

    def bookmark(self) -> bool:
        return self.keyboard_shortcut("ctrl", "d")

    def find_in_page(self) -> bool:
        return self.keyboard_shortcut("ctrl", "f")
