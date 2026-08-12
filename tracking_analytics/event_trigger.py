"""Event trigger: fire alerts for geofences, intrusions, unknown faces."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from modeling.two_d_boxes import Detection
from tracking_analytics.object_tracker import Track


@dataclass
class Alert:
    kind: str  # geofence | intrusion | unknown_face | hazard
    message: str
    severity: str = "warning"  # info | warning | critical
    bbox: Optional[list] = None
    identity: str = ""


class EventTrigger:
    """Evaluate detections/tracks against configured rules and emit alerts."""

    def __init__(self, geofence_boxes: Optional[List[list]] = None,
                 restricted_labels: Optional[set] = None) -> None:
        self.geofence_boxes = geofence_boxes or []
        self.restricted_labels = restricted_labels or set()

    def evaluate_detections(self, detections: List[Detection],
                            unknown_face_ids: Optional[set] = None) -> List[Alert]:
        alerts: List[Alert] = []
        unknown_face_ids = unknown_face_ids or set()
        for d in detections:
            if d.label in self.restricted_labels:
                alerts.append(Alert("intrusion", f"Restricted item '{d.label}' detected",
                                    severity="critical", bbox=d.bbox.to_xyxy()))
            if d.label == "face" and d.identity in unknown_face_ids:
                alerts.append(Alert("unknown_face", "Unknown face detected",
                                    severity="critical", bbox=d.bbox.to_xyxy(), identity=d.identity))
            if self.geofence_boxes:
                cx, cy = d.bbox.center
                for zone in self.geofence_boxes:
                    if zone[0] <= cx <= zone[2] and zone[1] <= cy <= zone[3]:
                        alerts.append(Alert("geofence",
                                            f"{d.label} entered restricted zone",
                                            severity="warning", bbox=d.bbox.to_xyxy()))
                        break
        return alerts

    def evaluate_tracks(self, tracks: List[Track], unknown_face_ids: Optional[set] = None) -> List[Alert]:
        alerts: List[Alert] = []
        for t in tracks:
            cx = (t.bbox[0] + t.bbox[2]) / 2
            cy = (t.bbox[1] + t.bbox[3]) / 2
            for zone in self.geofence_boxes:
                if zone[0] <= cx <= zone[2] and zone[1] <= cy <= zone[3]:
                    alerts.append(Alert("geofence",
                                        f"Track {t.track_id} ({t.label}) in restricted zone",
                                        severity="warning", bbox=t.bbox))
        return alerts
