###############################################################################
# This file implements various minimax search agents.
#
# CSC 384 Assignment 2 Starter Code
# version 2.0
###############################################################################
from wrapt_timeout_decorator import timeout

from mancala_game import play_move
from utils import *

def minimax_max_basic(board, curr_player, heuristic_func):
    """
    Perform Minimax Search for MAX player.
    Return the best move and its minimax value.
    If the board is a terminal state, return None as its best move.

    :param board: the current board
    :param curr_player: the current player
    :param heuristic_func: the heuristic function
    :return the best move and its minimax value according to minimax search.
    """
    # check if current board state is a terminal state
    if not board.get_possible_moves(curr_player):
       max_utility = heuristic_func(board, curr_player)
       return None, max_utility

    # initialize best move and best value for a MAX player
    best_move = None
    best_value = float('-inf')

    # iterate over all the possible moves for the MAX player
    for move in board.get_possible_moves(curr_player):
        next_state = play_move(board, curr_player, move)

        _, value = minimax_min_basic(next_state, get_opponent(curr_player), heuristic_func)

        if value > best_value:
            best_move = move
            best_value = value

    return best_move, best_value


def minimax_min_basic(board, curr_player, heuristic_func):
    """
    Perform Minimax Search for MIN player.
    Return the best move and its minimax value.
    If the board is a terminal state, return None as its best move.

    :param board: the current board
    :param curr_player: the ccurrent player
    :param heuristic_func: the heuristic function
    :return the best move and its minimax value according to minimax search.
    """
    if not board.get_possible_moves(curr_player):
        max_utility = heuristic_func(board, get_opponent(curr_player))
        return None, max_utility

    best_move = None
    best_value = float('inf')


    # iterate over all the possible moves for the MAX player
    for move in board.get_possible_moves(curr_player):
        next_state = play_move(board, curr_player, move)

        _, value = minimax_max_basic(next_state, get_opponent(curr_player), heuristic_func)

        if value < best_value:
            best_move = move
            best_value = value

    return best_move, best_value


def minimax_max_limit(board, curr_player, heuristic_func, depth_limit):
    """
    Perform Minimax Search for MAX player up to the given depth limit.
    Return the best move and its estimated minimax value.
    If the board is a terminal state, return None as its best move.

    :param board: the current board
    :param curr_player: the current player
    :param heuristic_func: the heuristic function
    :param depth_limit: the depth limit
    :return the best move and its minimmax value estimated by our heuristic function.
    """
    # check if current board state is a terminal state or depth limit was reached
    if not board.get_possible_moves(curr_player) or depth_limit == 0:
       max_utility = heuristic_func(board, curr_player)
       return None, max_utility

    # initialize best move and best value for a MAX player
    best_move = None
    best_value = float('-inf')

    # iterate over all the possible moves for the MAX player
    for move in board.get_possible_moves(curr_player):
        next_state = play_move(board, curr_player, move)

        _, value = minimax_min_limit(next_state, get_opponent(curr_player), heuristic_func, depth_limit - 1)

        if value > best_value:
            best_move = move
            best_value = value

    return best_move, best_value


def minimax_min_limit(board, curr_player, heuristic_func, depth_limit):
    """
    Perform Minimax Search for MIN player  up to the given depth limit.
    Return the best move and its estimated minimax value.
    If the board is a terminal state, return None as its best move.

    :param board: the current board
    :param curr_player: the ccurrent player
    :param heuristic_func: the heuristic function
    :param depth_limit: the depth limit
    :return the best move and its minimmax value estimated by our heuristic function.
    """
    if not board.get_possible_moves(curr_player) or depth_limit == 0:
        max_utility = heuristic_func(board, get_opponent(curr_player))
        return None, max_utility

    best_move = None
    best_value = float('inf')


    # iterate over all the possible moves for the MAX player
    for move in board.get_possible_moves(curr_player):
        next_state = play_move(board, curr_player, move)

        _, value = minimax_max_limit(next_state, get_opponent(curr_player), heuristic_func, depth_limit - 1)

        if value < best_value:
            best_move = move
            best_value = value

    return best_move, best_value


def minimax_max_limit_opt(board, curr_player, heuristic_func, depth_limit, optimizations):
    """
    Perform Minimax Search for MAX player up to the given depth limit with the option of caching states.
    Return the best move and its minimmax value estimated by our heuristic function.
    If the board is a terminal state, return None as its best move.

    :param board: the current board
    :param curr_player: the ccurrent player
    :param heuristic_func: the heuristic function
    :param depth_limit: the depth limit
    :param optimizations: a dictionary to contain any data structures for optimizations.
        You can use a dictionary called "cache" to implement caching.
    :return the best move and its minimmax value estimated by our heuristic function.
    """
    state_hash = (hash(board), depth_limit)
 
    # check if current board state is cached and the depth limit is acceptable to use
    if state_hash in optimizations["cache"]:
       cached_move, cached_value, cached_depth = optimizations["cache"][state_hash]
       if cached_depth >= depth_limit:
          return cached_move, cached_value
       
    # check if current board state is a terminal state or depth limit was reached
    if not board.get_possible_moves(curr_player) or depth_limit == 0:
        value = heuristic_func(board, curr_player)
        optimizations["cache"][state_hash] = (None, value, depth_limit)
        return None, value 
   
    best_move = None
    best_value = float('-inf')

    for move in board.get_possible_moves(curr_player):
        next_state = play_move(board, curr_player, move)
        _, value = minimax_min_limit_opt(next_state, get_opponent(curr_player), heuristic_func, depth_limit - 1, optimizations)
        
        if value > best_value: 
           best_move = move
           best_value = value
 
    # Cache result
    optimizations["cache"][state_hash] = (best_move, best_value, depth_limit)
    return best_move, best_value


def minimax_min_limit_opt(board, curr_player, heuristic_func, depth_limit, optimizations):
    """
    Perform Minimax Search for MIN player up to the given depth limit with the option of caching states.
    Return the best move and its minimmax value estimated by our heuristic function.
    If the board is a terminal state, return None as its best move.

    :param board: the current board
    :param curr_player: the current player
    :param heuristic_func: the heuristic function
    :param depth_limit: the depth limit
    :param optimizations: a dictionary to contain any data structures for optimizations.
        You can use a dictionary called "cache" to implement caching.
    :return the best move and its minimmax value estimated by our heuristic function.
    """
    state_hash = (hash(board), depth_limit)

    # check if current board state is cached and the depth limit is acceptable to use
    if state_hash in optimizations["cache"]:
       cached_move, cached_value, cached_depth = optimizations["cache"][state_hash]
       if cached_depth >= depth_limit:
          return cached_move, cached_value

    # check if current board state is a terminal state or depth limit was reached
    if not board.get_possible_moves(curr_player) or depth_limit == 0:
        value = heuristic_func(board, get_opponent(curr_player))
        optimizations["cache"][state_hash] = (None, value, depth_limit)
        return None, value

    best_move = None
    best_value = float('inf')

    for move in board.get_possible_moves(curr_player):
        next_state = play_move(board, curr_player, move)
        _, value = minimax_max_limit_opt(next_state, get_opponent(curr_player), heuristic_func, depth_limit - 1, optimizations)
        
        if value < best_value: 
           best_move = move
           best_value = value
 
    # Cache result
    optimizations["cache"][state_hash] = (best_move, best_value, depth_limit)
    return best_move, best_value


###############################################################################
## DO NOT MODIFY THE CODE BELOW.
###############################################################################

@timeout(TIMEOUT, timeout_exception=AiTimeoutError)
def run_minimax(curr_board, player, limit, optimizations, hfunc):
    if optimizations is not None:
        opt = True
    else:
        opt = False

    if opt:
        move, value = minimax_max_limit_opt(curr_board, player, hfunc, limit, optimizations)
    elif limit >= 0:
        move, value = minimax_max_limit(curr_board, player, hfunc, limit)
    else:
        move, value = minimax_max_basic(curr_board, player, hfunc)
    
    return move, value
