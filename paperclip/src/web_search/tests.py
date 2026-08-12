"""
web_search Tests
===================
Unit tests for web_search module.
"""

import pytest
from unittest.mock import Mock, patch

from src.web_search.main import WebSearch, WebSearchConfig


class TestWebSearch:
    """Test cases for WebSearch."""

    def setup_method(self):
        """Set up test fixtures."""
        self.config = WebSearchConfig()
        self.module = WebSearch(config=self.config)

    def test_initialization(self):
        """Test module initialization."""
        assert self.module is not None
        assert self.module.config.enabled is True

    def test_get_capability_name(self):
        """Test getting capability name."""
        assert self.module.get_capability_name() == "web_search"

    def test_execute(self):
        """Test task execution."""
        result = self.module.execute("test task")
        assert result is not None

    def test_process_task(self):
        """Test task processing."""
        result = self.module._process_task("test", None)
        assert "test" in str(result).lower()
