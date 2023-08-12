"""CSC111 Winter 2023: Final Project
Main that runs a simulation.
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
import folium
from igraph import Graph
import plotly.graph_objects as go
from node import Node
from data_computations import create_provinces, populate_canada_data, populate_province_data_manitoba,\
    populate_province_data_saska, populate_province_data_bc
from visualization import map_canada_with_cases, plot_tree

###############################################################################
# Simulation
###############################################################################

def main() -> None:
    """
    Before running this simulation, make sure 'datasets' has been downloaded from the zip file.
    """
    canada = Node('Canada', 38_250_000)
    create_provinces(canada)
    print("Loading province data, it may take a few seconds.")
    populate_canada_data('datasets/all_provinces_covid_data.csv', canada)
    print("Loading Manitoba data, it may take a few seconds.")
    populate_province_data_manitoba(canada.get_child('Manitoba'), 'datasets/manitoba_covid_data_2020-2021.csv')
    print("Loading Saskatchewan data, it may take a few seconds.")
    populate_province_data_saska(canada.get_child('Saskatchewan'), 'datasets/saskatchewan_covid_data_2020-2021.csv')
    print("Loading BC data, it may take a few seconds (the biggest data set). It takes awhile, please dont kill.")
    populate_province_data_bc(canada.get_child('BC'), 'datasets/bc_covid_data_2020-2021.csv')
    print("Finished loading all data. Tree is created.")
    print("The map could be seen under the file name canada-covid-cases.html (in your folder for this project).")
    map_canada_with_cases(canada)
    plot_tree(canada)


if __name__ == '__main__':
    main()

    import doctest

    doctest.testmod(verbose=True)

    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (In PyCharm, select the lines below and press Ctrl/Cmd + / to toggle comments.)
    # You can use "Run file in Python Console" to run PythonTA,
    # and then also test your methods manually in the console.
    # import python_ta
    #
    # python_ta.check_all(config={
    #     'extra-imports': ['datetime', 'csv', 'plotly.graph_objects', 'pandas', 'folium', 'igraph', 'plotly', 'node',
    #                       'data_computations', 'visualization'],
    #     'allowed-io': ['main', 'populate_province_data_bc', 'read_all_provinces_csv'],
    #     'max-line-length': 120
    # })
