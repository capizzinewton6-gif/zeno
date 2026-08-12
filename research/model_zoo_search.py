"""Model zoo search: search and auto-download pre-trained models."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class ModelCandidate:
    name: str
    source: str  # huggingface | torchhub | ultralytics
    url: str
    task: str = "detection"
    size_mb: float = 0.0


class ModelZooSearch:
    """Search HuggingFace / TorchHub model hubs for pre-trained models."""

    def __init__(self, flash15=None) -> None:
        self._flash15 = flash15

    def search(self, query: str, limit: int = 5) -> List[ModelCandidate]:
        results = self._huggingface(query, limit)
        if results:
            return results
        return self._fallback(query)

    def _huggingface(self, query: str, limit: int) -> List[ModelCandidate]:
        try:
            from huggingface_hub import HfApi  # type: ignore
            api = HfApi()
            models = api.list_models(search=query, limit=limit, sort="downloads",
                                     direction=-1)
            out = []
            for m in models:
                out.append(ModelCandidate(
                    name=m.modelId, source="huggingface",
                    url=f"https://huggingface.co/{m.modelId}",
                    task=getattr(m, "pipeline_tag", "unknown")))
            return out
        except Exception:
            return []

    def _fallback(self, query: str) -> List[ModelCandidate]:
        q = query.lower()
        if "yolo" in q or "detect" in q:
            return [ModelCandidate("ultralytics/yolov8n", "ultralytics",
                                   "https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt",
                                   "detection", 6)]
        if "face" in q:
            return [ModelCandidate("insightface/buffalo_l", "insightface",
                                   "https://github.com/deepinsight/insightface/releases",
                                   "face_recognition")]
        return [ModelCandidate(query, "unknown", "", "unknown")]

    def download(self, candidate: ModelCandidate, dest: str) -> Optional[str]:
        try:
            import urllib.request
            import os
            os.makedirs(dest, exist_ok=True)
            target = os.path.join(dest, candidate.name.replace("/", "_") + ".bin")
            urllib.request.urlretrieve(candidate.url, target)
            return target
        except Exception:
            return None
