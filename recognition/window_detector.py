"""Detect open applications and windows."""

from __future__ import annotations

import logging
import platform
import subprocess
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class WindowDetector:
    """Detects open applications and their window titles."""

    def list_windows(self) -> List[Dict[str, Any]]:
        system = platform.system().lower()
        try:
            if system == "windows":
                return self._list_windows_windows()
            elif system == "darwin":
                return self._list_windows_macos()
            else:
                return self._list_windows_linux()
        except Exception as exc:
            logger.warning("Window listing failed on %s: %s", system, exc)
            return self._list_windows_psutil()

    def active_window(self) -> Dict[str, Any] | None:
        system = platform.system().lower()
        try:
            if system == "windows":
                return self._active_windows()
            elif system == "darwin":
                return self._active_macos()
            else:
                return self._active_linux()
        except Exception as exc:
            logger.debug("active_window failed: %s", exc)
            return None

    # ------------------------------------------------------------------ platform
    def _list_windows_windows(self) -> List[Dict[str, Any]]:
        try:
            import ctypes
            from collections import OrderedDict
            user32 = ctypes.windll.user32  # type: ignore[attr-defined]
            results = []
            titles = OrderedDict()

            EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_int, ctypes.c_int)

            def _enum(hwnd, _):
                length = user32.GetWindowTextLengthW(hwnd)
                if length > 0 and user32.IsWindowVisible(hwnd):
                    buf = ctypes.create_unicode_buffer(length + 1)
                    user32.GetWindowTextW(hwnd, buf, length + 1)
                    titles[hwnd] = buf.value
                return True

            user32.EnumWindows(EnumWindowsProc(_enum), 0)
            for hwnd, title in titles.items():
                results.append({"hwnd": hwnd, "title": title, "platform": "windows"})
            return results
        except Exception as exc:
            logger.debug("Windows enum failed: %s", exc)
            return self._list_windows_psutil()

    def _list_windows_macos(self) -> List[Dict[str, Any]]:
        try:
            out = subprocess.check_output(
                ["osascript", "-e",
                 'tell application "System Events" to get name of every process '
                 'whose background only is false'],
                stderr=subprocess.DEVNULL, timeout=5,
            ).decode().strip()
            return [{"title": name.strip(), "platform": "macos"} for name in out.split(",") if name.strip()]
        except Exception:
            return self._list_windows_psutil()

    def _list_windows_linux(self) -> List[Dict[str, Any]]:
        for tool in (["wmctrl", "-l"], ["xdotool", "search", "--name", ""]):
            try:
                out = subprocess.check_output(tool, stderr=subprocess.DEVNULL, timeout=5).decode()
                results = []
                for line in out.splitlines():
                    if line.strip():
                        parts = line.split(None, 3)
                        results.append({"title": parts[-1] if len(parts) > 2 else line, "platform": "linux"})
                if results:
                    return results
            except Exception:
                continue
        return self._list_windows_psutil()

    def _list_windows_psutil(self) -> List[Dict[str, Any]]:
        try:
            import psutil  # type: ignore
            seen = set()
            results = []
            for proc in psutil.process_iter(attrs=["pid", "name", "username"]):
                name = proc.info.get("name", "")
                if name and name not in seen:
                    seen.add(name)
                    results.append({"title": name, "pid": proc.info.get("pid"), "platform": "psutil"})
            return results
        except Exception:
            return []

    def _active_windows(self) -> Dict[str, Any] | None:
        try:
            import ctypes
            user32 = ctypes.windll.user32  # type: ignore[attr-defined]
            hwnd = user32.GetForegroundWindow()
            length = user32.GetWindowTextLengthW(hwnd)
            buf = ctypes.create_unicode_buffer(length + 1)
            user32.GetWindowTextW(hwnd, buf, length + 1)
            return {"hwnd": hwnd, "title": buf.value, "platform": "windows"}
        except Exception:
            return None

    def _active_macos(self) -> Dict[str, Any] | None:
        try:
            out = subprocess.check_output(
                ["osascript", "-e",
                 'tell application "System Events" to get name of first process whose frontmost is true'],
                stderr=subprocess.DEVNULL, timeout=5,
            ).decode().strip()
            return {"title": out, "platform": "macos"}
        except Exception:
            return None

    def _active_linux(self) -> Dict[str, Any] | None:
        try:
            out = subprocess.check_output(
                ["xdotool", "getactivewindow", "getwindowname"],
                stderr=subprocess.DEVNULL, timeout=5,
            ).decode().strip()
            return {"title": out, "platform": "linux"}
        except Exception:
            return None
