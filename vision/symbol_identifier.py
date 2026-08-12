"""Identify bra-ket notation, tensors, operator hats, and Dirac slash notation."""

from __future__ import annotations

import re


class SymbolIdentifier:
    """Classify physics notation in expressions / OCR output."""

    BRAKET = re.compile(r"<[a-zA-Z]+|[^|>]+|[a-zA-Z]+\|>")
    TENSOR = re.compile(r"[A-Za-z]+_\{[^}]+\}|[A-Za-z]+\^[A-Za-z0-9]")
    OPERATOR_HAT = re.compile(r"\\hat\{[a-zA-Z]+\}|\\hat[a-zA-Z]")
    DIRAC_SLASH = re.compile(r"\\slashed\{[a-zA-Z]+\}|[a-zA-Z]+\\!\\!/")

    @classmethod
    def identify(cls, text: str) -> dict[str, list[str]]:
        return {
            "braket": cls.BRAKET.findall(text),
            "tensor": cls.TENSOR.findall(text),
            "operator_hat": cls.OPERATOR_HAT.findall(text),
            "dirac_slash": cls.DIRAC_SLASH.findall(text),
        }

    @staticmethod
    def has_spinor(text: str) -> bool:
        return "psi" in text.lower() or "u(" in text or "v(" in text or "bar" in text
