"""Neural architecture backbone definitions (ResNet, EfficientNet, MobileNet).

These are lightweight reference builders. They are NOT used for training; they
provide canonical channel/layer specs used by model_loader and quantization so
the pipeline can reason about backbone shape without importing torch.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class BackboneSpec:
    name: str
    family: str
    stages: List[int] = field(default_factory=list)
    output_channels: List[int] = field(default_factory=list)
    params_m: float = 0.0
    notes: str = ""


_REGISTRY: Dict[str, BackboneSpec] = {
    "resnet50": BackboneSpec("resnet50", "resnet",
                             [3, 4, 6, 3], [256, 512, 1024, 2048], 25.6,
                             "Deep residual network, widely used for detection backbones."),
    "resnet18": BackboneSpec("resnet18", "resnet",
                             [2, 2, 2, 2], [64, 128, 256, 512], 11.7, "Light ResNet variant."),
    "efficientnet_b0": BackboneSpec("efficientnet_b0", "efficientnet",
                                    [3, 4, 9, 3], [40, 112, 320, 1280], 5.3,
                                    "Compound-scaled mobile backbone."),
    "mobilenet_v3_small": BackboneSpec("mobilenet_v3_small", "mobilenet",
                                       [3, 7, 5, 1], [24, 48, 96, 576], 2.9,
                                       "Depthwise-separable, edge-optimized."),
    "cspdarknet53": BackboneSpec("cspdarknet53", "csp",
                                 [4, 5, 7, 3], [256, 512, 1024, 1024], 27.6,
                                 "Default YOLOv4/v8 backbone family."),
}


def get_backbone(name: str) -> BackboneSpec:
    key = name.lower()
    if key not in _REGISTRY:
        raise KeyError(f"Unknown backbone '{name}'. Known: {sorted(_REGISTRY)}")
    return _REGISTRY[key]


def list_backbones() -> List[str]:
    return sorted(_REGISTRY.keys())
