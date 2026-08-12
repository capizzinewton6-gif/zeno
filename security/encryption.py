"""Secure stored information."""

from __future__ import annotations

import base64
import hashlib
import json
import logging
import os
from pathlib import Path
from typing import Any, Optional, Union

logger = logging.getLogger(__name__)

_BASE_DIR = Path(__file__).resolve().parent.parent
_KEY_FILE = _BASE_DIR / "security" / ".key"


class Encryption:
    """Symmetric encryption for sensitive stored data.

    Uses Fernet (cryptography library) when available, with a project-local
    key file. Falls back to a base64 obfuscation wrapper (NOT secure) when
    the cryptography library is absent, so the system remains importable.
    """

    def __init__(self, key: Optional[bytes] = None) -> None:
        self._fernet = None
        self._key = key or self._load_or_create_key()
        try:
            from cryptography.fernet import Fernet  # type: ignore
            self._fernet = Fernet(self._key)
        except Exception as exc:
            logger.warning("cryptography.Fernet unavailable; using obfuscation fallback: %s", exc)

    # ------------------------------------------------------------------ key
    def _load_or_create_key(self) -> bytes:
        try:
            if _KEY_FILE.exists():
                return _KEY_FILE.read_bytes()
            from cryptography.fernet import Fernet  # type: ignore
            key = Fernet.generate_key()
            _KEY_FILE.write_bytes(key)
            try:
                os.chmod(_KEY_FILE, 0o600)
            except Exception:
                pass
            return key
        except Exception:
            # Deterministic fallback key (obfuscation only)
            return base64.urlsafe_b64encode(hashlib.sha256(b"screen-ai-fallback").digest())

    # ------------------------------------------------------------------ api
    def encrypt(self, data: Union[str, bytes, dict, list]) -> str:
        if isinstance(data, (dict, list)):
            data = json.dumps(data, default=str)
        if isinstance(data, str):
            data = data.encode("utf-8")
        if self._fernet is not None:
            return self._fernet.encrypt(data).decode("utf-8")
        return base64.urlsafe_b64encode(data).decode("utf-8")

    def decrypt(self, token: str) -> str:
        if self._fernet is not None:
            return self._fernet.decrypt(token.encode("utf-8")).decode("utf-8")
        return base64.urlsafe_b64decode(token.encode("utf-8")).decode("utf-8")

    def encrypt_file(self, source: Union[str, Path], dest: Optional[Union[str, Path]] = None) -> Path:
        source = Path(source)
        dest = Path(dest) if dest else source.with_suffix(source.suffix + ".enc")
        content = source.read_bytes()
        token = self.encrypt(content)
        dest.write_text(token)
        return dest

    def decrypt_file(self, source: Union[str, Path]) -> bytes:
        source = Path(source)
        token = source.read_text()
        return self.decrypt(token).encode("utf-8")
