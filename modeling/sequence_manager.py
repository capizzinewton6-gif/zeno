"""Manage FASTA, GenBank, and FASTQ data files."""
from __future__ import annotations

import json
from pathlib import Path


class SequenceManager:
    def __init__(self):
        self.records: list[dict] = []

    def load_fasta(self, path: str | Path) -> list[dict]:
        text = Path(path).read_text(encoding="utf-8")
        records = []
        header, seq_lines = None, []
        for line in text.splitlines():
            if line.startswith(">"):
                if header is not None:
                    records.append(self._record(header, seq_lines))
                header, seq_lines = line[1:], []
            else:
                seq_lines.append(line.strip())
        if header is not None:
            records.append(self._record(header, seq_lines))
        self.records.extend(records)
        return records

    def write_fasta(self, records: list[dict], path: str | Path) -> str:
        out = []
        for r in records:
            out.append(">" + r["id"])
            seq = r["sequence"]
            for i in range(0, len(seq), 70):
                out.append(seq[i:i + 70])
        Path(path).write_text("\n".join(out) + "\n", encoding="utf-8")
        return str(path)

    def load_fastq(self, path: str | Path) -> list[dict]:
        lines = Path(path).read_text(encoding="utf-8").splitlines()
        records = []
        for i in range(0, len(lines), 4):
            if i + 3 < len(lines):
                records.append({
                    "id": lines[i][1:],
                    "sequence": lines[i + 1].strip(),
                    "quality": lines[i + 3].strip(),
                })
        self.records.extend(records)
        return records

    @staticmethod
    def _record(header, seq_lines):
        parts = header.split(None, 1)
        return {"id": parts[0], "description": parts[1] if len(parts) > 1 else "",
                "sequence": "".join(seq_lines)}

    def summary(self) -> dict:
        return {
            "n_records": len(self.records),
            "total_length": sum(len(r["sequence"]) for r in self.records),
            "ids": [r["id"] for r in self.records[:20]],
        }
