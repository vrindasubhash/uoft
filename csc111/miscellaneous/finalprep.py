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

    Representation Invariants:
    - all(item == self._vertices[item].item for item in self._vertices)
    """
    # Private Instance Attributes:
    #     - _vertices: A collection of the vertices contained in this graph.
    #                  Maps item to _Vertex instance.
    _vertices: dict[Any, _Vertex]

    def __init__(self) -> None:
        """Initialize an empty graph (no vertices or edges)."""
        self._vertices = {}

    def add_vertex(self, item: Any) -> None:
        """Add a vertex with the given item to this graph.

        The new vertex is not adjacent to any other vertices.

        Preconditions:
            - item not in self._vertices
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

    def adjacent0(self, item1: Any, item2: Any) -> bool:
        """Return whether item1 and item2 are adjacent vertices in this graph.

        Return False if item1 or item2 do not appear as vertices in this graph.
        >>> g = Graph()
        >>> g.add_vertex('a')
        >>> g.add_vertex('b')
        >>> g.add_vertex('c')
        >>> g.add_vertex('d')
        >>> g.add_edge('a', 'b')
        >>> g.add_edge('b', 'c')
        >>> g.adjacent('a', 'b')
        True
        >>> g.adjacent('a', 'd')
        False
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            return any(v2.item == item2 for v2 in v1.neighbours)
        else:
            # We didn't find an existing vertex for both items.
            return False

    def adjacent(self, item1: Any, item2: Any) -> bool:
        """Return whether item1 and item2 are adjacent vertices in this graph.

        Return False if item1 or item2 do not appear as vertices in this graph.
        >>> g = Graph()
        >>> g.add_vertex('a')
        >>> g.add_vertex('b')
        >>> g.add_vertex('c')
        >>> g.add_vertex('d')
        >>> g.add_edge('a', 'b')
        >>> g.add_edge('b', 'c')
        >>> g.adjacent('a', 'b')
        True
        >>> g.adjacent('a', 'd')
        False
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            v2 = self._vertices[item2]
            return v2 in v1.neighbours
        else:
            return False


# g = Graph()
# g.add_vertex('a')
# g.add_vertex('b')
# g.add_vertex('c')
# g.add_vertex('d')
# g.add_edge('a', 'b')
# g.add_edge('b', 'c')
# g.adjacent('a', 'b')
# # True
# g.adjacent('a', 'd')
# # False
