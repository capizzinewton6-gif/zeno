"""Automatic package import resolver."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

from repository_workspace.symbol_indexer import SymbolIndex, SymbolIndexer


@dataclass
class ImportSuggestion:
    statement: str
    symbol: str
    module: str
    confidence: float = 1.0


class AutoImporter:
    """Suggests and inserts missing imports."""

    # Built-in / common module maps per symbol (extensible)
    COMMON_PYTHON: dict[str, str] = {
        "Path": "pathlib", "dataclass": "dataclasses", "field": "dataclasses",
        "Any": "typing", "Optional": "typing", "List": "typing",
        "Dict": "typing", "Tuple": "typing", "Union": "typing",
        "Enum": "enum", "abstractmethod": "abc", "ABC": "abc",
        "wraps": "functools", "partial": "functools", "lru_cache": "functools",
        "datetime": "datetime", "timezone": "datetime",
        "Counter": "collections", "defaultdict": "collections", "deque": "collections",
        "json": "json", "os": "os", "sys": "sys", "re": "re",
        "math": "math", "time": "time", "logging": "logging",
        "argparse": "argparse", "subprocess": "subprocess",
        "unittest": "unittest", "pytest": "pytest",
    }

    def __init__(self, indexer: SymbolIndexer | None = None) -> None:
        self.indexer = indexer

    def suggest(self, source: str, language: str = "python",
                index: SymbolIndex | None = None) -> list[ImportSuggestion]:
        if language.lower() != "python":
            return []
        used = set(self._extract_names(source, language))
        existing = set(self._existing_imports(source))
        missing = used - existing - set(self.BUILTIN_PYTHON_RESERVED)
        suggestions: list[ImportSuggestion] = []
        for name in missing:
            if name in self.COMMON_PYTHON:
                mod = self.COMMON_PYTHON[name]
                suggestions.append(ImportSuggestion(
                    statement=f"from {mod} import {name}" if mod != name else f"import {mod}",
                    symbol=name, module=mod))
            elif index and index.lookup(name):
                loc = index.lookup(name)[0]
                suggestions.append(ImportSuggestion(
                    statement=f"# defined in {loc.file}:{loc.line}", symbol=name,
                    module=loc.file, confidence=0.5))
        return suggestions

    def apply(self, source: str, suggestions: list[ImportSuggestion],
              language: str = "python") -> str:
        if not suggestions:
            return source
        lines = source.splitlines()
        # Find insertion point (after existing imports)
        insert_at = 0
        for i, line in enumerate(lines):
            if line.startswith(("import ", "from ")):
                insert_at = i + 1
            elif line.strip() and not line.startswith("#") and insert_at:
                break
        new_imports = [s.statement for s in suggestions if s.statement and not s.statement.startswith("#")]
        return "\n".join(lines[:insert_at] + new_imports + lines[insert_at:]) + "\n"

    def _extract_names(self, source: str, language: str) -> list[str]:
        return re.findall(r"\b([A-Z][a-zA-Z0-9_]*)\b", source)

    def _existing_imports(self, source: str) -> list[str]:
        out: list[str] = []
        for line in source.splitlines():
            if line.startswith("from "):
                m = re.match(r"from\s+\S+\s+import\s+(.+)", line)
                if m:
                    out.extend(n.strip() for n in m.group(1).split(","))
            elif line.startswith("import "):
                m = re.match(r"import\s+(\S+)", line)
                if m:
                    out.append(m.group(1).split(".")[-1])
        return out

    BUILTIN_PYTHON_RESERVED = {
        "True", "False", "None", "self", "cls", "int", "str", "float", "bool",
        "list", "dict", "set", "tuple", "bytes", "range", "len", "print",
        "Exception", "ValueError", "TypeError", "KeyError", "IndexError",
        "AttributeError", "RuntimeError", "StopIteration", "NotImplemented",
    }
