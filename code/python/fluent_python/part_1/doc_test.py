#!/usr/bin/env python


# doctest(https://docs.python.org/3/library/doctest.html)是Python的一个标准库，做测试用的。这个库通过模拟控制台对话来检验表达式求值是
# 否正确.

# 我有时为了事先说明一段代码的目的，会在展示代码之前先摆出相应的 doctest 文本。这是因为我认为，在考虑如何实现一个功能之前，先严格地列出这个功能能做
# 什么，这能帮助我们在编程时把精力花在该花的地方

"""
This is the "example" module.

The example module supplies one function, factorial().  For example,

>>> factorial(5)
120
"""


def factorial(n):
    """Return the factorial of n, an exact integer >= 0.

    >>> [factorial(n) for n in range(6)]
    [1, 1, 2, 6, 24, 120]
    >>> factorial(30)
    265252859812191058636308480000000
    >>> factorial(-1)
    Traceback (most recent call last):
        ...
    ValueError: n must be >= 0

    Factorials of floats are OK, but the float must be an exact integer:
    >>> factorial(30.1)
    Traceback (most recent call last):
        ...
    ValueError: n must be exact integer
    >>> factorial(30.0)
    265252859812191058636308480000000

    It must also not be ridiculously large:
    >>> factorial(1e100)
    Traceback (most recent call last):
        ...
    OverflowError: n too large
    """

    import math
    if not n >= 0:
        raise ValueError("n must be >= 0")
    if math.floor(n) != n:
        raise ValueError("n must be exact integer")
    if n+1 == n:  # catch a value like 1e300
        raise OverflowError("n too large")
    result = 1
    factor = 2
    while factor <= n:
        result *= factor
        factor += 1
    return result


if __name__ == "__main__":
    import doctest
    doctest.testmod()


