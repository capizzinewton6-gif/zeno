"""
actions - music_player
=======================
Play local music.

Independent actions module for the Autonomous Computer AI Assistant.
Implements the standard execute(task, context) capability contract.
"""

import random
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, Optional

from core.capability import Capability


class MusicPlayer(Capability):
    """Play local music."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.name = "music_player"
        self.description = "Play local music."
        self._player = None

    def execute(self, task: str, context: Optional[Dict[str, Any]] = None) -> Any:
        low = task.lower()
        if low.startswith(("stop music", "pause music", "stop")):
            return self._stop()
        target = self._extract_target(task)
        files = self._find_files(target)
        if not files:
            return self.error(f"No audio files found for: {target}")
        track = random.choice(files) if target in ("", ".", "music") else files[0]
        return self._play(track)

    def _extract_target(self, task: str) -> str:
        task = task.strip()
        for prefix in ("play music", "play"):
            if task.lower().startswith(prefix):
                task = task[len(prefix):].strip()
        return task.strip("\"\'")

    def _find_files(self, target: str):
        exts = {".mp3", ".wav", ".ogg", ".flac", ".m4a"}
        search = Path(target) if target else Path(".")
        if search.is_file() and search.suffix.lower() in exts:
            return [search]
        if search.is_dir():
            return [p for p in search.rglob("*") if p.suffix.lower() in exts][:50]
        # Search current directory recursively.
        return [p for p in Path(".").rglob(target or "*") if p.suffix.lower() in exts][:50]

    def _play(self, track: Path) -> Any:
        try:
            if sys.platform == "darwin":
                self._player = subprocess.Popen(["afplay", str(track)])
            elif sys.platform.startswith("linux"):
                import shutil
                player = shutil.which("mpv") or shutil.which("cvlc") or shutil.which("aplay")
                if not player:
                    return self.error("No audio player found (install mpv/vlc/alsa-utils).")
                self._player = subprocess.Popen([player, str(track)])
            else:
                return self.error(f"Unsupported platform for playback: {sys.platform}")
            return self.ok(f"Playing: {track.name}", path=str(track))
        except Exception as exc:
            return self.error(str(exc))

    def _stop(self) -> Any:
        if self._player and self._player.poll() is None:
            self._player.terminate()
            return self.ok("Music stopped.")
        return self.ok("Nothing is playing.")

    def get_name(self) -> str:
        return self.name

    def get_description(self) -> str:
        return self.description
