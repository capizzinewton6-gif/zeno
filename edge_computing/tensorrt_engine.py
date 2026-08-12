"""TensorRT inference runtime optimization for NVIDIA GPUs / Jetson."""

from __future__ import annotations

from typing import Optional


class TensorRTEngine:
    """Load and run a serialized TensorRT engine; degrades gracefully when absent."""

    def __init__(self, engine_path: Optional[str] = None) -> None:
        self.engine_path = engine_path
        self._runtime = None
        self._engine = None
        self._context = None
        self._available = self._probe()

    def _probe(self) -> bool:
        try:
            import tensorrt as trt  # type: ignore
            return trt is not None
        except Exception:
            return False

    @property
    def available(self) -> bool:
        return self._available

    def load(self) -> bool:
        if not self._available or not self.engine_path:
            return False
        try:
            import tensorrt as trt  # type: ignore
            import pycuda.driver as cuda  # type: ignore  # noqa: F401
            self._runtime = trt.Runtime(trt.Logger())
            with open(self.engine_path, "rb") as f:
                self._engine = self._runtime.deserialize_cuda_engine(f.read())
            self._context = self._engine.create_execution_context()
            return self._engine is not None
        except Exception:
            return False

    def infer(self, *args, **kwargs):
        if self._context is None:
            raise RuntimeError("TensorRT engine not loaded (dependency or path missing).")
        raise NotImplementedError("Engine-specific inference binding is application-defined.")
