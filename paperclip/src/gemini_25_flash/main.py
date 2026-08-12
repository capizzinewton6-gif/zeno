"""
Gemini 2.5 Flash - Primary Engineering Intelligence Engine
==========================================================
Advanced reasoning, multi-step planning, and complex task execution.

Responsible for:
- Advanced reasoning
- Multi-step planning
- Software architecture design
- System architecture generation
- Source code generation
- Debugging
- Code optimization
- Security analysis
- Technical documentation generation
- AI application development
- Database design
- API design
- Deployment planning
- Autonomous decision making
- Long-context project understanding
- Workflow orchestration
"""

import os
from typing import Any, Dict, List, Optional
from dataclasses import dataclass

from loguru import logger

try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False
    logger.warning("google-generativeai not installed")


@dataclass
class Gemini25Config:
    """Configuration for Gemini 2.5 Flash."""
    model_name: str = "gemini-2.0-flash"
    temperature: float = 0.7
    max_tokens: int = 8192
    top_p: float = 0.95
    top_k: int = 40


class Gemini25Flash:
    """
    Gemini 2.5 Flash - Primary Engineering Intelligence Engine.
    
    Used for complex reasoning tasks requiring deep analysis,
    multi-step planning, and sophisticated decision making.
    """

    def __init__(self, api_key: Optional[str] = None, config: Optional[Gemini25Config] = None):
        """
        Initialize Gemini 2.5 Flash.
        
        Args:
            api_key: Gemini API key
            config: Model configuration
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY", "")
        self.config = config or Gemini25Config()
        
        if GENAI_AVAILABLE and self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(
                model_name=self.config.model_name,
                generation_config={
                    "temperature": self.config.temperature,
                    "max_output_tokens": self.config.max_tokens,
                    "top_p": self.config.top_p,
                    "top_k": self.config.top_k,
                }
            )
        else:
            self.model = None
            logger.warning("Gemini 2.5 Flash: API key not set or library not available")
        
        logger.info("Gemini 2.5 Flash initialized")

    def execute(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Execute a task with Gemini 2.5 Flash.
        
        Args:
            prompt: The task prompt
            context: Optional context dictionary
            
        Returns:
            Model response
        """
        if not self.model:
            return "Gemini 2.5 Flash: Model not initialized (API key required)"
        
        # Build full prompt with context
        full_prompt = self._build_prompt(prompt, context)
        
        try:
            response = self.model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            logger.error(f"Gemini 2.5 Flash error: {e}")
            return f"Error: {str(e)}"

    def _build_prompt(self, prompt: str, context: Optional[Dict[str, Any]]) -> str:
        """Build the full prompt with context."""
        full_prompt = prompt
        
        if context:
            context_str = "\n\n## Context\n"
            for key, value in context.items():
                context_str += f"- {key}: {value}\n"
            full_prompt += context_str
        
        return full_prompt

    def reason(self, problem: str, steps: int = 5) -> str:
        """
        Perform step-by-step reasoning on a problem.
        
        Args:
            problem: The problem to reason about
            steps: Number of reasoning steps
            
        Returns:
            Reasoned solution
        """
        reasoning_prompt = f"""Think through this step by step ({steps} steps):

Problem: {problem}

Think carefully about each step and explain your reasoning."""
        
        return self.execute(reasoning_prompt)

    def plan(self, goal: str, constraints: Optional[List[str]] = None) -> str:
        """
        Create a detailed plan to achieve a goal.
        
        Args:
            goal: The goal to achieve
            constraints: Optional constraints to consider
            
        Returns:
            Detailed plan
        """
        constraints_str = ""
        if constraints:
            constraints_str = "\n\nConstraints:\n" + "\n".join(f"- {c}" for c in constraints)
        
        planning_prompt = f"""Create a detailed plan to achieve the following goal:

Goal: {goal}
{constraints_str}

Break down the plan into clear, actionable steps."""
        
        return self.execute(planning_prompt)

    def analyze(self, subject: str, analysis_type: str = "comprehensive") -> str:
        """
        Perform analysis on a subject.
        
        Args:
            subject: The subject to analyze
            analysis_type: Type of analysis (comprehensive, security, performance, etc.)
            
        Returns:
            Analysis results
        """
        analysis_prompt = f"""Perform a {analysis_type} analysis of:

{subject}

Provide detailed findings and recommendations."""
        
        return self.execute(analysis_prompt)

    def generate_code(self, requirement: str, language: str = "python") -> str:
        """
        Generate code based on a requirement.
        
        Args:
            requirement: The code requirement
            language: Programming language
            
        Returns:
            Generated code
        """
        code_prompt = f"""Generate {language} code for the following requirement:

{requirement}

Provide clean, well-documented code."""
        
        return self.execute(code_prompt)

    def debug(self, code: str, error: Optional[str] = None) -> str:
        """
        Debug code and identify issues.
        
        Args:
            code: The code to debug
            error: Optional error message
            
        Returns:
            Debug analysis and fix suggestions
        """
        error_info = f"\n\nError: {error}" if error else ""
        debug_prompt = f"""Debug the following code:{error_info}

```{code}
```

Identify the issues and provide fixes."""
        
        return self.execute(debug_prompt)
