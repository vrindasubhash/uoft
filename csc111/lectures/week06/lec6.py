"""CSC111 Lecture 6 examples"""
from __future__ import annotations
from typing import Any, Optional
from python_ta.contracts import check_contracts


@check_contracts
def items_at_depth(nested_list: int | list, d: int) -> list[int]:
    """Return the list of all integers in nested_list that have depth d.
    Preconditions:
        - d >= 0
    >>> items_at_depth(10, 0)
    [10]
    >>> items_at_depth(10, 3)
    []
    >>> items_at_depth([10, [[20]], [[30], 40]], 0)
    []
    >>> items_at_depth([10, [[20]], [[30], 40]], 3)
    [20, 30]
    """
    # Exercise: try rewriting this code without using nested if statements,
    # and instead using compound if/elif conditions.
    if isinstance(nested_list, int):
        if d == 0:
            return [nested_list]
        else:
            return []
    else:
        if d == 0:
            return []
        else:
            result_so_far = []
            for sublist in nested_list:
                result_so_far.extend(items_at_depth(sublist, d - 1))
            return result_so_far


@check_contracts
class RecursiveList:
    """A recursive implementation of the List ADT.
    Note: this list can't store None values! (Because None is used as a special value
    for its attributes.)
    """
    # Private Instance Attributes:
    #   - _first: The first item in the list, or None if this list is empty.
    #   - _rest: A list containing the items that come after the first one,
    #            or None if this list is empty.
    _first: Optional[Any]
    _rest: Optional[RecursiveList]

    def __init__(self, first: Optional[Any], rest: Optional[RecursiveList]) -> None:
        """Initialize a new recursive list."""
        self._first = first
        self._rest = rest

    def sum(self) -> int:
        """Return the sum of the elements in this list.
        Preconditions:
            - every element in this list is an int
        >>> empty = RecursiveList(None, None)
        >>> empty.sum()
        0
        >>> single = RecursiveList(111, empty)
        >>> single.sum()
        111
        >>> four_items = RecursiveList(1,
        ...                            RecursiveList(2,
        ...                                          RecursiveList(3,
        ...                                                        RecursiveList(4,empty))))
        >>> four_items.sum()
        10
        """
        if self._first is None:  # Base case: this list is empty
            return 0
        else:
            return self._first + self._rest.sum()


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
