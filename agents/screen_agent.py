"""Main screen understanding agent.

Orchestrates capture, recognition, understanding, memory, and automation
into a single coherent screen-understanding pipeline.
"""

from __future__ import annotations

import logging
import time
from typing import Any, Dict, Optional

from ai_core.context_manager import ContextManager
from ai_core.ai_engine import get_engine
from agents.visual_agent import VisualAgent
from agents.assistant_agent import AssistantAgent
from agents.automation_agent import AutomationAgent
from agents.learning_agent import LearningAgent
from computer_vision.visual_memory import VisualMemory
from recognition.text_recognition import TextRecognition
from recognition.window_detector import WindowDetector
from screen_capture.screenshot_manager import ScreenshotManager
from understanding.screen_interpreter import ScreenInterpreter
from understanding.error_analyzer import ErrorAnalyzer

logger = logging.getLogger(__name__)


class ScreenAgent:
    """Top-level screen recognition and understanding agent."""

    def __init__(self, engine=None, capture: bool = True) -> None:
        self.engine = engine or get_engine()
        self.context = ContextManager()
        self.memory = VisualMemory()
        self.screenshot = ScreenshotManager()
        self.visual = VisualAgent()
        self.assistant = AssistantAgent(context=self.context)
        self.automation = AutomationAgent(assistant=self.assistant, context=self.context)
        self.learning = LearningAgent(memory=self.memory)
        self.interpreter = ScreenInterpreter(engine=self.engine)
        self.text = TextRecognition()
        self.windows = WindowDetector()
        self.errors = ErrorAnalyzer(engine=self.engine)
        self._last_image: Any = None

    # ------------------------------------------------------------------ capture
    def capture_screen(self, region: Optional[tuple] = None) -> Optional[str]:
        path = self.screenshot.capture(region=region)
        if path:
            self.context.set("last_screenshot", path)
        return path

    def load_image(self, path: str) -> Any:
        try:
            from PIL import Image  # type: ignore
            self._last_image = Image.open(path)
            return self._last_image
        except Exception as exc:
            logger.warning("load_image failed: %s", exc)
            return None

    # ------------------------------------------------------------------ analyze
    def analyze(self, image: Any = None, goal: Optional[str] = None) -> Dict[str, Any]:
        image = image or self._last_image
        if image is None:
            path = self.capture_screen()
            if path:
                image = self.load_image(path)
        if image is None:
            return {"error": "No image available to analyze."}

        visual = self.visual.analyze(image)
        interpretation = self.interpreter.interpret(image)
        ocr_text = self.text.read_all(image)
        windows = self.windows.list_windows()
        error_check = self.errors.detect(image, ocr_text=ocr_text)

        state = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "screenshot": self.context.get("last_screenshot"),
            "visual": visual,
            "interpretation": interpretation,
            "ocr": ocr_text,
            "windows": windows,
            "errors": error_check,
        }
        self.context.update(state)
        self.memory.remember(state)

        result = dict(state)
        if goal:
            result["suggestion"] = self.assistant.suggest(goal, state, image)
        return result

    # ------------------------------------------------------------------ act
    def suggest_action(self, goal: str, image: Any = None) -> Dict[str, Any]:
        image = image or self._last_image
        return self.assistant.suggest(goal, self.context.current, image)

    def automate(self, goal: str, image: Any = None, dry_run: bool = False) -> Dict[str, Any]:
        image = image or self._last_image
        return self.automation.execute_goal(goal, self.context.current, image, dry_run=dry_run)

    # ------------------------------------------------------------------ learn
    def learn_pattern(self, name: str, image: Any = None, metadata: Optional[Dict] = None) -> Dict[str, Any]:
        image = image or self._last_image
        if image is None:
            return {"error": "No image to learn from."}
        return self.learning.learn(name, image, metadata)

    def recognize_patterns(self, image: Any = None) -> list:
        image = image or self._last_image
        if image is None:
            return []
        return self.learning.recognize(image)

    # ------------------------------------------------------------------ state
    def current_state(self) -> Dict[str, Any]:
        return self.context.current

    def save_memory(self) -> None:
        self.memory.save()
        self.learning.persist_memory()
