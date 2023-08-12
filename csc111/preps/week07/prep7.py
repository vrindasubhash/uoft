"""CSC111 Winter 2023 Prep 7: Programming Exercises

Instructions (READ THIS FIRST!)
===============================

This module contains the graph implementation we studied in lecture, with a few
additional methods for you to implement on this exercise.

We have marked each place you need to write code with the word "TODO".
As you complete your work in this file, delete each TODO comment.

You may add additional doctests, but they will not be graded. You should test your work
carefully before submitting it!

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2023 Mario Badr and David Liu.
"""
from __future__ import annotations
from typing import Any


class _Vertex:
    """A vertex in a graph.

    Instance Attributes:
        - item: The data stored in this vertex.
        - neighbours: The vertices that are adjacent to this vertex.

    Representation Invariants:
        - self not in self.neighbours
        - all(self in u.neighbours for u in self.neighbours)
    """
    item: Any
    neighbours: set[_Vertex]

    def __init__(self, item: Any, neighbours: set[_Vertex]) -> None:
        """Initialize a new vertex with the given item and neighbours."""
        self.item = item
        self.neighbours = neighbours


class Graph:
    """A graph.
    """
    # Private Instance Attributes:
    #     - _vertices:
    #         A collection of the vertices contained in this graph.
    #         Maps item to _Vertex object.
    _vertices: dict[Any, _Vertex]

    def __init__(self) -> None:
        """Initialize an empty graph (no vertices or edges)."""
        self._vertices = {}

    def add_vertex(self, item: Any) -> None:
        """Add a vertex with the given item to this graph.

        The new vertex is not adjacent to any other vertices.
        """
        self._vertices[item] = _Vertex(item, set())

    def add_edge(self, item1: Any, item2: Any) -> None:
        """Add an edge between the two vertices with the given items in this graph.

        Raise a ValueError if item1 or item2 do not appear as vertices in this graph.

        Preconditions:
            - item1 != item2
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            v2 = self._vertices[item2]

            # Add the new edge
            v1.neighbours.add(v2)
            v2.neighbours.add(v1)
        else:
            # We didn't find an existing vertex for both items.
            raise ValueError

    def adjacent(self, item1: Any, item2: Any) -> bool:
        """Return whether item1 and item2 are adjacent vertices in this graph.

        Return False if item1 or item2 do not appear as vertices in this graph.
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            return any(v2.item == item2 for v2 in v1.neighbours)
        else:
            # We didn't find an existing vertex for both items.
            return False

    def get_neighbours(self, item: Any) -> set:
        """Return a set of the neighbours of the given item.

        Note that the *items* are returned, not the _Vertex objects themselves.

        Raise a ValueError if item does not appear as a vertex in this graph.
        """
        if item in self._vertices:
            v = self._vertices[item]
            return {neighbour.item for neighbour in v.neighbours}
        else:
            raise ValueError

    ###########################################################################
    # Prep exercises start here
    ###########################################################################
    def degree(self, item: Any) -> int:
        """Return the degree of the vertex corresponding to the given item.

        Raise a ValueError if item does not appear as a vertex in this graph.

        >>> example_graph = Graph()
        >>> example_graph.add_vertex(10)
        >>> example_graph.add_vertex(20)
        >>> example_graph.add_vertex(30)
        >>> example_graph.add_edge(10, 20)
        >>> example_graph.degree(10)
        1
        >>> example_graph.degree(30)
        0
        """
        count = 0
        if item not in self._vertices:
            raise ValueError

        for vertex in self._vertices:
            if self.adjacent(vertex, item):
                count += 1

        return count

    def verify_path(self, items: list) -> bool:
        """Return whether the given items form a path in this graph.

        Recall that a path is a sequence of distinct vertices v_0, v_1, ..., v_k
        such that every consecutive pair of vertices is adjacent.

        Note that you are given the ITEMS, not _Vertex objects.
        That means you'll either need to perform a dictionary lookup in self._vertices
        yourself, or pass the items to other Graph methods.

        Return False when the given items have duplicates, or when at least one of the
        items do not appear as a vertex in this graph. You may use try-except statements
        (see Section 10.6 of the Course Notes), but this is not required to implement
        this method.

        Preconditions:
            - items != []

        >>> example_graph = Graph()
        >>> example_graph.add_vertex(10)
        >>> example_graph.add_vertex(20)
        >>> example_graph.add_vertex(30)
        >>> example_graph.verify_path([10, 20, 30, 40])
        False
        """

        for i in range(len(items) - 1):
            if items[i + 1] not in self._vertices[items[i]].neighbours:
                return False
            for j in range(len(items)):
                if i != j and items[i] == items[j]:
                    return False
            if items[i] not in self._vertices:
                return False
        return True

    def add_all_edges(self, edges: set[tuple[Any, Any]]) -> None:
        """Add all given edges to this graph.

        Each element of edges is a tuple (x, y), representing the edge {x, y}.
        If an object in a given edge isn't represented by a vertex in this graph,
        add a new vertex containing the object to this graph before adding the edge.
        We strongly encourage you to make use of the Graph methods defined above.

        This method should NOT raise any ValueErrors.

        Preconditions:
        - all(edge[0] != edge[1] for edge in edges)

        >>> example_graph = Graph()
        >>> example_edges = {(1, 2), (1, 3), (3, 4)}
        >>> example_graph.add_all_edges(example_edges)
        >>> example_graph.get_neighbours(1) == {2, 3}
        True
        >>> example_graph.get_neighbours(3) == {1, 4}
        True
        """
        for edge in edges:
            if edge[0] not in self._vertices:
                self.add_vertex(edge[0])
            if edge[1] not in self._vertices:
                self.add_vertex(edge[1])
            self.add_edge(edge[0], edge[1])


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
    })
