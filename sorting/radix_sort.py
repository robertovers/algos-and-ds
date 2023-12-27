import math
from typing import List


def radix_sort_base_64(lst: List[int]) -> List[int]:
    return radix_sort(lst, 64)


def radix_sort_base_256(lst: List[int]) -> List[int]:
    return radix_sort(lst, 256)


def radix_sort(lst: List[int], b: int) -> List[int]:
    """
    Converts elements in the list into base b, then calls count sort on
    each digit of these elements until the list is sorted.

    Time:
        O(max + convert_list + max_dig*count_sort + n*convert_out)
        -> O(n + n*max_dig + (n+b)*max_dig + n*max_dig)
        -> O((n+b)*max_dig)
        -> O((n+b)*log_b(M)) since max_dig = log_b(M) + 1

    Space:
        O(max + convert_list + max_dig*count_sort + n*convert_out)
        -> O(n + n*max_dig + (n+b)*max_dig + n)
        -> O((n+b)*max_dig)
        -> O((n+b)*log_b(M))
    """
    if len(lst) <= 1:
        return lst

    offset = None
    if min(lst) < 0:
        # need to convert all numbers to positive
        offset = -1 * min(lst)
        lst = list(map(lambda x: x + offset, lst))

    max_num = max(lst)

    if max_num == 0:
        max_dig = 1
    else:
        max_dig = math.floor(math.log(max_num, b)) + 1

    lst = convert_list(lst, b, max_dig)

    for i in range(max_dig - 1, -1, -1):
        lst = count_sort(lst, b, i)

    for i in range(len(lst)):
        lst[i] = convert_out(lst[i], b)

    if offset:
        lst = list(map(lambda x: x - offset, lst))
    return lst


def count_sort(lst: list, b: int, ind: int) -> list:
    """
    Takes a list of integers, and applies count sort on the digits
    at index 'ind' of each integer.

    Time: O(n+b), where n is len(lst) and b is the base
    Space: O(n+b)
    """
    n = len(lst)
    count, pos, output = [], [], []

    output = [None for _ in range(n)]
    count = [0 for _ in range(b)]
    pos = [0 for _ in range(b)]

    for i in range(n):
        key = lst[i][ind]
        count[key] += 1

    pos[0] = 0
    for i in range(1, b):
        pos[i] = pos[i - 1] + count[i - 1]

    for i in range(n):
        key = lst[i][ind]
        output[pos[key]] = lst[i]
        pos[key] += 1

    return output


def convert_list(lst: list, b: int, max_dig: int) -> list:
    """
    Calls convert_num for each number in the list, returning
    the list in the given base.

    Time: O(n*convert_num) -> O(n*max_dig), where n is the length of lst
    Space: O(n*convert_num) -> O(n*max_dig)
    """
    for i in range(len(lst)):
        num = lst[i]
        lst[i] = convert_num(num, b, max_dig)

    return lst


def convert_num(num: int, b: int, max_dig: int) -> list:
    """
    Creates an empty array large enough to store all numbers
    in the given base, determined by max_dig, then builds the new
    number in base b from least to most significant digit.

    Time: O(max_dig)
    Space: O(max_dig)
    """
    res = [0 for _ in range(max_dig)]

    j = max_dig - 1
    while num > 0 and j >= 0:
        dig = num % b
        res[j] = dig
        num = num // b
        j -= 1

    return res


def convert_out(num: list, b: int) -> int:
    """
    Takes a list of lists of integers and returns a list of integers
    that have been converted to base 10.

    Time: O(len(num)) -> O(max_dig)
    Space: O(1)
    """
    res = 0
    for i in range(len(num)):
        exp = len(num) - i - 1
        res += num[i]*(b**exp)

    return res
