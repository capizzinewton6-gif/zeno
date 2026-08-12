"""Execute screen tasks."""

from __future__ import annotations

import json
import logging
import sqlite3
import time
from pathlib import Path
from typing import Any, Dict, List

from automation.click_automation import ClickAutomation
from automation.keyboard_controller import KeyboardController
from automation.mouse_controller import MouseController
from automation.typing_automation import TypingAutomation

logger = logging.getLogger(__name__)

_BASE_DIR = Path(__file__).resolve().parent.parent
_ACTIONS_DB = _BASE_DIR / "database" / "actions.db"


class TaskExecutor:
    """Executes automation workflows step by step."""

    def __init__(self) -> None:
        self.mouse = MouseController()
        self.keyboard = KeyboardController()
        self.clicks = ClickAutomation(mouse=self.mouse)
        self.typer = TypingAutomation(keyboard=self.keyboard)

    def execute(self, workflow: Dict[str, Any], dry_run: bool = False) -> Dict[str, Any]:
        steps = workflow.get("steps", [])
        name = workflow.get("name", "unnamed")
        results: List[Dict[str, Any]] = []
        for i, step in enumerate(steps):
            if dry_run:
                results.append({"step": i, "action": step.get("action"),
                                "status": "dry_run", "target": step.get("target")})
                continue
            result = self._execute_step(step)
            results.append({"step": i, "action": step.get("action"), "status": result})
            if not result:
                logger.warning("Step %d failed; continuing.", i)
        summary = {
            "workflow": name,
            "total_steps": len(steps),
            "executed": len(results),
            "results": results,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        }
        self._record(name, summary)
        return summary

    def _execute_step(self, step: Dict[str, Any]) -> bool:
        action = step.get("action", "").lower()
        target = step.get("target")
        try:
            if action == "click":
                x, y = target if isinstance(target, (list, tuple)) and len(target) >= 2 else (0, 0)
                return self.clicks.click_at(int(x), int(y))
            elif action == "type":
                return self.typer.type_text(str(target))
            elif action == "key":
                return self.keyboard.press(str(target))
            elif action == "wait":
                time.sleep(float(target))
                return True
            elif action == "scroll":
                return self.mouse.scroll(int(target))
            elif action == "conditional":
                logger.info("Conditional step noted; condition=%s", step.get("condition"))
                return True
            else:
                logger.warning("Unknown action: %s", action)
                return False
        except Exception as exc:
            logger.error("Step execution error (%s): %s", action, exc)
            return False

    def _record(self, name: str, summary: Dict[str, Any]) -> None:
        try:
            conn = sqlite3.connect(str(_ACTIONS_DB))
            conn.execute(
                "INSERT INTO actions (timestamp, action_type, description, target, coordinates, status, result) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (summary["timestamp"], "workflow", name, "", "",
                 "completed", json.dumps(summary)[:2000]),
            )
            conn.execute("UPDATE workflows SET last_run = ? WHERE name = ?",
                         (summary["timestamp"], name))
            conn.commit()
            conn.close()
        except Exception as exc:
            logger.debug("Failed to record task: %s", exc)
