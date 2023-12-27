from typing import List
from trees.heap import Heap


def heapsort(lst: List[int]) -> List[int]:
    """
    Heapsort sorts the list by first turning it into a Heap,
    and then repeatedly popping off the minimum element.

    Time: O(n*extract_min) -> O(nlogn)
    Space: O(n)
    """
    heap = Heap(lst)
    res = []
    for _ in range(len(lst)):
        res.append(heap.extract_min())
    return res
