"""Embedding generator: 128-d / 512-d biometric face vectors."""

from __future__ import annotations

from typing import List, Optional

import numpy as np

from modeling.feature_vectors import FeatureVector


class EmbeddingGenerator:
    """Generate face embeddings using InsightFace, face_recognition, or a deterministic fallback."""

    def __init__(self, backend: str = "auto", dim: int = 512) -> None:
        self.backend = backend
        self.dim = dim
        self._insight = None
        self._fr = None

    def generate(self, aligned_face: np.ndarray) -> np.ndarray:
        """Return an L2-normalized embedding vector."""
        if aligned_face is None or aligned_face.size == 0:
            return np.zeros(self.dim, dtype=np.float32)
        vec = self._insightface(aligned_face)
        if vec is not None:
            return vec
        vec = self._face_recognition(aligned_face)
        if vec is not None:
            return vec
        return self._fallback(aligned_face)

    def to_feature_vector(self, aligned_face: np.ndarray, label: str = "") -> FeatureVector:
        return FeatureVector(self.generate(aligned_face), label=label, source="embedding_generator")

    def _insightface(self, face: np.ndarray) -> Optional[np.ndarray]:
        try:
            from insightface.app import FaceAnalysis  # type: ignore
            if self._insight is None:
                self._insight = FaceAnalysis(name="buffalo_l")
                self._insight.prepare(ctx_id=-1)
            faces = self._insight.get(np.ascontiguousarray(face))
            if faces:
                emb = faces[0].embedding.astype(np.float32)
                n = np.linalg.norm(emb)
                return emb / n if n > 0 else emb
        except Exception:
            return None
        return None

    def _face_recognition(self, face: np.ndarray) -> Optional[np.ndarray]:
        try:
            import face_recognition  # type: ignore
            rgb = face[:, :, ::-1] if face.ndim == 3 else face
            encs = face_recognition.face_encodings(rgb)
            if encs:
                emb = np.asarray(encs[0], dtype=np.float32)
                n = np.linalg.norm(emb)
                return emb / n if n > 0 else emb
        except Exception:
            return None
        return None

    def _fallback(self, face: np.ndarray) -> np.ndarray:
        """Deterministic hash-based embedding so the pipeline runs without ML deps."""
        small = np.asarray(face, dtype=np.float32)
        if small.ndim == 3:
            small = small.mean(axis=2)
        import hashlib
        h = hashlib.sha256(small.tobytes()).digest()
        seed = np.frombuffer(h * (self.dim // 32 + 1), dtype=np.uint8).astype(np.float32)
        emb = (seed[:self.dim] / 255.0 - 0.5)
        n = np.linalg.norm(emb)
        return emb / n if n > 0 else emb
