############################################################
## CSC 384, Intro to AI, University of Toronto.
## Assignment 3 Starter Code
## v1.1
##
## Changes:
## - create_dot_constraints: 
##      Each dot constraint name must start with BlackDot or WhiteDot
## - create_no_dot_constraints:
##      Each no dot constraint name must start with NoDot
############################################################

from board import *
from cspbase import *

def kropki_model(board):
    """
    Create a CSP for a Kropki Sudoku Puzzle given a board of dimension.

    If a variable has an initial value, its domain should only contain the initial value.
    Otherwise, the variable's domain should contain all possible values (1 to dimension).

    We will encode all the constraints as binary constraints.
    Each constraint is represented by a list of tuples, representing the values that
    satisfy this constraint. (This is the table representation taught in lecture.)

    Remember that a Kropki sudoku has the following constraints.
    - Row constraint: every two cells in a row must have different values.
    - Column constraint: every two cells in a column must have different values.
    - Cage constraint: every two cells in a 2x3 cage (for 6x6 puzzle) 
            or 3x3 cage (for 9x9 puzzle) must have different values.
    - Black dot constraints: one value is twice the other value.
    - White dot constraints: the two values are consecutive (differ by 1).

    Make sure that you return a 2D list of variables separately. 
    Once the CSP is solved, we will use this list of variables to populate the solved board.
    Take a look at csprun.py for the expected format of this 2D list.

    :returns: A CSP object and a list of variables.
    :rtype: CSP, List[List[Variable]]

    """
    dim = board.dimension
    csp = CSP("Kropki Sudoku")

    # create variables with initial values as domains
    variables = []
    for row in range(dim):
        row_vars = []
        for col in range(dim):
            cell_value = board.cells[row][col]
            domain = [cell_value] if cell_value != 0 else list(range(1, dim + 1))
            var = Variable(f"Var({row},{col})", domain)
            row_vars.append(var)
            csp.add_var(var)
        variables.append(row_vars)

    # create tuples for constraints
    diff_tuples = satisfying_tuples_difference_constraints(dim)
    white_tuples = satisfying_tuples_white_dots(dim)
    black_tuples = satisfying_tuples_black_dots(dim)
    no_dot_tuples = satisfying_tuples_no_dots(dim)

    # add row and column constraints
    for constraint in create_row_and_col_constraints(dim, diff_tuples, variables):
        csp.add_constraint(constraint)

    # add cage constraints
    for constraint in create_cage_constraints(dim, diff_tuples, variables):
        csp.add_constraint(constraint)

    # add dot constraints (white and black)
    for constraint in create_dot_constraints(dim, board.dots, white_tuples, black_tuples, variables):
        csp.add_constraint(constraint)

    # add no dot constraints
    for constraint in create_no_dot_constraints(dim, board.dots, no_dot_tuples, variables):
        csp.add_constraint(constraint)

    return csp



def create_variables(dim, board):
    """
    Return a list of variables for the board, and initialize their domain appropriately.

    We recommend that your name each variable Var(row, col).

    :param dim: Size of the board
    :type dim: int

    :returns: A list of variables with an initial domain, one for each cell on the board
    :rtype: List[Variables]
    """
    variables = []
    for row in range(dim):
        for col in range(dim):
            if board.cells[row][col] != 0:
                # cell already has a value, domain is just that value
                domain = [board.cells[row][col]]
            else:
                # cell is empty, domain includes all possible values (1 to dim)
                domain = list(range(1, dim + 1))

            var = Variable(f"Var({row}, {col})", domain)
            variables.append(var)  # flatten into single list
    return variables

    
def satisfying_tuples_difference_constraints(dim):
    """
    Return a list of satifying tuples for binary difference constraints.

    :param dim: Size of the board
    :type dim: int

    :returns: A list of satifying tuples
    :rtype: List[(int,int)]
    """
    satisfying_tuples = []
    for i in range(1, dim + 1):
        for j in range(1, dim + 1):
            if i != j:
                satisfying_tuples.append((i, j))
    return satisfying_tuples



def satisfying_tuples_white_dots(dim):
    """
    Return a list of satifying tuples for white dot constraints.

    :param dim: Size of the board
    :type dim: int

    :returns: A list of satifying tuples
    :rtype: List[(int,int)]
    """
    satisfying_tuples = []
    for i in range(1, dim + 1):
        for j in range(1, dim + 1):
            if abs(i - j) == 1:  # i and j are consecutive
                satisfying_tuples.append((i, j))
    return satisfying_tuples




def satisfying_tuples_black_dots(dim):
    """
    Return a list of satifying tuples for black dot constraints.

    :param dim: Size of the board
    :type dim: int

    :returns: A list of satifying tuples
    :rtype: List[(int,int)]
    """
    satisfying_tuples = []
    for i in range(1, dim + 1):
        for j in range(1, dim + 1):
            if i == 2 * j or j == 2 * i:  # one value is twice the other
                satisfying_tuples.append((i, j))
    return satisfying_tuples



def create_row_and_col_constraints(dim, sat_tuples, variables):
    """
    Create and return a list of binary all-different row/column constraints.

    :param dim: Size of the board
    :type dim: int

    :param sat_tuples: A list of domain value pairs (value1, value2) such that 
        the two values in each tuple are different.
    :type sat_tuples: List[(int, int)]

    :param variables: A list of all the variables in the CSP
    :type variables: List[Variable]
        
    :returns: A list of binary all-different constraints
    :rtype: List[Constraint]
    """
    constraints = []

    # row constraints
    for row in range(dim):
        for col1 in range(dim):
            for col2 in range(col1 + 1, dim):
                var1 = variables[row][col1]
                var2 = variables[row][col2]

                # add each satisfying tuple to the constraint
                constraint = Constraint(f"Row-{row}-({col1},{col2})", [var1, var2])
                for tup in sat_tuples:
                    constraint.sat_tuples[tuple(tup)] = True
                constraints.append(constraint)

    # column constraints
    for col in range(dim):
        for row1 in range(dim):
            for row2 in range(row1 + 1, dim):
                var1 = variables[row1][col]
                var2 = variables[row2][col]

                # add each satisfying tuple to the constraint
                constraint = Constraint(f"Col-{col}-({row1},{row2})", [var1, var2])
                for tup in sat_tuples:
                    constraint.sat_tuples[tuple(tup)] = True
                constraints.append(constraint)


    return constraints
   


def create_cage_constraints(dim, sat_tuples, variables):
    """
    Create and return a list of binary all-different constraints for all cages.

    :param dim: Size of the board
    :type dim: int

    :param sat_tuples: A list of domain value pairs (value1, value2) such that 
        the two values in each tuple are different.
    :type sat_tuples: List[(int, int)]

    :param variables: A list of all the variables in the CSP
    :type variables: List[Variable]
        
    :returns: A list of binary all-different constraints
    :rtype: List[Constraint]
    """
    constraints = []

    # find cage size based on dimensions
    if dim == 6:
        cage_rows, cage_cols = 3, 2
    elif dim == 9:
        cage_rows, cage_cols = 3, 3
    else:
        raise ValueError("Invalid board dimension for cage constraints")

    # iterate over each cage
    for row_start in range(0, dim, cage_rows):
        for col_start in range(0, dim, cage_cols):
            # get the variables in the current cage
            cage_vars = []
            for r in range(row_start, row_start + cage_rows):
                for c in range(col_start, col_start + cage_cols):
                    cage_vars.append(variables[r][c])

            # make binary constraints for each unique pair in the cage
            for i in range(len(cage_vars)):
                for j in range(i + 1, len(cage_vars)):
                    var1 = cage_vars[i]
                    var2 = cage_vars[j]
                    constraint = Constraint(f"Cage-({row_start},{col_start})-({i},{j})", [var1, var2])

                    # add each satisfying tuple to the constraint
                    constraint.add_satisfying_tuples(sat_tuples)
                    constraints.append(constraint) 

    return constraints

    
def create_dot_constraints(dim, dots, white_tuples, black_tuples, variables):
    """
    Create and return a list of binary constraints, one for each dot.
 
    Note: the name of each black/white dot constraint must start with "BlackDot" or "WhiteDot".
    We recommend that you use the following naming convention.
    - For white dots: WhiteDot({},{})
    - For black dots: BlackDot({},{})

    :param dim: Size of the board
    :type dim: int
    
    :param dots: A list of dots, each dot is a Dot object.
    :type dots: List[Dot]

    :param white_tuples: A list of domain value pairs (value1, value2) such that 
        the two values in each tuple satisfy the white dot constraint.
    :type white_tuples: List[(int, int)]
    
    :param black_tuples: A list of domain value pairs (value1, value2) such that 
        the two values in each tuple satisfy the black dot constraint.
    :type black_tuples: List[(int, int)]

    :param variables: A list of all the variables in the CSP
    :type variables: List[Variable]
        
    :returns: A list of binary dot constraints
    :rtype: List[Constraint]
    """
    constraints = []

    for dot in dots:
        # get variables connected by the dot
        var1 = variables[dot.cell_row][dot.cell_col]
        var2 = variables[dot.cell2_row][dot.cell2_col]
   
        # decide the type of constraint by color of the dot
        if dot.color == CHAR_WHITE:
            # white dot constraint
            constraint = Constraint(f"WhiteDot({dot.cell_row},{dot.cell_col})", [var1, var2])
            constraint.add_satisfying_tuples(white_tuples)
        elif dot.color == CHAR_BLACK:
            # black dot constraint
            constraint = Constraint(f"BlackDot({dot.cell_row},{dot.cell_col})", [var1, var2])
            constraint.add_satisfying_tuples(black_tuples)
        else:
            continue  # skip if color is not white or black

        constraints.append(constraint)

    return constraints



def satisfying_tuples_no_dots(dim):
    """
    Return a list of satifying tuples for no dot constraints.

    :param dim: Size of the board
    :type dim: int

    :returns: A list of satifying tuples
    :rtype: List[(int,int)]
    """
    satisfying_tuples = []
    for i in range(1, dim + 1):
        for j in range(1, dim + 1):
            # Check that the pair does not satisfy white dot or black dot constraints
            if i != j and abs(i - j) != 1 and i != 2 * j and j != 2 * i:
                satisfying_tuples.append((i, j))
    return satisfying_tuples



def create_no_dot_constraints(dim, dots, no_dot_tuples, variables):
    """
    Create and return a list of binary constraints, one for each dot.

    Note: the name of each no-dot constraint must start with "NoDot"
    We recommend that you use the following naming convention.
    - NoDot({},{})

    :param dim: Size of the board
    :type dim: int
    
    :param dots: A list of dots, each dot is a Dot object.
    :type dots: List[Dot]
 
    :param no_dot_tuples: A list of domain value pairs (value1, value2) such that 
        the two values in each tuple satisfy the no dot constraint.
    :type no_dot_tuples: List[(int, int)]

    :param variables: A list of all the variables in the CSP
    :type variables: List[Variable]
        
    :returns: A list of binary no dot constraints
    :rtype: List[Constraint]
    """
    constraints = []

    # create set of cell pairs that have a dot constraint between them
    dot_pairs = set()
    for dot in dots:
        dot_pairs.add((dot.cell_row, dot.cell_col, dot.cell2_row, dot.cell2_col))
        dot_pairs.add((dot.cell2_row, dot.cell2_col, dot.cell_row, dot.cell_col))  # also add reverse for easier lookup

    # check all horizontal and vertical neighbors for "no dot" constraints
    for row in range(dim):
        for col in range(dim):
            # horizontal neighbor to the right
            if col + 1 < dim and (row, col, row, col + 1) not in dot_pairs:
                var1 = variables[row][col]
                var2 = variables[row][col + 1]
                constraint = Constraint(f"NoDot({row},{col})-({row},{col + 1})", [var1, var2])
                constraint.add_satisfying_tuples(no_dot_tuples)
                constraints.append(constraint)

            # vertical neighbor below
            if row + 1 < dim and (row, col, row + 1, col) not in dot_pairs:
                var1 = variables[row][col]
                var2 = variables[row + 1][col]
                constraint = Constraint(f"NoDot({row},{col})-({row + 1},{col})", [var1, var2])
                constraint.add_satisfying_tuples(no_dot_tuples)
                constraints.append(constraint)

    return constraints

