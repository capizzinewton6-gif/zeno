"""Visual agent: understands screen content."""

from __future__ import annotations

import logging
from typing import Any, Dict, List

from ai_models.vision_model import VisionModel
from computer_vision.image_analyzer import ImageAnalyzer
from computer_vision.color_analyzer import ColorAnalyzer
from recognition.screen_layout import ScreenLayout
from recognition.ui_element_detector import UIElementDetector

logger = logging.getLogger(__name__)


class VisualAgent:
    """Understands the visual content of the screen."""

    def __init__(self, vision_model: VisionModel | None = None) -> None:
        self.vision_model = vision_model or VisionModel()
        self.image_analyzer = ImageAnalyzer()
        self.color_analyzer = ColorAnalyzer()
        self.layout = ScreenLayout()
        self.ui_detector = UIElementDetector()

    def analyze(self, image: Any) -> Dict[str, Any]:
        return {
            "description": self.vision_model.understand(image),
            "layout": self.layout.analyze(image),
            "ui_elements": self.ui_detector.detect(image),
            "image_stats": self.image_analyzer.statistics(image),
            "colors": {
                "dominant": self.color_analyzer.dominant_colors(image),
                "distribution": self.color_analyzer.color_distribution(image),
                "average": self.color_analyzer.average_color(image),
            },
        }

    def describe(self, image: Any, question: str = "What is shown on this screen?") -> str:
        return self.vision_model.understand(image, question)

    def detect_changes(self, before: Any, after: Any) -> str:
        return self.vision_model.detect_changes(before, after)
