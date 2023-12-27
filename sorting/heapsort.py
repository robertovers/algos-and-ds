from typing import List
from trees.heap import Heap


def heapsort(lst: List[int]) -> List[int]:
    """
    Heapsort sorts a list by first turning into a Max-heap. It then
    swaps the largest element with the last in the heap, meaning it
    is now in its correct place in the sorted order. The heap invariant
    is then restored, and this routine is repeated until all elements
    have been processed.

    Time: O(nlogn)
    Space: O(1) auxiliary
    """
    heap = Heap(lst, lambda a, b: a > b)
    back = len(heap) - 1
    while back > 0:
        # swap the first (largest) element with the last in the heap
        heap.heap[back], heap.heap[0] = heap.heap[0], heap.heap[back]
        # sink the new first element until heap invariant is restored
        heap.sink(0, back)
        # decrease the back counter, as we are done with this element
        back -= 1

    return heap.heap
