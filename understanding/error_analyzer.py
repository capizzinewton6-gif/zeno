"""Detect error messages on screen."""

from __future__ import annotations

import json
import logging
import re
from typing import Any, Dict, Optional

from ai_core.ai_engine import get_engine

logger = logging.getLogger(__name__)

_ERROR_PATTERNS = re.compile(
    r"\b(error|failed|failure|exception|warning|cannot|could not|invalid|"
    r"unauthorized|denied|not found|crash|timeout|unavailable)\b",
    re.IGNORECASE,
)


class ErrorAnalyzer:
    """Detects and classifies error messages on screen."""

    def __init__(self, engine=None) -> None:
        self.engine = engine or get_engine()

    def detect(self, image: Any, ocr_text: Optional[str] = None) -> Dict[str, Any]:
        text = ocr_text or self._ocr(image)
        if not _ERROR_PATTERNS.search(text or ""):
            return {"has_error": False, "severity": "none", "message": None}

        raw = self.engine.reason(
            "Analyze this screen for error messages. Return JSON with 'has_error' (bool), "
            "'severity' (info/warning/error/critical), 'message', 'source', and 'suggested_fix'. "
            f"OCR text: {text[:1000]}\nRespond with ONLY JSON.",
            image,
        )
        data = self._safe_json(raw)
        data.setdefault("has_error", True)
        return data

    def classify(self, image: Any) -> str:
        return self.detect(image).get("severity", "unknown")

    def suggest_fix(self, image: Any) -> Optional[str]:
        return self.detect(image).get("suggested_fix")

    def _ocr(self, image: Any) -> str:
        try:
            from ai_models.ocr_model import OCRModel
            return OCRModel().read_text(image)
        except Exception as exc:
            logger.debug("OCR failed in ErrorAnalyzer: %s", exc)
            return ""

    @staticmethod
    def _safe_json(raw: str) -> Dict[str, Any]:
        try:
            text = raw.strip()
            if text.startswith("```"):
                text = text.split("```")[1]
                if text.lower().startswith("json"):
                    text = text[4:]
            data = json.loads(text)
            return data if isinstance(data, dict) else {"raw": data}
        except Exception:
            return {"raw": raw}
