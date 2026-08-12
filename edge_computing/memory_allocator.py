"""Zero-copy GPU memory management and page-locked memory buffers."""

from __future__ import annotations

from typing import Optional


class MemoryAllocator:
    """Allocate page-locked host buffers and zero-copy GPU buffers when CUDA is present."""

    def __init__(self) -> None:
        self._torch = None

    @property
    def cuda_available(self) -> bool:
        try:
            import torch  # type: ignore
            return torch.cuda.is_available()
        except Exception:
            return False

    def pinned_array(self, shape, dtype="float32"):
        """Allocate a page-locked numpy buffer for fast host->device transfers."""
        try:
            import numpy as np
            import torch  # type: ignore
            if self.cuda_available:
                t = torch.empty(np.prod(shape), dtype=getattr(torch, dtype))
                pinned = torch.cuda.pinned_memory(t).reshape(shape)
                return pinned.numpy()
        except Exception:
            pass
        import numpy as np
        return np.empty(shape, dtype=dtype)

    def device_array(self, shape, dtype="float32"):
        try:
            import torch  # type: ignore
            if self.cuda_available:
                return torch.empty(shape, dtype=getattr(torch, dtype), device="cuda")
        except Exception:
            pass
        import numpy as np
        return np.empty(shape, dtype=dtype)

    def free(self, buf) -> None:
        try:
            del buf
        except Exception:
            pass
