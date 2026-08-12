"""Gemini 2.5 Flash engine.

Provides advanced chemical reasoning, multi-step scientific planning,
reaction-mechanism reasoning, thermodynamic and kinetic analysis,
research-level chemical analysis, long-context chemical reasoning,
scientific decision making, chemical workflow orchestration, and
complex systems analysis.

This engine uses Google's Gemini 2.5 Flash model exclusively.
"""

import os
import logging

logger = logging.getLogger(__name__)

# Model identifier used across the application.
MODEL_NAME = "gemini-2.5-flash"
MODEL_FAMILY = "Google Gemini 2.5 Flash"

_DEFAULT_SYSTEM_INSTRUCTION = (
    "You are the advanced reasoning core of an AI Chemistry Laboratory Assistant. "
    "You perform rigorous chemical reasoning, multi-step scientific planning, "
    "reaction-mechanism analysis, thermodynamic and kinetic analysis, and "
    "research-level interpretation. Always cite physical laws and known "
    "constants. Prefer SI units. Flag safety concerns explicitly."
)


def _resolve_api_key(api_key=None):
    """Resolve a Gemini API key from the argument or environment."""
    key = api_key or os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not key:
        logger.warning("No GEMINI_API_KEY configured; Gemini 2.5 Flash will run in offline fallback mode.")
    return key


def get_model(system_instruction=_DEFAULT_SYSTEM_INSTRUCTION, api_key=None):
    """Return a configured Gemini 2.5 Flash model client.

    If the google-generativeai package is unavailable or no API key is set,
    None is returned and callers should use :func:`offline_response` instead.
    """
    key = _resolve_api_key(api_key)
    if not key:
        return None
    try:
        import google.generativeai as genai
    except Exception as exc:  # pragma: no cover - import guard
        logger.warning("google-generativeai not installed: %s", exc)
        return None
    try:
        genai.configure(api_key=key)
        return genai.GenerativeModel(MODEL_NAME, system_instruction=system_instruction)
    except Exception as exc:  # pragma: no cover - runtime guard
        logger.warning("Could not initialize Gemini 2.5 Flash client: %s", exc)
        return None


def offline_response(prompt, context=None):
    """Deterministic offline fallback when no API key / SDK is available.

    Returns a structured placeholder so the UI remains fully functional for
    simulations without external API calls.
    """
    return {
        "engine": MODEL_FAMILY,
        "model": MODEL_NAME,
        "mode": "offline-fallback",
        "prompt": prompt,
        "context": context or {},
        "response": (
            "[Gemini 2.5 Flash offline fallback] Advanced reasoning module is "
            "available in simulation mode. Provide GEMINI_API_KEY to enable live "
            "chemical reasoning. In simulation, this engine decomposes the task "
            "and returns a structured analysis scaffold."
        ),
        "notes": [
            "All simulations are performed on the user interface.",
            "Configure GEMINI_API_KEY to enable live Gemini 2.5 Flash reasoning.",
        ],
    }


def reason(prompt, context=None, system_instruction=_DEFAULT_SYSTEM_INSTRUCTION, api_key=None):
    """Run an advanced reasoning request through Gemini 2.5 Flash.

    Falls back to a deterministic offline response when the SDK or key is
    unavailable, so the application always returns structured output.
    """
    model = get_model(system_instruction=system_instruction, api_key=api_key)
    if model is None:
        return offline_response(prompt, context)
    try:
        full_prompt = prompt
        if context:
            full_prompt = f"Context:\n{context}\n\nTask:\n{prompt}"
        result = model.generate_content(full_prompt)
        return {
            "engine": MODEL_FAMILY,
            "model": MODEL_NAME,
            "mode": "live",
            "prompt": prompt,
            "context": context or {},
            "response": getattr(result, "text", str(result)),
        }
    except Exception as exc:  # pragma: no cover - runtime guard
        logger.warning("Gemini 2.5 Flash call failed, using offline fallback: %s", exc)
        offline = offline_response(prompt, context)
        offline["error"] = str(exc)
        return offline


def describe():
    """Return a human-readable description of this engine's responsibilities."""
    return {
        "name": "gemini_25_flash_engine",
        "model": MODEL_NAME,
        "family": MODEL_FAMILY,
        "responsibilities": [
            "Advanced chemical reasoning",
            "Multi-step scientific planning",
            "Reaction-mechanism reasoning",
            "Thermodynamic and kinetic analysis",
            "Research-level chemical analysis",
            "Long-context chemical reasoning",
            "Scientific decision making",
            "Chemical workflow orchestration",
            "Complex systems analysis",
        ],
    }
