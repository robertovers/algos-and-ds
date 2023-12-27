from typing import List
from z_algorithm import z_algorithm


def sp_array(pat: str) -> List[int]:
    z = z_algorithm(pat)
    sp = [0 for _ in range(len(pat))]
    for j in range(len(pat)-1, 0, -1):
        i = j + z[j] - 1  # find endpoint of z[j] box (end of pat[1...i])
        sp[i] = z[j]  # set sp[i] to z[j] value (longest proper suffix of pat[1...i])
    return sp


def pattern_match_kmp(txt: str, pat: str) -> List[int]:
    res = []
    n, m = len(txt), len(pat)
    sp = sp_array(pat)
    i = 0
    while i < n:
        j, k = i, 0  # txt, pat iterators
        while j < n and k < m and txt[j] == pat[k]:
            j += 1
            k += 1
        if k == m:  # occurrence found
            res += [i]
            i += (m-1) - sp[m-1]
        elif k > 0:
            i += k - sp[k]
        else:
            i += 1
    return res
