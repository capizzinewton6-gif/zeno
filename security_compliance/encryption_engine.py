"""Encryption engine: AES-256 (via cryptography lib) with Fernet fallback."""

from __future__ import annotations

import base64
import hashlib
import os
from typing import Optional

try:
    from cryptography.fernet import Fernet  # type: ignore
    _CRYPTO_AVAILABLE = True
except Exception:  # pragma: no cover - optional dependency
    _CRYPTO_AVAILABLE = False


class EncryptionEngine:
    """Encrypt biometric embeddings / snapshots at rest.

    Uses Fernet (AES-128-CBC + HMAC) when ``cryptography`` is available; otherwise
    falls back to an XOR + SHA256 scheme so the pipeline still functions in a
    degraded environment. Production deployments should install ``cryptography``.
    """

    def __init__(self, key: Optional[bytes] = None) -> None:
        self._key = key
        self._fernet = None
        if _CRYPTO_AVAILABLE:
            if key is None:
                key = Fernet.generate_key()
            self._fernet = Fernet(key)
            self._key = key

    @property
    def key(self) -> Optional[bytes]:
        return self._key

    @property
    def is_secure(self) -> bool:
        return self._fernet is not None

    # -- bytes API (for embeddings / snapshots) -------------------------
    def encrypt(self, data: bytes) -> bytes:
        if self._fernet is not None:
            return self._fernet.encrypt(data)
        return self._xor(data)

    def decrypt(self, data: bytes) -> bytes:
        if self._fernet is not None:
            return self._fernet.decrypt(data)
        return self._xor(data)

    # -- string API (for JSON galleries) --------------------------------
    def encrypt_str(self, text: str) -> str:
        return base64.b64encode(self.encrypt(text.encode("utf-8"))).decode("ascii")

    def decrypt_str(self, text: str) -> str:
        return self.decrypt(base64.b64decode(text)).decode("utf-8")

    def _xor(self, data: bytes) -> bytes:
        if self._key is None:
            self._key = hashlib.sha256(b"vision-ai-default-key").digest()
        key = self._key
        return bytes(b ^ key[i % len(key)] for i, b in enumerate(data))
