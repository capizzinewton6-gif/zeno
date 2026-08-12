"""Read textbook or blackboard math proofs via OCR (Gemini 1.5 Flash)."""

from __future__ import annotations

from typing import Any


def read_proof_from_image(image_path: str) -> dict[str, Any]:
    """Read a math proof from an image.

    Returns {"text": str, "source": "gemini" | "manual", "available": bool}.
    """
    try:
        from mathematics_ai.ai_core.gemini_15_flash_engine import Gemini15FlashEngine
        engine = Gemini15FlashEngine()
        if engine.is_available:
            prompt = "Transcribe this mathematical proof exactly, preserving LaTeX notation for symbols. Return the proof text."
            result = engine.analyze_image(image_path, prompt)
            return {"text": result, "source": "gemini", "available": True}
    except Exception as e:
        return {"text": "", "source": "error", "available": False, "error": str(e)}
    return {"text": "", "source": "manual", "available": False, "note": "provide GEMINI_API_KEY to enable proof OCR"}


def parse_proof_structure(text: str) -> dict[str, Any]:
    """Parse a transcribed proof into premise/steps/conclusion."""
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    if not lines:
        return {"premise": "", "steps": [], "conclusion": ""}
    premise = lines[0]
    steps = []
    for line in lines[1:]:
        if any(k in line.lower() for k in ("therefore", "qed", "■", "q.e.d", "hence", "thus")):
            break
        steps.append(line)
    conclusion = lines[-1] if lines else ""
    return {"premise": premise, "steps": steps, "conclusion": conclusion}


__all__ = ["read_proof_from_image", "parse_proof_structure"]
