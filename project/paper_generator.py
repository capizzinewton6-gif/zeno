"""Paper generator — generate publication-ready manuscripts (ACS format)."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.gemini_25_flash_engine import reason as gemini25_reason


class PaperGenerator:
    """Generate ACS-format manuscript drafts."""

    SECTIONS = ["Title", "Authors", "Abstract", "Introduction", "Results and Discussion",
                "Conclusion", "Experimental Section", "References", "Supporting Information"]

    def __init__(self, api_key=None):
        self.api_key = api_key

    def generate(self, title, authors, abstract, results, experimental, references=None):
        manuscript = {
            "format": "ACS",
            "title": title,
            "authors": authors,
            "abstract": abstract,
            "introduction": "(Auto-generated context — refine with literature.)",
            "results_and_discussion": results,
            "conclusion": "(Auto-generated conclusion — summarize key findings.)",
            "experimental_section": experimental,
            "references": references or [],
        }
        # Optionally enrich narrative with Gemini 2.5 Flash
        enriched = gemini25_reason(
            f"Draft an ACS-style Results & Discussion section for: {title}",
            context={"abstract": abstract, "results": results}, api_key=self.api_key
        )
        manuscript["ai_draft_assist"] = enriched
        return manuscript

    def to_markdown(self, manuscript):
        lines = [
            f"# {manuscript['title']}",
            "",
            f"**Authors:** {', '.join(manuscript['authors'])}",
            "",
            "## Abstract",
            manuscript["abstract"],
            "",
            "## Introduction",
            manuscript["introduction"],
            "",
            "## Results and Discussion",
            manuscript["results_and_discussion"],
            "",
            "## Conclusion",
            manuscript["conclusion"],
            "",
            "## Experimental Section",
            manuscript["experimental_section"],
            "",
            "## References",
        ]
        for i, ref in enumerate(manuscript["references"], 1):
            lines.append(f"{i}. {ref}")
        return "\n".join(lines)
