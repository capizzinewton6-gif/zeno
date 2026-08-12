"""Needleman-Wunsch, Smith-Waterman, and BLAST math."""
from __future__ import annotations


def needleman_wunsch(seq1, seq2, match=1, mismatch=-1, gap=-1):
    """Global alignment (returns score, aligned seq1, aligned seq2)."""
    n, m = len(seq1), len(seq2)
    score = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        score[i][0] = i * gap
    for j in range(m + 1):
        score[0][j] = j * gap
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            s = match if seq1[i - 1] == seq2[j - 1] else mismatch
            score[i][j] = max(
                score[i - 1][j - 1] + s,
                score[i - 1][j] + gap,
                score[i][j - 1] + gap,
            )
    # traceback
    a1, a2 = [], []
    i, j = n, m
    while i > 0 or j > 0:
        if i > 0 and j > 0:
            s = match if seq1[i - 1] == seq2[j - 1] else mismatch
            if score[i][j] == score[i - 1][j - 1] + s:
                a1.append(seq1[i - 1]); a2.append(seq2[j - 1])
                i -= 1; j -= 1
                continue
        if i > 0 and score[i][j] == score[i - 1][j] + gap:
            a1.append(seq1[i - 1]); a2.append("-")
            i -= 1
        else:
            a1.append("-"); a2.append(seq2[j - 1])
            j -= 1
    return score[n][m], "".join(reversed(a1)), "".join(reversed(a2))


def smith_waterman(seq1, seq2, match=2, mismatch=-1, gap=-1):
    """Local alignment (returns score, aligned seq1, aligned seq2)."""
    n, m = len(seq1), len(seq2)
    score = [[0] * (m + 1) for _ in range(n + 1)]
    max_score, max_pos = 0, (0, 0)
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            s = match if seq1[i - 1] == seq2[j - 1] else mismatch
            score[i][j] = max(
                0,
                score[i - 1][j - 1] + s,
                score[i - 1][j] + gap,
                score[i][j - 1] + gap,
            )
            if score[i][j] > max_score:
                max_score, max_pos = score[i][j], (i, j)
    a1, a2 = [], []
    i, j = max_pos
    while i > 0 and j > 0 and score[i][j] > 0:
        s = match if seq1[i - 1] == seq2[j - 1] else mismatch
        if score[i][j] == score[i - 1][j - 1] + s:
            a1.append(seq1[i - 1]); a2.append(seq2[j - 1])
            i -= 1; j -= 1
        elif score[i][j] == score[i - 1][j] + gap:
            a1.append(seq1[i - 1]); a2.append("-")
            i -= 1
        else:
            a1.append("-"); a2.append(seq2[j - 1])
            j -= 1
    return max_score, "".join(reversed(a1)), "".join(reversed(a2))


def blast_score(seq1, seq2, match=5, mismatch=-4):
    """A naive ungapped BLAST-style score over a sliding word window."""
    word = 3
    if len(seq1) < word or len(seq2) < word:
        return 0
    best = 0
    for i in range(len(seq1) - word + 1):
        for j in range(len(seq2) - word + 1):
            sc = 0
            k = 0
            while i + k < len(seq1) and j + k < len(seq2):
                sc += match if seq1[i + k] == seq2[j + k] else mismatch
                if sc < 0:
                    break
                best = max(best, sc)
                k += 1
    return best
