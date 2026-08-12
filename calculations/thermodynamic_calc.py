"""Nucleic acid hybridization and melting temperature (Tm)."""
from __future__ import annotations


def tm_wallace(seq):
    """Wallace rule for oligos < 14 nt: Tm = 2*(A+T) + 4*(G+C)."""
    seq = seq.upper()
    return 2 * (seq.count("A") + seq.count("T")) + 4 * (seq.count("G") + seq.count("C"))


def tm_gc_content(seq, salt_mM=50):
    """Salt-adjusted Tm (Marmur-Schildkraut-like)."""
    import math
    seq = seq.upper()
    if not seq:
        return 0.0
    gc = (seq.count("G") + seq.count("C")) / len(seq)
    salt = max(salt_mM / 1000.0, 1e-6)
    return 81.5 + 41.0 * gc - 675.0 / len(seq) + 16.6 * math.log10(salt)


def tm_nearest_neighbor(seq):
    """Simplified nearest-neighbor Tm using a small lookup of dinucleotides."""
    import math
    nn = {
        "AA": -9.1, "AT": -8.6, "TA": -6.0, "TT": -9.1,
        "CA": -5.8, "GT": -6.5, "CT": -7.8, "GA": -5.6,
        "CG": -5.7, "GC": -5.8, "GG": -11.0, "CC": -11.0,
        "AG": -7.8, "TG": -5.8, "AC": -6.5, "TC": -5.6,
    }
    seq = seq.upper()
    if len(seq) < 2:
        return 0.0
    dh = sum(nn.get(seq[i:i+2], -7.0) for i in range(len(seq) - 1))
    ds = -0.022 * 1e3  # simplified entropy term
    return dh / (ds + 1.987 * math.log(seq.count("C") + seq.count("G"))) - 273.15


def free_energy_hybridization(seq):
    """Very rough Gibbs free energy estimate of duplex formation."""
    seq = seq.upper()
    return -0.5 * (seq.count("G") + seq.count("C")) - 0.2 * (seq.count("A") + seq.count("T"))
