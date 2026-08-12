"""Report generator: detection accuracy and throughput analytics reports."""

from __future__ import annotations

import json
import os
from datetime import datetime
from typing import Dict, Optional

from tools.data_analyzer import DataAnalyzer, TrendReport
from tools.plot_generator import PlotGenerator


class ReportGenerator:
    """Compose text/JSON analytics reports from analyzer + telemetry."""

    def __init__(self, analyzer: Optional[DataAnalyzer] = None) -> None:
        self.analyzer = analyzer or DataAnalyzer()

    def add(self, detections) -> None:
        self.analyzer.add(detections)

    def text_report(self) -> str:
        r = self.analyzer.report()
        lines = [
            "=== Vision AI Analytics Report ===",
            f"Generated: {datetime.utcnow().isoformat()}",
            f"Total detections: {r.total_detections}",
            f"Average confidence: {r.avg_confidence:.3f}",
            "",
            "Label counts:",
        ]
        for label, n in sorted(r.label_counts.items(), key=lambda kv: kv[1], reverse=True):
            lines.append(f"  {label:<20} {n}")
        lines.append("")
        lines.append("Confidence histogram:")
        hist = self.analyzer.confidence_histogram(10)
        for i, c in enumerate(hist):
            lines.append(f"  {i/10:.1f}-{(i+1)/10:.1f}: {'#' * c} ({c})")
        return "\n".join(lines)

    def json_report(self) -> Dict:
        r = self.analyzer.report()
        return {
            "generated_at": datetime.utcnow().isoformat(),
            "total_detections": r.total_detections,
            "average_confidence": r.avg_confidence,
            "label_counts": r.label_counts,
            "confidence_histogram": self.analyzer.confidence_histogram(10),
            "per_frame": r.per_frame,
        }

    def save(self, path: str) -> str:
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "w") as f:
            json.dump(self.json_report(), f, indent=2)
        return path
