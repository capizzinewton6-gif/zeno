"""PCB designer: layout guidance and stackup design."""

from __future__ import annotations

from src.gemini_25_flash_engine import Gemini25FlashEngine


class PCBDesigner:
    def __init__(self, engine: Gemini25FlashEngine | None = None):
        self.engine = engine or Gemini25FlashEngine()

    def stackup(self, layers: int, application: str) -> str:
        return self.engine.generate(
            f"Design a {layers}-layer PCB stackup for {application}.",
            system="You are a PCB stackup engineer.")

    def layout_rules(self, circuit: str) -> str:
        return self.engine.generate(
            f"Provide PCB layout rules (trace widths, clearances, ground planes, "
            f"routing) for: {circuit}",
            system="You are a PCB layout engineer following IPC standards.")

    def drc_checklist(self, board: str) -> str:
        return self.engine.generate(
            f"Provide a DRC checklist for this PCB:\n{board}",
            system="You are a DRC reviewer.")

    def manufacturing_spec(self, board: str) -> str:
        return self.engine.generate(
            f"Produce PCB manufacturing specs (Gerber layers, finish, copper weight, "
            f"soldermask, silkscreen) for:\n{board}",
            system="You are a PCB manufacturing engineer.")
