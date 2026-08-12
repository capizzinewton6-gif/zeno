"""Discovers open-source coding models on HuggingFace."""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any

from capabilities.terminal_execution import TerminalExecution
from modeling.neural_backbones import NeuralBackbone, get_backbone


@dataclass
class ModelInfo:
    name: str
    author: str
    downloads: int = 0
    likes: int = 0
    tags: list[str] = field(default_factory=list)
    pipeline_tag: str = ""
    url: str = ""


@dataclass
class ModelSearchResult:
    query: str
    models: list[ModelInfo] = field(default_factory=list)
    error: str = ""


HF_API = "https://huggingface.co/api/models"


class ModelZooSearch:
    """Search the HuggingFace Hub for coding-capable models."""

    CODING_KEYWORDS = ("code", "coding", "python", "instruct", "coder", "starcoder")

    def __init__(self, terminal: TerminalExecution | None = None,
                 backbone: NeuralBackbone | None = None) -> None:
        self.terminal = terminal or TerminalExecution()
        self.backbone = backbone or get_backbone()

    def search(self, query: str, limit: int = 20) -> ModelSearchResult:
        import urllib.parse
        params = urllib.parse.urlencode({"search": query, "limit": limit,
                                         "full": "true"})
        url = f"{HF_API}?{params}"
        try:
            import urllib.request
            with urllib.request.urlopen(url, timeout=30) as resp:  # pragma: no cover - network
                data = json.loads(resp.read().decode())
        except Exception as exc:
            return ModelSearchResult(query=query, error=str(exc))
        models = [self._parse(m) for m in data]
        return ModelSearchResult(query=query, models=models)

    def recommend_coding_models(self, limit: int = 10) -> list[ModelInfo]:
        results: list[ModelInfo] = []
        for kw in self.CODING_KEYWORDS:
            res = self.search(kw, limit=limit)
            if res.models:
                results.extend(res.models)
            if len(results) >= limit:
                break
        # de-dupe by name
        seen: set[str] = set()
        unique: list[ModelInfo] = []
        for m in results:
            if m.name not in seen:
                seen.add(m.name)
                unique.append(m)
        return sorted(unique, key=lambda m: m.downloads, reverse=True)[:limit]

    def _parse(self, data: dict[str, Any]) -> ModelInfo:
        return ModelInfo(
            name=data.get("id", data.get("name", "")),
            author=data.get("author", ""),
            downloads=data.get("downloads", 0),
            likes=data.get("likes", 0),
            tags=data.get("tags", []),
            pipeline_tag=data.get("pipeline_tag", ""),
            url=f"https://huggingface.co/{data.get('id', '')}",
        )
