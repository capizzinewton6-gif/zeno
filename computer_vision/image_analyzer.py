"""Analyze screen images."""

from __future__ import annotations

import logging
from typing import Any, Dict, Tuple

logger = logging.getLogger(__name__)


class ImageAnalyzer:
    """Computes basic image statistics and properties."""

    def statistics(self, image: Any) -> Dict[str, Any]:
        arr = self._to_array(image)
        if arr is None:
            return {"available": False}
        try:
            mean = float(arr.mean())
            std = float(arr.std())
            return {
                "available": True,
                "shape": list(arr.shape),
                "dtype": str(arr.dtype),
                "mean": round(mean, 2),
                "std": round(std, 2),
                "min": int(arr.min()),
                "max": int(arr.max()),
            }
        except Exception as exc:
            logger.warning("image statistics failed: %s", exc)
            return {"available": False, "error": str(exc)}

    def dominant_color(self, image: Any) -> Tuple[int, int, int]:
        try:
            import numpy as np  # type: ignore
            arr = self._to_array(image)
            if arr is None:
                return (0, 0, 0)
            pixels = arr.reshape(-1, arr.shape[-1])
            return tuple(int(x) for x in pixels.mean(axis=0))[:3]
        except Exception as exc:
            logger.debug("dominant_color failed: %s", exc)
            return (0, 0, 0)

    def brightness(self, image: Any) -> float:
        stats = self.statistics(image)
        return stats.get("mean", 0)

    def is_dark(self, image: Any, threshold: float = 60.0) -> bool:
        return self.brightness(image) < threshold

    def resize(self, image: Any, width: int, height: int) -> Any:
        try:
            from PIL import Image  # type: ignore
            import io
            img = self._to_pil(image)
            if img is not None:
                return img.resize((width, height))
        except Exception as exc:
            logger.debug("resize failed: %s", exc)
        return image

    @staticmethod
    def _to_array(image: Any):
        try:
            import numpy as np  # type: ignore
            from PIL import Image  # type: ignore
            import io
            if isinstance(image, str):
                return np.array(Image.open(image))
            if isinstance(image, (bytes, bytearray)):
                return np.array(Image.open(io.BytesIO(image)))
            if isinstance(image, Image.Image):
                return np.array(image)
            if hasattr(image, "rgb") and hasattr(image, "size"):
                arr = np.frombuffer(image.rgb, dtype=np.uint8)
                return arr.reshape((image.size[1], image.size[0], 3))
        except Exception as exc:
            logger.debug("_to_array failed: %s", exc)
        return None

    @staticmethod
    def _to_pil(image: Any):
        try:
            from PIL import Image  # type: ignore
            import io
            if isinstance(image, str):
                return Image.open(image)
            if isinstance(image, (bytes, bytearray)):
                return Image.open(io.BytesIO(image))
            if isinstance(image, Image.Image):
                return image
            if hasattr(image, "rgb") and hasattr(image, "size"):
                return Image.frombytes("RGB", image.size, image.rgb)
        except Exception:
            return None
