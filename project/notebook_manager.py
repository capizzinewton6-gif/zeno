"""Track Electronic Lab Notebooks (ELN)."""
from __future__ import annotations

from datetime import datetime


class NotebookManager:
    def __init__(self):
        self.entries: list[dict] = []

    def add_entry(self, title: str, body: str, experiment_id: str = "",
                  tags: list[str] | None = None) -> dict:
        entry = {"id": len(self.entries) + 1, "title": title, "body": body,
                 "experiment_id": experiment_id,
                 "tags": tags or [],
                 "timestamp": datetime.utcnow().isoformat()}
        self.entries.append(entry)
        return entry

    def search(self, term: str) -> list[dict]:
        t = term.lower()
        return [e for e in self.entries
                if t in e["title"].lower() or t in e["body"].lower()
                or any(t in tag.lower() for tag in e["tags"])]

    def by_tag(self, tag: str) -> list[dict]:
        return [e for e in self.entries if tag.lower() in [t.lower() for t in e["tags"]]]

    def recent(self, n: int = 10) -> list[dict]:
        return self.entries[-n:]

    def annotate(self, entry_id: int, annotation: str) -> dict | None:
        for e in self.entries:
            if e["id"] == entry_id:
                e.setdefault("annotations", []).append(
                    {"time": datetime.utcnow().isoformat(), "text": annotation})
                return e
        return None
