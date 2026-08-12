"""Bounding box geometry: IoU, Generalized IoU, box overlap math."""

from __future__ import annotations

from typing import Sequence

import numpy as np


def _pair(box: Sequence[float]):
    x1, y1, x2, y2 = float(box[0]), float(box[1]), float(box[2]), float(box[3])
    if x2 < x1:
        x1, x2 = x2, x1
    if y2 < y1:
        y1, y2 = y2, y1
    return x1, y1, x2, y2


def intersection_area(a: Sequence[float], b: Sequence[float]) -> float:
    ax1, ay1, ax2, ay2 = _pair(a)
    bx1, by1, bx2, by2 = _pair(b)
    ix1, iy1 = max(ax1, bx1), max(ay1, by1)
    ix2, iy2 = min(ax2, bx2), min(ay2, by2)
    iw, ih = max(0.0, ix2 - ix1), max(0.0, iy2 - iy1)
    return iw * ih


def union_area(a: Sequence[float], b: Sequence[float]) -> float:
    ax1, ay1, ax2, ay2 = _pair(a)
    bx1, by1, bx2, by2 = _pair(b)
    area_a = max(0.0, ax2 - ax1) * max(0.0, ay2 - ay1)
    area_b = max(0.0, bx2 - bx1) * max(0.0, by2 - by1)
    return area_a + area_b - intersection_area(a, b)


def iou(a: Sequence[float], b: Sequence[float]) -> float:
    u = union_area(a, b)
    if u <= 0:
        return 0.0
    return intersection_area(a, b) / u


def generalized_iou(a: Sequence[float], b: Sequence[float]) -> float:
    """GIoU in [-1, 1]. Penalizes boxes that are far apart."""
    ax1, ay1, ax2, ay2 = _pair(a)
    bx1, by1, bx2, by2 = _pair(b)
    inter = intersection_area(a, b)
    uni = union_area(a, b)
    if uni <= 0:
        return 0.0
    enc_x1, enc_y1 = min(ax1, bx1), min(ay1, by1)
    enc_x2, enc_y2 = max(ax2, bx2), max(ay2, by2)
    enc_area = max(0.0, enc_x2 - enc_x1) * max(0.0, enc_y2 - enc_y1)
    return (inter / uni) - (enc_area - uni) / enc_area if enc_area > 0 else inter / uni


def pairwise_iou_matrix(boxes_a: np.ndarray, boxes_b: np.ndarray) -> np.ndarray:
    """Compute (M x N) IoU matrix between two sets of xyxy boxes."""
    a = np.asarray(boxes_a, dtype=np.float32)
    b = np.asarray(boxes_b, dtype=np.float32)
    if a.size == 0 or b.size == 0:
        return np.zeros((a.shape[0], b.shape[0]), dtype=np.float32)
    a = a[:, None, :]  # (M,1,4)
    b = b[None, :, :]  # (1,N,4)
    x1 = np.maximum(a[..., 0], b[..., 0])
    y1 = np.maximum(a[..., 1], b[..., 1])
    x2 = np.minimum(a[..., 2], b[..., 2])
    y2 = np.minimum(a[..., 3], b[..., 3])
    inter = np.clip(x2 - x1, 0, None) * np.clip(y2 - y1, 0, None)
    area_a = np.clip(a[..., 2] - a[..., 0], 0, None) * np.clip(a[..., 3] - a[..., 1], 0, None)
    area_b = np.clip(b[..., 2] - b[..., 0], 0, None) * np.clip(b[..., 3] - b[..., 1], 0, None)
    union = area_a + area_b - inter
    return np.where(union > 0, inter / union, 0.0)
