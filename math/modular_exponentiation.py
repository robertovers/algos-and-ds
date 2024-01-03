def modexp(a: int, b: int, n: int) -> int:
    """
    Computes the result of a^b mod n using modular exponentiation.
    """
    bin_rep = format(b, "b")
    current = a % n

    # base case
    if bin_rep[-1] == "1":  # LSB is 1; add first term to result
        result = current
    else:  # LSB is 0; skip first term and add 1 to result
        result = 1

    for b in bin_rep[:-1][::-1]:  # iterate remaining bits in reverse
        current = (current*current) % n  # update current
        if b == "1":  # update result with current if bit == 1 in binary rep
            result = (result*current) % n

    return result
