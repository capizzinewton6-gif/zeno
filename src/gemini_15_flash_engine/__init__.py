"""Gemini 1.5 Flash engine.

Responsible for fast document processing, literature parsing, metadata
extraction, information extraction, lightweight chemical analysis,
validation tasks, context preparation, research preprocessing, and
supporting autonomous chemistry workflows.

This engine uses Google's Gemini 1.5 Flash model exclusively.
"""

import os
import logging

logger = logging.getLogger(__name__)

MODEL_NAME = "gemini-1.5-flash"
MODEL_FAMILY = "Google Gemini 1.5 Flash"

_DEFAULT_SYSTEM_INSTRUCTION = (
    "You are the fast-processing core of an AI Chemistry Laboratory Assistant. "
    "You handle literature parsing, metadata extraction, lightweight chemical "
    "analysis, validation, and context preparation for deeper reasoning. "
    "Be concise and structured."
)


def _resolve_api_key(api_key=None):
    key = api_key or os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not key:
        logger.warning("No GEMINI_API_KEY configured; Gemini 1.5 Flash will run in offline fallback mode.")
    return key


def get_model(system_instruction=_DEFAULT_SYSTEM_INSTRUCTION, api_key=None):
    key = _resolve_api_key(api_key)
    if not key:
        return None
    try:
        import google.generativeai as genai
    except Exception as exc:  # pragma: no cover
        logger.warning("google-generativeai not installed: %s", exc)
        return None
    try:
        genai.configure(api_key=key)
        return genai.GenerativeModel(MODEL_NAME, system_instruction=system_instruction)
    except Exception as exc:  # pragma: no cover
        logger.warning("Could not initialize Gemini 1.5 Flash client: %s", exc)
        return None


def offline_response(prompt, context=None):
    return {
        "engine": MODEL_FAMILY,
        "model": MODEL_NAME,
        "mode": "offline-fallback",
        "prompt": prompt,
        "context": context or {},
        "response": (
            "[Gemini 1.5 Flash offline fallback] Fast-processing module is "
            "available in simulation mode. Provide GEMINI_API_KEY to enable live "
            "document and literature processing."
        ),
        "notes": [
            "All simulations are performed on the user interface.",
            "Configure GEMINI_API_KEY to enable live Gemini 1.5 Flash processing.",
        ],
    }


def process(prompt, context=None, system_instruction=_DEFAULT_SYSTEM_INSTRUCTION, api_key=None):
    """Run a fast-processing request through Gemini 1.5 Flash."""
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
    except Exception as exc:  # pragma: no cover
        logger.warning("Gemini 1.5 Flash call failed, using offline fallback: %s", exc)
        offline = offline_response(prompt, context)
        offline["error"] = str(exc)
        return offline


def describe():
    return {
        "name": "gemini_15_flash_engine",
        "model": MODEL_NAME,
        "family": MODEL_FAMILY,
        "responsibilities": [
            "Fast document processing",
            "Literature parsing",
            "Metadata extraction",
            "Information extraction",
            "Lightweight chemical analysis",
            "Validation tasks",
            "Context preparation",
            "Research preprocessing",
            "Supporting autonomous chemistry workflows",
        ],
    }
