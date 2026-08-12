"""
Model Router - AI Task Routing Engine
====================================
Routes tasks to appropriate Gemini models based on task requirements.
"""

import os
from enum import Enum
from typing import Any, Dict, Optional
from dataclasses import dataclass

from loguru import logger

from ..gemini_25_flash.main import Gemini25Flash
from ..gemini_15_flash.main import Gemini15Flash


class TaskType(Enum):
    """Task type classification for model routing."""
    REASONING = "reasoning"           # Complex reasoning, planning, analysis
    PROCESSING = "processing"         # Fast processing, extraction, summarization
    EXECUTION = "execution"           # Task execution, automation
    CREATION = "creation"             # Code generation, writing
    ANALYSIS = "analysis"            # Deep analysis, debugging


@dataclass
class RoutingConfig:
    """Configuration for model routing."""
    reasoning_tasks: str = "gemini_25_flash"
    processing_tasks: str = "gemini_15_flash"
    execution_tasks: str = "gemini_25_flash"
    creation_tasks: str = "gemini_25_flash"
    analysis_tasks: str = "gemini_25_flash"
    default: str = "gemini_15_flash"


class ModelRouter:
    """
    Routes AI tasks to appropriate Gemini models.
    
    Uses Gemini 2.5 Flash for:
    - Advanced reasoning
    - Multi-step planning
    - Software architecture design
    - Code generation
    - Complex decision making
    
    Uses Gemini 1.5 Flash for:
    - Fast context processing
    - File analysis
    - Documentation parsing
    - Information extraction
    - Lightweight reasoning
    """

    def __init__(self, api_key: Optional[str] = None, config: Optional[RoutingConfig] = None):
        """
        Initialize the model router.
        
        Args:
            api_key: Gemini API key (defaults to GEMINI_API_KEY env var)
            config: Routing configuration
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY", "")
        self.config = config or RoutingConfig()
        
        # Initialize models
        self.gemini_25 = Gemini25Flash(api_key=self.api_key)
        self.gemini_15 = Gemini15Flash(api_key=self.api_key)
        
        logger.info("Model Router initialized")

    def classify_task(self, task: str, context: Optional[Dict[str, Any]] = None) -> TaskType:
        """
        Classify a task to determine appropriate model.
        
        Args:
            task: The task description
            context: Optional context about the task
            
        Returns:
            TaskType classification
        """
        task_lower = task.lower()
        
        # Reasoning keywords
        reasoning_keywords = [
            "plan", "reason", "analyze", "think", "strategize",
            "design", "architect", "solve", "decide", "evaluate",
            "assess", "consider", "determine", "figure out",
            "complex", "advanced", "reasoning"
        ]
        
        # Processing keywords
        processing_keywords = [
            "read", "extract", "summarize", "parse", "scan",
            "index", "search", "find", "lookup", "get info",
            "quick", "fast", "simple", "basic"
        ]
        
        # Creation keywords
        creation_keywords = [
            "create", "write", "generate", "build", "make",
            "develop", "implement", "code", "script"
        ]
        
        # Analysis keywords
        analysis_keywords = [
            "debug", "review", "optimize", "improve", "fix",
            "refactor", "test", "validate", "verify"
        ]
        
        # Count matches
        reasoning_score = sum(1 for kw in reasoning_keywords if kw in task_lower)
        processing_score = sum(1 for kw in processing_keywords if kw in task_lower)
        creation_score = sum(1 for kw in creation_keywords if kw in task_lower)
        analysis_score = sum(1 for kw in analysis_keywords if kw in task_lower)
        
        # Determine task type
        scores = {
            TaskType.REASONING: reasoning_score,
            TaskType.PROCESSING: processing_score,
            TaskType.CREATION: creation_score,
            TaskType.ANALYSIS: analysis_score,
        }
        
        max_score = max(scores.values())
        if max_score > 0:
            for task_type, score in scores.items():
                if score == max_score:
                    return task_type
        
        return TaskType.PROCESSING  # Default to fast processing

    def route_task(self, task: str, context: Optional[Dict[str, Any]] = None) -> Any:
        """
        Route a task to the appropriate model and execute.
        
        Args:
            task: The task to execute
            context: Optional context for the task
            
        Returns:
            Task result from the appropriate model
        """
        task_type = self.classify_task(task, context)
        logger.debug(f"Task classified as: {task_type.value}")
        
        if task_type == TaskType.REASONING:
            return self.gemini_25.execute(task, context)
        elif task_type == TaskType.PROCESSING:
            return self.gemini_15.execute(task, context)
        elif task_type == TaskType.CREATION:
            return self.gemini_25.execute(task, context)
        elif task_type == TaskType.ANALYSIS:
            return self.gemini_25.execute(task, context)
        else:
            return self.gemini_15.execute(task, context)

    def get_model(self, model_name: str) -> Any:
        """
        Get a specific model by name.
        
        Args:
            model_name: Name of the model
            
        Returns:
            The requested model instance
        """
        if model_name == "gemini_25_flash":
            return self.gemini_25
        elif model_name == "gemini_15_flash":
            return self.gemini_15
        else:
            raise ValueError(f"Unknown model: {model_name}")

    def get_reasoning_model(self) -> Any:
        """Get the primary reasoning model (Gemini 2.5 Flash)."""
        return self.gemini_25

    def get_processing_model(self) -> Any:
        """Get the processing model (Gemini 1.5 Flash)."""
        return self.gemini_15
