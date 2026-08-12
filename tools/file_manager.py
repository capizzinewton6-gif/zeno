"""Manage simulation outputs, HDF5 datasets, and mesh files."""

from __future__ import annotations

import json
import os
import time
from typing import Any

import numpy as np


class FileManager:
    """Persist and reload simulation artifacts."""

    def __init__(self, root: str = "outputs"):
        self.root = root
        os.makedirs(self.root, exist_ok=True)

    def _path(self, name: str) -> str:
        safe = name.replace(" ", "_")
        return os.path.join(self.root, safe)

    def save_array(self, name: str, array: np.ndarray) -> str:
        path = self._path(name + ".npy")
        np.save(path, np.asarray(array))
        return path

    def load_array(self, name: str) -> np.ndarray:
        return np.load(self._path(name + ".npy"))

    def save_meta(self, name: str, meta: dict[str, Any]) -> str:
        path = self._path(name + ".json")
        with open(path, "w") as f:
            json.dump(meta, f, indent=2, default=str)
        return path

    def save_hdf5(self, name: str, datasets: dict[str, np.ndarray]) -> str:
        """Save multiple named arrays to a single HDF5 file (lazy h5py import)."""
        path = self._path(name + ".h5")
        import h5py  # local import; optional dependency
        with h5py.File(path, "w") as f:
            for key, arr in datasets.items():
                f.create_dataset(key, data=np.asarray(arr))
        return path

    def timestamp(self) -> str:
        return time.strftime("%Y%m%d-%H%M%S")

    def list_outputs(self) -> list[str]:
        return sorted(os.listdir(self.root))
