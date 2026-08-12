"""Git branch creation, committing, diffing, and merging."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from capabilities.terminal_execution import CommandResult, TerminalExecution


@dataclass
class GitDiff:
    files: list[str] = field(default_factory=list)
    insertions: int = 0
    deletions: int = 0
    raw: str = ""


@dataclass
class GitStatus:
    staged: list[str] = field(default_factory=list)
    unstaged: list[str] = field(default_factory=list)
    untracked: list[str] = field(default_factory=list)
    branch: str = ""
    clean: bool = True


class GitInterface:
    """Wraps git CLI operations in a safe interface."""

    def __init__(self, terminal: TerminalExecution | None = None,
                 workspace: str = ".") -> None:
        self.terminal = terminal or TerminalExecution(workspace=workspace)
        self.workspace = workspace

    def _git(self, args: str) -> CommandResult:
        return self.terminal.run(f"git -C {self.workspace} {args}")

    def init(self) -> CommandResult:
        return self._git("init")

    def status(self) -> GitStatus:
        res = self._git("status --porcelain=v1 -b")
        status = GitStatus()
        if not res.ok:
            return status
        for line in res.stdout.splitlines():
            if line.startswith("##"):
                status.branch = line[3:].split("...")[0].strip()
                continue
            if not line.strip():
                continue
            status.clean = False
            x, y = line[0], line[1]
            path = line[3:].strip()
            if x == "?":
                status.untracked.append(path)
            else:
                if x != " ":
                    status.staged.append(path)
                if y != " ":
                    status.unstaged.append(path)
        return status

    def branch(self, name: str) -> CommandResult:
        return self._git(f"checkout -b {name}")

    def checkout(self, name: str) -> CommandResult:
        return self._git(f"checkout {name}")

    def add(self, paths: list[str] | str = ".") -> CommandResult:
        p = " ".join(paths) if isinstance(paths, list) else paths
        return self._git(f"add {p}")

    def commit(self, message: str) -> CommandResult:
        # Use a heredoc-safe quoting
        safe = message.replace('"', '\\"')
        return self._git(f'commit -m "{safe}"')

    def diff(self, staged: bool = True) -> GitDiff:
        flag = "--cached" if staged else ""
        res = self._git(f"diff --stat {flag}")
        d = GitDiff()
        if not res.ok:
            return d
        d.raw = res.stdout
        for line in res.stdout.splitlines():
            if "|" in line:
                parts = line.split("|")
                if len(parts) == 2:
                    d.files.append(parts[0].strip())
                    nums = parts[1].strip()
                    d.insertions += nums.count("+")
                    d.deletions += nums.count("-")
        return d

    def merge(self, branch: str) -> CommandResult:
        return self._git(f"merge --no-ff {branch}")

    def log(self, n: int = 10) -> list[dict[str, str]]:
        res = self._git(f'log -{n} --pretty=format:"%H|%an|%ad|%s"')
        entries: list[dict[str, str]] = []
        if not res.ok:
            return entries
        for line in res.stdout.splitlines():
            parts = line.split("|", 3)
            if len(parts) == 4:
                entries.append({"hash": parts[0], "author": parts[1],
                                "date": parts[2], "message": parts[3]})
        return entries
