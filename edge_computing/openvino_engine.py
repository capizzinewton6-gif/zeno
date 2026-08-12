"""Intel OpenVINO runtime engine optimization for CPU/VPU."""

from __future__ import annotations

from typing import Optional


class OpenVINOEngine:
    """Load and run an OpenVINO IR model; degrades gracefully when absent."""

    def __init__(self, model_xml: Optional[str] = None,
                 weights_bin: Optional[str] = None, device: str = "CPU") -> None:
        self.model_xml = model_xml
        self.weights_bin = weights_bin
        self.device = device
        self._core = None
        self._model = None
        self._compiled = None

    @property
    def available(self) -> bool:
        try:
            from openvino import runtime  # type: ignore  # noqa: F401
            return True
        except Exception:
            return False

    def load(self) -> bool:
        if not self.available or not self.model_xml:
            return False
        try:
            from openvino import Core  # type: ignore
            self._core = Core()
            self._model = self._core.read_model(self.model_xml, self.weights_bin)
            self._compiled = self._core.compile_model(self._model, self.device)
            return self._compiled is not None
        except Exception:
            return False

    def infer(self, inputs):
        if self._compiled is None:
            raise RuntimeError("OpenVINO model not compiled.")
        return self._compiled(inputs)
