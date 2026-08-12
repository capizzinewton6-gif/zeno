"""Gemini 1.5 Flash engine - fast frame processing and lightweight analysis.

Responsible for: fast frame processing, image preprocessing, OCR preprocessing,
metadata extraction, lightweight visual analysis, feature extraction, validation
tasks, context preparation, and supporting real-time workflows.
"""

from __future__ import annotations

import base64
import os
from typing import Any, Dict, List, Optional, Sequence

MODEL_NAME = "gemini-1.5-flash"

try:
    from google import genai  # type: ignore
    _GENAI_AVAILABLE = True
except Exception:  # pragma: no cover
    _GENAI_AVAILABLE = False

try:
    import google.generativeai as genai_legacy  # type: ignore
    _LEGACY_AVAILABLE = True
except Exception:  # pragma: no cover
    _LEGACY_AVAILABLE = False


class Gemini15FlashEngine:
    """Wrapper around Gemini 1.5 Flash for fast, lightweight visual tasks."""

    model_name = MODEL_NAME

    def __init__(self, api_key: Optional[str] = None) -> None:
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        self._client = None
        self._model = None
        self._configure()

    def _configure(self) -> None:
        if not self.api_key:
            return
        if _GENAI_AVAILABLE:
            try:
                self._client = genai.Client(api_key=self.api_key)
                self._model = self._client.models
            except Exception:
                self._client = None
        if not self._client and _LEGACY_AVAILABLE:
            try:
                genai_legacy.configure(api_key=self.api_key)
                self._model = genai_legacy.GenerativeModel(MODEL_NAME)
            except Exception:
                self._model = None

    @property
    def is_available(self) -> bool:
        return bool(self.api_key and (_GENAI_AVAILABLE or _LEGACY_AVAILABLE))

    @staticmethod
    def _encode_image(image_bytes: bytes) -> Dict[str, Any]:
        return {"mime_type": "image/jpeg", "data": base64.b64encode(image_bytes).decode("ascii")}

    def _build_parts(self, text: str, images: Sequence[bytes]) -> List[Any]:
        parts: List[Any] = [text]
        for img in images:
            parts.append(self._encode_image(img))
        return parts

    def fast_analyze(self, prompt: str, images: Sequence[bytes] = ()) -> Any:
        """Lightweight visual analysis used in real-time loops."""
        if not self.is_available:
            return {"error": "offline", "engine": MODEL_NAME,
                    "message": f"[{MODEL_NAME} offline] {prompt[:120]}"}
        parts = self._build_parts(prompt, images)
        try:
            if _GENAI_AVAILABLE and self._client is not None:
                resp = self._model.generate_content(model=MODEL_NAME, contents=parts)
            else:
                resp = self._model.generate_content(parts)
            return getattr(resp, "text", str(resp))
        except Exception as exc:  # pragma: no cover
            return {"error": str(exc), "engine": MODEL_NAME}

    def extract_text(self, image_bytes: bytes) -> str:
        """OCR preprocessing: extract raw text from a frame."""
        out = self.fast_analyze("Extract all visible text from this image. Return plain text only.",
                                [image_bytes])
        if isinstance(out, str):
            return out
        # Offline / error response: no text available.
        return ""

    def extract_metadata(self, image_bytes: bytes) -> str:
        """Extract lightweight metadata (dimensions hint, dominant content)."""
        out = self.fast_analyze(
            "Describe this image's dominant content and lighting in one sentence.", [image_bytes])
        return out if isinstance(out, str) else str(out)

    def validate_detection(self, image_bytes: bytes, claimed_label: str) -> bool:
        """Validate a claimed detection is plausible in the frame."""
        out = self.fast_analyze(
            f"Is a '{claimed_label}' plausibly present in this image? Answer yes or no only.",
            [image_bytes])
        text = out if isinstance(out, str) else str(out)
        return text.strip().lower().startswith("y")

    def prepare_context(self, image_bytes: bytes) -> str:
        """Produce a compact context summary for the reasoning engine."""
        return self.extract_metadata(image_bytes)
