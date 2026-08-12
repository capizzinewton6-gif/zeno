"""Autonomous Painter (Microsoft Paint) automation.

Generates engineering blueprint PNGs without manual drawing. On Windows it
can drive mspaint.exe via pyautogui; elsewhere it falls back to matplotlib.
"""

from .painter import PainterAutomation

__all__ = ["PainterAutomation"]
