"""Simulation manager: playback speed, frame skipping, simulation parameters."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator, Optional

from core_vision.camera_stream import Frame


@dataclass
class SimulationConfig:
    playback_speed: float = 1.0
    frame_skip: int = 0
    max_frames: Optional[int] = None
    loop: bool = True


class SimulationManager:
    """Control playback parameters over any frame iterator."""

    def __init__(self, config: SimulationConfig = SimulationConfig()) -> None:
        self.config = config

    def run(self, stream: Iterator[Frame]) -> Iterator[Frame]:
        count = 0
        skip = self.config.frame_skip
        for frame in stream:
            if skip and count % (skip + 1) != 0:
                count += 1
                continue
            if self.config.max_frames is not None and count >= self.config.max_frames:
                break
            yield frame
            count += 1
