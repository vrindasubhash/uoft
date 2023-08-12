"""CSC110 Tutorial 4: Data Classes and For Loops, Exercise 1

Module Description
==================
This module contains the data classes and functions you should complete for Exercise 1.
Note that this file is very similar to tutorial3_part4.py from last week, so you should
have that file open while you're working on this exercise.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC110 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC110 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2022 David Liu, Mario Badr, and Tom Fairgrieve.
"""
import csv
from dataclasses import dataclass
import datetime

from python_ta.contracts import check_contracts


###############################################################################
# The new data class
###############################################################################
@check_contracts
@dataclass
class Delay:
    """A data type representing a specific subway delay instance.

    This corresponds to one row of the tabular data found in ttc-subway-delays.csv.

    Attributes:
        - Date: The date of the delay
        - Time: The time of the delay
        - Day: The day of the week on which the delay occurred.
        - Station: The name of the subway station where the delay occurred.
        - Code: The TTC delay code, which usually describes the cause of the delay. You can find a table showing the
                codes and descriptions in ttc-subway-delay-codes.csv.
        - Min_Delay: The length of the subway delay (in minutes).
        - Min_Gap: The length of time between subway trains (in minutes).
        - Bound: The direction in which the train was travelling. This is dependent on the line the train was on.
        - Line: The abbreviated name of the subway line where the delay occurred.
        - Vehicle: The id number of the train on which the delay occurred.

    Representation invariants:
        - Day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    """
    Date: datetime.date
    Time: datetime.time
    Day: str
    Station: str
    Code: str
    Min_Delay: int
    Min_Gap: int
    Bound: str
    Line: str
    Vehicle: int


@check_contracts
def read_csv_file(filename: str) -> tuple[list[str], list[Delay]]:
    """Return the headers and data stored in a csv file with the given filename.

    The return value is a tuple consisting of two elements:

    - The first is a list of strings for the headers of the csv file.
    - The second is a list of Delays (using the data class you just defined).

    Preconditions:
      - filename refers to a valid csv file with headers
        (notice that we can't express this as a Python expression)

    HINT: you can reuse almost exactly the same code as your tutorial3_part4.py from
    last week. We didn't write this code for you here because we want to you take a
    moment to review that code and copy it here yourself.
    """


@check_contracts
def process_row(row: list[str]) -> Delay:
    """Convert a row of subway delay data to Delay object.

    Notes:
    - This function is very similar to the process_row function from tutorial3_part4.py,
      except now you're returning a Delay object instead of list.

    Preconditions:
        - row has the correct format for the TTC subway delay data set
    """


###############################################################################
# From nested lists to data classes
###############################################################################
@check_contracts
def longest_delay_v1(data: list[Delay]) -> int:
    """Return the longest delay in the given data.

    Preconditions:
        - data != []
    """


@check_contracts
def average_delay_v1(data: list[Delay]) -> float:
    """Return the average subway delay in data.

    Preconditions:
        - data != []
    """


@check_contracts
def num_delays_by_month_v1(data: list[Delay], year: int, month: int) -> int:
    """Return the number of delays that occurred in the given month and year.

    Preconditions:
        - 0 <= month < 12
        - 2014 <= year <= 2018

    Hint: given a datetime.date value my_date, you can access three instance attributes
    to obtain the year, month, and day of the date.

        >>> my_date = datetime.date(2022, 10, 7)
        >>> my_date.year
        2022
        >>> my_date.month
        10
        >>> my_date.day
        7
    """


###############################################################################
# From comprehensions to loops
###############################################################################
@check_contracts
def longest_delay_v2(data: list[Delay]) -> int:
    """Return the longest delay in the given data.

    Preconditions:
        - data != []
    """


@check_contracts
def average_delay_v2(data: list[Delay]) -> float:
    """Return the average subway delay in data.

    Preconditions:
        - data != []
    """


@check_contracts
def num_delays_by_month_v2(data: list[Delay], year: int, month: int) -> int:
    """Return the number of delays that occurred in the given month and year.

    Preconditions:
    - 0 <= month < 12
    - 2014 <= year <= 2018
    """


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
