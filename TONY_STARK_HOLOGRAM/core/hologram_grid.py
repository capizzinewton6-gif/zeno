"""Holographic floor grid - the spatial canvas."""

from __future__ import annotations

from typing import Optional


class HologramGrid:
    """Raises and configures the holographic reference grid."""

    def __init__(self, ui=None, cells: int = 16):
        self.ui = ui
        self.cells = cells
        self.visible = False

    def raise_grid(self):
        if self.ui:
            self.ui.grid()
        self.visible = True
        if self.ui:
            self.ui.speak(f"Holographic grid materialised - {self.cells}x{self.cells} cells.")

    def lower_grid(self):
        self.visible = False
        if self.ui:
            self.ui.speak("Holographic grid lowered.")

    def status(self) -> dict:
        return {"grid_visible": self.visible, "cells": self.cells}

    def execute(self, task: str, context=None):
        if task in ("raise", "show", "on"):
            self.raise_grid()
            return self.status()
        if task in ("lower", "hide", "off"):
            self.lower_grid()
            return self.status()
        return {"module": "hologram_grid", "task": task, "status": "unknown"}
