"""CSC110 Tutorial 2: Functions, Logic, and Autocorrecting with Predicates (Exercise 4)

Module Description
==================
This module contains Python code with various logical and/or code style issues
that are checked by PythonTA. We have also provided code at the bottom of this
file that runs PythonTA to check the file and report issues.

To complete these exercise, please follow these three steps:

1. Scroll down to the main block at the bottom of this file and read the code
   that imports and runs PythonTA.
2. Run this file (right-click -> Run File in Python Console).
3. You should see your web browser open a webpage with a report from PythonTA.
   Read through this report to see what kinds of checks PythonTA made.
4. Modify this file to fix all of the issues reported by PythonTA.
   TIP: In PyCharm, press Ctrl/Cmd + A to select the contents of this file,
   and then go to the menu action Code -> Reformat Code. This will fix many of
   the style errors reported by PythonTA, though there will be other errors
   that you have to fix manually.
5. Re-run this file, which should display another PythonTA report.
6. Repeat steps 4-5 until here are no more errors reported!

This is the same process you'll follow to check your work with PythonTA for
the weekly prep programming exercises and assignments. If you aren't sure about
what an error means, you can click on the "Learn More" link next to the error
message to be taken to the PythonTA documentation website for more information.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC110 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC110 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2022 David Liu, Mario Badr, and Tom Fairgrieve.
"""


def my_function(x: int, y: int) -> int:
    """Return the sum of x and y.

    >>>  my_function(10, 20)
    30
    """
    return x + y


def has_blue(colours: list) -> bool:
    '''Return whether the given colours list contains the colour [0, 0, 255].

    '''
    if [0, 0, 255] in colours:
        return True
    else:
        return False


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 120
    })
