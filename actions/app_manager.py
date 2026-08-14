"""
actions - app_manager
======================
Open, close, install and uninstall apps.

Independent actions module for the Autonomous Computer AI Assistant.
Implements the standard execute(task, context) capability contract.
"""

import shutil
import subprocess
import sys
from typing import Any, Dict, Optional

from core.capability import Capability


class AppManager(Capability):
    """Open, close, install and uninstall apps."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.name = "app_manager"
        self.description = "Open, close, install and uninstall apps."

    def execute(self, task: str, context: Optional[Dict[str, Any]] = None) -> Any:
        low = task.lower()
        if low.startswith("close "):
            return self._close(task[6:].strip())
        if low.startswith("install "):
            return self._install(task[8:].strip())
        if low.startswith("uninstall "):
            return self._uninstall(task[10:].strip())
        if low.startswith(("open ", "launch ", "start ")):
            app = task.split(maxsplit=1)[1].strip() if len(task.split()) > 1 else ""
            return self._open(app)
        return self.error(f"Unrecognised app task: {task}")

    def _open(self, app: str) -> Any:
        if not app:
            return self.error("Specify an application name.")
        # Try common launchers across platforms.
        candidates = [app]
        if sys.platform.startswith("linux"):
            candidates.append(app.lower())
        for name in candidates:
            if shutil.which(name):
                try:
                    subprocess.Popen([name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    return self.ok(f"Launched {name}.")
                except Exception as exc:
                    return self.error(str(exc))
        try:
            if sys.platform.startswith("win"):
                subprocess.Popen(["start", "", app], shell=True)
            elif sys.platform == "darwin":
                subprocess.Popen(["open", "-a", app])
            else:
                subprocess.Popen([app], shell=True)
            return self.ok(f"Launched {app}.")
        except Exception as exc:
            return self.error(f"Could not launch {app}: {exc}")

    def _close(self, app: str) -> Any:
        if not app:
            return self.error("Specify an application name.")
        try:
            if sys.platform.startswith("win"):
                subprocess.run(["taskkill", "/IM", app, "/F"], capture_output=True, text=True)
            elif sys.platform == "darwin":
                subprocess.run(["osascript", "-e", f'quit app "{app}"'], capture_output=True, text=True)
            else:
                subprocess.run(["pkill", "-f", app], capture_output=True, text=True)
            return self.ok(f"Closed {app}.")
        except Exception as exc:
            return self.error(str(exc))

    def _install(self, package: str) -> Any:
        if not package:
            return self.error("Specify a package name.")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            return self.ok(f"Installed {package}.")
        except subprocess.CalledProcessError as exc:
            return self.error(f"Install failed: {exc}")

    def _uninstall(self, package: str) -> Any:
        if not package:
            return self.error("Specify a package name.")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "uninstall", "-y", package])
            return self.ok(f"Uninstalled {package}.")
        except subprocess.CalledProcessError as exc:
            return self.error(f"Uninstall failed: {exc}")

    def get_name(self) -> str:
        return self.name

    def get_description(self) -> str:
        return self.description
