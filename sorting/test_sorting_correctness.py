import pytest
import merge_sort
import quicksort
import radix_sort


def sorting_algorithms():
    algos = [
        merge_sort.merge_sort,
        quicksort.quicksort,
        radix_sort.radix_sort_base_64,
        radix_sort.radix_sort_base_256
    ]
    return algos


@pytest.mark.parametrize("sorting_algorithm", sorting_algorithms())
def test_sorting_empty_list(sorting_algorithm):
    input = []
    expected = []
    result = sorting_algorithm(input)
    assert result == expected


@pytest.mark.parametrize("sorting_algorithm", sorting_algorithms())
def test_sorting_single_item(sorting_algorithm):
    input = [1]
    expected = [1]
    result = sorting_algorithm(input)
    assert result == expected


@pytest.mark.parametrize("sorting_algorithm", sorting_algorithms())
def test_sorting_two_numbers(sorting_algorithm):
    input = [2, 1]
    expected = [1, 2]
    result = sorting_algorithm(input)
    assert result == expected


@pytest.mark.parametrize("sorting_algorithm", sorting_algorithms())
def test_sorting_three_numbers(sorting_algorithm):
    cases = [
        ([1, 3, 2], [1, 2, 3]),
        ([3, 1, 2], [1, 2, 3]),
        ([1, 2, 3], [1, 2, 3]),
        ([1, 0, 0], [0, 0, 1]),
        ([1, 1, 1], [1, 1, 1]),
    ]

    for input, expected in cases:
        result = sorting_algorithm(input)
        assert result == expected


@pytest.mark.parametrize("sorting_algorithm", sorting_algorithms())
def test_sorting_positive_numbers(sorting_algorithm):
    cases = [
        ([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
         [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),

        ([2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
         [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2]),

        ([0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 9],
         [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),

        ([7, 2, 4, 3, 5, 0, 10, 6, 1, 9, 8],
         [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
    ]

    for input, expected in cases:
        result = sorting_algorithm(input)
        assert result == expected


@pytest.mark.parametrize("sorting_algorithm", sorting_algorithms())
def test_sorting_negative_numbers(sorting_algorithm):
    cases = [
        ([-3, -1, -2, 0, -7, -5, -6, -4, -8, -10, -9],
         [-10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0]),

        ([0, 7, -2, 4, 3, 5, 10, -6, -1, 9, 8],
         [-6, -2, -1, 0, 3, 4, 5, 7, 8, 9, 10])
    ]

    for input, expected in cases:
        result = sorting_algorithm(input)
        assert result == expected
