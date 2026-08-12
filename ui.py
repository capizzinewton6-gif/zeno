"""Text-based desktop GUI for the Vision AI assistant.

A lightweight, dependency-free text interface that drives the VisionAgent over a
live (or synthetic) camera stream and over static image analysis. Designed to be
usable in any terminal, including headless/container environments.
"""

from __future__ import annotations

import os
import shlex
import sys
import time
from typing import Optional

from agents.vision_agent import PerceptionResult, VisionAgent
from core_vision.camera_stream import CameraStream
from simulation.synthetic_stream import SyntheticStream
from visualization.alert_popups import AlertPopups
from visualization.dashboard_ui import CameraTelemetry, DashboardUI


HELP_TEXT = """\
Vision AI - text GUI commands:
  help                 Show this help
  stream <source>      Open a camera/RTSP source (default: synthetic)
  webcam <index>       Open a local webcam by index (e.g. 0)
  step [n]             Process n frames from the active stream (default 1)
  run [n]              Continuously process n frames (default 30)
  image <path>         Analyze a static image file
  ask <instruction>    Set the natural-language instruction for the agent
  dashboard            Show multi-camera telemetry
  alerts               Show active alert popups
  report               Generate an analytics report
  export <path>        Export the current session report to <path>
  quit                 Exit
"""


class TextGUI:
    """Command-driven text interface around :class:`VisionAgent`."""

    def __init__(self, vision: Optional[VisionAgent] = None) -> None:
        self.vision = vision or VisionAgent()
        self.stream = None
        self.instruction = ""
        self.dashboard = DashboardUI()
        self.popups = AlertPopups()
        self._frame_count = 0

    # -- command dispatch ------------------------------------------------
    def handle(self, line: str) -> bool:
        parts = shlex.split(line)
        if not parts:
            return True
        cmd = parts[0].lower()
        if cmd in ("quit", "exit", "q"):
            print("Exiting Vision AI.")
            return False
        if cmd == "help":
            print(HELP_TEXT)
        elif cmd == "stream":
            self._open_stream(parts[1] if len(parts) > 1 else None)
        elif cmd == "webcam":
            self._open_webcam(int(parts[1]) if len(parts) > 1 else 0)
        elif cmd == "step":
            self._step(int(parts[1]) if len(parts) > 1 else 1)
        elif cmd == "run":
            self._run(int(parts[1]) if len(parts) > 1 else 30)
        elif cmd == "image":
            self._analyze_image(parts[1] if len(parts) > 1 else "")
        elif cmd == "ask":
            self.instruction = " ".join(parts[1:])
            print(f"Instruction set: {self.instruction}")
        elif cmd == "dashboard":
            print(self.dashboard.render_text())
        elif cmd == "alerts":
            print(self.popups.render_text())
        elif cmd == "report":
            print(self.vision.project.report.text_report())
        elif cmd == "export":
            path = parts[1] if len(parts) > 1 else "reports/session_report.json"
            print("Exported to:", self.vision.project.export_report(path))
        else:
            print(f"Unknown command: {cmd}. Type 'help'.")
        return True

    # -- actions ---------------------------------------------------------
    def _open_stream(self, source: Optional[str]) -> None:
        self._close_stream()
        if source is None:
            self.stream = SyntheticStream()
            print("Opened synthetic stream.")
        else:
            self.stream = CameraStream(source=source)
            print(f"Opening stream: {source} ...")
        if hasattr(self.stream, "open"):
            ok = self.stream.open()
            print("Stream open:", ok)

    def _open_webcam(self, index: int) -> None:
        self._close_stream()
        self.stream = CameraStream(source=index)
        print(f"Opening webcam {index} ...")
        print("Stream open:", self.stream.open())

    def _close_stream(self) -> None:
        if self.stream is not None and hasattr(self.stream, "release"):
            self.stream.release()
        self.stream = None

    def _step(self, n: int) -> None:
        if self.stream is None:
            print("No stream open. Use 'stream' or 'webcam' first.")
            return
        for _ in range(n):
            frame = self.stream.read() if hasattr(self.stream, "read") else next(self.stream, None)
            if frame is None:
                print("Stream ended.")
                break
            self._process_frame(frame)

    def _run(self, n: int) -> None:
        self._step(n)

    def _process_frame(self, frame) -> None:
        t0 = time.perf_counter()
        result = self.vision.perceive(frame, self.instruction)
        latency = (time.perf_counter() - t0) * 1000.0
        self._frame_count += 1
        self.vision.project.report.add(result.detections.detections)
        self.dashboard.update(CameraTelemetry(
            name="cam0", fps=1000.0 / max(latency, 1e-6), latency_ms=latency,
            detections=len(result.detections.detections.items),
            alerts=len(result.alerts), status="ok"))
        for a in result.alerts:
            self.popups.push(a)
        self._render(result, latency)

    def _render(self, result: PerceptionResult, latency_ms: float) -> None:
        print(f"\n[#{result.frame_index}] {latency_ms:.1f}ms  scene={result.scene}")
        dets = result.detections.detections.items
        if dets:
            print("  Detections:")
            for d in dets:
                ident = f" id={d.identity}" if d.identity else ""
                print(f"    - {d.label} ({d.confidence:.2f}){ident}")
        else:
            print("  Detections: none")
        if result.faces.detections.items:
            print(f"  Faces: {len(result.faces.detections.items)} "
                  f"(known={result.faces.known_count}, unknown={result.faces.unknown_count})")
        if result.tracks.tracks:
            print(f"  Tracks: {len(result.tracks.tracks)}")
        if result.ocr_text.strip():
            print(f"  OCR: {result.ocr_text.strip()[:80]}")
        if result.alerts:
            print("  Alerts:")
            for a in result.alerts:
                print(f"    ! [{a.severity}] {a.kind}: {a.message}")
        if result.decision:
            print(f"  Decision: {result.decision.summary[:100]}")

    def _analyze_image(self, path: str) -> None:
        if not path or not os.path.exists(path):
            print("Usage: image <existing-path>")
            return
        try:
            import cv2  # type: ignore
            image = cv2.imread(path)
        except Exception:
            print("Could not read image (OpenCV unavailable).")
            return
        if image is None:
            print("Failed to read image.")
            return
        print(f"Analyzing {path} ...")
        out = self.vision.analyze_static(image, self.instruction)
        print("  Scene:", out["scene"])
        print("  OCR:", out["ocr"][:120])
        print("  Detections:", len(out["detections"]))
        print("  Faces:", len(out["faces"]))
        if out["decision"]:
            print("  Decision:", out["decision"]["summary"][:100])

    # -- main loop -------------------------------------------------------
    def loop(self) -> None:
        print("=== Vision AI - text GUI ===")
        print("Type 'help' for commands. Default stream is synthetic.")
        self._open_stream(None)
        try:
            while True:
                try:
                    line = input("vision> ").strip()
                except (EOFError, KeyboardInterrupt):
                    print()
                    break
                if not self.handle(line):
                    break
        finally:
            self._close_stream()
