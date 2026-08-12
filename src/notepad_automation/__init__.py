"""Autonomous Notepad automation.

Generates engineering documentation (.txt) automatically. On Windows it can
drive notepad.exe via pyautogui; elsewhere it writes files directly.
"""

from .notepad import NotepadAutomation, DOCUMENT_NAMES, DOCUMENT_PROMPTS

__all__ = ["NotepadAutomation", "DOCUMENT_NAMES", "DOCUMENT_PROMPTS"]
