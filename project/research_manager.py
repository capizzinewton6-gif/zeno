"""Research manager — manage chemical research projects and synthesis targets."""

import time
import uuid


class ResearchManager:
    """Manage research projects and synthesis targets."""

    def __init__(self):
        self.projects = {}

    def create_project(self, name, target=None, description="", team=None):
        pid = str(uuid.uuid4())[:8]
        project = {
            "id": pid,
            "name": name,
            "target": target,
            "description": description,
            "team": team or [],
            "status": "planning",
            "created": time.time(),
            "milestones": [],
        }
        self.projects[pid] = project
        return project

    def add_milestone(self, pid, title, due=None):
        if pid not in self.projects:
            return {"error": "unknown project"}
        ms = {"title": title, "due": due, "status": "open"}
        self.projects[pid]["milestones"].append(ms)
        return ms

    def set_status(self, pid, status):
        if pid not in self.projects:
            return {"error": "unknown project"}
        self.projects[pid]["status"] = status
        return self.projects[pid]

    def list_projects(self):
        return [{"id": p["id"], "name": p["name"], "status": p["status"],
                 "target": p["target"]} for p in self.projects.values()]

    def get(self, pid):
        return self.projects.get(pid, {"error": "unknown project"})
