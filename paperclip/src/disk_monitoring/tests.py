"""
disk_monitoring Tests
===================
Unit tests for disk_monitoring module.
"""

import pytest
from unittest.mock import Mock, patch

from src.disk_monitoring.main import DiskMonitoring, DiskMonitoringConfig


class TestDiskMonitoring:
    """Test cases for DiskMonitoring."""

    def setup_method(self):
        """Set up test fixtures."""
        self.config = DiskMonitoringConfig()
        self.module = DiskMonitoring(config=self.config)

    def test_initialization(self):
        """Test module initialization."""
        assert self.module is not None
        assert self.module.config.enabled is True

    def test_get_capability_name(self):
        """Test getting capability name."""
        assert self.module.get_capability_name() == "disk_monitoring"

    def test_execute(self):
        """Test task execution."""
        result = self.module.execute("test task")
        assert result is not None

    def test_process_task(self):
        """Test task processing."""
        result = self.module._process_task("test", None)
        assert "test" in str(result).lower()
