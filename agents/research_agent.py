"""Research agent — researches literature, patents, and databases."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from research import PubChemSearch, ReactionSearch, PaperReader, PatentSearch, ReferenceManager
from src.gemini_15_flash_engine import process as gemini15_process


class ResearchAgent:
    """Orchestrate literature and database research."""

    def __init__(self, api_key=None):
        self.api_key = api_key
        self.pubchem = PubChemSearch()
        self.reactions = ReactionSearch(api_key=api_key)
        self.papers = PaperReader(api_key=api_key)
        self.patents = PatentSearch()
        self.refs = ReferenceManager()

    def handle(self, request):
        task = request.get("task", "")
        params = request.get("params", {}) or {}
        text = task.lower()
        if "pubchem" in text or "compound" in text or "property" in text:
            name = params.get("name", params.get("compound", "aspirin"))
            return {"agent": "ResearchAgent", "capability": "pubchem",
                    "result": self.pubchem.by_name(name)}
        if "reaction" in text:
            q = params.get("query", params.get("name", "Suzuki"))
            return {"agent": "ResearchAgent", "capability": "reaction_search",
                    "result": self.reactions.search_by_name(q)}
        if "patent" in text:
            q = params.get("query", task)
            return {"agent": "ResearchAgent", "capability": "patent_search",
                    "result": self.patents.search_uspto(q)}
        if "paper" in text or "literature" in text:
            text_body = params.get("text", "")
            return {"agent": "ResearchAgent", "capability": "paper_reader",
                    "result": (self.papers.summarize(text_body) if text_body
                               else self.papers.extract_metadata(task))}
        return {"agent": "ResearchAgent", "capability": "general_research",
                "result": gemini15_process(task, context=params, api_key=self.api_key)}
