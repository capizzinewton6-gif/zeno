"""File manager: video files, weight checkpoints, and datasets."""

from __future__ import annotations

import os
import shutil
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class Asset:
    path: str
    kind: str  # video | weights | dataset | config
    size_mb: float


class FileManager:
    """Locate and catalog model weights, videos, and datasets."""

    def __init__(self, base_dir: str = ".") -> None:
        self.base_dir = base_dir

    def find_weights(self, subdir: str = "weights") -> List[Asset]:
        return self._scan(subdir, {"*.pt", "*.onnx", "*.engine", "*.wts", "*.bin"})

    def find_videos(self, subdir: str = "videos") -> List[Asset]:
        return self._scan(subdir, {"*.mp4", "*.avi", "*.mov", "*.mkv"})

    def find_datasets(self, subdir: str = "datasets") -> List[Asset]:
        return self._scan(subdir, {"*.zip", "*.tar", "*.tar.gz"})

    def _scan(self, subdir: str, patterns: set) -> List[Asset]:
        root = os.path.join(self.base_dir, subdir)
        out: List[Asset] = []
        if not os.path.isdir(root):
            return out
        for dirpath, _, files in os.walk(root):
            for name in files:
                if any(name.endswith(ext.replace("*", "")) for ext in patterns):
                    p = os.path.join(dirpath, name)
                    try:
                        size = os.path.getsize(p) / (1024 ** 2)
                    except OSError:
                        size = 0.0
                    out.append(Asset(path=p, kind=subdir.rstrip("s"), size_mb=size))
        return out

    def ensure_dir(self, path: str) -> str:
        os.makedirs(path, exist_ok=True)
        return path

    def safe_copy(self, src: str, dst_dir: str) -> Optional[str]:
        if not os.path.isfile(src):
            return None
        os.makedirs(dst_dir, exist_ok=True)
        dst = os.path.join(dst_dir, os.path.basename(src))
        shutil.copy2(src, dst)
        return dst
