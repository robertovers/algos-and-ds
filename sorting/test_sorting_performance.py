import timeit
import random
from sorting import (merge_sort,
                     quicksort,
                     heapsort,
                     radix_sort)


def sorting_algorithms():
    algos = [
        ("Python `sorted`", sorted),
        ("Merge Sort", merge_sort.merge_sort),
        ("Quicksort", quicksort.quicksort),
        ("Heapsort", heapsort.heapsort),
        ("Radix Sort (base 64)", radix_sort.radix_sort_base_64),
        ("Radix Sort (base 256)", radix_sort.radix_sort_base_256)
    ]
    return algos


def run(n, k):
    print("\nBegin performance test (best time of five)")
    print(f"Array size: {n}")
    print(f"Array items: 1..{k}\n")

    print("Algorithm".ljust(25), "Time (s)")
    for name, f in sorting_algorithms():
        times = []
        for _ in range(5):
            arr = [random.randint(1, k) for _ in range(n)]
            ti = timeit.timeit(lambda: f(arr), number=1)
            times += [round(ti, 10)]
        best = min(times)
        print(name.ljust(25), best)


if __name__ == "__main__":
    n = 100000
    k = 10000
    run(n, k)
