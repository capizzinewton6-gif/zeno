"""User interface for the Screen Recognition AI."""

from __future__ import annotations

import logging
import shlex
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


class UI:
    """Command-line user interface for the Screen Recognition AI.

    Provides a simple REPL that forwards user commands to the ScreenAgent.
    A Tkinter-based graphical interface is available via :meth:`launch_gui`
    when a display is present.
    """

    HELP_TEXT = """\
Screen Recognition AI - Commands:
  capture                Capture a screenshot
  analyze [goal]        Analyze the current screen; optionally suggest action for goal
  describe              Describe what is on screen
  read                  Read text from screen (OCR)
  suggest <goal>        Suggest an action for a goal
  automate <goal>       Plan and (dry-run) execute a workflow for a goal
  run <goal>            Actually execute the workflow for a goal
  learn <name>          Learn the current screen as a named pattern
  recognize             Recognize known patterns on screen
  state                 Show the current screen state
  windows               List open windows
  errors                Check for error messages on screen
  help                   Show this help
  exit                  Quit
"""

    def __init__(self, agent) -> None:
        self.agent = agent

    # ------------------------------------------------------------------ REPL
    def start(self) -> None:
        print("Screen Recognition AI. Type 'help' for commands.")
        while True:
            try:
                line = input("screen-ai> ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                break
            if not line:
                continue
            self.handle(line)

    def handle(self, line: str) -> Optional[Dict[str, Any]]:
        try:
            parts = shlex.split(line)
        except ValueError:
            parts = line.split()
        if not parts:
            return None
        cmd = parts[0].lower()
        args = parts[1:]

        if cmd in ("exit", "quit"):
            self.agent.save_memory()
            raise SystemExit(0)
        elif cmd == "help":
            print(self.HELP_TEXT)
        elif cmd == "capture":
            path = self.agent.capture_screen()
            print(f"Captured: {path}")
        elif cmd == "analyze":
            goal = " ".join(args) if args else None
            result = self.agent.analyze(goal=goal)
            self._print_summary(result)
            return result
        elif cmd == "describe":
            print(self.agent.visual.describe(self.agent._last_image))
        elif cmd == "read":
            print(self.agent.text.read_all(self.agent._last_image))
        elif cmd == "suggest":
            if not args:
                print("Usage: suggest <goal>")
                return None
            goal = " ".join(args)
            result = self.agent.suggest_action(goal)
            print(result)
            return result
        elif cmd == "automate":
            if not args:
                print("Usage: automate <goal>")
                return None
            goal = " ".join(args)
            result = self.agent.automate(goal, dry_run=True)
            print(result)
            return result
        elif cmd == "run":
            if not args:
                print("Usage: run <goal>")
                return None
            goal = " ".join(args)
            result = self.agent.automate(goal, dry_run=False)
            print(result)
            return result
        elif cmd == "learn":
            if not args:
                print("Usage: learn <name>")
                return None
            name = " ".join(args)
            result = self.agent.learn_pattern(name)
            print(result)
            return result
        elif cmd == "recognize":
            matches = self.agent.recognize_patterns()
            print(f"Known patterns: {matches}")
            return {"matches": matches}
        elif cmd == "state":
            state = self.agent.current_state()
            self._print_summary(state)
            return state
        elif cmd == "windows":
            for w in self.agent.windows.list_windows():
                print(f"  - {w.get('title')}")
        elif cmd == "errors":
            result = self.agent.errors.detect(self.agent._last_image)
            print(result)
            return result
        else:
            print(f"Unknown command: {cmd}. Type 'help'.")

    @staticmethod
    def _print_summary(result: Dict[str, Any]) -> None:
        if not isinstance(result, dict):
            print(result)
            return
        if "error" in result:
            print(f"Error: {result['error']}")
            return
        interp = result.get("interpretation", {})
        print(f"Summary: {interp.get('summary', 'n/a')}")
        print(f"Context: {interp.get('context_type', 'n/a')}")
        ocr = result.get("ocr", "")
        if ocr:
            preview = ocr.strip().replace("\n", " ")[:200]
            print(f"Text: {preview}")
        err = result.get("errors", {})
        if err.get("has_error"):
            print(f"⚠ Error detected ({err.get('severity')}): {err.get('message')}")
        suggestion = result.get("suggestion")
        if suggestion:
            print(f"Suggestion: {suggestion}")

    # ------------------------------------------------------------------ GUI
    def launch_gui(self) -> None:  # pragma: no cover - requires display
        try:
            import tkinter as tk
            from tkinter import scrolledtext
        except Exception as exc:
            logger.error("Tkinter unavailable: %s", exc)
            print("GUI unavailable (no display). Use the command-line interface.")
            return

        root = tk.Tk()
        root.title("Screen Recognition AI")
        root.geometry("720x480")

        output = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=22)
        output.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        entry = tk.Entry(root)
        entry.pack(fill=tk.X, padx=8, pady=(0, 8))
        entry.focus_set()

        def _run(_event=None):
            line = entry.get().strip()
            entry.delete(0, tk.END)
            if not line:
                return
            output.insert(tk.END, f"screen-ai> {line}\n")
            import io, contextlib
            buf = io.StringIO()
            try:
                with contextlib.redirect_stdout(buf):
                    self.handle(line)
            except SystemExit:
                root.destroy()
                return
            output.insert(tk.END, buf.getvalue() + "\n")
            output.see(tk.END)

        entry.bind("<Return>", _run)
        output.insert(tk.END, self.HELP_TEXT + "\n")
        root.mainloop()
