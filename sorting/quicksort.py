from typing import List


def quicksort(lst: List[int]) -> List[int]:
    """
    Quicksort sorts the list by repeatedly picking a 'pivot', and
    moving items less than the pivot to its left, and greater to the
    right - which guarantees that the pivot is in its correct final
    position. This procedure is then repeated recursively on the items
    to the left and right of it.

    Time (best/average case): O(nlogn)
    Time (worst case): O(n^2)
    Space: O(n)
    """
    if len(lst) <= 1:
        return lst

    start_pivot_pos = pivot(lst)
    start_pivot = lst[start_pivot_pos]
    sort_l = quicksort(lst[:start_pivot_pos])
    sort_r = quicksort(lst[start_pivot_pos + 1:])
    return sort_l + [start_pivot] + sort_r


def pivot(lst: List[int]) -> int:
    """
    First, the pivot is arbitrarily picked as the first element in
    the list. Then, all items less than the pivot are moved to the
    left, and the remaining items stay in-place.

    Returns:
        The final index of the pivot after all items are moved.
    """
    pivot = lst[0]
    swap_pos = 1  # the end index of the items less than the pivot

    for i in range(1, len(lst)):
        if lst[i] < pivot:
            lst[i], lst[swap_pos] = lst[swap_pos], lst[i]
            swap_pos += 1

    # swap the pivot with the last item smaller than it
    # so that it's now in the correct position
    lst[0], lst[swap_pos - 1] = lst[swap_pos - 1], lst[0]
    return swap_pos - 1
