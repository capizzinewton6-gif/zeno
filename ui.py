"""User interface layout for CODING_AI (simple text-based UI)."""
from __future__ import annotations

import os
import sys
from typing import Any

from visualization.terminal_ui import TerminalUI


BANNER = r"""
 ____   ___  ____ _____ ___  ____    ____ ___  _    _    _   _
/ ___| / _ \|  _ \_   _/ _ \/ ___|  / ___/ _ \| |  | |  | | | |
\___ \| | | | |_) || || | | \___ \ | |  | | | | |  | |  | |_| |
 ___) | |_| |  __/ | || |_| |___) || |__| |_| | |__| |__|  _  |
|____/ \___/|_|    |_| \___/|____/  \____\___/|_____\____|_| |_|

A capability-based coding AI powered by Gemini.
"""


class UI:
    """Text-based REPL interface for interacting with the AI engine."""

    HELP = """\
Available commands:
  /help               Show this help
  /status             Show AI engine status and telemetry
  /agents             List available agents
  /capabilities       List available capabilities
  /languages          List supported languages
  /project <name>     Start a project session
  /tasks              Show task board
  /index              Index the current workspace
  /clean              Clean build artifacts and caches
  /scan               Run a security SAST scan on the workspace
  /diff <a> <b>       Show diff between two files
  /diagram <dir>      Render an architecture diagram of a directory
  /clear              Clear the screen
  /quit               Exit

Anything else is sent to the AI engine as a natural-language request.
"""

    def __init__(self, engine: Any | None = None) -> None:
        self.engine = engine
        self.tui = TerminalUI()

    def banner(self) -> None:
        print(BANNER)

    def prompt(self) -> str:
        return "zeno> "

    def run(self) -> None:
        """Main REPL loop."""
        self.banner()
        self.tui.info("Type /help for commands, or describe what you want to build.")
        print()
        while True:
            try:
                line = input(self.prompt()).strip()
            except (EOFError, KeyboardInterrupt):
                print("\nGoodbye.")
                break
            if not line:
                continue
            if line in ("/quit", "/exit", "/q"):
                print("Goodbye.")
                break
            self.handle(line)

    def handle(self, line: str) -> None:
        cmd, _, arg = line.partition(" ")
        if cmd == "/help":
            print(self.HELP)
        elif cmd == "/clear":
            os.system("clear" if os.name == "posix" else "cls")
        elif cmd == "/status":
            self._status()
        elif cmd == "/agents":
            self._list_agents()
        elif cmd == "/capabilities":
            self._list_capabilities()
        elif cmd == "/languages":
            self._list_languages()
        elif cmd == "/project":
            self._start_project(arg.strip())
        elif cmd == "/tasks":
            self._tasks()
        elif cmd == "/index":
            self._index()
        elif cmd == "/clean":
            self._clean()
        elif cmd == "/scan":
            self._scan()
        elif cmd == "/diff":
            self._diff(arg.strip())
        elif cmd == "/diagram":
            self._diagram(arg.strip())
        else:
            self._ask(line)

    # --- command implementations ---------------------------------------

    def _status(self) -> None:
        if not self.engine:
            self.tui.warning("Engine not initialized.")
            return
        s = self.engine.status()
        self.tui.table(
            ["Field", "Value"],
            [[k, str(v)] for k, v in s.items()],
            title="AI Engine Status",
        )

    def _list_agents(self) -> None:
        from ai_core.ai_engine import AGENT_KEYS
        self.tui.panel("Agents", "\n".join(f"  • {a}" for a in AGENT_KEYS))

    def _list_capabilities(self) -> None:
        caps = [
            "code_synthesis", "terminal_execution", "repository_indexer",
            "documentation_builder", "code_explainer",
        ]
        self.tui.panel("Capabilities", "\n".join(f"  • {c}" for c in caps))

    def _list_languages(self) -> None:
        langs = [
            "python", "javascript/typescript", "rust", "go", "c/cpp",
            "java/kotlin", "web_stack", "database_sql", "shell_scripting",
        ]
        self.tui.panel("Languages", "\n".join(f"  • {l}" for l in langs))

    def _start_project(self, name: str) -> None:
        if not name:
            self.tui.warning("Usage: /project <name>")
            return
        if not self.engine:
            self.tui.warning("Engine not initialized.")
            return
        result = self.engine.start_project(name)
        self.tui.success(f"Project '{name}' started: {result}")

    def _tasks(self) -> None:
        from project.task_manager import TaskManager
        tm = TaskManager()
        board = tm.board()
        rows = []
        for status, tasks in board.items():
            for t in tasks:
                rows.append([t["id"], status, t["priority"], t["title"]])
        if rows:
            self.tui.table(["ID", "Status", "Priority", "Title"], rows, title="Task Board")
        else:
            self.tui.info("No tasks yet.")
        self.tui.info(f"Progress: {tm.progress()}")

    def _index(self) -> None:
        from repository_workspace.file_tree_indexer import FileTreeIndexer
        idx = FileTreeIndexer().index(".")
        ext_rows = [[ext, str(len(files))] for ext, files in
                    sorted(idx.by_extension.items(), key=lambda x: -len(x[1]))[:15]]
        self.tui.table(["Extension", "Files"], ext_rows, title=f"Workspace Index ({idx.count} files)")

    def _clean(self) -> None:
        from repository_workspace.workspace_cleaner import WorkspaceCleaner
        result = WorkspaceCleaner().clean(".", dry_run=False)
        self.tui.success(
            f"Removed {len(result.removed_dirs)} dirs, {len(result.removed_files)} files, "
            f"freed {result.freed_bytes:,} bytes.")

    def _scan(self) -> None:
        from pathlib import Path
        from security_compliance.vulnerability_scanner import VulnerabilityScanner
        scanner = VulnerabilityScanner()
        vulns: list[Vulnerability] = []
        for p in Path(".").rglob("*.py"):
            if any(part in {"node_modules", ".venv", "venv", "__pycache__"} for part in p.parts):
                continue
            report = scanner.scan_file(str(p), "python")
            vulns.extend(report.vulnerabilities)
        if not vulns:
            self.tui.success("No vulnerabilities found.")
            return
        rows = [[v.severity, v.cwe, str(v.line), v.title] for v in vulns[:30]]
        self.tui.table(["Severity", "CWE", "Line", "Title"], rows, title=f"Security Scan ({len(vulns)} findings)")

    def _diff(self, args: str) -> None:
        from visualization.diff_viewer import DiffViewer
        paths = args.split()
        if len(paths) != 2:
            self.tui.warning("Usage: /diff <file_a> <file_b>")
            return
        try:
            a = open(paths[0], encoding="utf-8").read()
            b = open(paths[1], encoding="utf-8").read()
        except OSError as exc:
            self.tui.error(str(exc))
            return
        print(DiffViewer().side_by_side(a, b))

    def _diagram(self, path: str) -> None:
        from visualization.architecture_renderer import ArchitectureRenderer
        from pathlib import Path
        p = Path(path or ".")
        dirs = []
        for d in sorted(p.iterdir()):
            if d.is_dir() and not d.name.startswith(".") and d.name not in {"node_modules", "__pycache__"}:
                dirs.append({"path": d.name, "responsibility": d.name})
        blueprint = {"directories": dirs, "interfaces": [], "data_flow": []}
        print(ArchitectureRenderer().blueprint_to_mermaid(blueprint))

    def _ask(self, prompt: str) -> None:
        if not self.engine:
            self.tui.warning("Engine not initialized. Call ui with an AIEngine.")
            return
        self.tui.info("Thinking...")
        result = self.engine.handle(prompt)
        if result.success:
            self.tui.success(f"[{result.agent_used or result.capability_used}]")
            print(result.content)
        else:
            self.tui.error(result.error or "Request failed.")
