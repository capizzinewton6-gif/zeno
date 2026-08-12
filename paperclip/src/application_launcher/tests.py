"""
application_launcher Tests
===================
Unit tests for application_launcher module.
"""

import pytest
from unittest.mock import Mock, patch

from src.application_launcher.main import ApplicationLauncher, ApplicationLauncherConfig


class TestApplicationLauncher:
    """Test cases for ApplicationLauncher."""

    def setup_method(self):
        """Set up test fixtures."""
        self.config = ApplicationLauncherConfig()
        self.module = ApplicationLauncher(config=self.config)

    def test_initialization(self):
        """Test module initialization."""
        assert self.module is not None
        assert self.module.config.enabled is True

    def test_get_capability_name(self):
        """Test getting capability name."""
        assert self.module.get_capability_name() == "application_launcher"

    def test_execute(self):
        """Test task execution."""
        result = self.module.execute("test task")
        assert result is not None

    def test_process_task(self):
        """Test task processing."""
        result = self.module._process_task("test", None)
        assert "test" in str(result).lower()
