"""Extract LaTeX/MathJax from images (Math OCR).

Real Math OCR requires a vision model (e.g., pix2tex or Mathpix). This module
provides a graceful interface that uses Gemini 1.5 Flash when GEMINI_API_KEY is
set and otherwise suggests manual entry.
"""

from __future__ import annotations

from typing import Any


def extract_latex_from_image(image_path: str) -> dict[str, Any]:
    """Extract LaTeX from a math image.

    Returns {"latex": str, "source": "gemini" | "manual", "available": bool}.
    """
    try:
        from mathematics_ai.ai_core.gemini_15_flash_engine import Gemini15FlashEngine
        engine = Gemini15FlashEngine()
        if engine.is_available:
            prompt = "Extract the mathematical formula from this image and return it as LaTeX. Return only the LaTeX code."
            result = engine.analyze_image(image_path, prompt)
            return {"latex": result, "source": "gemini", "available": True}
    except Exception as e:
        return {"latex": "", "source": "error", "available": False, "error": str(e)}
    return {"latex": "", "source": "manual", "available": False, "note": "provide GEMINI_API_KEY to enable OCR"}


def extract_mathjax_from_html(html: str) -> list[str]:
    """Extract MathJax delimiters from HTML."""
    import re
    patterns = [r"\\\[.+?\\\]", r"\(.+?\)", r"\$\$.+?\$\$", r"\$.+?\$"]
    found = []
    for p in patterns:
        found.extend(re.findall(p, html, re.DOTALL))
    return found


__all__ = ["extract_latex_from_image", "extract_mathjax_from_html"]
