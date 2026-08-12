"""Windows/Linux/Mac support."""

from __future__ import annotations

import logging
import platform
import shutil
import subprocess
from typing import Any, Dict

logger = logging.getLogger(__name__)


class OperatingSystem:
    """Cross-platform OS abstractions."""

    def __init__(self) -> None:
        self.system = platform.system().lower()
        self.release = platform.release()
        self.version = platform.version()

    @property
    def is_windows(self) -> bool:
        return self.system == "windows"

    @property
    def is_macos(self) -> bool:
        return self.system == "darwin"

    @property
    def is_linux(self) -> bool:
        return self.system == "linux"

    def info(self) -> Dict[str, Any]:
        return {
            "system": self.system,
            "release": self.release,
            "version": self.version,
            "machine": platform.machine(),
            "processor": platform.processor(),
        }

    def open_path(self, path: str) -> bool:
        try:
            if self.is_windows:
                os.startfile(path)  # type: ignore[attr-defined]
            elif self.is_macos:
                subprocess.Popen(["open", path])
            else:
                subprocess.Popen(["xdg-open", path])
            return True
        except Exception as exc:
            logger.warning("open_path failed: %s", exc)
            return False

    def open_url(self, url: str) -> bool:
        return self.open_path(url)

    def run_command(self, command: list[str], timeout: int = 30) -> Dict[str, Any]:
        try:
            result = subprocess.run(
                command, capture_output=True, text=True, timeout=timeout, check=False,
            )
            return {
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
            }
        except Exception as exc:
            return {"returncode": -1, "stdout": "", "stderr": str(exc)}

    def clipboard_get(self) -> str:
        try:
            import pyperclip  # type: ignore
            return pyperclip.paste()
        except Exception:
            return ""

    def clipboard_set(self, text: str) -> bool:
        try:
            import pyperclip  # type: ignore
            pyperclip.copy(text)
            return True
        except Exception:
            return False

    def screenshot_tool_available(self) -> bool:
        return shutil.which("python") is not None or True

    def notify(self, title: str, message: str) -> None:
        try:
            if self.is_macos:
                subprocess.Popen(["osascript", "-e",
                                 f'display notification "{message}" with title "{title}"'])
            elif self.is_linux:
                subprocess.Popen(["notify-send", title, message])
            else:
                logger.info("Notification: %s - %s", title, message)
        except Exception as exc:
            logger.debug("notify failed: %s", exc)
