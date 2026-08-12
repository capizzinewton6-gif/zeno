"""AI safety layer: biometric data handling rules and system integrity checks."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class SafetyConfig:
    anonymize_unknown_faces: bool = True
    encrypt_embeddings: bool = True
    max_face_retention_days: int = 30
    require_consent: bool = True
    allow_remote_replay: bool = False
    integrity_checks: bool = True


class SafetyLayer:
    """Enforces biometric handling and system-integrity rules before actions."""

    def __init__(self, config: SafetyConfig = SafetyConfig()) -> None:
        self.config = config
        self.violations: List[str] = []

    def check_biometric_storage(self, embedding_present: bool, consent_given: bool,
                               encrypted: bool) -> bool:
        if embedding_present and self.config.require_consent and not consent_given:
            self.violations.append("biometric_storage: consent missing")
            return False
        if embedding_present and self.config.encrypt_embeddings and not encrypted:
            self.violations.append("biometric_storage: embeddings must be encrypted")
            return False
        return True

    def check_face_publishing(self, is_known: bool, anonymized: bool) -> bool:
        if not is_known and self.config.anonymize_unknown_faces and not anonymized:
            self.violations.append("face_publishing: unknown face must be anonymized")
            return False
        return True

    def check_retention(self, age_days: int) -> bool:
        if age_days > self.config.max_face_retention_days:
            self.violations.append(
                f"retention: record {age_days}d > limit {self.config.max_face_retention_days}d")
            return False
        return True

    def check_integrity(self, checksum_ok: bool) -> bool:
        if self.config.integrity_checks and not checksum_ok:
            self.violations.append("integrity: checksum mismatch")
            return False
        return True

    def clear(self) -> None:
        self.violations.clear()
