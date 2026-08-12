"""Take and manage screenshots."""

from __future__ import annotations

import hashlib
import io
import logging
import os
import sqlite3
import time
from pathlib import Path
from typing import Any, Optional, Tuple

logger = logging.getLogger(__name__)

_BASE_DIR = Path(__file__).resolve().parent.parent
_SHOT_DIR = _BASE_DIR / "memory" / "screenshots"
_SCREENSHOTS_DB = _BASE_DIR / "database" / "screenshots.db"


class ScreenshotManager:
    """Captures, stores, and indexes screenshots."""

    def __init__(self, output_dir: Optional[str] = None, monitor: int = 0,
                 fmt: str = "PNG") -> None:
        self.output_dir = Path(output_dir) if output_dir else _SHOT_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.monitor = monitor
        self.fmt = fmt.upper()

    # ------------------------------------------------------------------ capture
    def capture(self, region: Optional[Tuple[int, int, int, int]] = None) -> Optional[str]:
        """Capture a screenshot and save to disk. Returns the file path."""
        try:
            import mss  # type: ignore
        except Exception as exc:
            logger.error("mss not available: %s", exc)
            return None

        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}_{int(time.time()*1000) % 1000:03d}.{self.fmt.lower()}"
        path = self.output_dir / filename

        with mss.mss() as sct:
            monitors = sct.monitors
            target = {"top": 0, "left": 0, "width": 1, "height": 1}
            if region:
                left, top, width, height = region
                target = {"top": top, "left": left, "width": width, "height": height}
            elif len(monitors) > self.monitor + 1:
                target = monitors[self.monitor + 1]
            elif monitors:
                target = monitors[0]

            shot = sct.grab(target)
            try:
                from mss.tools import to_png  # type: ignore
                if self.fmt == "PNG":
                    to_png(shot.rgb, shot.size, output=str(path))
                else:
                    to_png(shot.rgb, shot.size, output=str(path))
            except Exception:
                # Fallback via Pillow
                from PIL import Image  # type: ignore
                import numpy as np  # type: ignore
                img = Image.frombytes("RGB", shot.size, shot.bgra, "raw", "BGRX")
                img.save(path, format=self.fmt)

        width = target.get("width", 0)
        height = target.get("height", 0)
        self._record(path, width, height)
        logger.info("Screenshot saved: %s", path)
        return str(path)

    # ------------------------------------------------------------------ storage
    def _record(self, path: Path, width: int, height: int) -> None:
        try:
            file_hash = self._hash_file(path)
            conn = sqlite3.connect(str(_SCREENSHOTS_DB))
            conn.execute(
                "INSERT INTO screenshots (timestamp, path, monitor, width, height, hash, metadata) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (time.strftime("%Y-%m-%dT%H:%M:%S"), str(path), self.monitor,
                 width, height, file_hash, "{}"),
            )
            conn.commit()
            conn.close()
        except Exception as exc:
            logger.warning("Failed to record screenshot metadata: %s", exc)

    @staticmethod
    def _hash_file(path: Path) -> str:
        h = hashlib.md5()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()

    def list_screenshots(self, limit: int = 50) -> list:
        try:
            conn = sqlite3.connect(str(_SCREENSHOTS_DB))
            cur = conn.execute(
                "SELECT id, timestamp, path, width, height FROM screenshots "
                "ORDER BY id DESC LIMIT ?", (limit,)
            )
            rows = cur.fetchall()
            conn.close()
            return rows
        except Exception as exc:
            logger.warning("Failed to list screenshots: %s", exc)
            return []

    def cleanup_old(self, max_age_days: int = 7) -> int:
        cutoff = time.time() - max_age_days * 86400
        removed = 0
        for f in self.output_dir.glob("*"):
            try:
                if f.stat().st_mtime < cutoff:
                    f.unlink()
                    removed += 1
            except Exception:
                pass
        return removed
