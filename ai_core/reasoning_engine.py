"""Reasoning engine: spatial and temporal reasoning, behavior and anomaly detection."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ai_core.context_manager import ContextManager


@dataclass
class ReasoningResult:
    findings: List[str]
    anomalies: List[str]
    behaviors: List[str]
    raw: Dict[str, Any]


class ReasoningEngine:
    """Local heuristics over the rolling context window.

    For deep semantic reasoning the AI engine delegates to Gemini 2.5 Flash; this
    module provides fast, deterministic spatial/temporal reasoning that does not
    require a network round-trip.
    """

    def __init__(self, context: ContextManager) -> None:
        self.context = context

    def reason(self) -> ReasoningResult:
        findings: List[str] = []
        anomalies: List[str] = []
        behaviors: List[str] = []

        history = self.context.history
        if not history:
            return ReasoningResult(findings=["No frames in context."], anomalies=[],
                                   behaviors=[], raw={"frame_count": 0})

        counts = self.context.label_counts()
        for label, n in counts.items():
            findings.append(f"{label} appeared {n} time(s) in the last {len(history)} frames.")

        anomalies.extend(self._detect_sudden_changes(history))
        behaviors.extend(self._detect_persistence(counts, history))
        return ReasoningResult(findings=findings, anomalies=anomalies,
                               behaviors=behaviors,
                               raw={"frame_count": len(history), "label_counts": counts})

    def _detect_sudden_changes(self, history) -> List[str]:
        if len(history) < 2:
            return []
        prev_labels = {d["label"] for d in history[-2].detections}
        curr_labels = {d["label"] for d in history[-1].detections}
        appeared = curr_labels - prev_labels
        disappeared = prev_labels - curr_labels
        out = []
        if appeared:
            out.append(f"Sudden appearance: {sorted(appeared)}")
        if disappeared:
            out.append(f"Sudden disappearance: {sorted(disappeared)}")
        return out

    def _detect_persistence(self, counts, history) -> List[str]:
        out: List[str] = []
        threshold = max(2, len(history) // 2)
        for label, n in counts.items():
            if n >= threshold:
                out.append(f"Persistent presence: {label} ({n}/{len(history)} frames)")
        return out
