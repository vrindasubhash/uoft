"""CSC111 Winter 2023 Assignment 3: Graphs and Interconnection Networks

Instructions (READ THIS FIRST!)
===============================

This Python module contains the start of functions and/or classes you'll define
for Part 4 of this assignment. You may, but are not required to, add doctest
examples to help test your work. We strongly encourage you to do so!

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
from a3_network import Channel, NodeAddress, Node, Packet
from a3_part1 import AbstractRing, AbstractTorus, AbstractStar


def short_distance(n1: int, n2: int, k: int) -> int:
    """shortest distance between two nodes, considers wrap around.
    """
    if n1 == n2:
        return 0

    a = abs(n1 - n2)
    b = k - a

    return min(a, b)


@check_contracts
class GreedyChannelRing(AbstractRing):
    """An implementation of the Greedy-Channel Ring Network.
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

        node = self.get_node(current_address)

        minimum = float('inf')
        min_list = []

        # find neighbors with the fastest path
        for a, c in node.channels.items():
            neighbor_score = self.get_distance(current_address, a) + c.total_occupancy()
            if neighbor_score < minimum:
                minimum = neighbor_score
                min_list = [c]
            elif neighbor_score == minimum:
                min_list.append(c)

        distance_list = [(self.get_distance(ch.get_other_endpoint(node).address, packet.destination), ch)
                         for ch in min_list]
        return greedy_channel_select(distance_list)

    def get_distance(self, n1: NodeAddress, n2: NodeAddress) -> int:
        """Return the shortest path distance between the two given node (addresses).

        Remember that path distance is measured as the number of channels/edges, not nodes.
        When n1 == n2, the shortest path distance is 0.

        Preconditions:
            - n1 in self._nodes
            - n2 in self._nodes
        """
        return short_distance(n1, n2, self.k)


@check_contracts
class GreedyChannelTorus(AbstractTorus):
    """An implementation of the Greedy-Channel Torus Network.
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

        node = self.get_node(current_address)

        minimum = float('inf')
        min_list = []

        # find neighbors with the fastest path
        for a, c in node.channels.items():
            neighbor_score = self.get_distance(current_address, a) + c.total_occupancy()
            if neighbor_score < minimum:
                minimum = neighbor_score
                min_list = [c]
            elif neighbor_score == minimum:
                min_list.append(c)

        distance_list = [(self.get_distance(ch.get_other_endpoint(node).address, packet.destination), ch)
                         for ch in min_list]
        return greedy_channel_select(distance_list)

    def get_distance(self, n1: NodeAddress, n2: NodeAddress) -> int:
        """Return the shortest path distance between the two given node (addresses).

        Remember that path distance is measured as the number of channels/edges, not nodes.
        When n1 == n2, the shortest path distance is 0.

        Preconditions:
            - n1 in self._nodes
            - n2 in self._nodes
        """
        if n1 == n2:
            return 0
        return short_distance(n1[0], n2[0], self.k) + short_distance(n1[1], n2[1], self.k)


@check_contracts
class GreedyChannelStar(AbstractStar):
    """An implementation of the Greedy-Channel Star Network.
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

        node = self.get_node(current_address)

        minimum = float('inf')
        min_list = []

        # find neighbors with the fastest path
        for a, c in node.channels.items():
            neighbor_score = self.get_distance(current_address, a) + c.total_occupancy()
            if neighbor_score < minimum:
                minimum = neighbor_score
                min_list = [c]
            elif neighbor_score == minimum:
                min_list.append(c)

        distance_list = [(self.get_distance(ch.get_other_endpoint(node).address, packet.destination), ch)
                         for ch in min_list]
        return greedy_channel_select(distance_list)

    def get_distance(self, n1: NodeAddress, n2: NodeAddress) -> int:
        """Return the shortest path distance between the two given node (addresses).

        Remember that path distance is measured as the number of channels/edges, not nodes.
        When n1 == n2, the shortest path distance is 0.

        Preconditions:
            - n1 in self._nodes
            - n2 in self._nodes
        """
        if n1 == n2:
            return 0

        if n2 in self.get_node(n1).channels:
            return 1

        return 2


@check_contracts
def greedy_channel_select(channels: list[tuple[int, Channel]]) -> Channel:
    """Return the channel that minimizes the quantity described under "Greedy Channel Routing Algorithn"
    on the assignment handout.

    Each tuple in channels is of the form (d, channel), where d is the shortest-path distance
    from the neighbour to the packet's destination, and channel is the channel to that neighbour.

    Break ties as described on the assignment handout.

    Preconditions:
    - channels != []
    - all(tup[0] >= 0 for tup in channels)
    """
    min_distance = float('inf')
    min_channels = []

    # finds shortest channels
    for d, c in channels:
        if d < min_distance:
            min_distance = d
            min_channels = [c]
        elif d == min_distance:
            min_channels.append(c)

    # randomly break tie between shortest channels
    # random.randint(0,0) returns 0
    return min_channels[random.randint(0, len(min_channels) - 1)]


###################################################################################################
# Question 2
###################################################################################################
@check_contracts
class GreedyPathRing(AbstractRing):
    """An implementation of the Greedy-Path Ring Network.
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

        node = self.get_node(current_address)
        return greedy_path_select(node.find_paths(packet.destination, set()))


@check_contracts
class GreedyPathTorus(AbstractTorus):
    """An implementation of the Greedy-Path Torus Network.
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

        node = self.get_node(current_address)
        return greedy_path_select(node.find_paths(packet.destination, set()))


@check_contracts
class GreedyPathStar(AbstractStar):
    """An implementation of the Greedy-Path Star Network.
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

        node = self.get_node(current_address)
        return greedy_path_select(node.find_paths(packet.destination, set()))


@check_contracts
def greedy_path_select(paths: list[list[Channel]]) -> Channel:
    """Return the first channel in the path that minimizes the quantity described under "Greedy Path Routing Algorithn"
    on the assignment handout.

    Break ties as described on the assignment handout.

    Preconditions:
    - paths != []
    - every element of paths is a valid path
    - every path in paths starts at the same node
    - every path in paths ends at the same node
    """

    min_score = float('inf')
    min_paths = []

    # find paths with smallest scores
    for p in paths:
        s = compute_path_score(p)
        if s < min_score:
            min_score = s
            min_paths = [p]
        elif s == min_score:
            min_paths.append(p)

    # find shortest path
    short_score = float('inf')
    short_paths = []

    for p in min_paths:
        length = len(p)
        if length < short_score:
            short_score = length
            short_paths = [p]
        elif length == short_score:
            short_paths.append(p)

    # break tie
    return short_paths[random.randint(0, len(short_paths) - 1)][0]


@check_contracts
def compute_path_score(path: list[Channel]) -> int:
    """Return the "Greedy Path Routing Algorithm" path score for the given path.

    See assignment handout for details.

    Preconditions:
        - path is a valid path
        - path != []
    """
    total_occupacy = 0

    for i in range(len(path)):
        total_occupacy += max(path[i].total_occupancy() - i, 0)

    return len(path) + total_occupacy


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
