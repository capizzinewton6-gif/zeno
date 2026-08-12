"""
Autonomous Execution Engine - Main Module
=========================================
Coordinates all capability modules for autonomous task execution.
"""

import os
import yaml
from typing import Any, Dict, List, Optional
from dataclasses import dataclass

from loguru import logger

from .capability_manager import CapabilityManager


@dataclass
class ExecutionConfig:
    """Configuration for autonomous execution."""
    max_iterations: int = 100
    timeout_seconds: int = 300
    retry_on_error: bool = True
    max_retries: int = 3
    confirm_destructive: bool = True


class AutonomousExecutionEngine:
    """
    Main execution engine for Paperclip.
    
    Coordinates all capability modules to execute tasks
    autonomously while maintaining independence of each module.
    
    Responsibilities:
    - Task decomposition and planning
    - Capability selection and orchestration
    - Execution monitoring and retry
    - Result aggregation
    - Context sharing between capabilities
    """

    def __init__(
        self,
        model_router: Any,
        workspace: str = None,
        config_path: str = None
    ):
        """
        Initialize the autonomous execution engine.
        
        Args:
            model_router: The AI model router for task processing
            workspace: Working directory for file operations
            config_path: Path to configuration file
        """
        self.workspace = workspace or os.getcwd()
        self.model_router = model_router
        
        # Load configuration
        self.config = self._load_config(config_path)
        self.execution_config = ExecutionConfig(
            max_iterations=self.config.get("execution", {}).get("max_iterations", 100),
            timeout_seconds=self.config.get("execution", {}).get("timeout_seconds", 300),
            retry_on_error=self.config.get("execution", {}).get("retry_on_error", True),
            max_retries=self.config.get("execution", {}).get("max_retries", 3),
            confirm_destructive=self.config.get("execution", {}).get("confirm_destructive", True),
        )
        
        # Initialize capability manager
        enabled = self._get_enabled_capabilities()
        self.capability_manager = CapabilityManager(enabled_capabilities=enabled)
        
        # Execution state
        self.current_task: Optional[str] = None
        self.execution_history: List[Dict[str, Any]] = []
        self.context: Dict[str, Any] = {}
        
        logger.info("Autonomous Execution Engine initialized")

    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    return yaml.safe_load(f) or {}
            except Exception as e:
                logger.warning(f"Failed to load config from {config_path}: {e}")
        
        return {}

    def _get_enabled_capabilities(self) -> List[str]:
        """Get list of enabled capabilities from config."""
        capabilities_config = self.config.get("capabilities", {})
        return [name for name, enabled in capabilities_config.items() if enabled]

    def execute_task(self, task: str) -> str:
        """
        Execute a task autonomously.
        
        Args:
            task: The task description
            
        Returns:
            Result of task execution
        """
        logger.info(f"Executing task: {task}")
        self.current_task = task
        
        try:
            # Step 1: Analyze task and create execution plan
            plan = self._plan_execution(task)
            
            # Step 2: Execute plan steps
            result = self._execute_plan(plan)
            
            # Step 3: Return result
            self.execution_history.append({
                "task": task,
                "plan": plan,
                "result": result,
                "status": "success"
            })
            
            return result
            
        except Exception as e:
            logger.error(f"Task execution failed: {e}")
            self.execution_history.append({
                "task": task,
                "error": str(e),
                "status": "failed"
            })
            return f"I encountered an error while executing your task: {str(e)}"

    def _plan_execution(self, task: str) -> Dict[str, Any]:
        """
        Create an execution plan for the task.
        
        Args:
            task: The task description
            
        Returns:
            Execution plan dictionary
        """
        # Use Gemini 2.5 Flash for planning
        planning_prompt = f"""Analyze this task and create an execution plan:

Task: {task}

Break down the task into clear steps and identify which capabilities are needed.
Consider dependencies between steps and potential issues.

Return a structured plan with:
1. Task analysis
2. Required capabilities
3. Step-by-step execution order
4. Potential risks"""

        plan_text = self.model_router.route_task(
            planning_prompt,
            context={"workspace": self.workspace}
        )
        
        # Parse plan (simplified - in production would use structured output)
        plan = {
            "task": task,
            "analysis": plan_text,
            "steps": self._extract_steps(plan_text),
            "capabilities_needed": self._extract_capabilities(plan_text)
        }
        
        return plan

    def _extract_steps(self, plan_text: str) -> List[Dict[str, Any]]:
        """Extract execution steps from plan text."""
        steps = []
        lines = plan_text.split('\n')
        
        for i, line in enumerate(lines):
            if line.strip() and (line[0].isdigit() or line.startswith('-')):
                steps.append({
                    "description": line.strip(),
                    "status": "pending"
                })
        
        # If no clear steps found, create a single step
        if not steps:
            steps.append({
                "description": "Execute task",
                "status": "pending"
            })
        
        return steps

    def _extract_capabilities(self, plan_text: str) -> List[str]:
        """Extract required capabilities from plan text."""
        # Common capability keywords
        keywords = {
            "search": ["file_search", "web_search"],
            "open": ["application_launcher", "folder_navigation"],
            "click": ["mouse_control"],
            "type": ["keyboard_control"],
            "read": ["pdf_processing", "word_processing", "document_retrieval"],
            "write": ["file_operations", "text_generation"],
            "execute": ["terminal_execution", "python_execution"],
            "browse": ["browser_automation", "website_navigation"],
            "calculate": ["calculator_engine"],
            "convert": ["unit_conversion"],
            "monitor": ["cpu_monitoring", "memory_monitoring", "disk_monitoring"],
        }
        
        plan_lower = plan_text.lower()
        needed = []
        
        for action, capabilities in keywords.items():
            if action in plan_lower:
                needed.extend(capabilities)
        
        return list(set(needed)) if needed else ["general"]

    def _execute_plan(self, plan: Dict[str, Any]) -> str:
        """
        Execute a plan step by step.
        
        Args:
            plan: The execution plan
            
        Returns:
            Final result
        """
        steps = plan.get("steps", [])
        results = []
        
        for i, step in enumerate(steps):
            if i >= self.execution_config.max_iterations:
                logger.warning("Max iterations reached")
                break
            
            try:
                # Execute step using appropriate capability
                step_result = self._execute_step(step)
                results.append(step_result)
                step["status"] = "completed"
                
            except Exception as e:
                logger.error(f"Step {i+1} failed: {e}")
                step["status"] = "failed"
                step["error"] = str(e)
                
                if self.execution_config.retry_on_error:
                    # Retry logic
                    for retry in range(self.execution_config.max_retries):
                        try:
                            step_result = self._execute_step(step)
                            results.append(step_result)
                            step["status"] = "completed"
                            break
                        except Exception as retry_error:
                            logger.warning(f"Retry {retry+1} failed: {retry_error}")
                            continue
                else:
                    break
        
        # Aggregate results
        return self._aggregate_results(results)

    def _execute_step(self, step: Dict[str, Any]) -> str:
        """Execute a single step."""
        description = step.get("description", "")
        
        # Use AI to determine how to execute this step
        execution_prompt = f"""Execute this step: {description}

Context:
- Workspace: {self.workspace}
- Current task: {self.current_task}

Provide the result of executing this step."""

        return self.model_router.route_task(
            execution_prompt,
            context={"workspace": self.workspace}
        )

    def _aggregate_results(self, results: List[str]) -> str:
        """Aggregate step results into final response."""
        if not results:
            return "Task completed with no results."
        
        if len(results) == 1:
            return results[0]
        
        # Summarize multiple results
        summary_prompt = f"""Summarize these execution results:

{' '.join(results)}

Provide a concise summary of what was accomplished."""

        return self.model_router.get_processing_model().summarize(
            "\n\n".join(results)
        )

    def get_capability_status(self) -> Dict[str, str]:
        """Get status of all capabilities."""
        return self.capability_manager.get_capability_status()

    def enable_capability(self, capability_name: str) -> bool:
        """Enable a capability module."""
        return self.capability_manager.enable_capability(capability_name)

    def disable_capability(self, capability_name: str) -> bool:
        """Disable a capability module."""
        return self.capability_manager.disable_capability(capability_name)

    def get_execution_history(self) -> List[Dict[str, Any]]:
        """Get the execution history."""
        return self.execution_history
