"""Notebook manager — track Electronic Lab Notebooks (ELN)."""

import time
import uuid


class NotebookManager:
    """Manage electronic lab notebook entries."""

    def __init__(self):
        self.entries = []

    def add_entry(self, title, body, experiment_id=None, tags=None):
        entry = {
            "id": str(uuid.uuid4())[:8],
            "timestamp": time.time(),
            "title": title,
            "body": body,
            "experiment_id": experiment_id,
            "tags": tags or [],
        }
        self.entries.append(entry)
        return entry

    def search(self, query):
        q = query.lower()
        return [e for e in self.entries
                if q in e["title"].lower() or q in e["body"].lower() or any(q in t.lower() for t in e["tags"])]

    def by_experiment(self, experiment_id):
        return [e for e in self.entries if e["experiment_id"] == experiment_id]

    def export_markdown(self):
        lines = []
        for e in self.entries:
            lines.append(f"## {e['title']}")
            lines.append(f"_{time.strftime('%Y-%m-%d %H:%M', time.localtime(e['timestamp']))}_")
            lines.append("")
            lines.append(e["body"])
            if e["tags"]:
                lines.append("")
                lines.append("Tags: " + ", ".join(e["tags"]))
            lines.append("")
            lines.append("---")
            lines.append("")
        return "\n".join(lines)
