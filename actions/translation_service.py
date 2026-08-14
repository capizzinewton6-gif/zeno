"""
actions - translation_service
==============================
Translate 100+ languages.

Independent actions module for the Autonomous Computer AI Assistant.
Implements the standard execute(task, context) capability contract.
"""

import urllib.parse
from typing import Any, Dict, Optional

from core.capability import Capability

try:
    import requests  # type: ignore
    _HAS_REQUESTS = True
except ImportError:  # pragma: no cover
    _HAS_REQUESTS = False


class TranslationService(Capability):
    """Translate 100+ languages."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.name = "translation_service"
        self.description = "Translate 100+ languages."
        self.timeout = int(self.config.get("timeout", 10))

    def execute(self, task: str, context: Optional[Dict[str, Any]] = None) -> Any:
        if not _HAS_REQUESTS:
            return self.error("requests is not installed. Run: pip install requests")
        text, target = self._parse(task)
        if not text:
            return self.error("No text to translate found in task.")
        translated = self._translate(text, target)
        if translated is None:
            return self.error("Translation services are currently unavailable.")
        return self.ok(f"({target}) {translated}", source_text=text, target=target)

    def _translate(self, text: str, target: str):
        """Try multiple free translation endpoints; return first success or None."""
        endpoints = [
            ("https://translate.iamzash.com/translate", "libre"),
            ("https://libretranslate.de/translate", "libre"),
        ]
        for url, kind in endpoints:
            try:
                resp = requests.post(
                    url,
                    json={"q": text, "source": "auto", "target": target, "format": "text"},
                    timeout=self.timeout,
                )
                if resp.status_code == 200:
                    val = resp.json().get("translatedText")
                    if val:
                        return val
            except Exception:
                continue
        # Fallback: MyMemory (GET, langpair format).
        try:
            resp = requests.get(
                "https://api.mymemory.translated.net/get",
                params={"q": text, "langpair": f"en|{target}"},
                timeout=self.timeout,
            )
            resp.raise_for_status()
            return resp.json()["responseData"]["translatedText"]
        except Exception:
            return None

    def _parse(self, task: str):
        import re
        # Expect: translate "text" to <lang>
        quoted = re.findall(r'["\']([^"\']+)["\']', task)
        text = quoted[0] if quoted else ""
        m = re.search(r"\bto\s+([a-zA-Z]{2,4})\b", task, re.I)
        target = (m.group(1).lower() if m else "es")
        if not text:
            # fallback: "translate <text> to <lang>"
            m2 = re.match(r"translate\s+(.+?)\s+to\s+[a-zA-Z]{2,4}\b", task, re.I)
            text = m2.group(1).strip() if m2 else ""
        return text, target

    def get_name(self) -> str:
        return self.name

    def get_description(self) -> str:
        return self.description
