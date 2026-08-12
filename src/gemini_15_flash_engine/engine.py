"""Gemini 1.5 Flash engine: fast document processing, patent and literature
parsing, metadata extraction, information extraction, lightweight technical
analysis, validation tasks, context preparation, research preprocessing, and
supporting autonomous invention workflows."""

from __future__ import annotations

import json
import logging
import os
import re
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

MODEL_NAME = "gemini-1.5-flash"
DISPLAY_NAME = "Gemini 1.5 Flash"

RESPONSIBILITIES = [
    "Fast document processing",
    "Patent and literature parsing",
    "Metadata extraction",
    "Information extraction",
    "Lightweight technical analysis",
    "Validation tasks",
    "Context preparation",
    "Research preprocessing",
    "Supporting autonomous invention workflows",
]


def _load_api_key() -> Optional[str]:
    key = os.environ.get("GEMINI_API_KEY", "")
    if key:
        return key
    path = os.path.join(os.path.dirname(__file__), "..", "..", "config", "api_keys.json")
    path = os.path.abspath(path)
    if os.path.exists(path):
        try:
            with open(path) as f:
                return json.load(f).get("gemini_api_key") or None
        except (json.JSONDecodeError, OSError):
            return None
    return None


class Gemini15FlashEngine:
    """Thin wrapper around Google's Gemini 1.5 Flash model with offline fallback."""

    def __init__(self, api_key: Optional[str] = None, temperature: float = 0.3,
                 max_output_tokens: int = 4096, top_p: float = 0.9):
        self.model_name = MODEL_NAME
        self.display_name = DISPLAY_NAME
        self.responsibilities = RESPONSIBILITIES
        self.temperature = temperature
        self.max_output_tokens = max_output_tokens
        self.top_p = top_p
        self.api_key = api_key or _load_api_key()
        self._client = None
        if self.api_key:
            try:
                from google import genai  # type: ignore
                self._client = genai.Client(api_key=self.api_key)
                logger.info("Gemini 1.5 Flash engine connected.")
            except Exception as exc:  # pragma: no cover
                logger.warning("google-genai unavailable, using offline stub: %s", exc)
                self._client = None
        else:
            logger.info("No Gemini API key configured; engine running in offline stub mode.")

    @property
    def is_online(self) -> bool:
        return self._client is not None

    def generate(self, prompt: str, system: Optional[str] = None,
                 temperature: Optional[float] = None) -> str:
        if self._client is not None:
            try:
                cfg: Dict[str, Any] = {
                    "temperature": temperature if temperature is not None else self.temperature,
                    "max_output_tokens": self.max_output_tokens,
                    "top_p": self.top_p,
                }
                if system:
                    resp = self._client.models.generate_content(
                        model=self.model_name, contents=prompt,
                        config=cfg | {"system_instruction": system})
                else:
                    resp = self._client.models.generate_content(
                        model=self.model_name, contents=prompt, config=cfg)
                return getattr(resp, "text", str(resp))
            except Exception as exc:  # pragma: no cover
                logger.warning("Online generate failed, using stub: %s", exc)
        return self._stub(prompt, system)

    # ---- Fast / supporting responsibilities -------------------------------

    def extract_metadata(self, text: str) -> Dict[str, Any]:
        """Extract title, authors, date, and keywords from a technical document."""
        online_text = ""
        if self._client is not None:
            online_text = self.generate(
                f"Extract title, authors, date, and keywords as JSON from:\n{text[:3000]}",
                system="Return strict JSON with keys title, authors, date, keywords.")
        parsed = self._try_json(online_text)
        if parsed:
            return parsed
        # Deterministic fallback extraction.
        title_match = re.search(r"Title:\s*(.+)", text, re.IGNORECASE)
        author_match = re.search(r"Author[s]?:\s*(.+)", text, re.IGNORECASE)
        date_match = re.search(r"(19|20)\d{2}", text)
        return {
            "title": title_match.group(1).strip() if title_match else "Untitled",
            "authors": [a.strip() for a in author_match.group(1).split(",")] if author_match else [],
            "date": date_match.group(0) if date_match else "unknown",
            "keywords": [w for w in re.findall(r"\b[A-Za-z][A-Za-z\-]{4,}\b", text.lower())][:10],
        }

    def parse_patent(self, patent_text: str) -> Dict[str, Any]:
        online_text = ""
        if self._client is not None:
            online_text = self.generate(
                "Parse this patent into JSON with keys patent_number, title, inventor, "
                "abstract, claims (list), classification:\n" + patent_text[:3000],
                system="Return strict JSON.")
        parsed = self._try_json(online_text)
        if parsed:
            return parsed
        return {
            "patent_number": self._regex_group(patent_text, r"(US\s?\d[\d,]{6,})", "unknown"),
            "title": self._regex_group(patent_text, r"Title[:\s]+(.+)", "Untitled patent"),
            "inventor": self._regex_group(patent_text, r"Inventor[s]?[:\s]+(.+)", "unknown"),
            "abstract": patent_text[:500],
            "claims": [l for l in patent_text.splitlines() if re.match(r"\d+\.", l.strip())][:10],
            "classification": self._regex_group(patent_text, r"(IPC|CPC)[:\s]+([\w/]+)", "unknown"),
        }

    def preprocess_research(self, query: str) -> str:
        return self.generate(
            f"Prepare a concise research brief with key terms, subtopics, and "
            f"search queries for: {query}",
            system="You are a research preprocessing assistant.")

    def validate(self, claim: str) -> str:
        return self.generate(
            f"Validate this engineering claim for correctness and note any errors: {claim}",
            system="You are a validation engine. Be concise.")

    def summarize(self, text: str) -> str:
        return self.generate(
            f"Summarize concisely:\n{text[:4000]}",
            system="You are a fast summarizer.")

    def prepare_context(self, items: List[str]) -> str:
        joined = "\n".join(f"- {i}" for i in items)
        return self.generate(
            f"Prepare a structured context digest from these items:\n{joined}",
            system="You are a context preparation assistant.")

    # ---- Helpers / offline stub -------------------------------------------

    @staticmethod
    def _try_json(text: str) -> Optional[Dict[str, Any]]:
        if not text:
            return None
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if not match:
            return None
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            return None

    @staticmethod
    def _regex_group(text: str, pattern: str, default: str) -> str:
        m = re.search(pattern, text)
        return m.group(m.lastindex or 1).strip() if m else default

    def _stub(self, prompt: str, system: Optional[str]) -> str:
        snippet = prompt if len(prompt) <= 600 else prompt[:600] + "..."
        return (
            f"[{self.display_name} · offline stub]\n"
            f"(Configure GEMINI_API_KEY to enable live model responses.)\n\n"
            f"Request:\n{snippet}"
        )


def get_engine(**kwargs) -> Gemini15FlashEngine:
    return Gemini15FlashEngine(**kwargs)
