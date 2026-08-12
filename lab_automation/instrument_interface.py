"""Connect to thermocyclers, sequencers, and plate readers (protocol/JSON)."""
from __future__ import annotations


class Thermocycler:
    @staticmethod
    def pcr_program(denature_c=95, denature_s=30, anneal_c=55,
                    anneal_s=30, extend_c=72, extend_s=60, cycles=30,
                    final_extend_s=300, hot_start=True) -> list[dict]:
        prog = []
        if hot_start:
            prog.append({"stage": "hot_start", "temp_c": denature_c, "duration_s": 120})
        prog.append({"stage": "initial_denature", "temp_c": denature_c, "duration_s": denature_s * 2})
        for c in range(cycles):
            prog.append({"cycle": c + 1, "denature": denature_c,
                         "anneal": anneal_c, "extend": extend_c})
        prog.append({"stage": "final_extend", "temp_c": extend_c, "duration_s": final_extend_s})
        prog.append({"stage": "hold", "temp_c": 4})
        return prog

    @staticmethod
    def estimated_time(program: list[dict], cycles=30) -> int:
        # rough seconds
        return cycles * (30 + 30 + 60) + 300 + 120


class PlateReader:
    @staticmethod
    def absorbance_protocol(wavelength_nm: int = 600, n_reads: int = 1,
                            shake: bool = True) -> dict:
        return {"mode": "absorbance", "wavelength_nm": wavelength_nm,
                "reads_per_well": n_reads, "shake_before_read": shake}

    @staticmethod
    def fluorescence_protocol(excitation: int, emission: int,
                              gain: str = "auto") -> dict:
        return {"mode": "fluorescence", "excitation_nm": excitation,
                "emission_nm": emission, "gain": gain}


class Sequencer:
    @staticmethod
    def illumina_run_summary(read_length=150, paired_end=True,
                             n_reads_estimate=1e6) -> dict:
        bases = read_length * (2 if paired_end else 1) * n_reads_estimate
        return {"platform": "Illumina", "read_length": read_length,
                "paired_end": paired_end, "estimated_reads": n_reads_estimate,
                "estimated_output_bases": int(bases)}

    @staticmethod
    def nanopore_run_summary(flowcell: str = "R10.4", target_bases=1e9) -> dict:
        return {"platform": "Oxford Nanopore", "flowcell": flowcell,
                "target_bases": int(target_bases)}
