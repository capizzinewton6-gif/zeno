"""Learning agent: learns UI patterns."""

from __future__ import annotations

import json
import logging
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from computer_vision.pattern_recognition import PatternRecognition
from computer_vision.visual_memory import VisualMemory

logger = logging.getLogger(__name__)

_BASE_DIR = Path(__file__).resolve().parent.parent
_PATTERNS_FILE = _BASE_DIR / "memory" / "ui_patterns.json"


class LearningAgent:
    """Learns and stores UI patterns for future recognition."""

    def __init__(self, memory: VisualMemory | None = None,
                 patterns_file: Optional[str] = None) -> None:
        self.memory = memory or VisualMemory()
        self.patterns_file = Path(patterns_file) if patterns_file else _PATTERNS_FILE
        self.patterns = self._load_patterns()
        self.recognizer = PatternRecognition()

    def learn(self, name: str, image: Any, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        pattern_hash = self.recognizer.hash_image(image)
        entry = {
            "name": name,
            "hash": pattern_hash,
            "metadata": metadata or {},
            "learned_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "occurrences": 1,
        }
        existing = self.patterns["patterns"].get(name)
        if existing:
            entry["occurrences"] = existing.get("occurrences", 1) + 1
            existing.update(entry)
        else:
            self.patterns["patterns"][name] = entry
        self.memory.remember({"event": "learn", "pattern": name, "hash": pattern_hash})
        self._save_patterns()
        logger.info("Learned pattern '%s' (occurrences=%d).", name, entry["occurrences"])
        return entry

    def recognize(self, image: Any) -> List[str]:
        """Return names of known patterns whose hash matches the image."""
        target_hash = self.recognizer.hash_image(image)
        matches = [name for name, p in self.patterns["patterns"].items()
                   if p.get("hash") == target_hash]
        return matches

    def find_similar(self, image: Any, threshold: float = 0.9) -> List[Dict[str, Any]]:
        results = []
        for name, pattern in self.patterns["patterns"].items():
            # Without storing full images, hash equality is our similarity proxy.
            target = self.recognizer.hash_image(image)
            sim = 1.0 if pattern.get("hash") == target else 0.0
            if sim >= threshold:
                results.append({"name": name, "similarity": sim})
        return results

    def forget(self, name: str) -> bool:
        if name in self.patterns["patterns"]:
            del self.patterns["patterns"][name]
            self._save_patterns()
            return True
        return False

    def list_patterns(self) -> List[Dict[str, Any]]:
        return list(self.patterns["patterns"].values())

    # ------------------------------------------------------------------ storage
    def _load_patterns(self) -> Dict[str, Any]:
        try:
            if self.patterns_file.exists():
                with open(self.patterns_file, "r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception as exc:
            logger.warning("Failed to load UI patterns: %s", exc)
        return {"version": 1, "patterns": {}}

    def _save_patterns(self) -> None:
        try:
            self.patterns_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.patterns_file, "w", encoding="utf-8") as f:
                json.dump(self.patterns, f, indent=2)
        except Exception as exc:
            logger.warning("Failed to save UI patterns: %s", exc)

    def persist_memory(self) -> None:
        self.memory.save()
