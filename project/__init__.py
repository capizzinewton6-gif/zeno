"""project package — research, task, notebook, documentation, paper management."""

from .research_manager import ResearchManager
from .task_manager import TaskManager
from .notebook_manager import NotebookManager
from .documentation import Documentation
from .paper_generator import PaperGenerator

__all__ = [
    "ResearchManager", "TaskManager", "NotebookManager",
    "Documentation", "PaperGenerator",
]
