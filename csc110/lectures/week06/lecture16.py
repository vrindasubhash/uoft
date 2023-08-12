def euclidean_gcd(a: int, b: int) -> int:
    """Return the gcd of a and b

    >>> euclidean_gcd(124124124, 110)
    2
    >>> euclidean_gcd(19201, 3587)
    211
    """

    # x = a
    # y = b
    x, y = a, b

    while y != 0:
        # loop invariant: gcd(a, b) == gcd(x, y)
        assert math.gcd(a, b) == math.gcd(x, y)
        # apply the theorem
        r = x % y

        x = y
        y = r

    return x
