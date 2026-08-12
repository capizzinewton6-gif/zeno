"""Landmark transforms: similarity/affine/perspective matrices for face alignment."""

from __future__ import annotations

from typing import Sequence

import numpy as np

# Standard ArcFace 5-point template (112x112 aligned face)
ARCFACE_TEMPLATE = np.array([
    [38.2946, 51.6963],
    [73.5318, 51.5014],
    [56.0252, 71.7366],
    [41.5493, 92.3655],
    [70.7299, 92.2041],
], dtype=np.float32)


def umeyama(src: np.ndarray, dst: np.ndarray, scale: bool = True) -> np.ndarray:
    """Compute a similarity transform (2x3) mapping src points to dst points."""
    src = np.asarray(src, dtype=np.float64)
    dst = np.asarray(dst, dtype=np.float64)
    assert src.shape == dst.shape and src.shape[0] >= 2
    src_mean = src.mean(axis=0)
    dst_mean = dst.mean(axis=0)
    src_centered = src - src_mean
    dst_centered = dst - dst_mean
    cov = (src_centered.T @ dst_centered) / src.shape[0]
    u, _, vt = np.linalg.svd(cov)
    d = np.sign(np.linalg.det(u) * np.linalg.det(vt))
    s = np.ones(src.shape[1])
    s[-1] = d
    r = (u * s) @ vt
    if scale:
        src_var = (src_centered ** 2).sum(axis=0).mean()
        c = np.trace(r @ cov.T) / src_var if src_var > 0 else 1.0
    else:
        c = 1.0
    t = dst_mean - c * r @ src_mean
    m = np.hstack([c * r, t.reshape(2, 1)])
    return m.astype(np.float32)


def align_points(points: Sequence[Sequence[float]],
                 template: np.ndarray = ARCFACE_TEMPLATE,
                 output_size: int = 112) -> np.ndarray:
    """Return the 2x3 affine matrix to align 5 landmarks to the template."""
    src = np.asarray(points, dtype=np.float32)
    if src.shape[0] != template.shape[0]:
        raise ValueError(f"Expected {template.shape[0]} landmarks, got {src.shape[0]}")
    scale = output_size / 112.0
    scaled_template = template * scale
    return umeyama(src, scaled_template, scale=True)


def perspective_matrix(src: np.ndarray, dst: np.ndarray) -> np.ndarray:
    """3x3 perspective transform mapping src (4 points) to dst (4 points)."""
    src = np.asarray(src, dtype=np.float32)
    dst = np.asarray(dst, dtype=np.float32)
    assert src.shape == dst.shape == (4, 2)
    a = np.zeros((8, 8), dtype=np.float32)
    b = np.zeros(8, dtype=np.float32)
    for i in range(4):
        x, y = src[i]
        xp, yp = dst[i]
        a[i] = [x, y, 1, 0, 0, 0, -x * xp, -y * xp]
        a[i + 4] = [0, 0, 0, x, y, 1, -x * yp, -y * yp]
        b[i] = xp
        b[i + 4] = yp
    h = np.linalg.solve(a, b)
    return np.append(h, 1.0).reshape(3, 3).astype(np.float32)
