"""Audit logger: immutable event logging for biometric matches and breaches."""

from __future__ import annotations

import hashlib
import json
import os
import time
from typing import Any, Dict, List, Optional


class AuditLogger:
    """Append-only, hash-chained audit log for security-sensitive events.

    Each entry stores the SHA-256 of the previous entry, forming a tamper-evident
    chain. Entries are JSON-lines so the log is greppable and durable.
    """

    def __init__(self, path: str = "logs/audit.log") -> None:
        self.path = path
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        self._prev_hash = self._last_hash()

    def log(self, event_type: str, details: Dict[str, Any],
            actor: str = "system", severity: str = "info") -> str:
        entry = {
            "ts": time.time(),
            "type": event_type,
            "actor": actor,
            "severity": severity,
            "details": details,
            "prev_hash": self._prev_hash,
        }
        serialized = json.dumps(entry, sort_keys=True)
        entry["hash"] = hashlib.sha256(serialized.encode("utf-8")).hexdigest()
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
        self._prev_hash = entry["hash"]
        return entry["hash"]

    def verify(self) -> bool:
        """Verify the hash chain integrity of the entire log."""
        prev = ""
        with open(self.path, "r", encoding="utf-8") as f:
            for line in f:
                entry = json.loads(line)
                expected_prev = entry.get("prev_hash", "")
                stored_hash = entry.pop("hash", "")
                recomputed = hashlib.sha256(
                    json.dumps(entry, sort_keys=True).encode("utf-8")).hexdigest()
                if expected_prev != prev or recomputed != stored_hash:
                    return False
                prev = stored_hash
        return True

    def tail(self, n: int = 20) -> List[dict]:
        if not os.path.exists(self.path):
            return []
        with open(self.path, "r", encoding="utf-8") as f:
            lines = f.readlines()[-n:]
        return [json.loads(l) for l in lines if l.strip()]

    def _last_hash(self) -> str:
        if not os.path.exists(self.path):
            return ""
        try:
            with open(self.path, "rb") as f:
                f.seek(-2, os.SEEK_END)
                while f.read(1) != b"\n":
                    f.seek(-2, os.SEEK_CUR)
                last = f.readline().decode("utf-8")
            return json.loads(last).get("hash", "")
        except Exception:
            return ""
