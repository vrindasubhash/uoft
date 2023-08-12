"""CSC111 Winter 2023 Assignment 3: Graphs and Interconnection Networks

Instructions (READ THIS FIRST!)
===============================

This Python module contains the start of three network classes you'll define
for Part 1 of this assignment.

You may, but are not required, to add doctest examples to check your work
for this part of the assignment (and all other parts).

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2023 Mario Badr and David Liu.
"""
from python_ta.contracts import check_contracts

# NOTE: Node and NodeAddress must be imported for check_contracts
# to work correctly, even if they aren't being used directly in this
# module. Don't remove them (even if you get a warning about them in PyCharm)!
from a3_network import AbstractNetwork, Node, NodeAddress


def wrap_address(i: int, k: int) -> int:
    """ Wraps around for addresses that are edge cases.
    """
    if i == k:
        return 0
    if i == -1:
        return k - 1
    return i


@check_contracts
class AbstractRing(AbstractNetwork):
    """An abstract network with a ring topology.

    See the assignment handout for a description of this and other network topologies you're implementing.

    Representation Invariants:
        - all(isinstance(address, int) for address in self._nodes)
    """
    k: int

    def __init__(self, k: int) -> None:
        """Initialize this network with a ring topology of radix k.

        Preconditions:
            - k >= 3
        """
        super().__init__()

        self.k = k

        for i in range(k):
            self.add_node(i)

        for i in range(k):
            self.add_channel(i, wrap_address(i + 1, k))


@check_contracts
class AbstractTorus(AbstractNetwork):
    """An abstract network with a torus topology.

    See the assignment handout for a description of this and other network topologies you're implementing.

    Representation Invariants:
        - all(isinstance(address, tuple) for address in self._nodes)
    """
    k: int

    def __init__(self, k: int) -> None:
        """Initialize this network with a torus topology of radix k.

        Preconditions:
            - k >= 3
        """
        super().__init__()

        self.k = k

        for i in range(k):
            for j in range(k):
                self.add_node((i, j))

        for i in range(k):
            for j in range(k):
                self.add_channel((i, j), (wrap_address(i - 1, k), j))
                self.add_channel((i, j), (wrap_address(i + 1, k), j))
                self.add_channel((i, j), (i, wrap_address(j - 1, k)))
                self.add_channel((i, j), (i, wrap_address(j + 1, k)))


@check_contracts
class AbstractStar(AbstractNetwork):
    """An abstract network with a star topology.

    A star topology has k1 central nodes that are all adjacent to each other and k2 outer nodes that
    are each adjacent to all central nodes.

    See the assignment handout for a description of this and other network topologies you're implementing.

    Private Instance Attributes (in addition to _nodes from AbstractNetwork):
        - _num_central: the number of central nodes
        - _num_outer: the number of outer nodes

    Representation Invariants:
        - all(isinstance(address, int) for address in self._nodes)
        - self._num_central >= 1
        - self._num_outer >= 1
    """
    _num_central: int
    _num_outer: int

    def __init__(self, k1: int, k2: int) -> None:
        """Initialize this network with a star topology of k1 central nodes and k2 outer nodes.

        Preconditions:
            - k1 >= 1
            - k2 >= 1

        Implementation note:
            - In addition to initialzing self._nodes, make sure to initialize the other two
              instance attributes described in the class docstring.
        """
        super().__init__()
        self._num_central = k1
        self._num_outer = k2

        for i in range(k1 + k2):
            self.add_node(i)

        for i in range(k1):
            for j in range(k1 + k2):
                if i != j:
                    self.add_channel(i, j)

    def is_central(self, node_address: int) -> bool:
        """Checks if the given node address is a central node.
        """
        return node_address < self._num_central

    def get_num_central(self) -> int:
        """Get number of central nodes.
        """
        return self._num_central


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)

    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (In PyCharm, select the lines below and press Ctrl/Cmd + / to toggle comments.)
    # You can use "Run file in Python Console" to run PythonTA,
    # and then also test your methods manually in the console.
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 120,
        'extra-imports': ['a3_network'],
        'disable': ['abstract-method', 'unused-import']
    })
