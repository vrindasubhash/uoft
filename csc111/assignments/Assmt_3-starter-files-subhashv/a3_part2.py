"""CSC111 Winter 2023 Assignment 3: Graphs and Interconnection Networks

Instructions (READ THIS FIRST!)
===============================

This Python module contains the start of the classes you'll define for Part 2
of this assignment. As with Part 1, you may, but are not required to, add
doctest examples to help test your work. We strongly encourage you to do so!

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2023 Mario Badr and David Liu.
"""
import random
from typing import Optional

from python_ta.contracts import check_contracts

# NOTE: Node and NodeAddress must be imported for check_contracts
# to work correctly, even if they aren't being used directly in this
# module. Don't remove them (even if you get a warning about them in PyCharm)!
from a3_network import Channel, Packet, NodeAddress, Node
from a3_part1 import AbstractRing, AbstractStar, AbstractTorus


def wrap_address(i: int, k: int) -> int:
    """ Wraps around for addresses that are edge cases.
    """
    if i == k:
        return 0
    if i == -1:
        return k - 1
    return i


@check_contracts
class AlwaysRightRing(AbstractRing):
    """An implementation of the Always-Right Ring Network.

    Note that you only need to implement the route_packet method for this class.
    It will inherit the initializer from AbstractRing and the other useful methods
    from AbstractNetwork!
    """

    def route_packet(self, current_address: NodeAddress, packet: Packet) -> Optional[Channel]:
        """Return the channel that the packet should traverse next, given that it has
        just arrived at the node with address current_address.

        That is, the returned channel has the node corresponding to current_address as
        one of its endpoints. Ideally, but not necessarily, traversing the returned channel
        helps get the given packet closer to its destination.

        Return None if the current_address is equal to the packet's destination!

        Preconditions:
        - current_address in self._nodes
        - packet.source in self._nodes
        - packet.destination in self._nodes
        """

        # Check if we already reached the destination
        if current_address == packet.destination:
            return None

        # find the channel to the right, given a node
        current_node = self.get_node(current_address)
        next_address = wrap_address(current_address + 1, self.k)
        return current_node.channels[next_address]


def get_direction(k: int, start: int, end: int) -> int:
    """Going to return 1 or -1. 1 means go right, -1 means go left
    """
    a = end - start

    if a == 0:
        return 0

    a1 = abs(a)
    b = k - a1

    if a > 0:
        if a1 <= b:
            return 1
        else:
            return -1
    else:
        if a1 <= b:
            return -1
        else:
            return 1


@check_contracts
class ShortestPathRing(AbstractRing):
    """An implementation of the Shortest-Path Ring Network.

    Note that you only need to implement the route_packet method for this class.
    It will inherit the initializer from AbstractRing and the other useful methods
    from AbstractNetwork!
    """

    def route_packet(self, current_address: NodeAddress, packet: Packet) -> Optional[Channel]:
        """Return the channel that the packet should traverse next, given that it has
        just arrived at the node with address current_address.

        That is, the returned channel has the node corresponding to current_address as
        one of its endpoints. Ideally, but not necessarily, traversing the returned channel
        helps get the given packet closer to its destination.

        Return None if the current_address is equal to the packet's destination!

        Preconditions:
        - current_address in self._nodes
        - packet.source in self._nodes
        - packet.destination in self._nodes
        """

        # Check if we already reached the destination
        if current_address == packet.destination:
            return None

        # figure out whether to go left or right
        direction = get_direction(self.k, current_address, packet.destination)

        current_node = self.get_node(current_address)
        next_address = wrap_address(current_address + direction, self.k)
        return current_node.channels[next_address]


@check_contracts
class ShortestPathTorus(AbstractTorus):
    """An implementation of the Shortest-Path Torus Network.

    Note that you only need to implement the route_packet method for this class.
    It will inherit the initializer from AbstractTorus and the other useful methods
    from AbstractNetwork!
    """

    def route_packet(self, current_address: NodeAddress, packet: Packet) -> Optional[Channel]:
        """Return the channel that the packet should traverse next, given that it has
        just arrived at the node with address current_address.

        That is, the returned channel has the node corresponding to current_address as
        one of its endpoints. Ideally, but not necessarily, traversing the returned channel
        helps get the given packet closer to its destination.

        Return None if the current_address is equal to the packet's destination!

        Preconditions:
        - current_address in self._nodes
        - packet.source in self._nodes
        - packet.destination in self._nodes

        Implementation notes:
            - To determine the next node address, you'll need to recover the radix of this torus.
              There are a few different approaches for this, but if you want to calculate a square
              root, we haven't allowed you to import math.sqrt, but you can use "** 0.5" instead.
        """
        # Check if we already reached the destination
        if current_address == packet.destination:
            return None

        current_node = self.get_node(current_address)

        # figure out whether to go left or right
        l_or_r = get_direction(self.k, current_address[0], packet.destination[0])

        if l_or_r != 0:
            # Initially moves left or right until you reach the correct column.
            next_address = (wrap_address((current_address[0] + l_or_r), self.k), current_address[1])
        else:
            # Already in correct column, now finding the correct row.
            u_or_d = get_direction(self.k, current_address[1], packet.destination[1])
            next_address = (current_address[0], wrap_address((current_address[1] + u_or_d), self.k))

        return current_node.channels[next_address]


@check_contracts
class ShortestPathStar(AbstractStar):
    """An implementation of the Shortest-Path Star Network.

    Note that you only need to implement the route_packet method for this class.
    It will inherit the initializer from AbstractStar and the other useful methods
    from AbstractNetwork!
    """

    def route_packet(self, current_address: NodeAddress, packet: Packet) -> Optional[Channel]:
        """Return the channel that the packet should traverse next, given that it has
        just arrived at the node with address current_address.

        That is, the returned channel has the node corresponding to current_address as
        one of its endpoints. Ideally, but not necessarily, traversing the returned channel
        helps get the given packet closer to its destination.

        Return None if the current_address is equal to the packet's destination!

        Preconditions:
        - current_address in self._nodes
        - packet.source in self._nodes
        - packet.destination in self._nodes
        """

        # Check if we already reached the destination
        if current_address == packet.destination:
            return None

        current_node = self.get_node(current_address)

        if self.is_central(current_address) or self.is_central(packet.destination):
            next_address = packet.destination
        else:
            next_address = random.randint(0, self.get_num_central() - 1)

        return current_node.channels[next_address]


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
        'extra-imports': ['random', 'a3_network', 'a3_part1'],
        'disable': ['unused-import']
    })
