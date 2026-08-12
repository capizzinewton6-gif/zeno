"""Model loader: PyTorch, ONNX, TensorRT, OpenVINO weights (lazy + graceful fallback)."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class LoadedModel:
    name: str
    backend: str  # pytorch | onnx | tensorrt | openvino | none
    handle: Any = None
    input_shape: Optional[tuple] = None
    available: bool = False

    def __call__(self, *args, **kwargs):
        if not self.available or self.handle is None:
            raise RuntimeError(f"Model '{self.name}' ({self.backend}) is not loaded.")
        return self.handle(*args, **kwargs)


class ModelLoader:
    """Resolve and load model weights across backends with graceful degradation."""

    def __init__(self, weights_dir: str = "weights") -> None:
        self.weights_dir = weights_dir
        os.makedirs(weights_dir, exist_ok=True)

    # -- discovery -------------------------------------------------------
    def resolve_path(self, name: str) -> Optional[str]:
        for ext in (".pt", ".pth", ".onnx", ".engine", ".xml", ".bin"):
            candidate = os.path.join(self.weights_dir, name + ext)
            if os.path.exists(candidate):
                return candidate
        return None

    # -- backends --------------------------------------------------------
    def _load_pytorch(self, path: str) -> Any:
        try:
            import torch  # type: ignore
        except Exception as exc:  # pragma: no cover
            raise RuntimeError(f"torch unavailable: {exc}")
        return torch.jit.load(path) if path.endswith((".pt", ".pth")) else None

    def _load_onnx(self, path: str) -> Any:
        try:
            import onnxruntime as ort  # type: ignore
        except Exception as exc:  # pragma: no cover
            raise RuntimeError(f"onnxruntime unavailable: {exc}")
        return ort.InferenceSession(path)

    def _load_tensorrt(self, path: str) -> Any:
        try:
            import tensorrt as trt  # type: ignore
            import pycuda.driver as cuda  # noqa: F401  type: ignore
        except Exception as exc:  # pragma: no cover
            raise RuntimeError(f"tensorrt unavailable: {exc}")
        # Minimal: return the engine file path; full runtime lives in edge_computing
        return path

    def _load_openvino(self, path: str) -> Any:
        try:
            from openvino.runtime import Core  # type: ignore
        except Exception as exc:  # pragma: no cover
            raise RuntimeError(f"openvino unavailable: {exc}")
        core = Core()
        return core.compile_model(core.read_model(path), "CPU")

    # -- public ----------------------------------------------------------
    def load(self, name: str, prefer: str = "auto") -> LoadedModel:
        path = self.resolve_path(name)
        if path is None:
            return LoadedModel(name=name, backend="none", available=False)
        order = self._backend_order(path, prefer)
        for backend in order:
            try:
                handle = getattr(self, f"_load_{backend}")(path)
                return LoadedModel(name=name, backend=backend, handle=handle, available=True)
            except RuntimeError:
                continue
        return LoadedModel(name=name, backend="none", available=False)

    @staticmethod
    def _backend_order(path: str, prefer: str) -> list:
        ext = os.path.splitext(path)[1].lower()
        by_ext = {".pt": ["pytorch"], ".pth": ["pytorch"], ".onnx": ["onnx"],
                  ".engine": ["tensorrt"], ".xml": ["openvino"]}
        natural = by_ext.get(ext, ["pytorch", "onnx"])
        if prefer == "auto":
            return natural
        return [prefer] + [b for b in natural if b != prefer]
