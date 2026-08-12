"""
performance_monitoring Tests
===================
Unit tests for performance_monitoring module.
"""

import pytest
from unittest.mock import Mock, patch

from src.performance_monitoring.main import PerformanceMonitoring, PerformanceMonitoringConfig


class TestPerformanceMonitoring:
    """Test cases for PerformanceMonitoring."""

    def setup_method(self):
        """Set up test fixtures."""
        self.config = PerformanceMonitoringConfig()
        self.module = PerformanceMonitoring(config=self.config)

    def test_initialization(self):
        """Test module initialization."""
        assert self.module is not None
        assert self.module.config.enabled is True

    def test_get_capability_name(self):
        """Test getting capability name."""
        assert self.module.get_capability_name() == "performance_monitoring"

    def test_execute(self):
        """Test task execution."""
        result = self.module.execute("test task")
        assert result is not None

    def test_process_task(self):
        """Test task processing."""
        result = self.module._process_task("test", None)
        assert "test" in str(result).lower()
