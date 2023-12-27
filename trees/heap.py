from typing import List, TypeVar, Generic


T = TypeVar("T")


class Heap(Generic[T]):
    """
    A basic, generic heap data structure with the following operations:
        * insert
        * pop

    Args:
        lst: A list to turn into a heap
        invariant: The heap invariant (a comparison function).
            If not provided will default to `less than`.
    """

    def __init__(self, lst: List[T] = [],
                 invariant: callable = lambda a, b: a < b):
        self.heap = []
        self.invariant = invariant
        for x in lst:
            self.insert(x)

    def __len__(self) -> int:
        return len(self.heap)

    def insert(self, item: T) -> None:
        """
        Adds an element to the heap.

        Time: O(logN)
        """
        # add the item to the back of the heap
        self.heap.append(item)
        # rise the element until heap invariant is maintained
        self.rise(len(self.heap) - 1)

    def pop(self) -> T:
        """
        Pops the minimum element off of the heap.

        Time: O(logN)
        """
        min = self.heap[0]
        if len(self.heap) == 1:
            self.heap.pop(0)
            return min

        # replace the top (min) element with the last element in the heap
        self.heap[0] = self.heap.pop(-1)
        # sink the element down until heap invariant is maintained
        self.sink(0, len(self))
        return min

    def sink(self, idx: int, end: int) -> None:
        """
        Swaps the element at idx with its lowest child until the heap
        invariant is restored. We choose the lower child because the
        greater child would break the heap invariant after swapping.

        Time: O(logn)

        Args:
            end: An index for when to swap until. Used by Heapsort.
        """
        next = self.min_child(idx, end)
        while (next and next < end
               and not self.invariant(self.heap[idx], self.heap[next])):
            # swap the current element with the lower child
            self.heap[idx], self.heap[next] = self.heap[next], self.heap[idx]
            idx = next
            next = self.min_child(idx)

    def rise(self, idx: int) -> None:
        """
        Swaps the element at idx with its parent until the heap invariant
        is restored.

        Time: O(logn)
        """
        par = (idx - 1) // 2
        while idx > 0 and not self.invariant(self.heap[par], self.heap[idx]):
            # swap the current element with its parent
            self.heap[idx], self.heap[par] = self.heap[par], self.heap[idx]
            par, idx = (par - 1) // 2, par

    def min_child(self, v: int, end: int = None) -> T:
        left = 2 * v + 1
        right = 2 * v + 2
        if left > len(self.heap) - 1:
            return None
        elif left == len(self.heap) - 1 or right == end:
            return left
        elif self.invariant(self.heap[left], self.heap[right]):
            return left
        return right
