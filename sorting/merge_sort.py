from typing import List


def merge_sort(lst: List[int]) -> List[int]:
    """
    First, the list is recursively divided into sublists until reaching the
    base case of size one. Then, the sublists are merged together, maintaining
    sorted order after each merge, until the full list is is sorted.

    Time: O(nlogn)
    Space: O(n)
    """
    if len(lst) <= 1:
        return lst

    mid = len(lst) // 2
    left = merge_sort(lst[:mid])
    right = merge_sort(lst[mid:])
    res = merge(left, right)
    return res


def merge(a: List[int], b: List[int]) -> List[int]:
    """
    Merges two sorted lists into a single sorted list.

    Time: O(m+n), where m and n are the sizes of the two lists.
    """
    res = []
    i, j = 0, 0
    while i < len(a) and j < len(b):
        if a[i] < b[j]:
            res += [a[i]]
            i += 1
        else:
            res += [b[j]]
            j += 1
    res = res + a[i:] + b[j:]
    return res
