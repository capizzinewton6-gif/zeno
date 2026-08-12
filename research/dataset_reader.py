"""Dataset reader: load COCO, Pascal VOC, CelebA reference datasets."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class DatasetSample:
    image_path: str
    boxes: List[list]  # list of [x1,y1,x2,y2]
    labels: List[str]


class DatasetReader:
    """Minimal readers for common CV benchmark dataset layouts."""

    @staticmethod
    def load_coco(annotation_path: str, images_dir: str = "") -> List[DatasetSample]:
        if not os.path.exists(annotation_path):
            return []
        with open(annotation_path) as f:
            data = json.load(f)
        id_to_image = {im["id"]: im for im in data.get("images", [])}
        id_to_name = {c["id"]: c["name"] for c in data.get("categories", [])}
        by_image: dict = {}
        for ann in data.get("annotations", []):
            im = id_to_image.get(ann["image_id"])
            if not im:
                continue
            x, y, w, h = ann["bbox"]
            by_image.setdefault(im["id"], []).append(
                ([x, y, x + w, y + h], id_to_name.get(ann["category_id"], "object")))
        out = []
        for im in data.get("images", []):
            items = by_image.get(im["id"], [])
            path = os.path.join(images_dir, im["file_name"]) if images_dir else im["file_name"]
            out.append(DatasetSample(image_path=path,
                                     boxes=[b for b, _ in items],
                                     labels=[l for _, l in items]))
        return out

    @staticmethod
    def load_voc(annotation_dir: str) -> List[DatasetSample]:
        out: List[DatasetSample] = []
        if not os.path.isdir(annotation_dir):
            return out
        try:
            import xml.etree.ElementTree as ET
        except Exception:
            return out
        for name in os.listdir(annotation_dir):
            if not name.endswith(".xml"):
                continue
            tree = ET.parse(os.path.join(annotation_dir, name))
            root = tree.getroot()
            boxes, labels = [], []
            for obj in root.findall("object"):
                b = obj.find("bndbox")
                if b is None:
                    continue
                boxes.append([int(float(b.find(t).text)) for t in ("xmin", "ymin", "xmax", "ymax")])
                labels.append(obj.find("name").text)
            out.append(DatasetSample(image_path=root.find("filename").text or name,
                                     boxes=boxes, labels=labels))
        return out
