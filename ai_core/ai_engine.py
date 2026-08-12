"""Main orchestrator mapping requests to capabilities and agents.

The :class:`AIEngine` is the top-level entry point. It routes a user request
through planning, agent dispatch, capability execution, and safety gating,
returning a unified result envelope.
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Callable

from ai_core.context_manager import ContextManager, ContextRequest
from ai_core.knowledge_engine import KnowledgeEngine
from ai_core.planning_engine import ExecutionPlan, PlanningEngine
from ai_core.reasoning_engine import ReasoningEngine
from ai_core.safety_layer import SafetyLayer
from config import memory_file, save_json
from modeling.neural_backbones import NeuralBackbone, get_backbone

# Agent dispatch keys (lazy import to avoid circulars)
AGENT_KEYS = ("coding", "architect", "project_recommender", "refactoring",
              "debugging", "testing", "review", "project")


@dataclass
class AIResult:
    success: bool
    content: str
    plan: ExecutionPlan | None = None
    agent_used: str = ""
    capability_used: str = ""
    actions: list[str] = field(default_factory=list)
    latency_ms: float = 0.0
    error: str | None = None


class AIEngine:
    """Top-level orchestrator for CODING_AI."""

    def __init__(self, backbone: NeuralBackbone | None = None,
                 workspace: str = ".") -> None:
        self.backbone = backbone or get_backbone()
        self.workspace = workspace
        self.safety = SafetyLayer()
        self.knowledge = KnowledgeEngine()
        self.context_manager = ContextManager()
        self.reasoning = ReasoningEngine(self.backbone)
        self.planning = PlanningEngine(self.backbone, self.context_manager, self.reasoning)
        self._agents: dict[str, Any] = {}
        self._capabilities: dict[str, Any] = {}

    # -- Lifecycle -----------------------------------------------------------
    def initialize(self) -> None:
        """Lazily wire agents and capabilities (deferred to avoid import cycles)."""
        from agents.coding_agent import CodingAgent
        from agents.architect_agent import ArchitectAgent
        from agents.project_recommender import ProjectRecommenderAgent
        from agents.refactoring_agent import RefactoringAgent
        from agents.debugging_agent import DebuggingAgent
        from agents.testing_agent import TestingAgent
        from agents.review_agent import ReviewAgent
        from agents.project_agent import ProjectAgent

        self._agents = {
            "coding": CodingAgent(self.backbone, self.safety, self.workspace),
            "architect": ArchitectAgent(self.backbone, self.workspace),
            "project_recommender": ProjectRecommenderAgent(self.backbone, self.knowledge),
            "refactoring": RefactoringAgent(self.backbone, self.safety, self.workspace),
            "debugging": DebuggingAgent(self.backbone, self.workspace),
            "testing": TestingAgent(self.backbone, self.workspace),
            "review": ReviewAgent(self.backbone, self.workspace),
            "project": ProjectAgent(self.backbone, self.workspace),
        }

    # -- Routing -------------------------------------------------------------
    def route(self, user_message: str) -> str:
        """Classify a user message to the best agent key via the fast model."""
        prompt = (
            "Classify the user's request into exactly ONE agent from: "
            f"{', '.join(AGENT_KEYS)}. Reply with the single agent key only.\n\n"
            f"Request: {user_message}"
        )
        resp = self.backbone.fast(prompt)
        key = resp.text.strip().lower().split()[0] if resp.text else "coding"
        return key if key in AGENT_KEYS else "coding"

    # -- Main entry ----------------------------------------------------------
    def handle(self, user_message: str, *,
               relevant_files: list[str] | None = None,
               directives: list[str] | None = None) -> AIResult:
        start = time.perf_counter()
        self._log_session(user_message)
        self.initialize()
        agent_key = self.route(user_message)
        agent = self._agents[agent_key]

        plan = None
        try:
            plan = self.planning.plan(user_message, workspace=self.workspace,
                                      relevant_files=relevant_files or [],
                                      directives=directives or [])
            result = agent.run(user_message, plan=plan)
            latency = (time.perf_counter() - start) * 1000
            return AIResult(
                success=True, content=result.get("content", ""),
                plan=plan, agent_used=agent_key,
                capability_used=result.get("capability", ""),
                actions=result.get("actions", []), latency_ms=latency,
            )
        except Exception as exc:
            latency = (time.perf_counter() - start) * 1000
            return AIResult(success=False, content="", agent_used=agent_key,
                            plan=plan, latency_ms=latency, error=str(exc))

    # -- Direct agent access -------------------------------------------------
    def dispatch(self, agent_key: str, message: str, **kwargs: Any) -> Any:
        self.initialize()
        agent = self._agents.get(agent_key)
        if not agent:
            raise KeyError(f"Unknown agent: {agent_key}")
        return agent.run(message, **kwargs)

    # -- Status & project management ---------------------------------------
    def status(self) -> dict[str, Any]:
        """Return a snapshot of engine state for the UI."""
        from config import load_json, memory_file
        history = load_json(memory_file("session_history.json"))
        return {
            "workspace": self.workspace,
            "backbone": self.backbone.__class__.__name__,
            "agents": AGENT_KEYS,
            "sessions_logged": len(history.get("sessions", [])),
            "initialized": bool(self._agents),
        }

    def start_project(self, name: str, goal: str = "", stack: list[str] | None = None) -> str:
        """Initialize a project context for the current workspace."""
        from project.project_manager import ProjectManager
        pm = ProjectManager()
        pm.create_project(name=name, goal=goal or name, stack=stack or [])
        return f"Project '{name}' created in {self.workspace}"

    # -- Bookkeeping ---------------------------------------------------------
    def _log_session(self, message: str) -> None:
        from datetime import datetime, timezone

        import uuid

        session = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "prompt": message,
        }
        history = {"sessions": [], "current_session": None, "version": "1.0.0"}
        try:
            from config import load_json

            history = load_json(memory_file("session_history.json"))
        except Exception:
            pass
        history.setdefault("sessions", []).append(session)
        history["current_session"] = session["id"]
        save_json(memory_file("session_history.json"), history)
