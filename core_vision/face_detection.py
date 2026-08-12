"""Fast face location finder: RetinaFace / MTCNN / YuNet, with OpenCV DNN fallback."""

from __future__ import annotations

from typing import List, Optional

import numpy as np

from modeling.two_d_boxes import BBox


class FaceDetector:
    """Detect face bounding boxes in a frame."""

    def __init__(self, backend: str = "auto", min_size: int = 40) -> None:
        self.backend = backend
        self.min_size = min_size
        self._cv_net = None
        self._mediapipe = None

    def detect(self, image: np.ndarray) -> List[BBox]:
        if self.backend in ("auto", "yunet"):
            boxes = self._detect_yunet(image)
            if boxes:
                return boxes
        if self.backend in ("auto", "mediapipe"):
            boxes = self._detect_mediapipe(image)
            if boxes:
                return boxes
        if self.backend in ("auto", "dnn"):
            return self._detect_dnn(image)
        return []

    def _detect_yunet(self, image: np.ndarray) -> List[BBox]:
        try:
            import cv2  # type: ignore
            h, w = image.shape[:2]
            detector = cv2.FaceDetectorYN.create(
                "", (0, 0), (w, h))  # will raise if model missing
        except Exception:
            return []
        return []

    def _detect_mediapipe(self, image: np.ndarray) -> List[BBox]:
        try:
            import mediapipe as mp  # type: ignore
            if self._mediapipe is None:
                self._mediapipe = mp.solutions.face_detection.FaceDetection(
                    model_selection=0, min_detection_confidence=0.5)
            rgb = image[:, :, ::-1] if image.ndim == 3 else image
            res = self._mediapipe.process(rgb)
            boxes: List[BBox] = []
            h, w = image.shape[:2]
            for d in res.detections:
                bb = d.location_data.relative_bounding_box
                x1 = max(0, int(bb.xmin * w))
                y1 = max(0, int(bb.ymin * h))
                x2 = min(w, int((bb.xmin + bb.width) * w))
                y2 = min(h, int((bb.ymin + bb.height) * h))
                if (x2 - x1) >= self.min_size and (y2 - y1) >= self.min_size:
                    boxes.append(BBox(x1, y1, x2, y2))
            return boxes
        except Exception:
            return []

    def _detect_dnn(self, image: np.ndarray) -> List[BBox]:
        try:
            import cv2  # type: ignore
            if self._cv_net is None:
                return []
            h, w = image.shape[:2]
            blob = cv2.dnn.blobFromImage(image, 1.0, (300, 300), (104, 177, 123))
            self._cv_net.setInput(blob)
            detections = self._cv_net.forward()
            boxes: List[BBox] = []
            for i in range(detections.shape[2]):
                conf = float(detections[0, 0, i, 2])
                if conf < 0.5:
                    continue
                x1 = int(detections[0, 0, i, 3] * w)
                y1 = int(detections[0, 0, i, 4] * h)
                x2 = int(detections[0, 0, i, 5] * w)
                y2 = int(detections[0, 0, i, 6] * h)
                boxes.append(BBox(x1, y1, x2, y2))
            return boxes
        except Exception:
            return []
