"""Parse PDF/TeX physics papers, extract Hamiltonians and results."""

from __future__ import annotations

import re

from vision.equation_reader import EquationReader


class PaperReader:
    """Lightweight text-based paper parsing (no PDF dependency required)."""

    HAMILTONIAN_PATTERNS = [
        re.compile(r"H\s*=\s*([^,;\n]+)"),
        re.compile(r"\\mathcal\{H\}\s*=\s*([^,;\n]+)"),
        re.compile(r"H_\\text\{[^}]*\}\s*=\s*([^,;\n]+)"),
    ]

    @staticmethod
    def extract_hamiltonians(text: str) -> list[str]:
        results = []
        for pat in PaperReader.HAMILTONIAN_PATTERNS:
            for m in pat.findall(text):
                results.append(m.strip())
        return results

    @staticmethod
    def extract_abstract(text: str) -> str:
        m = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", text, re.DOTALL)
        return m.group(1).strip() if m else ""

    @staticmethod
    def extract_equations(text: str) -> list[str]:
        return re.findall(r"\\begin\{equation\}(.*?)\\end\{equation\}", text, re.DOTALL)

    @staticmethod
    def extract_citations(text: str) -> list[str]:
        return re.findall(r"\\cite\{([^}]+)\}", text)
