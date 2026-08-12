"""Project file manager: organized file storage."""

from __future__ import annotations

import os
import shutil
from typing import List


class FileManager:
    def __init__(self, root: str = "projects"):
        self.root = root
        os.makedirs(root, exist_ok=True)

    def project_dir(self, name: str) -> str:
        path = os.path.join(self.root, name)
        os.makedirs(path, exist_ok=True)
        return path

    def subfolder(self, project: str, folder: str) -> str:
        path = os.path.join(self.project_dir(project), folder)
        os.makedirs(path, exist_ok=True)
        return path

    def write(self, project: str, filename: str, content: str,
              folder: str = "") -> str:
        base = self.project_dir(project)
        path = os.path.join(base, folder) if folder else base
        os.makedirs(path, exist_ok=True)
        full = os.path.join(path, filename)
        with open(full, "w", encoding="utf-8") as f:
            f.write(content)
        return full

    def write_bytes(self, project: str, filename: str, data: bytes,
                    folder: str = "") -> str:
        base = self.project_dir(project)
        path = os.path.join(base, folder) if folder else base
        os.makedirs(path, exist_ok=True)
        full = os.path.join(path, filename)
        with open(full, "wb") as f:
            f.write(data)
        return full

    def list_files(self, project: str) -> List[str]:
        base = self.project_dir(project)
        files = []
        for dirpath, _, filenames in os.walk(base):
            for fn in filenames:
                files.append(os.path.relpath(os.path.join(dirpath, fn), base))
        return files

    def zip_project(self, project: str) -> str:
        base = self.project_dir(project)
        archive = shutil.make_archive(base, "zip", base)
        return archive

    def delete_project(self, project: str) -> bool:
        base = os.path.join(self.root, project)
        if os.path.isdir(base):
            shutil.rmtree(base)
            return True
        return False
