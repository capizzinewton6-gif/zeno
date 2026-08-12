"""Context manager: maintains video scene history and multi-frame context."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from typing import Any, Deque, Dict, List, Optional

from modeling.two_d_boxes import Detections


@dataclass
class FrameContext:
    frame_index: int
    timestamp: float
    detections: List[Dict[str, Any]]
    summary: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


class ContextManager:
    """Keeps a rolling window of frame contexts for temporal reasoning."""

    def __init__(self, window: int = 30) -> None:
        self.window = window
        self._history: Deque[FrameContext] = deque(maxlen=window)
        self._scene_label: str = "unknown"

    def add(self, frame_index: int, timestamp: float, detections: Detections,
            summary: str = "", metadata: Optional[Dict[str, Any]] = None) -> FrameContext:
        ctx = FrameContext(
            frame_index=frame_index, timestamp=timestamp,
            detections=[d.to_dict() for d in detections.items],
            summary=summary, metadata=metadata or {},
        )
        self._history.append(ctx)
        return ctx

    @property
    def history(self) -> List[FrameContext]:
        return list(self._history)

    @property
    def latest(self) -> Optional[FrameContext]:
        return self._history[-1] if self._history else None

    def set_scene_label(self, label: str) -> None:
        self._scene_label = label

    @property
    def scene_label(self) -> str:
        return self._scene_label

    def label_counts(self) -> Dict[str, int]:
        counts: Dict[str, int] = {}
        for ctx in self._history:
            for d in ctx.detections:
                counts[d["label"]] = counts.get(d["label"], 0) + 1
        return counts

    def summarize(self) -> str:
        counts = self.label_counts()
        if not counts:
            return "No detections in recent context."
        top = sorted(counts.items(), key=lambda kv: kv[1], reverse=True)[:5]
        return "; ".join(f"{lbl} x{n}" for lbl, n in top)
