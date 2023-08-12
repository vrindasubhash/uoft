"""David Lecture 1 code"""
from __future__ import annotations
from dataclasses import dataclass
import math  # For Exercise 1 Q1
from typing import Any, Optional
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
    def __init__(self) -> None:
        """Initialize an empty linked list.
        """
        self._first = None
    def sum_items(self) -> int:
        """Return the sum of the items in this linked list.
        Preconditions:
            - all items in this linked list are ints
        """
        sum_so_far = 0
        curr = self._first
        while curr is not None:  # or, while not (curr is None):
            sum_so_far = sum_so_far + curr.item
            curr = curr.next
        # Contrast with:
        # i = 0
        # while i < len(self):
        #     sum_so_far = sum_so_far + self[i]
        #     i = i + 1
        return sum_so_far
    ###########################################################################
    # Exercise 1: Linked List Traversal
    ###########################################################################
    def maximum(self) -> float:
        """Return the maximum element in this linked list.
        Preconditions:
            - every element in this linked list is a float
            - this linked list is not empty
        >>> linky = LinkedList()
        >>> node3 = _Node(30.0)
        >>> node2 = _Node(-20.5, node3)
        >>> node1 = _Node(10.1, node2)
        >>> linky._first = node1
        >>> linky.maximum()
        30.0
        """
        # Implementation note: as usual for compute maximums,
        # import the math module and initialize your accumulator
        # to -math.inf (negative infinity).
        max_so_far = -math.inf  # Comment: could also initialize to
self._first.item
        curr = self._first
        while curr is not None:  # or, while not (curr is None):
            if curr.item > max_so_far:
                max_so_far = curr.item
            # Or,
            # max_so_far = max(max_so_far, curr.item)
            curr = curr.next
        return max_so_far
    def __contains__(self, item: Any) -> bool:
        """Return whether item is in this list.
        >>> linky = LinkedList()
        >>> linky.__contains__(10)
        False
        >>> node2 = _Node(20)
        >>> node1 = _Node(10, node2)
        >>> linky._first = node1
        >>> linky.__contains__(20)
        True
        """
        curr = self._first
        while curr is not None:
            # We should be comparing the node's item with item, not the node
itself.
            # As written, this comparison will always be False (assuming item isn't
a _Node).
            # if curr.item == item:
            if curr == item:
                # We've found the item and can return early.
                return True
            curr = curr.next
        # If we reach the end of the loop without finding the item,
        # it's not in the linked list.
        return False
    def __getitem__(self, i: int) -> Any:
        """Return the item stored at index i in this linked list.
        Raise an IndexError if index i is out of bounds.
        Preconditions:
            - i >= 0
        """
        curr = self._first
        curr_index = 0
        while curr is not None:
            if curr_index == i:
                return curr.item
            curr = curr.next
            curr_index += 1
        raise IndexError
        # Version 2: not using an early return, but using a "compound loop
condition"
        # HOMEWORK: read about this in 13.2
        # curr = self._first
        # curr_index = 0  # the index of the current node
        #
        # # Idea: modify the loop condition so that we stop when EITHER:
        # #  1. we reach the end of the list (curr is None)
        # #  2. we reach the right index (curr_index == i)
        # while not (... or ...):
        #     curr = curr.next
        #     curr_index = curr_index + 1
        #
        # # Now, detect which of the two cases we're in (1 or 2)
        # # and handle each case separately.
        # if ...:
        #     ...
        # else:
        #     ...
if __name__ == '__main__':
    import doctest
    doctest.testmod()
