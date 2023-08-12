"""CSC111 Winter 2023 Prep 3: Programming Exercises

Instructions (READ THIS FIRST!)
===============================

This Python module contains a few functions that you should implement.
Each function represents a recursively-defined mathematical function,
corresponding to one in the starter file prep3_functions.pdf.
(You do not need to modify or submit prep3_functions.pdf, but you'll
need to read it to complete this programming exercise.)

We have marked each place you need to write code with the word "TODO".
As you complete your work in this file, delete each TODO comment.

TIP: the function definitions in the provided PDF file might seem daunting,
but this prep is actually just an exercise in translation between mathematical
expressions and Python code. Each of your functions in this file should look
very similar to the definitions in the PDF (and also very similar to the examples
of recursive Python functions in the Course Notes).

To test your work, we recommend calling each function in the Python console
using "small" input values (e.g., n = 0, n = 1), and manually calculating what
the expected return value should be based on the mathematical definition. Of course,
you can turn these checks into doctests for each function, though we are not grading
doctests for this prep.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2023 Mario Badr and David Liu.
"""
from python_ta.contracts import check_contracts


@check_contracts
def formula(n: int) -> float:
    """Return the value given by Definition 1 in prep3_functions.py.

    Preconditions:
        - n >= 0
    """
    if n == 0:
        return 4.0
    else:
        return formula(n - 1) + (4 * ((-1) ** n)) / (2 * n + 1)


@check_contracts
def formula_multiple_args(n: int, a: float, b: float) -> float:
    """Return the value given by Definition 2 in prep3_functions.py.

    Preconditions:
        - n >= 0
    """
    if n == 0:
        return 0.0
    else:
        return a * formula_multiple_args(n - 1, a, b) + b


def formula_double_recursion(n: int, m: int) -> int:
    """Return the value given by Definition 3 in prep3_functions.py.

    Preconditions:
        - n >= 0
        - m >= 0
    """
    if n == 0:
        return m
    elif m == 0:
        return 2 * formula_double_recursion(n - 1, n)
    else:
        return 3 + formula_double_recursion(n, m - 1)


@check_contracts
def create_list1(n: int) -> list[int]:
    """Return the value given by Definition 4 in prep3_functions.py.

    Preconditions:
        - n >= 0
    """
    if n == 0:
        return [0]
    else:
        return 2 * create_list1(n - 1) + [n]


@check_contracts
def create_list2(n: int, m: int) -> list:
    """Return the value given by Definition 5 in prep3_functions.py.

    Preconditions:
        - n >= 0
        - m >= 0

    TESTING NOTE: because this function makes two recursive calls instead of
    just one, it will be a lot slower than your other functions!
    We recommend testing your work with very small numbers, e.g. m, n <= 5.
    """
    if n == 0:
        return [m]
    elif m == 0:
        return [n]
    else:
        return [create_list2(n - 1, m), create_list2(n, m - 1)]


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)

    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (In PyCharm, select the lines below and press Ctrl/Cmd + / to toggle comments.)
    # You can use "Run file in Python Console" to run both pytest and PythonTA,
    # and then also test your methods manually in the console.
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 120
    })
