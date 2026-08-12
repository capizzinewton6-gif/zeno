"""Read and parse biological papers (bioRxiv, Nature)."""
from __future__ import annotations

import re

try:
    from Bio import Entrez  # type: ignore
    _HAS_ENTREZ = True
except Exception:
    _HAS_ENTREZ = False


class PaperReader:
    @staticmethod
    def parse_abstract(text: str) -> dict:
        """Extract structured fields from a PubMed-style abstract."""
        sections = {}
        current = "abstract"
        for line in text.splitlines():
            m = re.match(r"^([A-Z][A-Za-z ]+):\s*(.*)$", line)
            if m and len(m.group(1)) < 40:
                current = m.group(1).lower().strip()
                sections[current] = m.group(2).strip()
            else:
                sections.setdefault(current, "")
                if sections[current]:
                    sections[current] += " " + line.strip()
                else:
                    sections[current] = line.strip()
        return sections

    @staticmethod
    def extract_keywords(text: str, top_n: int = 20) -> list[tuple[str, int]]:
        """Simple frequency-based keyword extraction (stopwords excluded)."""
        stopwords = {"the", "a", "an", "and", "of", "in", "to", "with", "for",
                     "is", "are", "was", "were", "by", "on", "as", "at", "this",
                     "that", "we", "our", "their", "from", "or", "be", "using",
                     "used", "use", "these", "such", "not", "but", "which"}
        words = re.findall(r"[A-Za-z]{4,}", text.lower())
        freq = {}
        for w in words:
            if w in stopwords:
                continue
            freq[w] = freq.get(w, 0) + 1
        return sorted(freq.items(), key=lambda x: -x[1])[:top_n]

    @staticmethod
    def summarize(text: str, max_sentences: int = 3) -> str:
        """Extractive summary: first sentences up to a limit."""
        sentences = re.split(r"(?<=[.!?])\s+", text)
        return " ".join(sentences[:max_sentences])

    @staticmethod
    def fetch_pubmed_abstract(pmid: str, email: str = "biology-ai@example.com") -> dict:
        if not _HAS_ENTREZ:
            return {"status": "offline", "note": "Biopython Entrez not available."}
        try:
            Entrez.email = email
            handle = Entrez.efetch(db="pubmed", id=pmid, rettype="abstract", retmode="text")
            text = handle.read()
            handle.close()
            return {"pmid": pmid, "abstract": text,
                    "parsed": PaperReader.parse_abstract(text)}
        except Exception as e:
            return {"pmid": pmid, "error": str(e)}
