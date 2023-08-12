"""CSC111 Winter 2023: Final Project

Description
===============================

This module contains a collection of Python classes and functions that we used
represent a series of trees and graphs.

Copyright and Usage Information
===============================
This file is Copyright (c) 2023 Stefan Ateljevic, Veda Kesarwani, Sydelle Mago, and Vrinda Subhash.
"""
from __future__ import annotations

from turtle import position

from python_ta.contracts import check_contracts
from datetime import date, datetime
import csv
import pandas as pd
import folium
from igraph import Graph, EdgeSeq
import plotly.graph_objects as go
import os


###############################################################################
# Classes and Functions
###############################################################################


@check_contracts
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
        """Return a string representing this node.

        __repr__ is a special method that's called when the object is evaluated in the Python console.

        >>> parent = Node("Ontario", 1000000)
        >>> child1 = Node("Toronto", 500000)
        >>> child2 = Node("Ottawa", 400000)
        >>> parent.add_child("Toronto", child1)
        >>> parent.add_child("Ottawa", child2)
        >>> parent
        Ontario (Population: 1000000, Cumulative cases: 0, Children: [Toronto (Population: 500000, Cumulative cases: 0),
         Ottawa (Population: 400000, Cumulative cases: 0)])
        """
        # TODO fix and make it recursive to go through the nodes
        child_reprs = ', '.join([repr(child) for child in self.children.values()])
        if self.children:
            return f"{self.name} (Population: {self.population}, " \
                   f"Cumulative cases: {self.cumulative_cases}, Children: [{child_reprs}])"
        else:
            return f"{self.name} (Population: {self.population}, Cumulative cases: {self.cumulative_cases})"

    def add_child(self, name: str, node: Node) -> None:
        """Add a child to this node with the given name

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
        """ Return the total number of child nodes in the current node

        >>> parent = Node('Ontario', 1000000)
        >>> child1 = Node('Toronto', 500000)
        >>> child2 = Node('Ottawa', 400000)
        >>> parent.add_child('Toronto', child1)
        >>> parent.total_children()
        1
        >>> parent.add_child('Ottawa', child2)
        >>> parent.total_children()
        2
        """
        return len(self.children)

    def add_case(self, d: date, cases: int) -> None:
        """Updates the province/city cases for the given date.

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

        >>> ontario = Node('Ontario', 1000000)
        >>> d1 = date(2020, 3, 1)
        >>> ontario.add_case(d1, 5)
        >>> avg_cases_d1 = ontario.get_avg_cases(d1)
        >>> round(avg_cases_d1, 6)
        0.000005
        >>> d2 = date(2020, 3, 2)
        >>> ontario.add_case(d2, 10)
        >>> avg_cases_d2 = ontario.get_avg_cases(d2)
        >>> round(avg_cases_d1, 6)
        0.000015
        """
        cumulative, _ = self.cases[d]
        return cumulative / self.population

    def num_cases_increased(self, start_date: date, end_date: date) -> bool:
        """
        >>> ontario = Node("Ontario", 1000000)
        >>> start = date(2020, 3, 1)
        >>> ontario.add_case(start, 5)
        >>> end = date(2020, 3, 2)
        >>> ontario.add_case(end, 10)
        >>> ontario.num_cases_increased(start, end)
        True
        >>> end2 = date(2020, 3, 3)
        >>> ontario.add_case(end2, 3)
        >>> ontario.num_cases_increased(end_date, end2)
        False
        """
        _, start_cases = self.cases[start_date]
        _, end_cases = self.cases[end_date]

        return end_cases > start_cases

    def total_cases(self, start_date: date, end_date: date) -> int:
        """A method that returns the total cases of the province/city
        for a certain range date and mutates total_cases.

        >>> ontario = Node("Ontario", 1000000)
        >>> d1 = date(2020, 3, 1)
        >>> ontario.add_case(d1, 5)
        >>> d2 = date(2020, 3, 2)
        >>> ontario.add_case(d2, 10)
        >>> d3 = date(2020, 3, 3)
        >>> ontario.add_case(d3, 7)
        >>> ontario.total_cases(d1, d3)
        22
        >>> ontario.total_cases(d1, d2)
        15

        """
        sum_cases = 0
        for item_date in self.cases.keys():
            if item_date >= start_date and item_date <= end_date:
                _, c = self.cases[item_date]
                sum_cases += c
        return sum_cases

    def get_cases(self) -> int:
        """ Return the total number of cases in this tree.
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


###############################################################################
# Data Computations
###############################################################################
@check_contracts
def create_provinces(root: Node) -> None:
    """ Create province nodes with their respective populations and add them as children of the
    given root node

    >>> root1 = Node("Canada", 0)
    >>> create_provinces(root1)
    >>> len(root1.children)
    13
    >>> root1.get_child("Ontario").population
    6746210
    >>> root1.get_child("Quebec").population
    4705910
    """
    # source: https://www.statista.com/statistics/446061/canada-single-population-by-province/
    province_pops = {'Ontario': 6746210,
                     'Quebec': 4705910,
                     'BC': 2313080,
                     'Alberta': 2076909,
                     'Manitoba': 681723,
                     'Saskatchewan': 566419,
                     'Nova Scotia': 450742,
                     'New Brunswick': 350480,
                     'NL': 214350,
                     'PEI': 76921,
                     'Nunavut': 29991,
                     'NWT': 28211,
                     'Yukon': 23819}

    for name, pop in province_pops.items():
        p = Node(name, pop)
        root.add_child(name, p)


def populate_canada_data(csv_file: str, root: Node) -> None:
    """Read the csv_file and create a tree with data of the COVID-19 cases for the provinces in Canada.

    >>> root1 = Node("Canada", 0)
    >>> create_provinces(root1)
    >>> test_csv = os.path.join("path", "to", "your", "test_csv_file.csv")
    >>> populate_canada_data(test_csv, root)
    >>> root1.get_child("Ontario").cases
    {datetime.date(2020, 3, 1): (5, 5), datetime.date(2020, 3, 2): (15, 10), ...}
    """

    df = pd.read_csv(csv_file)
    for row1 in df.iterrows():
        # row is a tuple
        row1 = row1[1]
        name = row1['province']
        d = row1['date_report']

        # figuring format of date in the csv file
        if d.find('-') != -1:
            # ex: '15-04-2020'
            fmt = '%d-%m-%Y'
        else:
            # ex: '13/5/20'
            fmt = '%d/%m/%y'

        d = datetime.strptime(d, fmt)

        cases = row1['cases']
        cases = int(cases)

        p = root.get_child(name)
        p.add_case(d, cases)


def populate_province_data_manitoba(province: Node, csv_file: str) -> None:
    """Create nodes for the cities (children) of the Manitoba Province node.

    >>> manitoba = Node("Manitoba", 681723)
    >>> test_csv = os.path.join("path", "to", "your", "test_csv_file.csv")
    >>> populate_province_data_manitoba(manitoba, test_csv)
    >>> manitoba.get_child("Winnipeg").cases
    {datetime.date(2020, 12, 30): (1000, 50), datetime.date(2020, 12, 31): (1050, 50), ...}
    """
    df = pd.read_csv(csv_file)
    for row in df.iterrows():
        # row is a tuple
        row = row[1]
        name = row['RHA']

        # some records do not represent a city so skip them
        if name == 'All':
            continue
        d = row['Date']

        # ex: '12/30/20'
        fmt = '%m/%d/%y'

        d = datetime.strptime(d, fmt)

        cases = row['Daily_Cases']
        cases = int(cases)

        p = province.get_or_create_child(name)
        p.add_case(d, cases)


def populate_province_data_saskatchewan(province: Node, csv_file: str) -> None:
    """Create nodes for the cities(children) of the Saskatchewan Province node.
    """
    df = pd.read_csv(csv_file)
    for row in df.iterrows():
        # row is a tuple
        row = row[1]
        name = row['Region']
        d = row['Date']

        # ex: '1/15/20'
        fmt = '%m/%d/%y'

        d = datetime.strptime(d, fmt)

        cases = row['New Cases']
        cases = int(cases)

        p = province.get_or_create_child(name)
        p.add_case(d, cases)


def populate_province_data_BC(province: Node, csv_file: str) -> None:
    """Create nodes for the cities(children) of the BC Province node.
    """
    df = pd.read_csv(csv_file)
    for row in df.iterrows():
        # row is a tuple
        row = row[1]
        name = row['HA']

        # some records do not represent a city so skip them
        if name == 'Out of Canada':
            continue
        d = row['Reported_Date']

        # ex: '12/30/20'
        fmt = '%m/%d/%y'

        d = datetime.strptime(d, fmt)

        p = province.get_or_create_child(name)
        p.add_case(d, 1)


###############################################################################
# Simulation
###############################################################################
# def read_all_provinces_csv(csv_file: str) -> list[list[str, datetime.date, int]]:
#     """Read the given csv fle."""
#     with open(csv_file, newline='') as csvfile:
#         reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
#         data = []
#         for row in reader:
#             data.append(', '.join(row))
#


# canada = Node('Canada', 0)
# create_provinces(canada)


def get_total_cases(tree: Node, province: str) -> int:
    """A function that gets the total population for a specified province.

    >>> root = Node('Canada', 0)
    >>> create_provinces(root)
    """
    return tree.get_child(province).get_cases()


###############################################################################
# Visualization
###############################################################################


# BELOW IS THE CODE THAT CORRECTLY WORKS TO PLACE MARKERS ON THE CANADA MAP
def map_canada_with_cases(root: Node, ) -> folium.Map():
    """A method that creates a map of Canada and displays the provinces' COVID-19 information.
    """
    canada_map = folium.Map(location=[56.13, -106.35], tiles="OpenStreetMap", zoom_start=3)

    data = pd.DataFrame({
        'lon': [53.9333, 53.7267, 53.7609, 46.5653, 53.1355, 64.8255, 44.6816, 66.1605, 51.2538, 46.5107, 46.8033,
                52.9399, 64.2823],
        'lat': [-116.5765, -127.6476, -98.8139, -66.4619, -57.6604, -124.8457, -63.7443, -153.3691, -85.3232, -63.4168,
                -71.1631, -106.4509, -135.0000],
        'name': ['Alberta', 'British Columbia', 'Manitoba', 'New Brunswick', 'Newfoundland and Labrador',
                 'Northwest Territories', 'Nova Scotia', 'Nunavut', 'Ontario', 'Prince Edward Island',
                 'Quebec', 'Saskatchewan', 'Yukon'],
        'cases': []
    })
    # figure out how to compute the cases for a given time for each province and add it to data

    for _, row in data.iterrows():
        folium.Marker([row['lon'], row['lat']], popup=row['name'] + ' ' + row['cases']).add_to(canada_map)
    return canada_map


# TREE VISUAL
def plot_tree(root: Node) -> ...:
    num_vertices = root.total_children()
    v_label = list(map(str, range(num_vertices)))
    graph = Graph.Tree(num_vertices, 13)  # 13 stands for number of provinces
    lay = graph.layout('rt')

    pos = {k: lay[k] for k in range(num_vertices)}  # originally stored in position (delete this comment after)
    y_values = [lay[k][1] for k in range(num_vertices)]
    max_y = max(y_values)  # originally stored in M (delete this comment after)

    es = EdgeSeq(graph)  # sequence of edges
    edges = [e.tuple for e in graph.es]  # list of edges

    len_pos = len(pos)  # originally stored in L (delete this comment after)
    x_n = [pos[k][0] for k in range(len_pos)]
    y_n = [2 * max_y - pos[k][1] for k in range(len_pos)]
    x_e = []
    y_e = []
    for edge in edges:
        x_e += [pos[edge[0]][0], pos[edge[1]][0], None]
        y_e += [2 * max_y - pos[edge[0]][1], 2 * max_y - pos[edge[1]][1], None]

    labels = v_label

    # plotting
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_e,
                             y=y_e,
                             mode='lines',
                             line=dict(color='rgb(210,210,210)', width=1),
                             hoverinfo='none'
                             ))
    fig.add_trace(go.Scatter(x=x_n,
                             y=y_n,
                             mode='markers',
                             name='bla',
                             marker=dict(symbol='circle-dot',
                                         size=18,
                                         color='#6175c1',  # '#DB4551',
                                         line=dict(color='rgb(50,50,50)', width=1)
                                         ),
                             text=labels,
                             hoverinfo='text',
                             opacity=0.8
                             ))

    # making annotations
    def make_annotations(pos, text, font_size=10, font_color='rgb(250,250,250)') -> list[
        dict[str, int | str | dict[str, str | int | bool]]]:
        """This method names the subtreets in the tree.
        """
        L = len(pos)

        if len(text) != L:
            raise ValueError('The lists pos and text must have the same len')

        names = []
        province = ['Ontario', 'Quebec', 'BC', 'Alberta', 'Manitoba', 'Saskatchewan', 'Nova Scotia', 'New Brunswick'
                                                                                                     'NL', 'PEI',
                    'Nunavut', 'NWT', 'Yukon']

        for k in range(L):
            names.append(
                dict(
                    text=province[k],  # or replace labels with a different list for the text within the circle
                    x=pos[k][0], y=2 * max_y - pos[k][1],
                    xref='x1', yref='y1',
                    font=dict(color=font_color, size=font_size),
                    showarrow=False)
            )

        return names

    # add axis specifications and create the layout
    axis = dict(showline=False,  # hide axis line, grid, ticklabels and  title
                zeroline=False,
                showgrid=False,
                showticklabels=False,
                )

    fig.update_layout(title='COVID-19 Spread in Canada During the 2020-2021 Holiday Season',
                      annotations=make_annotations(pos, v_label),
                      font_size=12,
                      showlegend=False,
                      xaxis=axis,
                      yaxis=axis,
                      margin=dict(l=40, r=40, b=85, t=100),
                      hovermode='closest',
                      plot_bgcolor='rgb(248,248,248)'
                      )
    fig.show()


# simple test to check if everything is working
def test() -> None:
    root = Node('Canada', 38_250_000)
    create_provinces(root)
    populate_canada_data('project/all_provinces_covid_data.csv', root)
    BC = root.get_child('BC')
    d1 = datetime.strptime('1/2/22', '%d/%m/%y')
    d2 = datetime.strptime('16-05-2022', '%d-%m-%Y')
    BC.get_avg_cases(d1)
    # 0.14163582755460252
    BC.get_avg_cases(d2)
    # 0.15967324952012035
    BC.num_cases_increased(d1, d2)
    # False
    BC.num_cases_increased(d2, d1)
    # True
    populate_province_data_manitoba(root.get_child('Manitoba'), 'project/manitoba_covid_data_2020-2021.csv')
    populate_province_data_saskatchewan(root.get_child('Saskatchewan'), 'project/saskatchewan_covid_data_2020-2021.csv')
    populate_province_data_BC(root.get_child('BC'), 'project/bc_covid_data_2020-2021.csv')


if __name__ == '__main__':
    # test()

    import doctest

    doctest.testmod(verbose=True)

    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (In PyCharm, select the lines below and press Ctrl/Cmd + / to toggle comments.)
    # You can use "Run file in Python Console" to run PythonTA,
    # and then also test your methods manually in the console.
    # import python_ta
    #
    # python_ta.check_all(config={
    #     'max-line-length': 120,
    # })
