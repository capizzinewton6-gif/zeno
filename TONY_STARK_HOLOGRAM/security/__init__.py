"""security package - auto-registers its capability modules."""

from typing import Any, Dict, List

# Per-module imports (kept explicit so a failing import does not break
# the whole package).
from .biometric_lock import BiometricLock
from .encrypted_channel import EncryptedChannel
from .holographic_watermark import HolographicWatermark
from .session_security import SessionSecurity
from .tamper_detection import TamperDetection
from .user_authentication import UserAuthentication


def list_modules() -> List[str]:
    """Return the capability names registered in this package."""
    return [
        "biometric_lock",
        "encrypted_channel",
        "holographic_watermark",
        "session_security",
        "tamper_detection",
        "user_authentication",
    ]


def instantiate_all(config: Dict[str, Any] = None) -> Dict[str, Any]:
    """Instantiate every module in this package and return name->instance."""
    return {
        name: cls(config=config)
        for name, cls in (
            ("biometric_lock", BiometricLock),
            ("encrypted_channel", EncryptedChannel),
            ("holographic_watermark", HolographicWatermark),
            ("session_security", SessionSecurity),
            ("tamper_detection", TamperDetection),
            ("user_authentication", UserAuthentication),
        )
    }


__all__ = ["list_modules", "instantiate_all", "BiometricLock", "EncryptedChannel", "HolographicWatermark", "SessionSecurity", "TamperDetection", "UserAuthentication"]
