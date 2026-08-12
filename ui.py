"""Text-based user interface for the Zeno AI Inventor.

Provides an interactive command loop. The UI surfaces the lightweight model
descriptors (online status, responsibilities) so users can see which Gemini
engines are active.
"""

from __future__ import annotations

import os
import shlex
import sys
from typing import Callable

from ai_core.ai_engine import AIEngine
from agents import (
    EngineeringAgent, InventorAgent, DesignAgent, SimulationAgent,
    ResearchAgent, OptimizationAgent, ProjectAgent,
)
from src.invention_workflow_engine import InventionWorkflowEngine
from tools import FileManager


BANNER = r"""
+--------------------------------------------------------------+
|                        ZENO AI INVENTOR                       |
|       Autonomous AI Inventor, Engineer & Research Assistant    |
|                  (Gemini 2.5 Flash + 1.5 Flash)               |
+--------------------------------------------------------------+
"""

HELP_TEXT = """Available commands:
  invent <idea>            Run the full end-to-end invention workflow
  engineer <problem>       Solve an engineering problem
  design <spec>            Create a design
  simulate <spec>          Plan simulations for a system
  research <topic>         Research a topic
  improve <invention>      Improve an existing invention
  optimize <design>        Optimize a design
  project list             List saved projects
  project create <name>    Create a new project
  models                   Show active AI models
  help                     Show this help
  exit                     Quit
"""


class ZenoUI:
    def __init__(self, engine: AIEngine | None = None):
        self.engine = engine or AIEngine()
        self.engineering = EngineeringAgent(self.engine)
        self.inventor = InventorAgent(self.engine)
        self.design = DesignAgent(self.engine)
        self.simulation = SimulationAgent(self.engine)
        self.research = ResearchAgent(self.engine)
        self.optimization = OptimizationAgent(self.engine)
        self.project = ProjectAgent(self.engine)
        self.workflow = InventionWorkflowEngine(self.engine)
        self.file_manager = FileManager()

    # --- Display helpers -------------------------------------------------
    def show_models(self):
        print("\nActive AI Models:")
        for m in self.engine.models:
            status = "ONLINE" if m["online"] else "OFFLINE (stub)"
            print(f"  - {m['name']} [{m['role']}]  {status}")
            print(f"      id: {m['id']}")
            print(f"      responsibilities: {', '.join(m['responsibilities'][:3])}...")

    def banner(self):
        print(BANNER)
        self.show_models()
        print("\nType 'help' for commands.\n")

    # --- Command dispatch ------------------------------------------------
    def handle(self, line: str) -> bool:
        line = line.strip()
        if not line:
            return True
        try:
            parts = shlex.split(line)
        except ValueError:
            parts = line.split()
        cmd = parts[0].lower()

        if cmd in ("exit", "quit"):
            print("Goodbye.")
            return False
        if cmd == "help":
            print(HELP_TEXT)
        elif cmd == "models":
            self.show_models()
        elif cmd == "invent" and len(parts) > 1:
            self._run_invention(" ".join(parts[1:]))
        elif cmd == "engineer" and len(parts) > 1:
            print(self.engineering.solve(" ".join(parts[1:])))
        elif cmd == "design" and len(parts) > 1:
            print(self.design.design(" ".join(parts[1:])))
        elif cmd == "simulate" and len(parts) > 1:
            print(self.simulation.plan_simulations(" ".join(parts[1:])))
        elif cmd == "research" and len(parts) > 1:
            print(self.research.research(" ".join(parts[1:])))
        elif cmd == "improve" and len(parts) > 1:
            print(self.inventor.improve(" ".join(parts[1:])))
        elif cmd == "optimize" and len(parts) > 1:
            print(self.optimization.optimize(" ".join(parts[1:]), "cost, weight, strength"))
        elif cmd == "project":
            self._handle_project(parts[1:])
        else:
            print(f"Unknown command. Type 'help'.")
        return True

    def _run_invention(self, idea: str):
        print(f"\nStarting autonomous invention workflow for: {idea}\n")
        result = self.workflow.run(
            idea, progress=lambda m: print(f"  [{m}]"))
        print(f"\n=== Invention Package Complete ===")
        print(f"Concept: {result['concept'][:80]}...")
        print(f"Package: {result['package_name']}")
        print(f"Directory: {result['project_dir']}")
        print(f"Blueprints: {len(result['blueprints'])} files")
        print(f"Documents: {len(result['documents'])} files")
        print(f"Total files: {result['file_count']}")
        print(f"ZIP: {result['zip_package']}")

    def _handle_project(self, args: list[str]):
        if not args or args[0] == "list":
            for p in self.project.projects.list():
                print(f"  {p['id']}: {p['name']} [{p['status']}]")
        elif args[0] == "create" and len(args) > 1:
            name = args[1]
            desc = " ".join(args[2:]) or name
            p = self.project.create(name, desc)
            print(f"Created project {p['id']}: {p['name']}")

    # --- Main loop -------------------------------------------------------
    def loop(self):
        self.banner()
        while True:
            try:
                line = input("zeno> ")
            except (EOFError, KeyboardInterrupt):
                print("\nGoodbye.")
                break
            if not self.handle(line):
                break


def run():
    ZenoUI().loop()


if __name__ == "__main__":
    run()
