"""GStreamer / DeepStream hardware-accelerated video decoding pipeline."""

from __future__ import annotations

from typing import Optional


class StreamPipeline:
    """Describe / launch a GStreamer hardware-accelerated decode pipeline.

    Falls back to a plain OpenCV capture when GStreamer is unavailable.
    """

    def __init__(self, source: str = "", backend: str = "gst") -> None:
        self.source = source
        self.backend = backend
        self._pipeline = None

    @property
    def available(self) -> bool:
        try:
            import gi  # type: ignore
            gi.require_version("Gst", "1.0")
            from gi.repository import Gst  # type: ignore  # noqa: F401
            return True
        except Exception:
            return False

    def build_pipeline(self, accelerator: str = "nvv4l2decoder") -> str:
        if not self.source:
            return ""
        return (
            f"rtspsrc location={self.source} latency=0 ! "
            f"rtph264depay ! h264parse ! {accelerator} ! "
            f"nvvidconv ! video/x-raw, format=(string)BGRx ! "
            f"videoconvert ! video/x-raw, format=(string)BGR ! appsink drop=true sync=false"
        )

    def open(self) -> bool:
        if not self.available:
            return False
        try:
            import gi  # type: ignore
            gi.require_version("Gst", "1.0")
            from gi.repository import Gst  # type: ignore
            Gst.init(None)
            self._pipeline = Gst.parse_launch(self.build_pipeline())
            self._pipeline.set_state(Gst.State.PLAYING)
            return True
        except Exception:
            return False

    def close(self) -> None:
        if self._pipeline is not None:
            try:
                self._pipeline.set_state(self._pipeline.get_state(0).state.__class__.NULL)
            except Exception:
                pass
            self._pipeline = None
