"""Gemini 2.5 Flash engine - the advanced reasoning brain.

Responsible for: advanced visual reasoning, multi-step planning, scene
interpretation, contextual understanding, decision making, long-context visual
analysis, workflow orchestration, technical reasoning, cross-image reasoning,
and autonomous visual decision support.

This module deliberately has no dependency on OpenCV or torch so it can be
imported in any environment. It talks to the Gemini REST API (generativelanguage
/ google-genai SDK) lazily.
"""

from __future__ import annotations

import base64
import json
import os
from typing import Any, Dict, List, Optional, Sequence

MODEL_NAME = "gemini-2.5-flash"

try:  # google-genai is the preferred modern SDK
    from google import genai  # type: ignore
    _GENAI_AVAILABLE = True
except Exception:  # pragma: no cover - optional dependency
    _GENAI_AVAILABLE = False

try:  # legacy google-generativeai fallback
    import google.generativeai as genai_legacy  # type: ignore
    _LEGACY_AVAILABLE = True
except Exception:  # pragma: no cover
    _LEGACY_AVAILABLE = False


class Gemini25FlashEngine:
    """Wrapper around Gemini 2.5 Flash for high-level visual reasoning."""

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

    # -- input helpers ---------------------------------------------------
    @staticmethod
    def _encode_image(image_bytes: bytes) -> Dict[str, Any]:
        return {"mime_type": "image/jpeg", "data": base64.b64encode(image_bytes).decode("ascii")}

    def _build_parts(self, text: str, images: Sequence[bytes]) -> List[Any]:
        parts: List[Any] = [text]
        for img in images:
            parts.append(self._encode_image(img))
        return parts

    # -- public API ------------------------------------------------------
    def reason(self, prompt: str, images: Sequence[bytes] = (), json_mode: bool = True) -> Any:
        """Run advanced visual reasoning. Returns raw model output."""
        if not self.is_available:
            return self._offline_response(prompt, images, json_mode)
        parts = self._build_parts(prompt, images)
        try:
            if _GENAI_AVAILABLE and self._client is not None:
                resp = self._model.generate_content(
                    model=MODEL_NAME, contents=parts
                )
            else:
                resp = self._model.generate_content(parts)
            text = getattr(resp, "text", str(resp))
            return self._maybe_parse_json(text) if json_mode else text
        except Exception as exc:  # pragma: no cover
            return {"error": str(exc), "engine": MODEL_NAME}

    def plan(self, instruction: str, images: Sequence[bytes] = ()) -> Dict[str, Any]:
        """Convert a high-level instruction into a structured plan."""
        from ai_core import prompt as prompt_module

        system = prompt_module.load_prompt()
        full = f"{system}\n\nConvert this instruction into a structured plan JSON:\n{instruction}"
        result = self.reason(full, images, json_mode=True)
        if isinstance(result, dict):
            return result
        return {"plan": [], "capabilities": [], "decision": str(result), "alerts": []}

    def describe_scene(self, image_bytes: bytes) -> Dict[str, Any]:
        prompt = ("Describe this scene in structured JSON with keys: scene_type, "
                  "lighting, time_of_day, crowdedness, notable_objects, hazards, summary.")
        return self.reason(prompt, [image_bytes], json_mode=True)

    def compare_images(self, image_a: bytes, image_b: bytes) -> Dict[str, Any]:
        prompt = ("Compare these two images and report differences as JSON with keys: "
                  "differences (list), similarity (0-1), summary.")
        return self.reason(prompt, [image_a, image_b], json_mode=True)

    # -- offline fallback ------------------------------------------------
    def _offline_response(self, prompt: str, images: Sequence[bytes], json_mode: bool) -> Any:
        msg = (f"[{MODEL_NAME} offline] No GEMINI_API_KEY configured or SDK unavailable. "
               f"Prompt: {prompt[:120]}... | images: {len(images)}")
        if json_mode:
            return {"error": "offline", "engine": MODEL_NAME, "message": msg,
                    "plan": [], "capabilities": [], "decision": msg, "alerts": []}
        return msg


def load_prompt() -> str:
    from ai_core import prompt as prompt_module
    return prompt_module.load_prompt()
