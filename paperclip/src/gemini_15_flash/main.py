"""
Gemini 1.5 Flash - High-Speed Processing & Analysis Engine
==========================================================
Fast context processing, file analysis, and information extraction.

Responsible for:
- Fast context processing
- File analysis
- Code summarization
- Documentation parsing
- Project indexing
- Information extraction
- Knowledge retrieval
- Validation tasks
- Metadata extraction
- Lightweight reasoning
- Workspace scanning
- Research preprocessing
- Context compression
- Supporting autonomous workflows
"""

import os
from typing import Any, Dict, Optional
from dataclasses import dataclass

from loguru import logger

try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False
    logger.warning("google-generativeai not installed")


@dataclass
class Gemini15Config:
    """Configuration for Gemini 1.5 Flash."""
    model_name: str = "gemini-1.5-flash"
    temperature: float = 0.5
    max_tokens: int = 4096
    top_p: float = 0.95
    top_k: int = 40


class Gemini15Flash:
    """
    Gemini 1.5 Flash - High-Speed Processing & Analysis Engine.
    
    Used for fast, lightweight tasks like file analysis,
    information extraction, and context processing.
    """

    def __init__(self, api_key: Optional[str] = None, config: Optional[Gemini15Config] = None):
        """
        Initialize Gemini 1.5 Flash.
        
        Args:
            api_key: Gemini API key
            config: Model configuration
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY", "")
        self.config = config or Gemini15Config()
        
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
            logger.warning("Gemini 1.5 Flash: API key not set or library not available")
        
        logger.info("Gemini 1.5 Flash initialized")

    def execute(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Execute a task with Gemini 1.5 Flash.
        
        Args:
            prompt: The task prompt
            context: Optional context dictionary
            
        Returns:
            Model response
        """
        if not self.model:
            return "Gemini 1.5 Flash: Model not initialized (API key required)"
        
        # Build full prompt with context
        full_prompt = self._build_prompt(prompt, context)
        
        try:
            response = self.model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            logger.error(f"Gemini 1.5 Flash error: {e}")
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

    def summarize(self, content: str, max_length: int = 500) -> str:
        """
        Summarize content quickly.
        
        Args:
            content: Content to summarize
            max_length: Maximum summary length
            
        Returns:
            Summary
        """
        summarize_prompt = f"""Summarize the following content in no more than {max_length} characters:

{content}"""
        
        return self.execute(summarize_prompt)

    def extract_info(self, content: str, info_type: str) -> str:
        """
        Extract specific information from content.
        
        Args:
            content: Content to extract from
            info_type: Type of information to extract
            
        Returns:
            Extracted information
        """
        extract_prompt = f"""Extract all {info_type} from the following content:

{content}"""
        
        return self.execute(extract_prompt)

    def validate(self, content: str, rules: str) -> str:
        """
        Validate content against rules.
        
        Args:
            content: Content to validate
            rules: Validation rules
            
        Returns:
            Validation results
        """
        validate_prompt = f"""Validate the following content against these rules:

Rules:
{rules}

Content:
{content}

Report any violations."""
        
        return self.execute(validate_prompt)

    def index_content(self, content: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Index content for quick retrieval.
        
        Args:
            content: Content to index
            metadata: Optional metadata
            
        Returns:
            Indexed content
        """
        index_prompt = f"""Create a structured index of the following content:

{content}

Return key topics, keywords, and summary."""
        
        result = self.execute(index_prompt)
        
        return {
            "content": result,
            "metadata": metadata or {},
            "indexed": True
        }

    def parse_document(self, document: str, format_type: str = "auto") -> Dict[str, Any]:
        """
        Parse and structure document content.
        
        Args:
            document: Document content
            format_type: Expected format type
            
        Returns:
            Parsed document structure
        """
        parse_prompt = f"""Parse this document and extract:
- Title
- Sections/headings
- Key points
- Metadata

Document:
{document}"""
        
        result = self.execute(parse_prompt)
        
        return {
            "content": result,
            "format": format_type,
            "parsed": True
        }
