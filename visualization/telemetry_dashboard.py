"""Token consumption, response speed, and cost tracking charts."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class TelemetrySample:
    label: str
    input_tokens: int = 0
    output_tokens: int = 0
    latency_ms: float = 0.0
    cost_usd: float = 0.0


@dataclass
class TelemetryLog:
    samples: list[TelemetrySample] = field(default_factory=list)

    def add(self, sample: TelemetrySample) -> None:
        self.samples.append(sample)

    @property
    def total_tokens(self) -> int:
        return sum(s.input_tokens + s.output_tokens for s in self.samples)

    @property
    def total_cost(self) -> float:
        return sum(s.cost_usd for s in self.samples)

    @property
    def avg_latency_ms(self) -> float:
        if not self.samples:
            return 0.0
        return sum(s.latency_ms for s in self.samples) / len(self.samples)


class TelemetryDashboard:
    """Tracks and renders token/cost/latency telemetry."""

    # Rough per-1M-token pricing (USD); adjust to taste.
    PRICING = {
        "gemini-2.5-flash": {"input": 0.30, "output": 2.50},
        "gemini-1.5-flash": {"input": 0.075, "output": 0.30},
    }

    def __init__(self) -> None:
        self.log = TelemetryLog()

    def record(self, label: str, model: str, input_tokens: int,
               output_tokens: int, latency_ms: float) -> TelemetrySample:
        price = self.PRICING.get(model, {"input": 0.0, "output": 0.0})
        cost = (input_tokens / 1_000_000 * price["input"]
                + output_tokens / 1_000_000 * price["output"])
        sample = TelemetrySample(label=label, input_tokens=input_tokens,
                                  output_tokens=output_tokens,
                                  latency_ms=latency_ms, cost_usd=cost)
        self.log.add(sample)
        return sample

    def summary(self) -> dict[str, Any]:
        return {
            "samples": len(self.log.samples),
            "total_tokens": self.log.total_tokens,
            "total_cost_usd": round(self.log.total_cost, 6),
            "avg_latency_ms": round(self.log.avg_latency_ms, 1),
        }

    def bar_chart(self, metric: str = "output_tokens", width: int = 40) -> str:
        if not self.log.samples:
            return "(no telemetry)"
        values = [getattr(s, metric) for s in self.log.samples]
        max_v = max(values) if values else 1
        lines: list[str] = [f"{metric} by sample:"]
        for s, v in zip(self.log.samples, values):
            bar = "█" * int((v / max_v) * width) if max_v else ""
            lines.append(f"  {s.label[:20]:<20} {bar} {v}")
        return "\n".join(lines)
