import heapq
from typing import List, Dict


def adj(E: List[List[int]], u: str) -> List[int]:
    """
    Gets the adjacent vertices for a given adjacency matrix and vertex.

    Time: O(V)

    Args:
        E: An adjacency matrix stored as a nested list.
        u: A vertex label.
    """
    res = []
    for i, v in enumerate(E[u]):
        if v > 0:
            res += [i]
    return res


def dijkstra(V: List[str], E: List[List[int]], start: int) -> Dict:
    """
    Dijkstra's algorithm implemented with a priority queue.

    Args:
        V: A list of vertex labels.
        E: An adjacency matrix stored as a nested list.
        start: A vertex label of the node to search from.
    """
    Q = [(0, start)]  # (cost, vertex)
    fin = {}

    while Q:
        uc, u = heapq.heappop(Q)

        if V[u] in fin:
            continue

        fin[V[u]] = uc

        for v in adj(E, u):
            du = uc + E[u][v]
            heapq.heappush(Q, (du, v))

    return fin


if __name__ == "__main__":

    V = ["a", "b", "c", "d"]

    E = [[0, 0, 1, 2],  # a
         [1, 0, 5, 0],  # b
         [0, 0, 0, 4],  # c
         [0, 0, 0, 0]]  # d

    costs = dijkstra(V, E, 1)
    print(costs)
