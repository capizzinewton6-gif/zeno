"""Execution planner — Standard Operating Procedures (SOPs) and batch logs."""


class ExecutionPlanner:
    """Generate SOPs and batch execution logs."""

    def make_sop(self, title, steps, safety=None, equipment=None):
        return {
            "title": title,
            "type": "SOP",
            "safety": safety or [],
            "equipment": equipment or [],
            "steps": [{"n": i + 1, "action": s} for i, s in enumerate(steps)],
        }

    def batch_log(self, batch_id, sop_title, operator, start, observations=None):
        return {
            "batch_id": batch_id,
            "sop": sop_title,
            "operator": operator,
            "start": start,
            "observations": observations or [],
            "status": "in_progress",
        }

    def close_batch(self, log, end, yield_pct=None, notes=""):
        log["end"] = end
        log["status"] = "closed"
        log["yield_pct"] = yield_pct
        log["notes"] = notes
        return log
