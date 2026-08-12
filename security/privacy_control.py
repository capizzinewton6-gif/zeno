"""Protect screen data and enforce privacy controls."""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Tuple

logger = logging.getLogger(__name__)


class PrivacyControl:
    """Redacts and protects sensitive screen data."""

    SENSITIVE_KEYWORDS = (
        "password", "passwd", "pwd", "secret", "token", "api key", "apikey",
        "credit card", "ssn", "social security", "private key", "pin",
    )

    def __init__(self) -> None:
        self.redacted_regions: List[Tuple[int, int, int, int]] = []

    def is_sensitive_text(self, text: str) -> bool:
        low = (text or "").lower()
        return any(kw in low for kw in self.SENSITIVE_KEYWORDS)

    def redact_text(self, text: str) -> str:
        """Replace sensitive-looking content with placeholders."""
        if not text:
            return text
        low = text.lower()
        for kw in self.SENSITIVE_KEYWORDS:
            idx = low.find(kw)
            while idx != -1:
                # Redact the rest of the line after the keyword
                line_end = text.find("\n", idx)
                if line_end == -1:
                    line_end = len(text)
                text = text[:idx + len(kw)] + ": [REDACTED]" + text[line_end:]
                low = text.lower()
                idx = low.find(kw, idx + len(kw) + len(": [REDACTED]"))
        return text

    def add_redacted_region(self, region: Tuple[int, int, int, int]) -> None:
        self.redacted_regions.append(region)

    def mask_region(self, image: Any) -> Any:
        """Black out redacted regions of an image."""
        try:
            from PIL import Image, ImageDraw  # type: ignore
            import io
            if isinstance(image, str):
                img = Image.open(image)
            elif isinstance(image, (bytes, bytearray)):
                img = Image.open(io.BytesIO(image))
            else:
                img = image
            draw = ImageDraw.Draw(img)
            for x, y, w, h in self.redacted_regions:
                draw.rectangle([x, y, x + w, y + h], fill=(0, 0, 0))
            return img
        except Exception as exc:
            logger.debug("mask_region failed: %s", exc)
            return image

    def screen_report(self, screen_data: Dict[str, Any]) -> Dict[str, Any]:
        """Return a privacy-sanitized summary of screen data."""
        sanitized = {}
        for key, value in screen_data.items():
            if isinstance(value, str):
                sanitized[key] = self.redact_text(value)
            else:
                sanitized[key] = value
        return sanitized

    def should_store(self, screen_data: Dict[str, Any]) -> bool:
        """Decide whether screen data may be stored."""
        text = str(screen_data)
        # Allow storage but it will be redacted; never store raw secrets
        return not any(kw in text.lower() for kw in ("private key", "secret key"))
