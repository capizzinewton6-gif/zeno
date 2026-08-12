"""Privacy scrubber: data retention enforcement and automatic photo scrubbing."""

from __future__ import annotations

import os
import time
from typing import List

from security_compliance.face_anonymizer import FaceAnonymizer


class PrivacyScrubber:
    """Enforce retention limits and strip sensitive data from stored media."""

    def __init__(self, retention_days: int = 30,
                 anonymizer: FaceAnonymizer = FaceAnonymizer()) -> None:
        self.retention_days = retention_days
        self.anonymizer = anonymizer

    def purge_expired(self, directory: str, now: float = None) -> List[str]:
        """Delete files older than retention_days. Returns removed paths."""
        now = now if now is not None else time.time()
        cutoff = now - self.retention_days * 86400.0
        removed: List[str] = []
        if not os.path.isdir(directory):
            return removed
        for name in os.listdir(directory):
            path = os.path.join(directory, name)
            if os.path.isfile(path) and os.path.getmtime(path) < cutoff:
                try:
                    os.remove(path)
                    removed.append(path)
                except OSError:
                    pass
        return removed

    def scrub_image(self, image, face_boxes):
        """Return a copy of image with all detected faces anonymized."""
        return self.anonymizer.anonymize(image, face_boxes)
