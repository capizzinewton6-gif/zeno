"""Gemini 2.5 Flash engine: advanced scientific reasoning, multi-stage engineering
planning, invention concept generation, system architecture design, mechanical and
electrical reasoning, optimization and trade-off analysis, research-level technical
analysis, long-context engineering reasoning, autonomous engineering decision making,
and workflow orchestration."""

from __future__ import annotations

import json
import logging
import os
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

MODEL_NAME = "gemini-2.5-flash"
DISPLAY_NAME = "Gemini 2.5 Flash"

# Responsibilities advertised by this engine (surfaced in the UI).
RESPONSIBILITIES = [
    "Advanced scientific reasoning",
    "Multi-stage engineering planning",
    "Invention concept generation",
    "System architecture design",
    "Mechanical and electrical reasoning",
    "Optimization and trade-off analysis",
    "Research-level technical analysis",
    "Long-context engineering reasoning",
    "Autonomous engineering decision making",
    "Workflow orchestration",
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


class Gemini25FlashEngine:
    """Thin wrapper around Google's Gemini 2.5 Flash model.

    Uses the ``google-genai`` SDK when available and an API key is configured.
    Otherwise it degrades to a deterministic offline stub so the rest of the
    system remains fully runnable in any environment.
    """

    def __init__(self, api_key: Optional[str] = None, temperature: float = 0.7,
                 max_output_tokens: int = 8192, top_p: float = 0.95):
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
                logger.info("Gemini 2.5 Flash engine connected.")
            except Exception as exc:  # pragma: no cover - depends on env
                logger.warning("google-genai unavailable, using offline stub: %s", exc)
                self._client = None
        else:
            logger.info("No Gemini API key configured; engine running in offline stub mode.")

    @property
    def is_online(self) -> bool:
        return self._client is not None

    def generate(self, prompt: str, system: Optional[str] = None,
                 temperature: Optional[float] = None) -> str:
        """Generate a completion for ``prompt``.

        Falls back to a deterministic offline response when no API client is
        configured, so callers always receive a usable string.
        """
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
            except Exception as exc:  # pragma: no cover - network dependent
                logger.warning("Online generate failed, using stub: %s", exc)
        return self._stub(prompt, system)

    # ---- High-level reasoning responsibilities -----------------------------

    def scientific_reasoning(self, query: str) -> str:
        return self.generate(
            f"Provide rigorous scientific reasoning for: {query}",
            system="You are a world-class scientist. Be precise and cite principles.")

    def engineering_plan(self, objective: str) -> str:
        return self.generate(
            f"Decompose this engineering objective into a multi-stage plan with "
            f"deliverables: {objective}",
            system="You are a senior engineering planner.")

    def generate_concepts(self, problem: str, n: int = 3) -> List[str]:
        text = self.generate(
            f"Generate {n} original invention concepts to solve: {problem}. "
            f"Return one concept per line, numbered.",
            system="You are a world-class inventor.")
        return [line for line in text.splitlines() if line.strip()]

    def system_architecture(self, requirements: str) -> str:
        return self.generate(
            f"Design a complete system architecture satisfying: {requirements}",
            system="You are a systems architect.")

    def optimize(self, design: str, objectives: List[str]) -> str:
        objs = ", ".join(objectives)
        return self.generate(
            f"Optimize this design for {objs} and present trade-offs:\n{design}",
            system="You are an optimization engineer.")

    def feasibility_analysis(self, concept: str) -> str:
        return self.generate(
            f"Analyze technical feasibility of: {concept}. Cover scientific, "
            f"manufacturing, economic, and regulatory feasibility.",
            system="You are a feasibility analyst.")

    def orchestrate_workflow(self, steps: List[str]) -> str:
        joined = "\n".join(f"{i+1}. {s}" for i, s in enumerate(steps))
        return self.generate(
            f"Orchestrate this engineering workflow, noting dependencies and outputs:\n{joined}",
            system="You are a workflow orchestration engine.")

    # ---- Offline stub ------------------------------------------------------

    def _stub(self, prompt: str, system: Optional[str]) -> str:
        snippet = prompt if len(prompt) <= 600 else prompt[:600] + "..."
        return (
            f"[{self.display_name} · offline stub]\n"
            f"(Configure GEMINI_API_KEY to enable live model responses.)\n\n"
            f"Request:\n{snippet}"
        )


def get_engine(**kwargs) -> Gemini25FlashEngine:
    return Gemini25FlashEngine(**kwargs)
