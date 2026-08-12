"""Image quality checker: blur, low exposure, glare, frame corruption."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class QualityReport:
    is_acceptable: bool
    blur_score: float
    exposure: float
    glare: float
    issues: list


class ImageQualityChecker:
    """Cheap, local image-quality gate used before heavy processing."""

    def __init__(self, blur_threshold: float = 80.0,
                 low_exposure: float = 40.0, high_exposure: float = 220.0,
                 glare_ratio: float = 0.15) -> None:
        self.blur_threshold = blur_threshold
        self.low_exposure = low_exposure
        self.high_exposure = high_exposure
        self.glare_ratio = glare_ratio

    def check(self, image: np.ndarray) -> QualityReport:
        issues = []
        if image is None or image.size == 0:
            return QualityReport(False, 0, 0, 0, ["empty_or_corrupt_frame"])
        gray = image.mean(axis=2) if image.ndim == 3 else image
        blur = self._laplacian_variance(image)
        exposure = float(gray.mean())
        glare = float(np.mean(gray > 240))
        if blur < self.blur_threshold:
            issues.append("blurry")
        if exposure < self.low_exposure:
            issues.append("underexposed")
        elif exposure > self.high_exposure:
            issues.append("overexposed")
        if glare > self.glare_ratio:
            issues.append("glare")
        return QualityReport(is_acceptable=not issues, blur_score=blur,
                             exposure=exposure, glare=glare, issues=issues)

    @staticmethod
    def _laplacian_variance(image: np.ndarray) -> float:
        try:
            import cv2  # type: ignore
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if image.ndim == 3 else image
            return float(cv2.Laplacian(gray, cv2.CV_64F).var())
        except Exception:
            return float(np.var(image))
