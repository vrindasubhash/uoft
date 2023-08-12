"""CSC110 Tutorial 2: Functions, Logic, and Autocorrecting with Predicates (Exercise 1)

Module Description
==================
Write your functions for Exercise 1 in this file. Note that you're responsible
for the entire function design, following the steps of the Function Design Recipe.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC110 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC110 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2022 David Liu, Mario Badr, and Tom Fairgrieve.
"""

def average_string_len(strings: list) -> float:
    """Returns the average length of the strings in strings, or returns -1.0 if the list is empty.

    >>> average_string_len(['dogs', 'cats', 'byee'])
    4.0
    >>> average_string_len([])
    -1.0
    """
    if (strings == []):
        return -1.0

    lengths = [len(s) for s in strings]
    return sum(lengths)/len(strings)



if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
