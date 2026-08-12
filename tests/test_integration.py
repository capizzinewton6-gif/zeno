"""Integration tests verifying the full vision pipeline end-to-end."""

from __future__ import annotations

import os
import sys

import numpy as np

# Ensure the project root is importable when run directly.
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from core_vision.camera_stream import Frame  # noqa: E402
from agents.vision_agent import VisionAgent  # noqa: E402
from ai_core.ai_engine import AIEngine  # noqa: E402
from ai_core.safety_layer import SafetyLayer, SafetyConfig  # noqa: E402
from facial_processing.gallery_manager import GalleryManager  # noqa: E402
from facial_processing.embedding_generator import EmbeddingGenerator  # noqa: E402
from modeling.two_d_boxes import BBox, Detection, Detections  # noqa: E402
from tracking_analytics.object_tracker import ObjectTracker  # noqa: E402
from tracking_analytics.event_trigger import EventTrigger  # noqa: E402
from security_compliance.encryption_engine import EncryptionEngine  # noqa: E402
from security_compliance.audit_logger import AuditLogger  # noqa: E402


def _synthetic_frame(index: int = 0) -> Frame:
    img = np.zeros((480, 640, 3), dtype=np.uint8)
    img[100:300, 200:400] = (0, 255, 0)
    return Frame(index=index, image=img, timestamp=float(index))


def test_kernel_math():
    from calculations import bbox_geometry, vector_metrics, probability_scores
    assert abs(bbox_geometry.iou([0, 0, 10, 10], [5, 5, 15, 15]) - 1 / 7) < 1e-6
    assert abs(vector_metrics.cosine_similarity([1, 0], [1, 1]) - 0.7071) < 1e-3
    s = probability_scores.softmax([1, 2, 3])
    assert abs(sum(s) - 1.0) < 1e-6
    print("test_kernel_math: PASS")


def test_bbox_dataclass():
    b = BBox.from_xywh(0, 0, 10, 5)
    assert b.to_xyxy() == [0, 0, 10, 5]
    assert b.area == 50.0
    assert b.center == (5.0, 2.5)
    print("test_bbox_dataclass: PASS")


def test_object_tracker():
    tr = ObjectTracker()
    dets = [Detection.from_xyxy("person", 0.9, [10, 10, 50, 90])]
    active = tr.update(dets)
    assert len(active) >= 1
    print("test_object_tracker: PASS")


def test_encryption_roundtrip():
    enc = EncryptionEngine()
    if not enc.is_secure:
        print("test_encryption_roundtrip: SKIP (cryptography not installed, using XOR fallback)")
    msg = b"biometric-embedding-secret"
    assert enc.decrypt(enc.encrypt(msg)) == msg
    s = "hello gallery"
    assert enc.decrypt_str(enc.encrypt_str(s)) == s
    print("test_encryption_roundtrip: PASS")


def test_audit_chain():
    path = "/tmp/_vision_audit_test.log"
    if os.path.exists(path):
        os.remove(path)
    log = AuditLogger(path)
    log.log("match", {"identity": "id1"}, actor="tester")
    log.log("alert", {"kind": "intrusion"}, actor="tester", severity="critical")
    assert log.verify() is True
    assert len(log.tail()) == 2
    print("test_audit_chain: PASS")


def test_gallery_enroll_match():
    gen = EmbeddingGenerator(dim=128)
    emb = gen.generate(np.zeros((112, 112, 3), dtype=np.uint8) + 40)
    gm = GalleryManager(store_path="/tmp/_vision_gallery_test.json")
    gm.enroll("id1", "Alice", emb)
    ident, score = gm.match(emb)
    assert ident == "id1"
    assert score >= 0.5
    print("test_gallery_enroll_match: PASS")


def test_safety_layer():
    sl = SafetyLayer(SafetyConfig(require_consent=True, encrypt_embeddings=True))
    assert sl.check_biometric_storage(True, False, True) is False
    sl.clear()
    assert sl.check_biometric_storage(True, True, True) is True
    print("test_safety_layer: PASS")


def test_event_trigger():
    det = [Detection.from_xyxy("knife", 0.9, [10, 10, 30, 50])]
    et = EventTrigger(restricted_labels={"knife"})
    alerts = et.evaluate_detections(det)
    assert any(a.kind == "intrusion" for a in alerts)
    print("test_event_trigger: PASS")


def test_vision_agent_perceive():
    va = VisionAgent()
    res = va.perceive(_synthetic_frame(0), instruction="describe the scene")
    assert res.frame_index == 0
    assert isinstance(res.scene, str)
    assert res.decision is not None
    print("test_vision_agent_perceive: PASS")


def test_static_analysis():
    va = VisionAgent()
    out = va.analyze_static(np.zeros((240, 320, 3), dtype=np.uint8),
                            instruction="read any text")
    for key in ("detections", "faces", "scene", "ocr", "decision"):
        assert key in out
    print("test_static_analysis: PASS")


def test_ai_engine_offline():
    eng = AIEngine()
    d = eng.decide("find all people and read any text")
    assert isinstance(d.summary, str)
    report = eng.to_report(d)
    assert "goal" in report and "plan" in report
    print("test_ai_engine_offline: PASS")


def run_all():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    passed = 0
    for t in tests:
        t()
        passed += 1
    print(f"\n{passed}/{len(tests)} tests passed.")


if __name__ == "__main__":
    run_all()
