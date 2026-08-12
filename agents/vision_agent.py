"""Core perception orchestrator (Vision Agent).

Wires the AI engine (brain) to capability modules (hands). Produces a unified
perception result per frame that the UI / main loop can render or act on.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

import numpy as np

from ai_core.ai_engine import AIEngine, Decision
from agents.face_recognizer_agent import FaceRecognizerAgent, FaceResult
from agents.object_detector_agent import ObjectDetectorAgent, DetectionResult
from agents.optimization_agent import OptimizationAgent
from agents.project_agent import ProjectAgent
from agents.research_agent import ResearchAgent
from agents.tracking_agent import TrackingAgent, TrackingResult
from core_vision.camera_stream import Frame
from core_vision.spatial_estimation import SpatialEstimator
from tracking_analytics.event_trigger import Alert, EventTrigger
from tracking_analytics.heatmapping import Heatmapper
from vision_input.image_ocr import ImageOCR
from vision_input.scene_classifier import SceneClassifier


@dataclass
class PerceptionResult:
    frame_index: int
    timestamp: float
    detections: DetectionResult
    faces: FaceResult
    tracks: TrackingResult
    scene: str
    ocr_text: str
    alerts: List[Alert]
    decision: Optional[Decision] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class VisionAgent:
    """Top-level autonomous perception orchestrator."""

    def __init__(self, ai_engine: Optional[AIEngine] = None,
                 detector: Optional[ObjectDetectorAgent] = None,
                 face_agent: Optional[FaceRecognizerAgent] = None,
                 tracking: Optional[TrackingAgent] = None,
                 optimization: Optional[OptimizationAgent] = None,
                 project: Optional[ProjectAgent] = None,
                 research: Optional[ResearchAgent] = None,
                 scene: Optional[SceneClassifier] = None,
                 ocr: Optional[ImageOCR] = None,
                 spatial: Optional[SpatialEstimator] = None,
                 events: Optional[EventTrigger] = None,
                 heatmap: Optional[Heatmapper] = None) -> None:
        self.ai = ai_engine or AIEngine()
        self.detector = detector or ObjectDetectorAgent()
        self.face_agent = face_agent or FaceRecognizerAgent()
        self.tracking = tracking or TrackingAgent()
        self.optimization = optimization or OptimizationAgent()
        self.project = project or ProjectAgent()
        self.research = research or ResearchAgent()
        self.scene = scene or SceneClassifier()
        self.ocr = ocr or ImageOCR()
        self.spatial = spatial or SpatialEstimator()
        self.events = events or EventTrigger()
        self.heatmap = heatmap or Heatmapper()

    def perceive(self, frame: Frame, instruction: str = "") -> PerceptionResult:
        image = frame.image
        t0 = frame.timestamp

        det = self.detector.run(image, frame_index=frame.index, timestamp=t0)
        faces = self.face_agent.run(image, frame_index=frame.index, timestamp=t0)
        tracks = self.tracking.run(det.detections.items + faces.detections.items,
                                   frame_index=frame.index)
        scene_info = self.scene.classify(image)
        ocr_text = self.ocr.extract(image).text
        alerts = self.events.evaluate_detections(
            det.detections.items + faces.detections.items,
            unknown_face_ids={d.identity for d in faces.detections.items
                              if d.label == "face" and not d.identity} or None)
        self.heatmap.add_tracks(tracks.tracks)

        decision = None
        if instruction:
            decision = self.ai.decide(instruction)

        result = PerceptionResult(
            frame_index=frame.index, timestamp=t0,
            detections=det, faces=faces, tracks=tracks,
            scene=scene_info.scene_type, ocr_text=ocr_text,
            alerts=alerts, decision=decision,
            metadata={"lighting": scene_info.lighting,
                      "time_of_day": scene_info.time_of_day})
        self.project.log("perceive", {"frame": frame.index,
                                      "detections": len(det.detections.items),
                                      "alerts": len(alerts)})
        return result

    def analyze_static(self, image: np.ndarray, instruction: str = "") -> Dict[str, Any]:
        """Analyze a single image / screenshot without the live pipeline."""
        det = self.detector.run(image)
        faces = self.face_agent.run(image)
        scene_info = self.scene.classify(image)
        ocr_text = self.ocr.extract(image).text
        decision = self.ai.decide(instruction) if instruction else None
        return {
            "detections": [d.to_dict() for d in det.detections.items],
            "faces": [{"identity": d.identity, "confidence": d.confidence}
                      for d in faces.detections.items],
            "scene": scene_info.summary,
            "ocr": ocr_text,
            "decision": self.ai.to_report(decision) if decision else None,
        }
