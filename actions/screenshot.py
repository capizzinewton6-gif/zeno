"""
actions - screenshot
=====================
Capture screenshots.

Independent actions module for the Autonomous Computer AI Assistant.
Implements the standard execute(task, context) capability contract.
"""

import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, Optional

from core.capability import Capability


class Screenshot(Capability):
    """Capture screenshots."""

    OUT_DIR = Path(__file__).resolve().parent.parent / "memory" / "screenshots"

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.name = "screenshot"
        self.description = "Capture screenshots."

    def execute(self, task: str, context: Optional[Dict[str, Any]] = None) -> Any:
        self.OUT_DIR.mkdir(parents=True, exist_ok=True)
        fname = f"shot_{time.strftime('%Y%m%d_%H%M%S')}.png"
        out = self.OUT_DIR / fname
        try:
            if sys.platform.startswith("linux"):
                # Try maim, then scrot, then import (ImageMagick).
                import shutil, subprocess
                if shutil.which("maim"):
                    subprocess.run(["maim", str(out)], check=True)
                elif shutil.which("scrot"):
                    subprocess.run(["scrot", str(out)], check=True)
                elif shutil.which("import"):
                    subprocess.run(["import", "-window", "root", str(out)], check=True)
                else:
                    return self.error("No screenshot tool found (install maim/scrot/ImageMagick).")
            elif sys.platform == "darwin":
                subprocess.run(["screencapture", str(out)], check=True)
            elif sys.platform.startswith("win"):
                subprocess.run(["powershell", "-c", f"Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.Screen]::PrimaryScreen"], check=True)
            else:
                return self.error(f"Unsupported platform: {sys.platform}")
            return self.ok(f"Screenshot saved to {out}", path=str(out))
        except Exception as exc:
            return self.error(str(exc))

    def get_name(self) -> str:
        return self.name

    def get_description(self) -> str:
        return self.description
