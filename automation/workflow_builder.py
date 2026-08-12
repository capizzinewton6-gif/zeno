"""Create automation tasks (workflows)."""

from __future__ import annotations

import json
import logging
import sqlite3
import time
from pathlib import Path
from typing import Any, Dict, List

logger = logging.getLogger(__name__)

_BASE_DIR = Path(__file__).resolve().parent.parent
_ACTIONS_DB = _BASE_DIR / "database" / "actions.db"


class WorkflowBuilder:
    """Builds reusable multi-step automation workflows."""

    def __init__(self, name: str = "", description: str = "") -> None:
        self.name = name
        self.description = description
        self.steps: List[Dict[str, Any]] = []

    def add_click(self, x: int, y: int, description: str = "") -> "WorkflowBuilder":
        self.steps.append({"action": "click", "target": [x, y], "description": description})
        return self

    def add_type(self, text: str, description: str = "") -> "WorkflowBuilder":
        self.steps.append({"action": "type", "target": text, "description": description})
        return self

    def add_key(self, key: str, description: str = "") -> "WorkflowBuilder":
        self.steps.append({"action": "key", "target": key, "description": description})
        return self

    def add_wait(self, seconds: float, description: str = "") -> "WorkflowBuilder":
        self.steps.append({"action": "wait", "target": seconds, "description": description})
        return self

    def add_scroll(self, clicks: int, description: str = "") -> "WorkflowBuilder":
        self.steps.append({"action": "scroll", "target": clicks, "description": description})
        return self

    def add_conditional(self, condition: str, then_steps: List[Dict[str, Any]],
                        description: str = "") -> "WorkflowBuilder":
        self.steps.append({
            "action": "conditional", "condition": condition,
            "then": then_steps, "description": description,
        })
        return self

    def add_step(self, step: Dict[str, Any]) -> "WorkflowBuilder":
        self.steps.append(step)
        return self

    def build(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "steps": self.steps,
            "created": time.strftime("%Y-%m-%dT%H:%M:%S"),
        }

    def save(self) -> int:
        workflow = self.build()
        try:
            conn = sqlite3.connect(str(_ACTIONS_DB))
            cur = conn.execute(
                "INSERT INTO workflows (name, description, steps, created, last_run) "
                "VALUES (?, ?, ?, ?, ?)",
                (workflow["name"], workflow["description"],
                 json.dumps(workflow["steps"]), workflow["created"], None),
            )
            conn.commit()
            wid = cur.lastrowid
            conn.close()
            logger.info("Saved workflow '%s' with id %d", self.name, wid)
            return wid
        except Exception as exc:
            logger.warning("Failed to save workflow: %s", exc)
            return -1

    @staticmethod
    def load(workflow_id: int) -> Dict[str, Any] | None:
        try:
            conn = sqlite3.connect(str(_ACTIONS_DB))
            cur = conn.execute(
                "SELECT id, name, description, steps FROM workflows WHERE id = ?",
                (workflow_id,),
            )
            row = cur.fetchone()
            conn.close()
            if row:
                return {"id": row[0], "name": row[1], "description": row[2],
                        "steps": json.loads(row[3])}
        except Exception as exc:
            logger.warning("Failed to load workflow %d: %s", workflow_id, exc)
        return None

    @staticmethod
    def list_workflows() -> List[Dict[str, Any]]:
        try:
            conn = sqlite3.connect(str(_ACTIONS_DB))
            cur = conn.execute("SELECT id, name, description FROM workflows ORDER BY id DESC")
            rows = [{"id": r[0], "name": r[1], "description": r[2]} for r in cur.fetchall()]
            conn.close()
            return rows
        except Exception:
            return []
