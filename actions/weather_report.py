"""
actions - weather_report
=========================
Weather forecasts.

Independent actions module for the Autonomous Computer AI Assistant.
Implements the standard execute(task, context) capability contract.
"""

from typing import Any, Dict, Optional

from core.capability import Capability

try:
    import requests  # type: ignore
    _HAS_REQUESTS = True
except ImportError:  # pragma: no cover
    _HAS_REQUESTS = False


class WeatherReport(Capability):
    """Weather forecasts."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.name = "weather_report"
        self.description = "Weather forecasts."
        self.timeout = int(self.config.get("timeout", 10))

    def execute(self, task: str, context: Optional[Dict[str, Any]] = None) -> Any:
        if not _HAS_REQUESTS:
            return self.error("requests is not installed. Run: pip install requests")
        location = self._extract_location(task)
        if not location:
            return self.error("No location found in task.")
        try:
            # wttr.in provides free weather without an API key.
            resp = requests.get(f"https://wttr.in/{location}?format=j1", timeout=self.timeout,
                                headers={"User-Agent": "curl/7.0"})
            resp.raise_for_status()
            data = resp.json()
        except Exception as exc:
            return self.error(str(exc))
        cur = data.get("current_condition", [{}])[0]
        area = data.get("nearest_area", [{}])[0]
        lines = [
            f"Location: {area.get('areaName', [{}])[0].get('value', location)}, {area.get('region', [{}])[0].get('value', '')}, {area.get('country', [{}])[0].get('value', '')}",
            f"Temperature: {cur.get('temp_C')}°C ({cur.get('temp_F')}°F)",
            f"Feels like: {cur.get('FeelsLikeC')}°C",
            f"Condition: {cur.get('weatherDesc', [{}])[0].get('value', 'unknown')}",
            f"Humidity: {cur.get('humidity')}%",
            f"Wind: {cur.get('windspeedKmph')} km/h {cur.get('winddir16Point')}",
        ]
        return self.ok("\n".join(lines), location=location)

    def _extract_location(self, task: str) -> str:
        task = task.strip()
        for prefix in ("weather for:", "weather in:", "weather:", "forecast for:", "forecast in:"):
            if task.lower().startswith(prefix):
                return task[len(prefix):].strip().strip("\"\'")
        return task.strip().strip("\"\'")

    def get_name(self) -> str:
        return self.name

    def get_description(self) -> str:
        return self.description
