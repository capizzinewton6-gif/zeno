"""Visual side-by-side and inline diff renderer."""
from __future__ import annotations

from typing import Any


class DiffViewer:
    """Renders text diffs in side-by-side or inline form."""

    def inline(self, before: str, after: str, context: int = 3) -> str:
        import difflib
        diff = difflib.unified_diff(
            before.splitlines(keepends=True),
            after.splitlines(keepends=True),
            fromfile="before", tofile="after", n=context,
        )
        return "".join(self._color(line) for line in diff)

    def side_by_side(self, before: str, after: str, width: int = 50) -> str:
        import difflib
        sm = difflib.SequenceMatcher(None, before.splitlines(), after.splitlines())
        left_lines: list[str] = []
        right_lines: list[str] = []
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag == "equal":
                for i, j in zip(range(i1, i2), range(j1, j2)):
                    left_lines.append(before.splitlines()[i])
                    right_lines.append(after.splitlines()[j])
            elif tag == "replace":
                left_lines.extend(before.splitlines()[i1:i2])
                right_lines.extend(after.splitlines()[j1:j2])
            elif tag == "delete":
                left_lines.extend(before.splitlines()[i1:i2])
                right_lines.extend([""] * (i2 - i1))
            elif tag == "insert":
                left_lines.extend([""] * (j2 - j1))
                right_lines.extend(after.splitlines()[j1:j2])
        out: list[str] = [f"{'BEFORE':<{width}} | {'AFTER'}"]
        out.append("-" * width + "-+-" + "-" * width)
        for l, r in zip(left_lines, right_lines):
            out.append(f"{l[:width]:<{width}} | {r[:width]}")
        return "\n".join(out)

    def stats(self, before: str, after: str) -> dict[str, int]:
        import difflib
        sm = difflib.SequenceMatcher(None, before.splitlines(), after.splitlines())
        adds = dels = 0
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag == "insert":
                adds += j2 - j1
            elif tag == "delete":
                dels += i2 - i1
            elif tag == "replace":
                adds += j2 - j1
                dels += i2 - i1
        return {"additions": adds, "deletions": dels}

    def _color(self, line: str) -> str:
        if line.startswith("+") and not line.startswith("+++"):
            return f"\033[32m{line}\033[0m"
        if line.startswith("-") and not line.startswith("---"):
            return f"\033[31m{line}\033[0m"
        if line.startswith("@@"):
            return f"\033[36m{line}\033[0m"
        return line
