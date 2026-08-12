"""Containment monitoring and airflow alarms."""
from __future__ import annotations


class BiosafetyInterlocks:
    @staticmethod
    def check_airflow(face_velocity_m_s: float, min_velocity: float = 0.4) -> dict:
        ok = face_velocity_m_s >= min_velocity
        return {"face_velocity": face_velocity_m_s,
                "minimum": min_velocity, "status": "ok" if ok else "ALARM",
                "alarm": "low airflow" if not ok else None}

    @staticmethod
    def check_pressure_differential(pa: float, target_pa: float = -50) -> dict:
        ok = pa <= target_pa  # negative pressure for containment
        return {"differential_pa": pa, "target_pa": target_pa,
                "status": "ok" if ok else "ALARM",
                "alarm": "loss of negative pressure" if not ok else None}

    @staticmethod
    def hepa_integrity(integrity_pct: float, threshold: float = 99.97) -> dict:
        ok = integrity_pct >= threshold
        return {"integrity": integrity_pct, "threshold": threshold,
                "status": "ok" if ok else "ALARM",
                "alarm": "HEPA filter breach" if not ok else None}

    @staticmethod
    def door_interlock(door_open: bool, during_operation: bool = True) -> dict:
        alarm = door_open and during_operation
        return {"door_open": door_open, "operation_active": during_operation,
                "status": "ok" if not alarm else "ALARM",
                "alarm": "door open during operation" if alarm else None}
