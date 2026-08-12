"""Open and control applications."""

from __future__ import annotations

import logging
import subprocess
from typing import Dict, List

from integrations.operating_system import OperatingSystem

logger = logging.getLogger(__name__)


class ApplicationControl:
    """Launch, focus, and close desktop applications."""

    def __init__(self) -> None:
        self.os = OperatingSystem()

    # ------------------------------------------------------------------ launch
    def launch(self, app_name: str) -> bool:
        try:
            if self.os.is_windows:
                subprocess.Popen(["cmd", "/c", "start", "", app_name])
            elif self.os.is_macos:
                subprocess.Popen(["open", "-a", app_name])
            else:
                subprocess.Popen([app_name])
            logger.info("Launched application: %s", app_name)
            return True
        except Exception as exc:
            logger.warning("Failed to launch %s: %s", app_name, exc)
            return False

    def launch_via_path(self, path: str) -> bool:
        try:
            subprocess.Popen([path])
            return True
        except Exception as exc:
            logger.warning("Failed to launch via path %s: %s", path, exc)
            return False

    # ------------------------------------------------------------------ focus
    def focus(self, app_name: str) -> bool:
        try:
            if self.os.is_windows:
                subprocess.Popen(["cmd", "/c", "start", "", app_name])
            elif self.os.is_macos:
                subprocess.Popen(["open", "-a", app_name])
            else:
                subprocess.Popen(["wmctrl", "-a", app_name])
            return True
        except Exception as exc:
            logger.warning("Failed to focus %s: %s", app_name, exc)
            return False

    # ------------------------------------------------------------------ close
    def close(self, app_name: str, force: bool = False) -> bool:
        try:
            if self.os.is_windows:
                cmd = ["taskkill", "/IM", app_name]
                if force:
                    cmd.append("/F")
                subprocess.run(cmd, check=False)
            elif self.os.is_macos:
                script = f'quit app "{app_name}"'
                subprocess.Popen(["osascript", "-e", script])
            else:
                cmd = ["killall"]
                if force:
                    cmd.append("-9")
                cmd.append(app_name)
                subprocess.run(cmd, check=False)
            logger.info("Closed application: %s", app_name)
            return True
        except Exception as exc:
            logger.warning("Failed to close %s: %s", app_name, exc)
            return False

    def list_running(self) -> List[Dict[str, str]]:
        from recognition.window_detector import WindowDetector
        return WindowDetector().list_windows()

    def is_running(self, app_name: str) -> bool:
        low = app_name.lower()
        return any(low in str(w.get("title", "")).lower() for w in self.list_running())
