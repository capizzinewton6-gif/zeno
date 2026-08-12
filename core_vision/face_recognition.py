"""Face recognition: embedding extractor (ArcFace / Facenet / InsightFace / dlib)."""

from __future__ import annotations

from typing import List, Optional

import numpy as np

from core_vision.face_detection import FaceDetector
from core_vision.frame_preprocessor import FramePreprocessor
from facial_processing.face_aligner import FaceAligner
from facial_processing.embedding_generator import EmbeddingGenerator
from facial_processing.gallery_manager import GalleryManager
from modeling.two_d_boxes import BBox, Detection


class FaceRecognizer:
    """Detect, align, embed, and match faces against a gallery."""

    def __init__(self, detector: Optional[FaceDetector] = None,
                 aligner: Optional[FaceAligner] = None,
                 embedder: Optional[EmbeddingGenerator] = None,
                 gallery: Optional[GalleryManager] = None,
                 threshold: float = 0.55) -> None:
        self.detector = detector or FaceDetector()
        self.aligner = aligner or FaceAligner()
        self.embedder = embedder or EmbeddingGenerator()
        self.gallery = gallery or GalleryManager()
        self.threshold = threshold
        self.pre = FramePreprocessor()

    def recognize(self, image: np.ndarray) -> List[Detection]:
        boxes = self.detector.detect(image)
        out: List[Detection] = []
        for box in boxes:
            face = self._crop(image, box)
            aligned = self.aligner.align(face)
            emb = self.embedder.generate(aligned)
            identity, score = self.gallery.match(emb, self.threshold)
            out.append(Detection(
                label="face", confidence=float(score),
                bbox=box, identity=identity,
                embedding=emb.tolist() if hasattr(emb, "tolist") else list(emb),
                source="face_recognizer",
            ))
        return out

    @staticmethod
    def _crop(image: np.ndarray, box: BBox) -> np.ndarray:
        h, w = image.shape[:2]
        x1, y1, x2, y2 = box.to_int_tuple()
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(w, x2), min(h, y2)
        return image[y1:y2, x1:x2]
