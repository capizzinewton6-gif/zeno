"""Live filesystem event listener for real-time changes."""
from __future__ import annotations

import threading
import time
from collections import deque
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

try:  # pragma: no cover - optional
    from watchdog.events import FileSystemEvent, FileSystemEventHandler  # type: ignore
    from watchdog.observers import Observer  # type: ignore
    _WD = True
except Exception:  # pragma: no cover
    _WD = False


@dataclass
class FileEvent:
    type: str  # created, modified, deleted, moved
    path: str
    timestamp: float = field(default_factory=time.time)


class WorkspaceWatcher:
    """Polls or watches the filesystem for changes."""

    def __init__(self, workspace: str = ".") -> None:
        self.workspace = workspace
        self._events: deque[FileEvent] = deque(maxlen=1000)
        self._callbacks: list[Callable[[FileEvent], None]] = []
        self._observer: Any = None
        self._poll_state: dict[str, float] = {}
        self._polling = False

    def on_event(self, callback: Callable[[FileEvent], None]) -> None:
        self._callbacks.append(callback)

    def start(self) -> None:
        if _WD:
            self._start_watchdog()
        else:
            self._polling = True
            threading.Thread(target=self._poll_loop, daemon=True).start()

    def stop(self) -> None:
        if self._observer:
            self._observer.stop()
            self._observer.join()
        self._polling = False

    def events(self) -> list[FileEvent]:
        return list(self._events)

    def _start_watchdog(self) -> None:  # pragma: no cover
        watcher = self

        class Handler(FileSystemEventHandler):
            def on_any_event(self, event: FileSystemEvent) -> None:
                fe = FileEvent(type=event.event_type, path=event.src_path)
                watcher._emit(fe)

        self._observer = Observer()
        self._observer.schedule(Handler(), self.workspace, recursive=True)
        self._observer.start()

    def _poll_loop(self) -> None:
        self._poll_state = self._snapshot()
        while self._polling:
            time.sleep(1.0)
            current = self._snapshot()
            for path, mtime in current.items():
                if path not in self._poll_state:
                    self._emit(FileEvent(type="created", path=path))
                elif self._poll_state[path] != mtime:
                    self._emit(FileEvent(type="modified", path=path))
            for path in self._poll_state:
                if path not in current:
                    self._emit(FileEvent(type="deleted", path=path))
            self._poll_state = current

    def _snapshot(self) -> dict[str, float]:
        snap: dict[str, float] = {}
        for dirpath, _, filenames in __import__("os").walk(self.workspace):
            for f in filenames:
                p = Path(dirpath) / f
                try:
                    snap[str(p)] = p.stat().st_mtime
                except OSError:
                    continue
        return snap

    def _emit(self, event: FileEvent) -> None:
        self._events.append(event)
        for cb in self._callbacks:
            try:
                cb(event)
            except Exception:
                continue
