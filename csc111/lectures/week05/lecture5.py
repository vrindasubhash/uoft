"""CSC111 Lecture 5 Examples"""


def sum_n(n: int) -> int:
    """Return the sum of the numbers between 0 and n, inclusive.
    Preconditions:
        - n >= 0
    >>> sum_n(4)
    10
    """
    if n == 0:
        return 0
    else:
        return sum_n(n - 1) + n


def euclidean_gcd(a: int, b: int) -> int:
    """Return the gcd of a and b.
    Preconditions:
        - a >= 0 and b >= 0
    """
    x = a
    y = b
    while y != 0:
        print(x, y)
        x, y = y, x % y
    return x


def euclidean_gcd_rec(a: int, b: int) -> int:
    """Return the gcd of a and b (using recursion!).
    Preconditions:
        - a >= 0 and b >= 0
    """
    print(a, b)
    if b == 0:
        return a
    else:
        return euclidean_gcd_rec(b, a % b)


def sum_list(numbers: list[int]) -> int:
    """Return the sum of the numbers in the given list.
    >>> sum_list([1, 2, 3])
    6
    """
    sum_so_far = 0
    for num in numbers:
        sum_so_far += num
    return sum_so_far


def sum_list2(lists_of_numbers: list[list[int]]) -> int:
    """Return the sum of the numbers in the given list of lists.
    >>> sum_list2([[1], [10, 20], [1, 2, 3]])
    37
    """
    sum_so_far = 0
    for numbers in lists_of_numbers:
        # numbers is a list[int]
        sum_so_far += sum_list(numbers)
    return sum_so_far


def sum_list3(lists_of_lists_of_numbers: list[list[list[int]]]) -> int:
    """Return the sum of the numbers in the given list of lists of lists.
    >>> sum_list3([[[1], [10, 20], [1, 2, 3]], [[2, 3], [4, 5]]])
    51
    """
    sum_so_far = 0
    for lists_of_numbers in lists_of_lists_of_numbers:
        # lists_of_numbers is a list[list[int]]
        sum_so_far += sum_list2(lists_of_numbers)
    return sum_so_far


def sum_list8(x: list[list[list[list[list[list[list[list[int]]]]]]]]) -> int:
    ...


def sum_nested(nested_list: int | list) -> int:
    """Return the sum of the integers in nested_list.
    nested_list is a nested list of integers (using our definition from lecture).
    """
    if isinstance(nested_list, int):
        return nested_list
    else:
        # Note: could use a for loop instead of a comprehension
        return sum(sum_nested(sublist) for sublist in nested_list)


def flatten(nested_list: int | list) -> list[int]:
    """Return a (non-nested) list of the integers in nested_list.
    The integers are returned in the left-to-right order they appear in
    nested_list.
    """
    if isinstance(nested_list, int):
        return [nested_list]
    else:
        result_so_far = []
        for sublist in nested_list:
            result_so_far.extend(flatten(sublist))
        return result_so_far


def depth(nested_list: int | list) -> int:
    """Return the depth of this nested list."""
    if isinstance(nested_list, int):  # Our "normal" base case
        return 0
    elif nested_list == []:  # An additional base case!
        return 1
    else:
        # Note: could use a for loop instead of a comprehension
        return 1 + max(depth(sublist) for sublist in nested_list)


def nested_list_contains(nested_list: int | list, item: int) -> bool:
    """Return whether the given item appears in nested_list.
    If nested_list is an integer, return whether it is equal to item.
    >>> nested_list_contains(10, 10)
    True
    >>> nested_list_contains(10, 5)
    False
    >>> nested_list_contains([[1, [30], 40], [], 77], 50)
    False
    >>> nested_list_contains([[1, [30], 40], [], 77], 40)
    True
    """
    if isinstance(nested_list, int):
        return nested_list == item
    else:
        # Version 1 (comprehension and any)
        return any(nested_list_contains(sublist, item) for sublist in nested_list)
        # Version 2 (loop and early return)
        # for sublist in nested_list:
        #     if nested_list_contains(sublist, item):
        #         return True
        #
        # return False
