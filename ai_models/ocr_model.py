"""Text recognition model combining local OCR with Gemini."""

from __future__ import annotations

import io
import json
import logging
from typing import Any, Dict, List, Optional

from ai_core.ai_engine import get_engine

logger = logging.getLogger(__name__)


class OCRModel:
    """Reads text from screen images.

    Uses pytesseract locally when available; falls back to Gemini 1.5 Flash
    for transcription and structured extraction.
    """

    def __init__(self, engine=None) -> None:
        self.engine = engine or get_engine()
        self._tesseract = self._load_tesseract()

    @staticmethod
    def _load_tesseract():
        try:
            import pytesseract  # type: ignore
            from PIL import Image  # type: ignore  # noqa: F401
            return pytesseract
        except Exception:
            logger.info("pytesseract not available; will rely on Gemini for OCR.")
            return None

    def read_text(self, image: Any) -> str:
        if self._tesseract is not None:
            try:
                from PIL import Image  # type: ignore
                if isinstance(image, str):
                    img = Image.open(image)
                elif isinstance(image, (bytes, bytearray)):
                    img = Image.open(io.BytesIO(image))
                else:
                    img = image
                return self._tesseract.image_to_string(img)
            except Exception as exc:
                logger.debug("Local OCR failed (%s); falling back to Gemini.", exc)
        return self.engine.analyze_fast(
            "Transcribe ALL visible text on this screen exactly as it appears.",
            image,
        )

    def extract_structured(self, image: Any) -> Dict[str, Any]:
        raw = self.engine.analyze_fast(
            "Extract text from this screen as JSON: {\"blocks\": [{\"text\", \"bbox\": "
            "[x,y,w,h], \"type\"}]}. Respond with ONLY JSON.",
            image,
        )
        try:
            text = raw.strip()
            if text.startswith("```"):
                text = text.split("```")[1]
                if text.lower().startswith("json"):
                    text = text[4:]
            data = json.loads(text)
            return data if isinstance(data, dict) else {"blocks": data}
        except Exception:
            return {"raw": raw}

    def find_text(self, image: Any, query: str) -> Optional[Dict[str, Any]]:
        blocks = self.extract_structured(image).get("blocks", [])
        low = query.lower()
        for block in blocks:
            if low in str(block.get("text", "")).lower():
                return block
        return None
