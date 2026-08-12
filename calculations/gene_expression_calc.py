"""2^-ddCt qPCR and transcriptomics normalization."""
from __future__ import annotations

import math


def delta_ct(target_ct, reference_ct):
    return target_ct - reference_ct


def delta_delta_ct(sample_dct, control_dct):
    return sample_dct - control_dct


def fold_change_ddct(target_ct, reference_ct, control_target_ct,
                     control_reference_ct):
    """Return fold change using the 2^-ddCt method."""
    dct = delta_ct(target_ct, reference_ct)
    ddct = delta_delta_ct(dct, delta_ct(control_target_ct, control_reference_ct))
    return 2 ** (-ddct)


def normalize_to_reference(values, reference_values):
    """Normalize a vector of expression values to a reference gene vector."""
    if len(values) != len(reference_values):
        raise ValueError("Length mismatch")
    return [v / r for v, r in zip(values, reference_values) if r != 0]


def geomean(values):
    product = 1.0
    for v in values:
        if v <= 0:
            raise ValueError("Geometric mean requires positive values")
        product *= v
    return product ** (1 / len(values))


def rpk(count, length_kb, library_size):
    """Reads per kilobase (RPK)."""
    if length_kb == 0 or library_size == 0:
        raise ValueError("length and library size must be > 0")
    return count / (length_kb * library_size)
