"""Project management capabilities (One Capability = One Module)."""

from .project_manager import ProjectManager
from .task_manager import TaskManager
from .version_manager import VersionManager
from .documentation import Documentation
from .report_generator import ReportGenerator

__all__ = [
    "ProjectManager", "TaskManager", "VersionManager",
    "Documentation", "ReportGenerator",
]
