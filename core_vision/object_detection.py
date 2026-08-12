"""Real-time object detection engine.

Primary backend: local YOLO (ultralytics) when available.
Fallback: Gemini 2.5 Flash vision describing labeled detections.
This keeps the capability functional on machines without heavy CV stacks.
"""

from __future__ import annotations

import json
from typing import List, Optional

import numpy as np

from core_vision.frame_preprocessor import FramePreprocessor
from modeling.two_d_boxes import Detection
from modeling.parameters import Parameters


class ObjectDetector:
    def __init__(self, model_name: str = "yolov8n.pt", parameters: Parameters = Parameters(),
                 flash25=None) -> None:
        self.model_name = model_name
        self.parameters = parameters
        self.pre = FramePreprocessor(input_size=parameters.input_size, normalize=False)
        self._model = None
        self._flash25 = flash25

    def _load_yolo(self):
        if self._model is not None:
            return
        try:
            from ultralytics import YOLO  # type: ignore
            self._model = YOLO(self.model_name)
        except Exception:
            self._model = None

    def detect(self, image: np.ndarray) -> List[Detection]:
        """Run detection. Returns a list of Detection."""
        self._load_yolo()
        if self._model is not None:
            return self._detect_yolo(image)
        return self._detect_gemini(image)

    def _detect_yolo(self, image: np.ndarray) -> List[Detection]:
        results = self._model(image, verbose=False)
        out: List[Detection] = []
        for r in results:
            names = r.names
            boxes = r.boxes
            for b in boxes:
                xyxy = b.xyxy[0].tolist()
                conf = float(b.conf[0])
                cls = int(b.cls[0])
                label = names.get(cls, str(cls))
                out.append(Detection.from_xyxy(label, conf, xyxy, source="yolo"))
        return out

    def _detect_gemini(self, image: np.ndarray) -> List[Detection]:
        if self._flash25 is None:
            from src.gemini_25_flash_engine import Gemini25FlashEngine
            self._flash25 = Gemini25FlashEngine()
        jpeg = self.pre.to_jpeg_bytes(image, self.parameters.jpeg_quality)
        if not jpeg:
            return []
        prompt = ("List every distinct object visible in this image as JSON: "
                  "{\"objects\":[{\"label\":str,\"confidence\":0-1,\"bbox\":[x1,y1,x2,y2]}]}. "
                  "Coordinates are in image pixel space.")
        result = self._flash25.reason(prompt, [jpeg], json_mode=True)
        return self._parse(result, image.shape[:2])

    def _parse(self, result, image_shape) -> List[Detection]:
        if not isinstance(result, dict):
            return []
        objects = result.get("objects", [])
        out: List[Detection] = []
        for obj in objects:
            try:
                bbox = obj["bbox"]
                out.append(Detection.from_xyxy(
                    str(obj.get("label", "object")),
                    float(obj.get("confidence", 0.5)),
                    bbox, source="gemini"))
            except Exception:
                continue
        return out
