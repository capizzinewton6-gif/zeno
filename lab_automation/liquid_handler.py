"""Automated pipetting robots (Opentrons/Tecan) protocol planning."""
from __future__ import annotations


class LiquidHandler:
    def __init__(self, deck_layout: dict | None = None):
        self.deck = deck_layout or {
            "tip_rack": "A1",
            "reagent_reservoir": "A2",
            "sample_plate": "A3",
            "waste": "A4",
        }

    def transfer(self, source: str, dest: str, volume_ul: float,
                 tip_change: bool = True) -> dict:
        return {"action": "transfer", "source": source, "dest": dest,
                "volume_ul": volume_ul, "new_tip": tip_change}

    def serial_dilution(self, source: str, dest_wells: list[str],
                        volume_ul: float, dilution_factor: float) -> list[dict]:
        steps = []
        for well in dest_wells:
            steps.append({
                "action": "transfer", "source": source, "dest": well,
                "volume_ul": volume_ul, "dilution_factor": dilution_factor,
                "new_tip": True,
            })
            source = well
        return steps

    def multichannel_dispense(self, source: str, columns: int, volume_ul: float) -> list[dict]:
        return [{"action": "dispense", "source": source, "column": c,
                 "wells": 8, "volume_ul": volume_ul} for c in range(1, columns + 1)]

    def protocol_summary(self, steps: list[dict]) -> dict:
        total_ul = sum(s.get("volume_ul", 0) for s in steps)
        return {"total_steps": len(steps), "total_volume_ul": total_ul,
                "tips_required": sum(1 for s in steps if s.get("new_tip"))}
