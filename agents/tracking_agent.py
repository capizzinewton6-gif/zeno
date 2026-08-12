"""Tracking agent: tracks target persistence across video frames."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from tracking_analytics.occlusion_handler import OcclusionHandler
from tracking_analytics.object_tracker import ObjectTracker, Track
from tracking_analytics.persistence_engine import PersistenceEngine


@dataclass
class TrackingResult:
    tracks: List[Track]
    new_ids: List[int]
    reidentified: List[int]


class TrackingAgent:
    """Maintain multi-object tracks with occlusion handling and ReID."""

    def __init__(self, tracker: Optional[ObjectTracker] = None,
                 occlusion: Optional[OcclusionHandler] = None,
                 persistence: Optional[PersistenceEngine] = None) -> None:
        self.tracker = tracker or ObjectTracker()
        self.occlusion = occlusion or OcclusionHandler()
        self.persistence = persistence or PersistenceEngine()

    def run(self, detections, frame_index: int = 0) -> TrackingResult:
        active = self.tracker.update(detections)
        active = self.occlusion.resolve(active)
        return TrackingResult(tracks=active, new_ids=[t.track_id for t in active if t.hits == 1],
                              reidentified=[])
