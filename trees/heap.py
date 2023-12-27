from typing import List, TypeVar, Generic


T = TypeVar("T")


class Heap(Generic[T]):
    """
    A basic heap data structure with the following operations:
        - insert
        - extract_min
    """

    def __init__(self, lst: List[T] = []):
        self.heap = []
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
        self.__rise(len(self.heap) - 1)

    def extract_min(self) -> T:
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
        self.__sink(0)
        return min

    def __min_child(self, v: int) -> T:
        left = 2 * v + 1
        right = 2 * v + 2
        if left > len(self.heap) - 1:
            return None
        elif left == len(self.heap) - 1:
            return left
        elif self.heap[left] < self.heap[right]:
            return left
        return right

    def __sink(self, idx: int) -> None:
        next = self.__min_child(idx)
        while (next is not None) and (self.heap[idx] > self.heap[next]):
            self.heap[idx], self.heap[next] = self.heap[next], self.heap[idx]
            idx = next
            next = self.__min_child(idx)

    def __rise(self, idx: int) -> None:
        par = (idx - 1) // 2
        while idx > 0 and self.heap[par] > self.heap[idx]:
            self.heap[idx], self.heap[par] = self.heap[par], self.heap[idx]
            par, idx = (par - 1) // 2, par
