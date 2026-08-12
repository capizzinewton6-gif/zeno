"""
natural_language_understanding Tests
===================
Unit tests for natural_language_understanding module.
"""

import pytest
from unittest.mock import Mock, patch

from src.natural_language_understanding.main import NaturalLanguageUnderstanding, NaturalLanguageUnderstandingConfig


class TestNaturalLanguageUnderstanding:
    """Test cases for NaturalLanguageUnderstanding."""

    def setup_method(self):
        """Set up test fixtures."""
        self.config = NaturalLanguageUnderstandingConfig()
        self.module = NaturalLanguageUnderstanding(config=self.config)

    def test_initialization(self):
        """Test module initialization."""
        assert self.module is not None
        assert self.module.config.enabled is True

    def test_get_capability_name(self):
        """Test getting capability name."""
        assert self.module.get_capability_name() == "natural_language_understanding"

    def test_execute(self):
        """Test task execution."""
        result = self.module.execute("test task")
        assert result is not None

    def test_process_task(self):
        """Test task processing."""
        result = self.module._process_task("test", None)
        assert "test" in str(result).lower()
