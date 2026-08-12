"""Tracking evaluator: MOTA, MOTP, IDF1 performance scores."""

from __future__ import annotations

from typing import Dict, List, Tuple

import numpy as np

from calculations.bbox_geometry import iou


class TrackingEvaluator:
    """Compute multi-object tracking metrics (MOTA, MOTP, IDF1)."""

    def __init__(self, iou_threshold: float = 0.5) -> None:
        self.iou_threshold = iou_threshold

    def evaluate(self, gt: List[List[Tuple[int, list]]],
                 pred: List[List[Tuple[int, list]]]) -> Dict[str, float]:
        """``gt``/``pred`` are per-frame lists of (track_id, bbox_xyxy)."""
        total_gt = 0
        total_pred = 0
        matches = 0
        iou_sum = 0.0
        for g_frame, p_frame in zip(gt, pred):
            total_gt += len(g_frame)
            total_pred += len(p_frame)
            matched_g, matched_p = set(), set()
            for gi, (gid, gbox) in enumerate(g_frame):
                best_iou, best_pi = 0.0, -1
                for pi, (pid, pbox) in enumerate(p_frame):
                    if pi in matched_p:
                        continue
                    cur = iou(gbox, pbox)
                    if cur > best_iou:
                        best_iou, best_pi = cur, pi
                if best_pi >= 0 and best_iou >= self.iou_threshold:
                    matches += 1
                    iou_sum += best_iou
                    matched_g.add(gi)
                    matched_p.add(best_pi)
        misses = total_gt - matches
        false_pos = total_pred - matches
        mota = 1.0 - (misses + false_pos) / max(total_gt, 1)
        motp = iou_sum / max(matches, 1)
        idf1 = matches / max(total_gt + total_pred - matches, 1)
        return {"MOTA": float(mota), "MOTP": float(motp),
                "IDF1": float(idf1), "matches": float(matches),
                "misses": float(misses), "false_positives": float(false_pos)}
