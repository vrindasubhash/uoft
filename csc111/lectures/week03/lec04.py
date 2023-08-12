"""CSC111 Winter 2021: Lecture 4 code
(also includes code from Lecture 3)
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Iterable, Optional
@dataclass
class _Node:
    """A node in a linked list.
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
    def __getitem__(self, i: int) -> Any:
        # Version 1
        curr = self._first
        curr_index = 0
        while curr is not None:
            if curr_index == i:
                return curr.item
            curr = curr.next
            curr_index = curr_index + 1
        raise IndexError
        # Version 2
        # curr = self._first
        # curr_index = 0
        #
        # while not (curr is None or curr_index == i):
        #     curr = curr.next
        #     curr_index = curr_index + 1
        #
        # assert curr is None or curr_index == i
        #
        # if curr is None:
        #     raise IndexError
        # else:
        #     return curr.item
    def append(self, item: Any) -> None:
        """Append item to the end of this list.
        >>> lst = LinkedList([1, 2, 3])
        >>> lst.append(4)
        >>> lst.to_list()
        [1, 2, 3, 4]
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
    def insert(self, i: int, item: Any) -> None:
        """Insert the given item at index i in this list.
        Raise IndexError if i > len(self).
        Note that adding to the end of the list (i == len(self)) is okay.
        Preconditions:
            - i >= 0
        >>> lst = LinkedList([1, 2, 10, 200])
        >>> lst.insert(2, 300)
        >>> lst.to_list()
        [1, 2, 300, 10, 200]
        """
        # Create the new node to add (this occurs in all cases)
        new_node = _Node(item)
        if i == 0:
            # Need to reassign self._first to add new_node at the front
            # new_node.next = self._first
            # self._first = new_node
            self._first, new_node.next = new_node, self._first
        else:
            # Need to mutate the (i-1)-th node to add new_node
            curr = self._first
            curr_index = 0
            while curr is not None:
                if curr_index == i - 1:
                    # curr refers to the (i-1)-th node
                    curr.next, new_node.next = new_node, curr.next
                    return
                curr = curr.next
                curr_index += 1
            # At this point, i - 1 is not a valid index,
            # therefore i > len(self), and so we raise an IndexError
            raise IndexError
    def pop(self, i: int) -> Any:
        """Remove and return the item at index i.
        Raise IndexError if i >= len(self).
        Preconditions:
            - i >= 0
        >>> lst = LinkedList([1, 2, 10, 200])
        >>> lst.pop(1)
        2
        >>> lst.to_list()
        [1, 10, 200]
        """
        if self._first is None:
            raise IndexError
        elif i == 0:
            # Remove and return the first node (need to update self._first)
            # This is close but subtly wrong (FIXED by adding a separate check for empty list)
            item = self._first.item
            self._first = self._first.next
            return item
        else:
            # Remove and return the i-th node
            # (need to iterate to the (i-1)-th node!)
            curr = self._first
            curr_index = 0
            # Compound loop condition version (for practice!)
            # NOTE: it is possible to use curr.next is None in the condition instead,
            # though there is a subtletly that I didn't want to get into during lecture.
            # Using "curr.next is None" will also ensure that curr is not None,
            # since curr = curr.next in the loop.
            while not (curr is None or curr_index == i - 1):
                curr = curr.next
                curr_index += 1
            # After the loop ends, the following is True:
            assert curr is None or curr_index == i - 1
            if curr is None or curr.next is None:
                raise IndexError
            else:
                item = curr.next.item
                curr.next = curr.next.next
                return item
            # Alternate version using a second "previous node" loop variable.
            # prev, curr = None, self._first
            # curr_index = 0
            #
            # # Now, iterate to the i-th node
            # while not (curr is None or curr_index == i):
            #     # Update both curr and prev in the loop
            #     prev, curr = curr, curr.next
            #     curr_index += 1
            #
            # # After the loop ends, the following is True:
            # assert curr is None or curr_index == i
            #
            # if curr is None:
            #     raise IndexError
            # else:
            #     # Return curr's item and update prev's "next" link.
            #     item = curr.item
            #     prev.next = curr.next
            #     return item
    def remove(self, item: Any) -> None:
        """Remove the first occurrence of item from the list.
        Raise ValueError if the item is not found in the list.
        >>> lst = LinkedList([10, 20, 30, 20])
        >>> lst.remove(20)
        >>> lst.to_list()
        [10, 30, 20]
        """
        prev, curr = None, self._first
        while not (curr is None or curr.item == item):
            prev, curr = curr, curr.next
        # Assert what we know after the loop ends
        assert curr is None or curr.item == item
        if curr is None:
            raise ValueError
        else:  # curr.item == item  (the item was found)
            if prev is None:  # curr is the first node in the list
                self._first = curr.next
                # Alternate:
                # self._first = self._first.next
            else:
                prev.next = curr.next
        # Alternate (flattening the nested if statement using "elif")
        # if curr is None:
        #     raise ValueError
        # elif prev is None:  # curr is the first node in the list
        #     self._first = curr.next
        # else:
        #     prev.next = curr.next
