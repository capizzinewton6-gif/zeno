"""Image OCR: text extraction from video frames (license plates, labels)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

import numpy as np

from core_vision.frame_preprocessor import FramePreprocessor


@dataclass
class OCRResult:
    text: str
    boxes: List[list]
    confidence: float


class ImageOCR:
    """Extract text from frames using EasyOCR/Tesseract, with Gemini 1.5 fallback."""

    def __init__(self, backend: str = "auto", flash15=None) -> None:
        self.backend = backend
        self._reader = None
        self._flash15 = flash15
        self._pre = FramePreprocessor()

    def extract(self, image: np.ndarray) -> OCRResult:
        for fn in (self._easyocr, self._tesseract):
            res = fn(image)
            if res is not None:
                return res
        return self._gemini(image)

    def _easyocr(self, image: np.ndarray) -> Optional[OCRResult]:
        try:
            import easyocr  # type: ignore
            if self._reader is None:
                self._reader = easyocr.Reader(["en"], gpu=False)
            results = self._reader.readtext(image)
            texts, boxes = [], []
            for box, text, conf in results:
                texts.append(text)
                boxes.append([list(p) for p in box])
            return OCRResult(text=" ".join(texts), boxes=boxes,
                             confidence=sum(float(c) for _, _, c in results) / max(len(results), 1))
        except Exception:
            return None

    def _tesseract(self, image: np.ndarray) -> Optional[OCRResult]:
        try:
            import pytesseract  # type: ignore
            text = pytesseract.image_to_string(image)
            data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
            boxes = []
            for i in range(len(data["text"])):
                if data["text"][i].strip():
                    boxes.append([data["left"][i], data["top"][i],
                                  data["left"][i] + data["width"][i],
                                  data["top"][i] + data["height"][i]])
            return OCRResult(text=text, boxes=boxes, confidence=0.7)
        except Exception:
            return None

    def _gemini(self, image: np.ndarray) -> OCRResult:
        if self._flash15 is None:
            from src.gemini_15_flash_engine import Gemini15FlashEngine
            self._flash15 = Gemini15FlashEngine()
        jpeg = self._pre.to_jpeg_bytes(image, 85)
        if not jpeg:
            return OCRResult(text="", boxes=[], confidence=0.0)
        text = self._flash15.extract_text(jpeg)
        return OCRResult(text=text, boxes=[], confidence=0.8)
