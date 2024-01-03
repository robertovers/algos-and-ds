from typing import List
from copy import copy


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


def dfs_stack(V: List[str], E: List[List[int]], start: int) -> None:
    """
    Depth first search implemented with a stack.

    Args:
        V: A list of vertex labels.
        E: An adjacency matrix stored as a nested list.
        start: A vertex label of the node to search from.
    """
    Q = [start]
    visited = {}
    while Q:
        u = Q.pop()
        visited[u] = 1
        for v in adj(E, u):
            if v not in visited:
                Q += [v]
    return


def dfs_recursive(V: List[str], E: List[List[int]], u: int) -> List[List[int]]:
    """
    Tail-recursive depth first search.

    Args:
        V: A list of vertex labels.
        E: An adjacency matrix stored as a nested list.
        start: A vertex label of the node to search from.

    Returns:
        A nested list of paths explored.
    """

    def aux(E, u, path=[], vis={}) -> List[int]:
        for v in adj(E, u):
            if v not in vis:
                path += [v]
                return aux(E, v, path, copy(vis))
        return path

    paths = []
    for v in adj(E, u):
        paths += [aux(E, v, [u, v], {})]
    return [[V[i] for i in p] for p in paths]


def bfs_stack(V: List[str], E: List[List[int]], start: int) -> None:
    """
    Breadth-first search implemented with a stack.
    """
    Q = [start]
    visited = {}
    while Q:
        u = Q.pop(0)
        visited[u] = 1
        for v in adj(E, u):
            if v not in visited:
                Q += [v]
    return


if __name__ == "__main__":

    V = ["a", "b", "c", "d"]

    E = [[0, 0, 0, 0],  # a
         [1, 0, 1, 0],  # b
         [0, 0, 0, 1],  # c
         [0, 0, 0, 0]]  # d

    paths = dfs_recursive(V, E, 1)
    print(paths)
