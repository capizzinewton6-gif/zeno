"""Camera calibration: lens distortion correction and chessboard calibration."""

from __future__ import annotations

from typing import List, Tuple

import numpy as np


def calibrate_chessboard(object_points: List[np.ndarray], image_points: List[np.ndarray],
                         image_size: Tuple[int, int]) -> dict:
    """Wrapper around cv2.calibrateCamera when OpenCV is available.

    Falls back to a zero-distortion identity intrinsic estimate if OpenCV is
    absent, so the pipeline keeps running in degraded environments.
    """
    try:
        import cv2  # type: ignore
    except Exception:  # pragma: no cover
        w, h = image_size
        focal = 0.7 * max(w, h)
        return {
            "camera_matrix": intrinsic_from_focal(focal, w, h).tolist(),
            "dist_coeffs": np.zeros(5).tolist(),
            "rvecs": [], "tvecs": [], "rms": 0.0, "backend": "fallback",
        }
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(
        object_points, image_points, image_size, None, None)
    return {
        "camera_matrix": mtx.tolist(), "dist_coeffs": dist.tolist(),
        "rvecs": [r.tolist() for r in rvecs],
        "tvecs": [t.tolist() for t in tvecs],
        "rms": float(ret), "backend": "opencv",
    }


def intrinsic_from_focal(focal_px: float, width: int, height: int) -> np.ndarray:
    return np.array([[focal_px, 0, width / 2.0],
                     [0, focal_px, height / 2.0],
                     [0, 0, 1.0]], dtype=np.float32)


def undistort_points(points: np.ndarray, camera_matrix: np.ndarray,
                     dist_coeffs: np.ndarray) -> np.ndarray:
    try:
        import cv2  # type: ignore
        return cv2.undistortPoints(points.reshape(-1, 1, 2), camera_matrix,
                                   dist_coeffs, None, camera_matrix).reshape(-1, 2)
    except Exception:  # pragma: no cover
        return points
