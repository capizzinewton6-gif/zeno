"""Tracks completed features, milestones, and project roadmaps."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from config import load_json, memory_file, save_json


@dataclass
class Milestone:
    name: str
    description: str = ""
    completed: bool = False
    completed_at: str = ""


@dataclass
class Feature:
    name: str
    status: str = "planned"  # planned, in_progress, done
    milestone: str = ""
    notes: str = ""


@dataclass
class Roadmap:
    project: str
    milestones: list[Milestone] = field(default_factory=list)
    features: list[Feature] = field(default_factory=list)


class ProgressionTracker:
    """Persists project progression to the memory layer."""

    STORE = "project_context.json"

    def __init__(self) -> None:
        self._data = load_json(memory_file(self.STORE))

    def set_goal(self, project: str, stack: list[str] | None = None) -> None:
        self._data["project_goal"] = project
        if stack:
            self._data["technology_stack"] = stack
        self._save()

    def add_milestone(self, milestone: Milestone) -> None:
        self._data.setdefault("milestones", []).append(milestone.__dict__)
        self._save()

    def complete_milestone(self, name: str) -> bool:
        for m in self._data.get("milestones", []):
            if m["name"] == name:
                m["completed"] = True
                m["completed_at"] = datetime.now(timezone.utc).isoformat()
                self._save()
                return True
        return False

    def add_feature(self, feature: Feature) -> None:
        self._data.setdefault("features", []).append(feature.__dict__)
        self._save()

    def update_feature(self, name: str, status: str) -> bool:
        for f in self._data.get("features", []):
            if f["name"] == name:
                f["status"] = status
                self._save()
                return True
        return False

    def roadmap(self) -> Roadmap:
        milestones = [Milestone(**m) for m in self._data.get("milestones", [])]
        features = [Feature(**f) for f in self._data.get("features", [])]
        return Roadmap(project=self._data.get("project_goal", ""),
                       milestones=milestones, features=features)

    def progress(self) -> dict[str, Any]:
        ms = self._data.get("milestones", [])
        feats = self._data.get("features", [])
        ms_done = sum(1 for m in ms if m.get("completed"))
        feats_done = sum(1 for f in feats if f.get("status") == "done")
        return {
            "milestones": {"done": ms_done, "total": len(ms)},
            "features": {"done": feats_done, "total": len(feats)},
            "percent": (
                (ms_done + feats_done) / max(1, len(ms) + len(feats)) * 100
            ),
        }

    def _save(self) -> None:
        self._data.setdefault("version", "1.0.0")
        save_json(memory_file(self.STORE), self._data)
