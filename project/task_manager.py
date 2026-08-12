"""Task manager — track synthesis steps, characterization runs, and purifications."""

import time


class TaskManager:
    """Track chemistry project tasks."""

    def __init__(self):
        self.tasks = []
        self._next_id = 1

    def add_task(self, title, category="synthesis", assignee=None, priority="medium"):
        task = {
            "id": self._next_id,
            "title": title,
            "category": category,
            "assignee": assignee,
            "priority": priority,
            "status": "todo",
            "created": time.time(),
            "completed": None,
        }
        self._next_id += 1
        self.tasks.append(task)
        return task

    def complete(self, task_id):
        for t in self.tasks:
            if t["id"] == task_id:
                t["status"] = "done"
                t["completed"] = time.time()
                return t
        return {"error": "task not found"}

    def by_category(self, category):
        return [t for t in self.tasks if t["category"] == category]

    def open_tasks(self):
        return [t for t in self.tasks if t["status"] != "done"]

    def summary(self):
        total = len(self.tasks)
        done = sum(1 for t in self.tasks if t["status"] == "done")
        return {"total": total, "done": done, "open": total - done}
