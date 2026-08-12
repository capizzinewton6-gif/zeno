"""AI engine layer for Mathematics AI.

Mathematics AI uses Google Gemini models exclusively: gemini-2.5-flash
(advanced reasoning) and gemini-1.5-flash (fast preprocessing). Each engine
adapter calls the real Gemini API when a GEMINI_API_KEY is available and falls
back to a deterministic local reasoning path otherwise, so the system runs
end-to-end in any environment.
"""

from mathematics_ai.ai_core.engine_base import EngineResponse, EngineConfig
from mathematics_ai.ai_core.gemini_25_flash_engine import Gemini25FlashEngine
from mathematics_ai.ai_core.gemini_15_flash_engine import Gemini15FlashEngine
from mathematics_ai.ai_core.model_router import ModelRouter
from mathematics_ai.ai_core.reasoning_engine import ReasoningEngine, ReasoningTrace
from mathematics_ai.ai_core.planning_engine import PlanningEngine, ExecutionPlan
from mathematics_ai.ai_core.context_manager import ContextManager, ProblemContext
from mathematics_ai.ai_core.knowledge_engine import KnowledgeEngine
from mathematics_ai.ai_core.safety_layer import SafetyLayer, SafetyError

__all__ = [
    "EngineResponse", "EngineConfig", "Gemini25FlashEngine", "Gemini15FlashEngine",
    "ModelRouter", "ReasoningEngine", "ReasoningTrace", "PlanningEngine",
    "ExecutionPlan", "ContextManager", "ProblemContext", "KnowledgeEngine",
    "SafetyLayer", "SafetyError",
]
