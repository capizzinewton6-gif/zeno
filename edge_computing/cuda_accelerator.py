"""PyTorch CUDA and CuDNN acceleration wrapper."""

from __future__ import annotations

from typing import Optional


class CudaAccelerator:
    """Thin wrapper around PyTorch CUDA availability and device management."""

    def __init__(self, device_id: int = 0) -> None:
        self.device_id = device_id
        self._torch = None

    @property
    def available(self) -> bool:
        try:
            import torch  # type: ignore
            return torch.cuda.is_available()
        except Exception:
            return False

    @property
    def device_name(self) -> str:
        try:
            import torch  # type: ignore
            if torch.cuda.is_available():
                return torch.cuda.get_device_name(self.device_id)
        except Exception:
            pass
        return "cpu"

    def device(self):
        try:
            import torch  # type: ignore
            return torch.device(f"cuda:{self.device_id}" if torch.cuda.is_available() else "cpu")
        except Exception:
            return "cpu"

    def to_device(self, tensor, non_blocking: bool = True):
        try:
            return tensor.to(self.device(), non_blocking=non_blocking)
        except Exception:
            return tensor

    def memory_allocated_mb(self) -> float:
        try:
            import torch  # type: ignore
            if torch.cuda.is_available():
                return torch.cuda.memory_allocated(self.device_id) / (1024 ** 2)
        except Exception:
            pass
        return 0.0

    def synchronize(self) -> None:
        try:
            import torch  # type: ignore
            if torch.cuda.is_available():
                torch.cuda.synchronize(self.device_id)
        except Exception:
            pass
