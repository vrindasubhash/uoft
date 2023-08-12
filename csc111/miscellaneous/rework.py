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
from python_ta.contracts import check_contracts
from typing import Any
from datetime import date, datetime
import csv
import pandas as pd
import folium


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
    """
    name: str
    population: int
    cumulative_cases: int
    cases: dict[date, (int, int)]
    children: dict[str, Node]

    def __init__(self, name: str, population: int) -> None:
        """Initialize this tree with the given address and no connections to other nodes."""
        self.name = name
        self.population = population
        self.cumulative_cases = 0
        self.cases = {}
        self.children = {}

    def __repr__(self) -> str:
        """Return a string representing this node.

        __repr__ is a special method that's called when the object is evaluated in the Python console.
        """
        # TODO fix recursively
        return f'Node({self.name})'

    def add_child(self, name: str, node: Node) -> None:
        self.children[name] = node

    def get_child(self, name: str) -> Node:
        return self.children[name]

    def get_or_create_child(self, name: str) -> Node:
        if name not in self.children:
            self.children[name] = Node(name, -1)
        return self.children[name]

    def add_case(self, d: date, cases: int) -> None:
        """Updates the province/city cases for the given date.
        """
        self.cumulative_cases += cases
        if d in self.cases:
            _, c = self.cases[d]
            cases += c
        self.cases[d] = (self.cumulative_cases, cases)


    def get_avg_cases(self, d: date) -> float:
        """Return the average number of COVID-19 cases in this province/city by date.
        """
        cumulative, _ = self.cases[d]
        return cumulative/self.population

    def num_cases_increased(self, start_date: date, end_date: date) -> bool:
        """
        For this province/city, return whether the number of new cases has increased between the start date
        and end date.

        This just considers the start and end date, doesn't consider days in between.
        """
        _, start_cases = self.cases[start_date]
        _, end_cases = self.cases[end_date]

        return end_cases > start_cases


    def total_cases(self, start_date: date, end_date: date) -> int:
        """A method that returns the total cases of the province/city for a certain range date and mutates total_cases."""
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
    """Load a list of data of the COVID-19 cases per province and corresponding dates.

    Return a tuple of two values:
        - the first element is the network created from the specification in the first line
          of the CSV file
        - the second element is a list of tuples, where each tuple is of the form (timestamp, packet),
          created from all other lines of the CSV file

    Preconditions:
        - csv_file refers to a valid CSV file in the format described on the assignment handout

    # the cols we need from the data: province, date_report, cases, cumulative_cases
    # date format in the data set is dd-mm-yyyy
    """

    df = pd.read_csv(csv_file)
    for row in df.iterrows():
        # row is a tuple
        row = row[1]
        name = row['province']
        d = row['date_report']

        # figuring format of date in the csv file
        if d.find('-') != -1:
            # ex: '15-04-2020'
            fmt = '%d-%m-%Y'
        else:
            # ex: '13/5/20'
            fmt = '%d/%m/%y'

        d = datetime.strptime(d, fmt)

        cases = row['cases']
        cases = int(cases)

        p = root.get_child(name)
        p.add_case(d, cases)


def populate_province_data_manitoba(province: Node, csv_file: str) -> None:
    df = pd.read_csv(csv_file)
    for row in df.iterrows():
        # row is a tuple
        row = row[1]
        name = row['RHA']

        #some records do not represent a city so skip them
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
# Visualization
###############################################################################

m = folium.Map(location=[56.13, -106.35], tiles="OpenStreetMap", zoom_start=3)

data = pd.DataFrame({
    'lon': [53.93, 53.73, 53.76, 46.56, 53.13, 64.82, 44.69, 70.30, 51.25, 46.51, 46.81, 52.94, 64.28],
    'lat': [-116.58, -127.65, -98.81, -66.46, -57.66, -124.85, -62.66, -83.11, -85.32, -63.42, -71.21, -106.45, -135],
    'name': ['Alberta', 'British Columbia', 'Manitoba', 'New Brunswick', 'Newfoundland and Labrador',
             'Northwest Territories', 'Nova Scotia', 'Nunavut', 'Ontario', 'Prince Edward Island',
             'Quebec', 'Saskatchewan', 'Yukon'],
    'value': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
}, dtype=str)

for i in range(0, len(data)):
    folium.Marker(
        location=[data.iloc[i]['lat'], data.iloc[i]['lon']],
        popup=data.iloc[i]['name'],
        icon=folium.DivIcon(
            html=f"""<div style="font-family: courier new; color: black">{data.iloc[i]['name']}</div>""")
    ).add_to(m)

for i in range(0, len(data)):
    folium.Circle(
        location=(data.iloc[i]['lat'], data.iloc[i]['lon']),
        popup=data.iloc[i]['name'],
        radius=float(data.iloc[i]['value']) * 20000,
        color='crimson',
        fill=True,
        fill_color='crimson'
    ).add_to(m)

m.save("covid-canada-spread.html")


#simple test to check if everything is working
def test() -> None:
    canada = Node('Canada', 38_250_000)
    create_provinces(canada)
    populate_canada_data('project/all_provinces_covid_data.csv', canada)
    BC = canada.get_child('BC')
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
    populate_province_data_manitoba(canada.get_child('Manitoba'), 'project/manitoba_covid_data_2020-2021.csv')
    populate_province_data_saskatchewan(canada.get_child('Saskatchewan'),
                                        'project/saskatchewan_covid_data_2020-2021.csv')
    populate_province_data_BC(canada.get_child('BC'), 'project/bc_covid_data_2020-2021.csv')



if __name__ == '__main__':
    #test()

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
