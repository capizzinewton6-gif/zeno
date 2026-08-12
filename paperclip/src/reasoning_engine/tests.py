"""
reasoning_engine Tests
===================
Unit tests for reasoning_engine module.
"""

import pytest
from unittest.mock import Mock, patch

from src.reasoning_engine.main import ReasoningEngine, ReasoningEngineConfig


class TestReasoningEngine:
    """Test cases for ReasoningEngine."""

    def setup_method(self):
        """Set up test fixtures."""
        self.config = ReasoningEngineConfig()
        self.module = ReasoningEngine(config=self.config)

    def test_initialization(self):
        """Test module initialization."""
        assert self.module is not None
        assert self.module.config.enabled is True

    def test_get_capability_name(self):
        """Test getting capability name."""
        assert self.module.get_capability_name() == "reasoning_engine"

    def test_execute(self):
        """Test task execution."""
        result = self.module.execute("test task")
        assert result is not None

    def test_process_task(self):
        """Test task processing."""
        result = self.module._process_task("test", None)
        assert "test" in str(result).lower()
