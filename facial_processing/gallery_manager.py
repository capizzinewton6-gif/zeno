"""Gallery manager: enroll, update, index known subject faces."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

import numpy as np

from facial_processing.vector_matcher import VectorMatcher
from security_compliance.encryption_engine import EncryptionEngine


@dataclass
class Subject:
    identity: str
    name: str
    embeddings: List[List[float]] = field(default_factory=list)
    metadata: Dict = field(default_factory=dict)


class GalleryManager:
    """In-memory + JSON-backed face gallery with optional encryption."""

    def __init__(self, store_path: str = "memory/known_faces.json",
                 matcher: Optional[VectorMatcher] = None,
                 encryptor: Optional[EncryptionEngine] = None) -> None:
        self.store_path = store_path
        self.matcher = matcher or VectorMatcher()
        self.encryptor = encryptor
        self.subjects: Dict[str, Subject] = {}
        self.load()

    def enroll(self, identity: str, name: str, embedding: np.ndarray,
               metadata: Optional[Dict] = None) -> None:
        emb_list = np.asarray(embedding, dtype=np.float32).tolist()
        if identity not in self.subjects:
            self.subjects[identity] = Subject(identity=identity, name=name, metadata=metadata or {})
        self.subjects[identity].embeddings.append(emb_list)
        self.save()

    def match(self, query: np.ndarray, threshold: float = 0.55) -> Tuple[str, float]:
        """Return (identity or '', similarity score)."""
        if not self.subjects:
            return ("", 0.0)
        best_identity = ""
        best_score = 0.0
        for ident, subj in self.subjects.items():
            gallery = np.array(subj.embeddings, dtype=np.float32) if subj.embeddings else np.zeros((0, 0))
            idx, score = self.matcher.match(query, gallery, threshold)
            if idx >= 0 and score > best_score:
                best_score = score
                best_identity = ident
        return (best_identity, best_score)

    def remove(self, identity: str) -> bool:
        if identity in self.subjects:
            del self.subjects[identity]
            self.save()
            return True
        return False

    def list_subjects(self) -> List[str]:
        return list(self.subjects.keys())

    # -- persistence -----------------------------------------------------
    def save(self) -> None:
        data = {"version": 1, "identities": {}}
        for ident, subj in self.subjects.items():
            data["identities"][ident] = {
                "name": subj.name,
                "embeddings": subj.embeddings,
                "metadata": subj.metadata,
            }
        payload = json.dumps(data)
        if self.encryptor is not None:
            payload = self.encryptor.encrypt_str(payload)
        os.makedirs(os.path.dirname(self.store_path) or ".", exist_ok=True)
        with open(self.store_path, "w", encoding="utf-8") as f:
            f.write(payload)

    def load(self) -> None:
        if not os.path.exists(self.store_path):
            return
        with open(self.store_path, "r", encoding="utf-8") as f:
            raw = f.read()
        if self.encryptor is not None:
            try:
                raw = self.encryptor.decrypt_str(raw)
            except Exception:
                raw = "{}"
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            data = {}
        for ident, info in data.get("identities", {}).items():
            self.subjects[ident] = Subject(
                identity=ident, name=info.get("name", ident),
                embeddings=info.get("embeddings", []),
                metadata=info.get("metadata", {}))
