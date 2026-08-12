"""Real-time barcode and QR code decoding from video frames."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

import numpy as np


@dataclass
class CodeResult:
    data: str
    code_type: str
    bbox: list
    confidence: float = 1.0


class BarcodeQRReader:
    """Decode barcodes/QR codes via pyzbar or OpenCV's WeChat QR detector."""

    def __init__(self, backend: str = "auto") -> None:
        self.backend = backend
        self._cv_detector = None

    def read(self, image: np.ndarray) -> List[CodeResult]:
        if self.backend in ("auto", "pyzbar"):
            res = self._pyzbar(image)
            if res:
                return res
        if self.backend in ("auto", "opencv"):
            return self._opencv(image)
        return []

    def _pyzbar(self, image: np.ndarray) -> List[CodeResult]:
        try:
            from pyzbar.pyzbar import decode  # type: ignore
            out: List[CodeResult] = []
            for d in decode(image):
                out.append(CodeResult(
                    data=d.data.decode("utf-8", errors="replace"),
                    code_type=d.type,
                    bbox=[list(p) for p in d.polygon]))
            return out
        except Exception:
            return []

    def _opencv(self, image: np.ndarray) -> List[CodeResult]:
        try:
            import cv2  # type: ignore
            if self._cv_detector is None:
                self._cv_detector = cv2.QRCodeDetector()
            data, points, _ = self._cv_detector.detectAndDecode(image)
            if data:
                bbox = points.reshape(-1, 2).tolist() if points is not None else []
                return [CodeResult(data=data, code_type="qr", bbox=bbox)]
        except Exception:
            pass
        return []
