"""CSC111 Winter 2023: Final Project
The node class that represents provinces and cities.
===============================
This module contains a collection of Python classes and functions that we used
represent a series of trees and graphs.
Copyright and Usage Information
===============================
This file is Copyright (c) 2023 Stefan Ateljevic, Veda Kesarwani, Sydelle Mago, and Vrinda Subhash.
"""
from __future__ import annotations

# import csv
from datetime import date, datetime


# from python_ta.contracts import check_contracts
# import pandas as pd
# import folium
# from igraph import Graph
# import plotly.graph_objects as go

###############################################################################
# Classes and Functions
###############################################################################


# @check_contracts
class Node:
    """A tree that represents an entity which can be either a province or a city in Canada.

    Instance Attributes:
    - name:
        The name of the province or city .
    - population:
        The total population of the province.
    - cumulative_cases:
        The total cases up until a given day.
    - cases:
        A dictionary with the key being the date, and value being a tuple, where the
         first value is the cumulative cases until that day and the second value is just the cases for that day.
    - children:
        A dictionary with the key being a string which is the name of the province/city and the value
         being the Node reffering to that province/city.

    Representation Invariants:
    - isinstance(self.name, str)
    - isinstance(self.population, int)
    - self.population >= 0
    - isinstance(self.cumulative_cases, int)
    - self.cumulative_cases >= 0

    """
    name: str
    population: int
    cumulative_cases: int
    cases: dict[date, (int, int)]
    children: dict[str, Node]

    def __init__(self, name: str, population: int) -> None:
        """Initialize this tree with the given address and no connections to other nodes.
        >>> node = Node("Ontario", 1000000)
        >>> node.name
        'Ontario'
        >>> node.population
        1000000
        >>> node.cumulative_cases
        0
        >>> len(node.cases)
        0
        >>> len(node.children)
        0
        """
        self.name = name
        self.population = population
        self.cumulative_cases = 0
        self.cases = {}
        self.children = {}

    def __repr__(self) -> str:
        """Return a string representing this node. __repr__ is a special method that's called when the object is
        evaluated in the Python console.
        >>> parent = Node("Ontario", 1000000)
        >>> child1 = Node("Toronto", 500000)
        >>> child2 = Node("Ottawa", 400000)
        >>> parent.add_child("Toronto", child1)
        >>> parent.add_child("Ottawa", child2)
        >>> parent
        Ontario (Population: 1000000, Cumulative cases: 0, \
Children: [Toronto (Population: 500000, Cumulative cases: 0), \
Ottawa (Population: 400000, Cumulative cases: 0)])
        """
        child_reprs = ', '.join([repr(child) for child in self.children.values()])
        if self.children:
            return f"{self.name} (Population: {self.population}, " \
                   f"Cumulative cases: {self.cumulative_cases}, Children: [{child_reprs}])"
        else:
            return f"{self.name} (Population: {self.population}, Cumulative cases: {self.cumulative_cases})"

    def add_child(self, name: str, node: Node) -> None:
        """Add a child to this node with the given name

        Preconditions:
        - name != ''
        - name not in self.children
        - isinstance(node, Node)

        >>> parent = Node('Ontario', 1000000)
        >>> child = Node('Toronto', 500000)
        >>> parent.add_child('Toronto', child)
        >>> len(parent.children)
        1
        >>> parent.children['Toronto'].name
        'Toronto'
        """
        self.children[name] = node

    def get_child(self, name: str) -> Node:
        """ Return the child node with the given name

        Preconditions:
        - name != ''
        - name in self.children

        >>> parent = Node('Ontario', 1000000)
        >>> child = Node('Toronto', 500000)
        >>> parent.add_child('Toronto', child)
        >>> retrieved_child = parent.get_child('Toronto')
        >>> retrieved_child.name
        'Toronto'
        >>> retrieved_child.population
        500000
        """
        return self.children[name]

    def get_or_create_child(self, name: str) -> Node:
        """ Return the child node with the given name, or create and return a new child node

        Preconditions:
        - name != ''

        if it does not exist
        >>> parent = Node('Ontario', 1000000)
        >>> existing_child = Node('Toronto', 500000)
        >>> parent.add_child('Toronto', existing_child)
        >>> retrieved_child = parent.get_or_create_child('Toronto')
        >>> retrieved_child.name
        'Toronto'
        >>> new_child = parent.get_or_create_child('Ottawa')
        >>> new_child.name
        'Ottawa'
        >>> new_child.population
        -1
        """
        if name not in self.children:
            self.children[name] = Node(name, -1)
        return self.children[name]

    def total_children(self) -> int:
        """ Return the total number of descendants from this node

        Preconditions:
        - all(isinstance(value, Node) for value in self.children.values())

        >>> root = Node("Ontario", 1000000)
        >>> child1 = Node("Toronto", 500000)
        >>> child2 = Node("Ottawa", 400000)
        >>> root.add_child("Toronto", child1)
        >>> child1.add_child("North York", Node("North York", 200000))
        >>> root.add_child("Ottawa", child2)
        >>> root.total_children()
        4
        """
        num = 1  # include this node
        for subtree in self.children.values():
            num += subtree.total_children()
        return num

    def add_case(self, d: date, cases: int) -> None:
        """Updates the province/city cases for the given date.

        Preconditions:
        - isinstance(d, date)
        - isinstance(cases, int)
        - cases >= 0

        >>> ontario = Node('Ontario', 1000000)
        >>> ontario.cumulative_cases
        0
        >>> d1 = date(2020, 3, 1)
        >>> ontario.add_case(d1, 5)
        >>> ontario.cumulative_cases
        5
        >>> ontario.cases[d1]
        (5, 5)
        >>> d2 = date(2020, 3, 2)
        >>> ontario.add_case(d2, 10)
        >>> ontario.cumulative_cases
        15
        >>> ontario.cases[d2]
        (15, 10)
        """
        self.cumulative_cases += cases
        if d in self.cases:
            _, c = self.cases[d]
            cases += c
        self.cases[d] = (self.cumulative_cases, cases)

    def get_avg_cases(self, d: date) -> float:
        """Return the average number of COVID-19 cases in this province/city by date.

        Preconditions:
        - isinstance(d, date)
        - d in self.cases

        >>> ontario = Node('Ontario', 1000000)
        >>> d1 = date(2020, 3, 1)
        >>> ontario.add_case(d1, 5)
        >>> avg_cases_d1 = ontario.get_avg_cases(d1)
        >>> round(avg_cases_d1, 6)
        5e-06
        >>> d2 = date(2020, 3, 2)
        >>> ontario.add_case(d2, 1000)
        >>> avg_cases_d2 = ontario.get_avg_cases(d2)
        >>> round(avg_cases_d2, 6)
        0.001005
        """
        cumulative, _ = self.cases[d]
        return cumulative / self.population

    def num_cases_increased(self, start_date: date, end_date: date) -> bool:
        """

        Preconditions:
        - isinstance(start_date, date)
        - isinstance(end_date, date)
        - start_date in self.cases
        - end_date in self.cases
        - start_date < end_date

        >>> ontario = Node("Ontario", 1000000)
        >>> start = date(2020, 3, 1)
        >>> ontario.add_case(start, 5)
        >>> end = date(2020, 3, 2)
        >>> ontario.add_case(end, 10)
        >>> ontario.num_cases_increased(start, end)
        True
        >>> end2 = date(2020, 3, 3)
        >>> ontario.add_case(end2, 3)
        >>> ontario.num_cases_increased(end, end2)
        False
        """
        _, start_cases = self.cases[start_date]
        _, end_cases = self.cases[end_date]

        return end_cases > start_cases

    def total_cases_in_date_range(self, start_date: date, end_date: date) -> int:
        """A method that returns the total cases of the province/city
        for a certain range date and mutates total_cases.

        Preconditions:
        - isinstance(start_date, date)
        - isinstance(end_date, date)
        - start_date in self.cases
        - end_date in self.cases
        - start_date <= end_date

        >>> ontario = Node("Ontario", 1000000)
        >>> d1 = date(2020, 3, 1)
        >>> ontario.add_case(d1, 5)
        >>> d2 = date(2020, 3, 2)
        >>> ontario.add_case(d2, 10)
        >>> d3 = date(2020, 3, 3)
        >>> ontario.add_case(d3, 7)
        >>> ontario.total_cases_in_date_range(d1, d3)
        22
        >>> ontario.total_cases_in_date_range(d1, d2)
        15
        """
        sum_cases = 0
        for item_date in self.cases:
            if start_date <= item_date <= end_date:
                _, c = self.cases[item_date]
                sum_cases += c
        return sum_cases

    def get_cases(self) -> int:
        """ Return the total number of cases in this tree

        Preconditions:
        - all(isinstance(value, Node) for value in self.children.values())

        >>> root = Node("Canada", 0)
        >>> create_provinces(root)
        >>> ontario = root.get_child("Ontario")
        >>> ontario.add_case(date(2020, 3, 1), 5)
        >>> ontario.add_case(date(2020, 3, 2), 10)
        >>> quebec = root.get_child("Quebec")
        >>> quebec.add_case(date(2020, 3, 1), 3)
        >>> quebec.add_case(date(2020, 3, 2), 8)
        >>> root.get_cases()
        26
        """
        # There are 4 situations:
        # 1. Canada Node: it does not have cumulative_cases updated. Get sum of childrens cases.
        # 2. It is a province with no cities (children). Use the cumulative_cases
        # 3. It is a provice with cities (children). Ignore the children and just use the cumulative_cases
        # 4. It is a city. It is a leaf. You should never reach there.

        if self.name == 'Canada':
            # case 1
            s = 0
            for c in self.children.values():
                s += c.get_cases()
        else:
            # case 2,3
            s = self.cumulative_cases

        return s
