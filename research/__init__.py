"""Research capabilities (One Capability = One Module)."""

from .web_search import WebSearch
from .patent_search import PatentSearch
from .paper_reader import PaperReader
from .technology_search import TechnologySearch
from .reference_manager import ReferenceManager

__all__ = [
    "WebSearch", "PatentSearch", "PaperReader",
    "TechnologySearch", "ReferenceManager",
]
