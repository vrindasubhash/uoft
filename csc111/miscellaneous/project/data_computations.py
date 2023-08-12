"""CSC111 Winter 2023: Final Project
The data computations that create the tree and reading the csv files.
===============================
This module contains a collection of Python classes and functions that we used
represent a series of trees and graphs.
Copyright and Usage Information
===============================
This file is Copyright (c) 2023 Stefan Ateljevic, Veda Kesarwani, Sydelle Mago, and Vrinda Subhash.
"""
from __future__ import annotations

import csv
from datetime import date, datetime
from python_ta.contracts import check_contracts
import pandas as pd
# import folium
# from igraph import Graph
# import plotly.graph_objects as go
from node import Node

###############################################################################
# Data Computations
###############################################################################
# @check_contracts
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


def populate_province_data_saska(province: Node, csv_file: str) -> None:
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


def populate_province_data_bc(province: Node, csv_file: str) -> None:
    """Create nodes for the cities(children) of the BC Province node.
    """
    c = 0

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
        c += 1
        if c % 500 == 0:
            print(".", end='')


###############################################################################
# Reading the CSV file
###############################################################################

def read_all_provinces_csv(csv_file: str) -> list[list[str, datetime.date, int]]:
    """Read the given csv fle.
    Returns a list of lists, where each inner list contains:
        - the province name
        - a date in datetime format
        - the number of COVID cases on that date for that province
    """
    with open(csv_file, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        data = []

        for row in reader:
            province, date_str, cases_str, cumulative_cases_str = row

            if date_str.find('-') != -1:
                # ex: '15-04-2020'
                fmt = '%d-%m-%Y'
            else:
                # ex: '13/5/20'
                fmt = '%d/%m/%y'

            date_stripped = datetime.strptime(date_str, fmt).date()
            cases = int(cases_str)
            cumulative_cases = int(cumulative_cases_str)
            data.append([province, date_stripped, cases, cumulative_cases])

    return data


def get_total_cases(root: Node, province: str) -> int:
    """A function that gets the total cases for a specified province.
    """
    total_cases = 0

    for prov in root.children:
        if province == prov:
            province_data = root.children[prov].cases

            if province_data is not None:
                cases = list(province_data.values())

                for tup in cases:
                    total_cases += tup[1]

            else:
                total_cases = 0

    return total_cases
