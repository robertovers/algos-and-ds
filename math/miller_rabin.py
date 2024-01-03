import random
from modular_exponentiation import modexp


def miller_rabin(n: int, k: int, a: int = 0) -> bool:
    """
    Performs the Miller-Rabin primality test.

    Time: O(klog^3(n))

    Args:
        n: The number to test.
        k: The number of tests to perform.
        a: A random number.
    """
    if n == 2 or n == 3:
        return True
    if n == 1 or n % 2 == 0:
        return False

    # find s and t such that n-1 = (2^s)*t
    s, t = 0, n-1
    while t % 2 == 0:
        s += 1
        t //= 2

    # run k tests
    for _ in range(k):
        if a == 0:
            a = random.randint(1, n-1)

        # compute x sequence
        x = []
        prev = None
        for _ in range(s+1):
            if not prev:
                # (a**t) % n
                current = modexp(a, t, n)
                x.append(current)
                prev = current
            else:
                # (prev*prev) % n
                current = modexp(prev, 2, n)
                x.append(current)
                prev = current

        # check if n satisfies fermat's little theorem for a
        if x[s] != 1:
            return False

        # sequence test
        for j in range(s+1):
            if x[j] == 1 and (x[j-1] != 1 and x[j-1] != n-1):
                return False

    return True


if __name__ == '__main__':

    print(miller_rabin(17, 5))
    print(miller_rabin(16, 5))
    print(miller_rabin(34, 5))
    print(miller_rabin(31, 5))
