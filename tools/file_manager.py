"""Manage FASTA, FASTQ, BAM, PDB, and FCS files."""
from __future__ import annotations

import gzip
import json
from pathlib import Path


class FileManager:
    @staticmethod
    def read_file(path: str | Path, encoding: str = "utf-8") -> str:
        p = Path(path)
        if p.suffix == ".gz":
            with gzip.open(p, "rt", encoding=encoding) as f:
                return f.read()
        return p.read_text(encoding=encoding)

    @staticmethod
    def write_file(path: str | Path, content: str, compress: bool = False) -> str:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        if compress or p.suffix == ".gz":
            with gzip.open(p, "wt", encoding="utf-8") as f:
                f.write(content)
        else:
            p.write_text(content, encoding="utf-8")
        return str(p)

    @staticmethod
    def detect_format(path: str | Path) -> str:
        ext = Path(path).suffix.lower()
        if ext == ".gz":
            ext = Path(path).suffixes[-2].lower()
        formats = {".fasta": "FASTA", ".fa": "FASTA", ".fna": "FASTA",
                    ".fastq": "FASTQ", ".fq": "FASTQ",
                    ".bam": "BAM", ".sam": "SAM",
                    ".pdb": "PDB", ".ent": "PDB",
                    ".fcs": "FCS", ".json": "JSON",
                    ".csv": "CSV", ".tsv": "TSV", ".genbank": "GenBank"}
        return formats.get(ext, ext or "unknown")

    @staticmethod
    def count_records(path: str | Path, fmt: str | None = None) -> int:
        if fmt is None:
            fmt = FileManager.detect_format(path)
        text = FileManager.read_file(path)
        if fmt == "FASTA":
            return sum(1 for line in text.splitlines() if line.startswith(">"))
        if fmt == "FASTQ":
            return len([l for l in text.splitlines() if l]) // 4
        return -1

    @staticmethod
    def load_json(path: str | Path) -> dict:
        return json.loads(FileManager.read_file(path))

    @staticmethod
    def save_json(data: dict, path: str | Path, indent: int = 2) -> str:
        return FileManager.write_file(path, json.dumps(data, indent=indent))
