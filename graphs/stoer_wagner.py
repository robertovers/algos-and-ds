from typing import List, Tuple, Dict
from heapq import heappush, heappop


def min_cut(V: List[int], E: List[List[int]], a: int) -> int:
    """
    Stoer-Wagner Algorithm

    Time:
        O(V*min_cut_phase)
        -> O(VE+V^2logV)

    Args:
        V: A list of vertices.
        E: An adjacency matrix stored as a nested list.
        a: An arbitrarily chosen starting node.
    """
    mincut = -1
    merges = {}
    for s in V:
        merges[s] = [s]
    for i in range(len(V)-1):
        V, E, cut, merges, size = min_cut_phase(V, E, a, merges)
        s, t, wt = cut
        print(f"iter {i}/{len(E)}: s={s} t={t} cut={wt}")
        if mincut == -1 or wt < mincut:
            mincut = wt
    return mincut


def min_cut_phase(V: List[int], E: List[List[int]],
                  a: int, merges: Dict) -> Tuple:
    """
    Time: O(E+VlogV)
    """
    A = [a]
    H = []

    # initialise heap
    for v in V:
        if v in A:
            continue
        w = E[v][a]
        if w > 0:
            heappush(H, (-w, v))

    while set(A) != set(V):
        # add the most "tightly connected" node to A
        w, u = heappop(H)
        A += [u]

        # update weights in heap to include edges going to u
        for v, wv in enumerate(E[u]):
            if wv == 0 or v in A:
                continue
            wh = 0
            for wt, k in H:
                if k == v:
                    wh = wt
                    break
            heappush(H, (wh-E[u][v], v))

    s, t = A[-2], A[-1]  # cut of the phase

    # weight of cut
    wt = sum([E[m][t] for m in V])

    # merge the edges s & t into s and add weights for edges connected to both
    merges[s] = merges[s] + merges[t]
    for m in range(len(E)):
        if m != s:
            E[m][s] = E[s][m]+E[t][m]
            E[s][m] = E[s][m]+E[t][m]

    # remove t
    V.remove(t)
    del merges[t]
    for v in range(len(E)):
        E[v][t] = 0
        E[t][v] = 0

    return V, E, (s, t, wt), merges
