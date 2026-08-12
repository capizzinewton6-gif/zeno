"""Standardized benchmarking against COCO, LFW, WIDER FACE."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Dict, List

from calculations.bbox_geometry import iou


@dataclass
class BenchmarkResult:
    dataset: str
    precision: float = 0.0
    recall: float = 0.0
    f1: float = 0.0
    map50: float = 0.0
    samples: int = 0


class BenchmarkRunner:
    """Run a detector against a labeled dataset and compute detection metrics."""

    def __init__(self, iou_threshold: float = 0.5) -> None:
        self.iou_threshold = iou_threshold

    def run(self, dataset: str, predict_fn: Callable,
            samples: List[dict]) -> BenchmarkResult:
        tp = fp = fn = 0
        ap_sum = 0.0
        for sample in samples:
            preds = predict_fn(sample["image"])
            gts = sample.get("boxes", [])
            matched_g = set()
            for p in preds:
                best_iou, best_g = 0.0, -1
                for gi, g in enumerate(gts):
                    if gi in matched_g:
                        continue
                    cur = iou(p, g)
                    if cur > best_iou:
                        best_iou, best_g = cur, gi
                if best_g >= 0 and best_iou >= self.iou_threshold:
                    tp += 1
                    matched_g.add(best_g)
                else:
                    fp += 1
            fn += len(gts) - len(matched_g)
            ap_sum += len(matched_g) / max(len(gts) + fp - len(matched_g), 1)
        precision = tp / max(tp + fp, 1)
        recall = tp / max(tp + fn, 1)
        f1 = 2 * precision * recall / max(precision + recall, 1e-6)
        return BenchmarkResult(dataset=dataset, precision=precision, recall=recall,
                               f1=f1, map50=ap_sum / max(len(samples), 1),
                               samples=len(samples))
