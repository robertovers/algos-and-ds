from typing import List
from z_algorithm import z_algorithm


def alphaIndex(char: str) -> int:
    return ord(char) - 32  # first printable ASCII char has code 32


def badCharTable(pat: str) -> List[List[int]]:
    ALPHA_LEN = 95  # no of printable ASCII chars
    table = [[-1 for _ in range(ALPHA_LEN)] for _ in range(len(pat))]

    for i, c in enumerate(pat):
        for j in range(ALPHA_LEN):
            if i + 1 < len(table):
                table[i + 1][j] = table[i][j]
                table[i + 1][alphaIndex(c)] = i

    return table


def zSuffixArray(pat: str) -> List[int]:
    return z_algorithm(pat[::-1])[::-1]


def goodSuffixArray(pat: str) -> List[int]:
    m = len(pat)
    gs = [-1 for _ in range(m+1)]
    zs_array = zSuffixArray(pat)

    for p in range(m-1):
        j = m - zs_array[p]  # find start position j of suffix with len zs[p]
        gs[j] = p

    return gs


def matchedPrefixArray(pat: str) -> List[int]:
    res = [0 for _ in range(len(pat))]
    zs_array = zSuffixArray(pat)
    longest = 0

    for i, z in enumerate(zs_array):
        if z == i + 1:
            longest = z
        res[-i - 1] = longest

    return res


def patternMatchBM(txt: str, pat: str) -> List[int]:
    res = []
    m = len(pat)
    n = len(txt)

    if m == 0 or n == 0 or m > n:
        return []

    # galil optimisation variables
    start = -1
    stop = -1

    # preprocessing
    bc_table = badCharTable(pat)
    gs_array = goodSuffixArray(pat)
    mp_array = matchedPrefixArray(pat)

    i = m - 1
    while i < n:

        # scan R to L
        j = i  # txt iterator
        k = m - 1  # pat iterator
        while txt[j] == pat[k] and k >= 0:
            j -= 1
            k -= 1
            if k == stop and k > 0:  # galil's optimisation
                k = start - 1
                j = j - (stop - start) - 1

        # mismatch on rightmost char
        if k == m - 1:
            start, stop = -1, -1
            i += k - bc_table[k][alphaIndex(txt[j])]  # bad character rule

        # match found
        elif k == -1:
            res += [j + 1]
            if m > 1:
                start = 0
                stop = mp_array[1] - 1
                i += m - mp_array[1]
            else:
                start, stop = -1, -1
                i += 1

        else:
            # bad character rule
            bc_shift = k - bc_table[k][alphaIndex(txt[j])]

            # good suffix rule (gs_array[k+1] > -1)
            if gs_array[k+1] > -1:
                gs_shift = m - gs_array[k+1] - 1

                start = gs_array[k+1] - m + k + 2
                stop = gs_array[k+1]

            # good suffix rule (gs_array[k+1] == -1)
            else:
                gs_shift = m - mp_array[k+1]

                start = 0
                stop = mp_array[k+1] - 1

            if bc_shift > gs_shift:
                start, stop = -1, -1
                i += bc_shift
            else:
                i += gs_shift

    return res
