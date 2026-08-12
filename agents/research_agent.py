"""Research agent: researches PubMed, NCBI, and UniProt."""
from __future__ import annotations

from ai_core.ai_engine import AIEngine


class ResearchAgent:
    def __init__(self, ai: AIEngine | None = None):
        self.ai = ai or AIEngine()

    def search_pubmed(self, query: str, max_results: int = 5) -> dict:
        from research.ncbi_search import NCBISearch
        return NCBISearch().search_pubmed(query, max_results)

    def fetch_genbank(self, accession: str) -> dict:
        from research.ncbi_search import NCBISearch
        return NCBISearch().fetch_genbank(accession)

    def search_uniprot(self, query: str, max_results: int = 5) -> dict:
        from research.uniprot_pdb_search import UniProtPDBSearch
        return UniProtPDBSearch().search_uniprot(query, max_results)

    def search_pdb(self, query: str, max_results: int = 5) -> dict:
        from research.uniprot_pdb_search import UniProtPDBSearch
        return UniProtPDBSearch().search_pdb(query, max_results)

    def read_paper(self, pmid: str) -> dict:
        from research.paper_reader import PaperReader
        return PaperReader.fetch_pubmed_abstract(pmid)

    def summarize_abstract(self, text: str, max_sentences: int = 3) -> str:
        from research.paper_reader import PaperReader
        return PaperReader.summarize(text, max_sentences)

    def search_patents(self, query: str, max_results: int = 5) -> dict:
        from research.patent_search import PatentSearch
        return PatentSearch.search_summary(query, max_results)

    def summarize(self, text: str) -> str:
        return self.ai.fast_parse(text)
