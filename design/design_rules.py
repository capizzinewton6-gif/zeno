"""Engineering design rules: rule-based checks and design guidance."""

from __future__ import annotations

from src.gemini_25_flash_engine import Gemini25FlashEngine

# A small built-in rule base.
DESIGN_RULES = [
    {"id": "DR-001", "rule": "Avoid sharp internal corners; use fillets to reduce stress concentration.",
     "category": "mechanical"},
    {"id": "DR-002", "rule": "Maintain uniform wall thickness for molded/cast parts.",
     "category": "manufacturing"},
    {"id": "DR-003", "rule": "Provide adequate clearance for moving parts (min 0.5 mm).",
     "category": "mechanical"},
    {"id": "DR-004", "rule": "Design for assembly: minimize part count and fastener types.",
     "category": "manufacturing"},
    {"id": "DR-005", "rule": "Keep trace width consistent; avoid 90-degree angles in PCB layout.",
     "category": "electronics"},
    {"id": "DR-006", "rule": "Decouple power supplies near ICs with bypass capacitors.",
     "category": "electronics"},
    {"id": "DR-007", "rule": "Apply a safety factor >= 2 for static structural loads.",
     "category": "safety"},
    {"id": "DR-008", "rule": "Provide strain relief for cables and flexing conductors.",
     "category": "electrical"},
]


class DesignRules:
    def __init__(self, engine: Gemini25FlashEngine | None = None):
        self.engine = engine or Gemini25FlashEngine()
        self.rules = list(DESIGN_RULES)

    def rules_by_category(self, category: str) -> list[dict]:
        return [r for r in self.rules if r["category"] == category]

    def check(self, design_description: str) -> str:
        rules_text = "\n".join(f"- {r['rule']}" for r in self.rules)
        return self.engine.generate(
            f"Check this design against these engineering design rules and report "
            f"violations and recommendations:\nRules:\n{rules_text}\n\nDesign:\n{design_description}",
            system="You are a design-rule checker.")

    def add_rule(self, rule: str, category: str = "general"):
        self.rules.append({"id": f"DR-{len(self.rules)+1:03d}",
                           "rule": rule, "category": category})
