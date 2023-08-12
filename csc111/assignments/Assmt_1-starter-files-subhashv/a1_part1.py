"""CSC111 Assignment 1: Linked Lists and Blockchain

Instructions (READ THIS FIRST!)
===============================

This Python module contains the code for Part 1 of this assignment. We have included
a condensed version of the linked list class from lecture, keeping only the methods
you need to complete this part of the assignment. Please consult the assignment handout
for details.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2023 David Liu, Mario Badr
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Iterable, Optional


@dataclass
class _Node:
    """A node in a linked list.

    Note that this is considered a "private class", one which is only meant
    to be used in this module by the LinkedList class, but not by client code.

    Instance Attributes:
      - item: The data stored in this node.
      - next: The next node in the list, if any.
    """
    item: Any
    next: Optional[_Node] = None  # By default, this node does not link to any other node


class LinkedList:
    """A linked list implementation of the List ADT.
    """
    # Private Instance Attributes:
    #   - _first: The first node in this linked list, or None if this list is empty.
    _first: Optional[_Node]

    def __init__(self, items: Iterable) -> None:
        """Initialize a new linked list containing the given items.
        """
        # This is the basic version of the initializer we studied in lecture
        self._first = None
        for item in items:
            self.append(item)

    def to_list(self) -> list:
        """Return a built-in Python list containing the items of this linked list.

        The items in this linked list appear in the same order in the returned list.
        """
        items_so_far = []

        curr = self._first
        while curr is not None:
            items_so_far.append(curr.item)
            curr = curr.next

        return items_so_far

    def append(self, item: Any) -> None:
        """Append item to the end of this list.
        """
        new_node = _Node(item)

        if self._first is None:
            self._first = new_node
        else:
            curr = self._first
            while curr.next is not None:
                curr = curr.next

            # After the loop, curr is the last node in the LinkedList.
            assert curr is not None and curr.next is None
            curr.next = new_node

    ###########################################################################
    # Assignment 1, Part 1 (new method)
    ###########################################################################
    def swap_first_and_last(self) -> None:
        """Mutate this linked list by swapping the first and last items.

        Do nothing if there are fewer than two items in this linked list.
        """

        if self.to_list() == []:
            return
        elif len(self.to_list()) == 1:
            return

        curr = self._first

        while curr.next is not None:
            curr = curr.next

        # After the loop ends, curr is the last node in the linked list.
        assert curr.next is None

        # Swap the first item and last item
        temp = self._first.item
        self._first.item = curr.item
        curr.item = temp


def test_swap_first_and_last_error1() -> None:
    """A test case that illustrates an error in LinkedList.swap_first_and_last.

    Your test case should have the following structure:
    1. Create a "test input" linked list.
    2. Call the LinkedList.swap_first_and_last method on the linked list.
    3. Call LinkedList.to_list on the linked list to obtain a list of its elements.
    4. Compare that list against the expected list of elements (using
       an assert statement).
    """
    lst1 = LinkedList([1, 2, 3, 4])
    lst1.swap_first_and_last()
    assert lst1.to_list() == [4, 2, 3, 1]


def test_swap_first_and_last_error2() -> None:
    """A test case that illustrates a *different* error in LinkedList.swap_first_and_last.

    Follow the same instructions as the previous test case. Note that the error this
    test case reveals must be different from the error revealed by your first test
    case above.
    """
    lst2 = LinkedList([])
    lst2.swap_first_and_last()
    assert lst2.to_list() == []


def test_swap_first_and_last_no_error() -> None:
    """A test case that illustrates a case when LinkedList.swap_first_and_last is correct.

    Follow the same instructions as the previous test cases. Note that this test case
    should pass even though the given implementation of swap_first_and_last contains
    errors.
    """
    lst3 = LinkedList([1])
    lst3.swap_first_and_last()
    assert lst3.to_list() == [1]


if __name__ == '__main__':
    # This runs pytest on the tests cases you've defined in this file.
    import pytest

    pytest.main(['a1_part1.py', '-v'])

    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (In PyCharm, select the lines below and press Ctrl/Cmd + / to toggle comments.)
    # You can use "Run file in Python Console" to run both pytest and PythonTA,
    # and then also test your methods manually in the console.
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['invalid-name']
    })
