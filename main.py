"""Main screen recognition AI controller.

Entry point that wires the AI engine, agents, and UI together.
"""

from __future__ import annotations

import argparse
import logging
import os
import sys
from pathlib import Path

# Ensure the project root is importable when run directly.
_ROOT = Path(__file__).resolve().parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from ai_core.ai_engine import AIEngine, get_engine  # noqa: E402
from ai_core.command_parser import CommandParser  # noqa: E402
from agents.screen_agent import ScreenAgent  # noqa: E402
from ui import UI  # noqa: E402

logging.basicConfig(
    level=os.environ.get("LOG_LEVEL", "INFO"),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("screen-ai")


class ScreenRecognitionAI:
    """Top-level application controller."""

    def __init__(self, api_key: str | None = None) -> None:
        self.engine = AIEngine(api_key=api_key) if api_key else get_engine()
        self.agent = ScreenAgent(engine=self.engine)
        self.command_parser = CommandParser(engine=self.engine)
        self.ui = UI(self.agent)
        logger.info("Screen Recognition AI initialized (online=%s).", self.engine.is_online)

    def run_command(self, command: str) -> dict:
        """Parse and execute a single natural-language command."""
        parsed = self.command_parser.parse(command)
        intent = parsed.get("intent", "unknown")
        target = parsed.get("target")
        if intent == "screenshot":
            path = self.agent.capture_screen()
            return {"intent": intent, "screenshot": path}
        if intent == "describe":
            result = self.agent.analyze()
            return {"intent": intent, "result": result}
        if intent == "read":
            text = self.agent.text.read_all(self.agent._last_image)
            return {"intent": intent, "text": text}
        if intent in ("click", "type", "scroll", "open", "close"):
            suggestion = self.agent.suggest_action(command)
            return {"intent": intent, "suggestion": suggestion}
        # Default: analyze with the command as the goal
        result = self.agent.analyze(goal=command)
        return {"intent": intent, "result": result}

    def start_cli(self) -> None:
        self.ui.start()

    def start_gui(self) -> None:
        self.ui.launch_gui()


def main() -> None:
    parser = argparse.ArgumentParser(description="Screen Recognition AI")
    parser.add_argument("--api-key", default=os.environ.get("GEMINI_API_KEY"),
                        help="Google Gemini API key")
    parser.add_argument("--command", default=None,
                        help="Run a single command and exit")
    parser.add_argument("--gui", action="store_true",
                        help="Launch the graphical interface")
    parser.add_argument("--analyze", action="store_true",
                        help="Capture and analyze the screen once, then exit")
    args = parser.parse_args()

    app = ScreenRecognitionAI(api_key=args.api_key)

    if args.command:
        result = app.run_command(args.command)
        import json
        print(json.dumps(result, default=str, indent=2))
        return

    if args.analyze:
        result = app.agent.analyze()
        import json
        print(json.dumps(result, default=str, indent=2))
        return

    if args.gui:
        app.start_gui()
        return

    app.start_cli()


if __name__ == "__main__":
    main()
