############################################################
## CSC 384, Intro to AI, University of Toronto.
## Assignment 1 Starter Code
## v1.0
############################################################

from typing import List
import heapq
from heapq import heappush, heappop
import time
import argparse
import math # for infinity

from board import *

def is_goal(state):
    """
    Returns True if the state is the goal state and False otherwise.

    :param state: the current state.
    :type state: State
    :return: True or False
    :rtype: bool
    """
    
    return state.board.boxes == state.board.storage

def get_path(state):
    """
    Return a list of states containing the nodes on the path 
    from the initial state to the given state in order.

    :param state: The current state.
    :type state: State
    :return: The path.
    :rtype: List[State]
    """
    path = []

    # add all the states by going through their parents until you reach the initial state
    while state != None:
       path.append(state)
       state = state.parent

    # reverse the path to get in correct order; initial to current state
    path.reverse()

    return path


def get_successors(state):
    """
    Return a list containing the successor states of the given state.
    The states in the list may be in any arbitrary order.

    :param state: The current state.
    :type state: State
    :return: The list of successor states.
    :rtype: List[State]
    """
    successors = []
    moves = [(1, 0), (0, 1), (-1, 0), (0, -1)] # can potentially move right, up, left, or down
    robot_current_pos = state.board.robots[0] # assumes only one robot

    
    for move_x, move_y in moves:
        robot_new_pos = (robot_current_pos[0] + move_x, robot_current_pos[1] + move_y)
 
        # if the robot moves outside the boundaries of the board, move is invalid
        if not (0 <= robot_new_pos[0] < state.board.width and 0 <= robot_new_pos[1] < state.board.height):
            continue

        # if the robot would run into a wall, move is invalid
        if robot_new_pos in state.board.obstacles:
           continue
    
        # if the robot would be pushing a box
        if robot_new_pos in state.board.boxes: 
           box_new_pos = (robot_new_pos[0] + move_x, robot_new_pos[1] + move_y)
           
           # if the box would be moved outside the boundaries of the board, move is invalid
           if not (0 <= box_new_pos[0] < state.board.width and 0 <= box_new_pos[1] < state.board.height):
                continue

           # if the box would be pushed into a wall, or another box, move is invalid
           if box_new_pos in state.board.obstacles or box_new_pos in state.board.boxes:
              continue 
         
           # box can be moved into a valid spot
           box_positions = set(state.board.boxes) # change the locations of the boxes
           box_positions.remove(robot_new_pos)
           box_positions.add(box_new_pos)

           # make a new board with a successor state
           # condition: robot pushed box into valid spot 
           board_new = Board(state.board.name, state.board.width, state.board.height, [robot_new_pos], frozenset(box_positions), state.board.storage, state.board.obstacles)
        else:
           # make a new board with a successor state
           # condition: robot moved to a valid empty spot
           # box positions didn't change; robot didn't interact with a box
           board_new = Board(state.board.name, state.board.width, state.board.height, [robot_new_pos], state.board.boxes, state.board.storage, state.board.obstacles)


        # add new board state to successors
        successors.append(State(board_new, state.hfn, state.depth + 1, state))


    return successors


def dfs(init_board):
    """
    Run the DFS algorithm given an initial board.

    If the function finds a goal state, it returns a list of states representing
    the path from the initial state to the goal state in order and the cost of
    the solution found.
    Otherwise, it returns am empty list and -1.

    :param init_board: The initial board.
    :type init_board: Board
    :return: (the path to goal state, solution cost)
    :rtype: List[State], int
    """

    raise NotImplementedError


def a_star(init_board, hfn):
    """
    Run the A_star search algorithm given an initial board and a heuristic function.

    If the function finds a goal state, it returns a list of states representing
    the path from the initial state to the goal state in order and the cost of
    the solution found.
    Otherwise, it returns am empty list and -1.

    :param init_board: The initial starting board.
    :type init_board: Board
    :param hfn: The heuristic function.
    :type hfn: Heuristic (a function that consumes a Board and produces a numeric heuristic value)
    :return: (the path to goal state, solution cost)
    :rtype: List[State], int
    """

    raise NotImplementedError


def heuristic_basic(board):
    """
    Returns the heuristic value for the given board
    based on the Manhattan Distance Heuristic function.

    Returns the sum of the Manhattan distances between each box 
    and its closest storage point.

    :param board: The current board.
    :type board: Board
    :return: The heuristic value.
    :rtype: int
    """

    raise NotImplementedError


def heuristic_advanced(board):
    """
    An advanced heuristic of your own choosing and invention.

    :param board: The current board.
    :type board: Board
    :return: The heuristic value.
    :rtype: int
    """

    raise NotImplementedError


def solve_puzzle(board: Board, algorithm: str, hfn):
    """
    Solve the given puzzle using the given type of algorithm.

    :param algorithm: the search algorithm
    :type algorithm: str
    :param hfn: The heuristic function
    :type hfn: Optional[Heuristic]

    :return: the path from the initial state to the goal state
    :rtype: List[State]
    """

    print("Initial board")
    board.display()

    time_start = time.time()

    if algorithm == 'a_star':
        print("Executing A* search")
        path, step = a_star(board, hfn)
    elif algorithm == 'dfs':
        print("Executing DFS")
        path, step = dfs(board)
    else:
        raise NotImplementedError

    time_end = time.time()
    time_elapsed = time_end - time_start

    if not path:

        print('No solution for this puzzle')
        return []

    else:

        print('Goal state found: ')
        path[-1].board.display()

        print('Solution is: ')

        counter = 0
        while counter < len(path):
            print(counter + 1)
            path[counter].board.display()
            print()
            counter += 1

        print('Solution cost: {}'.format(step))
        print('Time taken: {:.2f}s'.format(time_elapsed))

        return path


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--inputfile",
        type=str,
        required=True,
        help="The file that contains the puzzle."
    )
    parser.add_argument(
        "--outputfile",
        type=str,
        required=True,
        help="The file that contains the solution to the puzzle."
    )
    parser.add_argument(
        "--algorithm",
        type=str,
        required=True,
        choices=['a_star', 'dfs'],
        help="The searching algorithm."
    )
    parser.add_argument(
        "--heuristic",
        type=str,
        required=False,
        default=None,
        choices=['zero', 'basic', 'advanced'],
        help="The heuristic used for any heuristic search."
    )
    args = parser.parse_args()

    # set the heuristic function
    heuristic = heuristic_zero
    if args.heuristic == 'basic':
        heuristic = heuristic_basic
    elif args.heuristic == 'advanced':
        heuristic = heuristic_advanced

    # read the boards from the file
    board = read_from_file(args.inputfile)

    # solve the puzzles
    path = solve_puzzle(board, args.algorithm, heuristic)

    # save solution in output file
    outputfile = open(args.outputfile, "w")
    counter = 1
    for state in path:
        print(counter, file=outputfile)
        print(state.board, file=outputfile)
        counter += 1
    outputfile.close()
