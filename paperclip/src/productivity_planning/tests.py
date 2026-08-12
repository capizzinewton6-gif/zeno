"""
productivity_planning Tests
===================
Unit tests for productivity_planning module.
"""

import pytest
from unittest.mock import Mock, patch

from src.productivity_planning.main import ProductivityPlanning, ProductivityPlanningConfig


class TestProductivityPlanning:
    """Test cases for ProductivityPlanning."""

    def setup_method(self):
        """Set up test fixtures."""
        self.config = ProductivityPlanningConfig()
        self.module = ProductivityPlanning(config=self.config)

    def test_initialization(self):
        """Test module initialization."""
        assert self.module is not None
        assert self.module.config.enabled is True

    def test_get_capability_name(self):
        """Test getting capability name."""
        assert self.module.get_capability_name() == "productivity_planning"

    def test_execute(self):
        """Test task execution."""
        result = self.module.execute("test task")
        assert result is not None

    def test_process_task(self):
        """Test task processing."""
        result = self.module._process_task("test", None)
        assert "test" in str(result).lower()
