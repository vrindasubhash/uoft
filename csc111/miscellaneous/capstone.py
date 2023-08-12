"""CSC111 Winter 2023: Final Project

Description
===============================

This module contains a collection of Python classes and functions that we used
represent a series of trees and graphs.

Copyright and Usage Information
===============================
This file is Copyright (c) 2023 Stefan Ateljevic, Veda Kesarwani, Sydelle Mago, and Vrinda Subhash.
"""

from python_ta.contracts import check_contracts
from typing import Any
import datetime
import csv
import pandas as pd
import folium


###############################################################################
# Classes and Functions
###############################################################################

@check_contracts
# class City:
#     """A class representing the COVID-19 data for the specified city.
#
#     Instance Attributes:
#     - city:
#         The name of the city.
#     - population:
#         The total population of the city.
#     - average_cases:
#         The average COVID-19 cases in the city for the indicated time period.
#     - cases:
#         A dictionary mapping the date to its corresponding number of cases that day.
#     """
#     city: str
#     population: int
#     average_cases: int
#     cases: dict[datetime.date, int]
#
#     def __init__(self, city: str, population: int, average_cases: int, cases: dict[datetime.date, int]) -> None:
#         """Initialize this tree with the given address and no connections to other nodes."""
#         self.city = city
#         self.population = population
#         self.average_cases = average_cases
#         self.cases = cases
#
#     def __repr__(self) -> str:
#         """Return a string representing this node.
#
#         __repr__ is a special method that's called when the object is evaluated in the Python console.
#         """
#         return f'City({self.city}, {self.population}, {self.average_cases}, {self.cases})'
#
#     def date_to_cases(self, date: datetime.date, cases: int) -> None:
#         """A mutating method that adds the date with its corresponding cases to self.cases.
#         >>> city_data = City("Example City", 100000, 50, {datetime.date(2022, 1, 1): 45})
#         >>> city_data.date_to_cases(datetime.date(2022, 1, 2), 55)
#         >>> city_data.cases
#         {datetime.date(2022, 1, 1): 45, datetime.date(2022, 1, 2): 55}
#         """
#
#         self.cases[date] = cases
#
#     def total_cases(self, date_range: [datetime.date, datetime.date]) -> int:
#         """A method that returns the total cases of the city for a certain range date.
#
#         If date_range[0] == date_range[1], then we are only counting the total cases of the city for a single day.
#         >>> city_data = City("Example City", 100000, 50, {
#         ...     datetime.date(2022, 1, 1): 45,
#         ...     datetime.date(2022, 1, 2): 55,
#         ...     datetime.date(2022, 1, 3): 60
#         ... })
#         >>> city_data.total_cases((datetime.date(2022, 1, 1), datetime.date(2022, 1, 2)))
#         100
#         >>> city_data.total_cases((datetime.date(2022, 1, 2), datetime.date(2022, 1, 3)))
#         115
#         >>> city_data.total_cases((datetime.date(2022, 1, 1), datetime.date(2022, 1, 3)))
#         160
#         >>> city_data.total_cases((datetime.date(2022, 1, 3), datetime.date(2022, 1, 3)))
#         60
#         """
#         total_cases = 0
#         for date in self.cases:
#             if date_range[0] <= date <= date_range[1]:
#                 total_cases += self.cases[date]
#         return total_cases
#
#     def average_case(self, date_range: [datetime.date, datetime.date]) -> None:
#         """A mutating method that mutates self.average_cases to equal the average cases during the given date range.
#
#         >>> city_data = City("Example City", 100000, 50, {
#         ...     datetime.date(2022, 1, 1): 45,
#         ...     datetime.date(2022, 1, 2): 55,
#         ...     datetime.date(2022,  1, 3): 60
#         ... })
#         >>> city_data.average_case((datetime.date(2022, 1, 1), datetime.date(2022, 1, 2)))
#         >>> city_data.average_cases
#         50
#
#         >>> city_data.average_case((datetime.date(2022, 1, 2), datetime.date(2022, 1, 3)))
#         >>> city_data.average_cases
#         57
#
#         >>> city_data.average_case((datetime.date(2022, 1, 1), datetime.date(2022, 1, 3)))
#         >>> city_data.average_cases
#         53
#
#         >>> city_data.average_case((datetime.date(2022, 1, 3), datetime.date(2022, 1, 3)))
#         >>> city_data.average_cases
#         60
#
#         """
#
#         total_cases = self.total_cases(date_range)
#         days = (date_range[1] - date_range[0]).days + 1
#         self.average_cases = total_cases // days
#
#     def get_population(self, date_range: [datetime.date, datetime.date], case_rate: float) -> None:
#         """A mutating method that mutates self.population to equal the population during the given date range.
#
#         The population is estimated based on the total cases and case rate provided.
#
#         >>> city_data = City("Example City", 100000, 50, {datetime.date(2022, 1, 1): 45,
#         ...     datetime.date(2022, 1, 2): 55,
#         ...     datetime.date(2022, 1, 3): 60})
#         >>> city_data.get_population((datetime.date(2022, 1, 1), datetime.date(2022, 1, 3)), 0.001)
#         >>> city_data.population
#         160000
#
#         >>> city_data.get_population((datetime.date(2022, 1, 2), datetime.date(2022, 1, 3)), 0.0005)
#         >>> city_data.population
#         230000
#         """
#         total_cases = self.total_cases(date_range)
#         self.population = int(total_cases / case_rate)
#

@check_contracts
class Province:
    """A province in the spread.

    Instance Attributes:
    - name:
        The name of the Province.
    - total_cases:
        The total cases in the city.
    """
    name: str
    total_cases: int
    neighbours: set[Province]

    def __init__(self, name: str, total_cases: int, neighbours: set[Province]) -> None:
        """Initialize this tree with the given address and no connections to other nodes."""
        self.name = name
        self.total_cases = total_cases
        self.neighbours = neighbours

    def __repr__(self) -> str:
        """Return a string representing this node.

        __repr__ is a special method that's called when the object is evaluated in the Python console.
        """
        return f'Province({self.province}, {self.capital}, {self.cities})'







@check_contracts
class Spread:
    """A graph that represents the provinces in Canada and the spread of the COVID-19 virus between different provinces.

    # Instance Attributes:
    # - provinces:
    #     A collections of the Provinces contained in this spread (Graph).
    """
    provinces: dict[str, Province]

    def __init__(self) -> None:
        """Initialize an empty spread (graph).
        """
        self.provinces = {}

    def __repr__(self) -> str:
        """Return a string representing this graph.

        __repr__ is a special method that's called when the object is evaluated in the Python console.
        """
        return f'Spread({self.provinces})'

    def add_province(self, name: str, num_cases: int) -> None:
        """Add a province to this spread.
        """
        self.provinces[name] = Province(name, num_cases, set())

    def add_edge(self, province1: str, province2: str) -> None:
        """Add a connection between two given boardering provinces in this spread.

         Precondition:
            - province1 != province2
         """
        if province1 in self.provinces and province2 in self.provinces:
            p1 = self.provinces[province1]
            p2 = self.provinces[province2]

            p1.neighbours.add(p2)
            p2.neighbours.add(p1)

        else:
            raise ValueError


###############################################################################
# Data Computations
###############################################################################
@check_contracts
def read_csv(csv_file: str) -> list[list[datetime.date, str, str]]:
    """Load a list of data of the COVID-19 cases and corresponding dates.

    Return a tuple of two values:
        - the first element is the network created from the specification in the first line
          of the CSV file
        - the second element is a list of tuples, where each tuple is of the form (timestamp, packet),
          created from all other lines of the CSV file

    Preconditions:
        - csv_file refers to a valid CSV file in the format described on the assignment handout

    >>> read_csv(...)
    [[datetime.date(2020, 9, 12), 'Resolved', 'London'],
     [datetime.date(2020, 9, 12), 'Resolved', 'Ottawa'],
     [datetime.date(2020, 6, 20), 'Resolved', 'Toronto']]

    # the cols we need from the data: province, date_report, cases, cumulative_cases
    # date format in the data set is dd-mm-yyyy
    """
    # covid_data = pd.read_csv(csv_file)
    # covid_data = covid_data.dropna()  # drops the null values in the data
    # covid_data = covid_data.drop(columns=['Row_ID', 'Accurate_Episode_Date', 'Test_Reported_Date', 'Specimen_Date',
    #                                       'Age_Group', 'Client_Gender', 'Case_AcquisitionInfo', 'Outbreak_Related',
    #                                       'Reporting_PHU_ID', 'Reporting_PHU_Address', 'Reporting_PHU_Postal_Code',
    #                                       'Reporting_PHU_Website', 'Reporting_PHU_Latitude',
    #                                       'Reporting_PHU_Longitude',
    #                                       'Reporting_PHU'],
    #                              axis=1)  # this removes all the columns that we are NOT interested in
    #
    # # converting the Case_Reported_Date column to a datetime.date object
    # covid_data['Case_Reported_Date'] = pd.to_datetime(covid_data['Case_Reported_Date'])
    # covid_data['Case_Reported_Date'] = covid_data['Case_Reported_Date'].dt.date
    #
    # # convert the pandas dataframe into our specified return type
    # # lst = covid_data.values
    # # updated_data = lst.tolist()
    # return updated_data

    # def read_all_provinces_csv(csv_file: str) -> list[list[str, datetime.date, int]]:


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

if __name__ == '__main__':
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
