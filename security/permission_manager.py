"""Screen access permissions."""

from __future__ import annotations

import json
import logging
import time
from pathlib import Path
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

_BASE_DIR = Path(__file__).resolve().parent.parent
_PREFS_FILE = _BASE_DIR / "memory" / "user_preferences.json"

_DEFAULT_POLICY = {
    "allow_screenshot": True,
    "allow_click": True,
    "allow_type": True,
    "allow_type_secure": True,
    "allow_key": True,
    "confirm_before_click": True,
    "confirm_before_type": False,
    "blocked_targets": [],
    "blocked_regions": [],
}


class PermissionManager:
    """Governs which screen actions the AI is allowed to perform."""

    def __init__(self, prefs_file: Optional[str] = None) -> None:
        self.prefs_file = Path(prefs_file) if prefs_file else _PREFS_FILE
        self.policy = self._load_policy()

    def _load_policy(self) -> Dict[str, Any]:
        try:
            if self.prefs_file.exists():
                with open(self.prefs_file, "r", encoding="utf-8") as f:
                    prefs = json.load(f).get("preferences", {})
                merged = dict(_DEFAULT_POLICY)
                merged.update(prefs.get("permissions", {}))
                return merged
        except Exception as exc:
            logger.warning("Failed to load permissions policy: %s", exc)
        return dict(_DEFAULT_POLICY)

    def check(self, action: str, context: Optional[Dict[str, Any]] = None) -> bool:
        """Return True if the action is permitted."""
        context = context or {}
        key = f"allow_{action}"
        if key in self.policy and not self.policy[key]:
            return False
        # Blocked targets
        target = str(context.get("target", ""))
        for blocked in self.policy.get("blocked_targets", []):
            if blocked and blocked.lower() in target.lower():
                return False
        # Blocked regions (for clicks)
        if action == "click" and "x" in context and "y" in context:
            x, y = context["x"], context["y"]
            for region in self.policy.get("blocked_regions", []):
                rx, ry, rw, rh = region
                if rx <= x <= rx + rw and ry <= y <= ry + rh:
                    return False
        confirm_key = f"confirm_before_{action}"
        if self.policy.get(confirm_key):
            logger.info("Action '%s' requires confirmation (context=%s).", action, context)
        return True

    def grant(self, action: str) -> None:
        self.policy[f"allow_{action}"] = True

    def revoke(self, action: str) -> None:
        self.policy[f"allow_{action}"] = False

    def set_confirm(self, action: str, confirm: bool) -> None:
        self.policy[f"confirm_before_{action}"] = confirm

    def add_blocked_target(self, target: str) -> None:
        self.policy.setdefault("blocked_targets", []).append(target)

    def add_blocked_region(self, region: tuple[int, int, int, int]) -> None:
        self.policy.setdefault("blocked_regions", []).append(list(region))

    def save(self) -> None:
        try:
            prefs = {"version": 1, "preferences": {"permissions": self.policy}}
            self.prefs_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.prefs_file, "w", encoding="utf-8") as f:
                json.dump(prefs, f, indent=2)
        except Exception as exc:
            logger.warning("Failed to save permissions: %s", exc)
