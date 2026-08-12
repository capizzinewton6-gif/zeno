"""
task_organization Tests
===================
Unit tests for task_organization module.
"""

import pytest
from unittest.mock import Mock, patch

from src.task_organization.main import TaskOrganization, TaskOrganizationConfig


class TestTaskOrganization:
    """Test cases for TaskOrganization."""

    def setup_method(self):
        """Set up test fixtures."""
        self.config = TaskOrganizationConfig()
        self.module = TaskOrganization(config=self.config)

    def test_initialization(self):
        """Test module initialization."""
        assert self.module is not None
        assert self.module.config.enabled is True

    def test_get_capability_name(self):
        """Test getting capability name."""
        assert self.module.get_capability_name() == "task_organization"

    def test_execute(self):
        """Test task execution."""
        result = self.module.execute("test task")
        assert result is not None

    def test_process_task(self):
        """Test task processing."""
        result = self.module._process_task("test", None)
        assert "test" in str(result).lower()
