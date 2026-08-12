"""Paper reader — read, parse, and extract chemistry papers (ACS, RSC, Wiley).

Uses Gemini 1.5 Flash for fast document/literature processing.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.gemini_15_flash_engine import process as gemini15_process


class PaperReader:
    """Parse chemistry papers and extract structured information."""

    SECTIONS = ["title", "authors", "abstract", "introduction", "methods",
                "results", "discussion", "conclusion", "references"]

    def __init__(self, api_key=None):
        self.api_key = api_key

    def extract_metadata(self, text):
        """Heuristic metadata extraction from raw paper text."""
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        title = lines[0] if lines else ""
        # Try to find abstract
        abstract = ""
        for i, line in enumerate(lines):
            if line.lower().startswith("abstract"):
                abstract = " ".join(lines[i:i + 6])
                break
        return {"title": title, "abstract": abstract[:500], "n_lines": len(lines)}

    def extract_reactions(self, text):
        """Find candidate reaction mentions by keyword scan."""
        keywords = ["yield", "catalyst", "reflux", "rt,", "stirred", "concentrated under",
                    "column chromatography", "NMR", "HRMS"]
        found = {kw: kw in text.lower() for kw in keywords}
        return {"detected_elements": found,
                "likely_contains_procedures": any(found.values())}

    def summarize(self, text):
        """Use Gemini 1.5 Flash to summarize the paper."""
        return gemini15_process(
            "Summarize this chemistry paper, highlighting the key reaction, conditions, and yield.",
            context={"paper_text": text[:8000]}, api_key=self.api_key
        )
