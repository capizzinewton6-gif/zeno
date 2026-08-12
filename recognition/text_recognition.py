"""Read text from screen (OCR)."""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from ai_models.ocr_model import OCRModel

logger = logging.getLogger(__name__)


class TextRecognition:
    """High-level text recognition facade over the OCR model."""

    def __init__(self, ocr_model: OCRModel | None = None) -> None:
        self.ocr_model = ocr_model or OCRModel()

    def read_all(self, image: Any) -> str:
        return self.ocr_model.read_text(image)

    def read_region(self, image: Any, region: tuple[int, int, int, int]) -> str:
        try:
            from PIL import Image  # type: ignore
            import io
            if isinstance(image, str):
                img = Image.open(image)
            elif isinstance(image, (bytes, bytearray)):
                img = Image.open(io.BytesIO(image))
            else:
                img = image
            x, y, w, h = region
            cropped = img.crop((x, y, x + w, y + h))
            return self.ocr_model.read_text(cropped)
        except Exception as exc:
            logger.warning("read_region failed: %s", exc)
            return self.ocr_model.read_text(image)

    def find_text(self, image: Any, query: str) -> Optional[Dict[str, Any]]:
        return self.ocr_model.find_text(image, query)

    def extract_blocks(self, image: Any) -> List[Dict[str, Any]]:
        data = self.ocr_model.extract_structured(image)
        if isinstance(data, dict):
            return data.get("blocks", [])
        return data if isinstance(data, list) else []
