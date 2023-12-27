from typing import List


def z_algorithm(txt: str) -> List[int]:
    """
    Time: O(n) where n = |txt|
        * Computes a single Z-value each iteration (n-1 iterations)
        * Cases 2a and 2b(1) have constant-time operations
        * Cases 1 and 2b(2) perform explicit comparisons until a mismatch, and
          we don't ever compare against the same substring twice (because this
          would fall under cases 2a and 2b(1))
        * We can have at most n-1 mismatches
        * Results in a total of O(n) comparisons plus O(n) work, O(n) overall
    """
    n = len(txt)
    if n == 0:
        return []
    if n == 1:
        return [1]

    z = [0 for _ in range(n)]
    z[0] = n

    # base case
    i, j = 0, 1
    while j < n and txt[i] == txt[j]:
        i += 1
        j += 1
    z[1] = j - 1

    if z[1] > 0:
        l, r = 1, z[1]
    else:
        l, r = 0, 0

    # general case
    for k in range(2, n):
        # case 1
        if k > r:
            i, j = 0, k
            while j < n and txt[i] == txt[j]:
                i += 1
                j += 1
            z[k] = i
            if z[k] != 0:
                l, r = k, j - 1

        # case 2a
        elif z[k - l] < r - k + 1:
            z[k] = z[k - l]

        # case 2b (1)
        elif z[k - l] > r - k + 1:
            z[k] = r - k + 1

        # case 2b (2)
        else:
            i, j = r - k + 1, r + 1
            while j < n and txt[i] == txt[j]:
                i += 1
                j += 1
            z[k] = i

    return z


def pattern_match_z(txt: str, pat: str) -> List[int]:
    """
    Time: O(|txt| + |str|)
        * Z-algorithm on string of length |txt| + |str| + 1 (terminal symbol)
    """
    res = []
    m = len(pat)
    n = len(txt)

    if m == 0 or n == 0 or m > n:
        return []

    s = pat + '$' + txt
    z = z_algorithm(s)

    for i in range(m + 1, len(s)):
        if z[i] == m:
            res += [i - m - 1]

    return res
