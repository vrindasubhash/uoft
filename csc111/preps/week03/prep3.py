def f(n: int) -> int:
    """Precondition: n >= 0"""
    if n == 0:
        return 0
    else:
        return f(n) + n

if __name__ == '__main__':
    f(4)
