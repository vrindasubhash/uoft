###############################################################################
# This file implements various alpha-beta pruning agents.
#
# CSC 384 Assignment 2 Starter Code
# version 2.0
###############################################################################
from wrapt_timeout_decorator import timeout

from mancala_game import play_move
from utils import *


def alphabeta_max_basic(board, curr_player, alpha, beta, heuristic_func):
    """
    Perform Alpha-Beta Search for MAX player.
    Return the best move and the estimated minimax value.

    If the board is a terminal state,
    return None as the best move and the heuristic value of the board as the best value.

    :param board: the current board
    :param curr_player: the current player
    :param alpha: current alpha value
    :param beta: current beta value
    :param heuristic_func: the heuristic function
    :return the best move and its minimax value.
    """
    # Check if the current board state is a terminal state
    if not board.get_possible_moves(curr_player):
        return None, heuristic_func(board, curr_player)

    # Initialize best move and best value for MAX player
    best_move = None
    best_value = float('-inf')

    # Iterate over all possible moves for the MAX player
    for move in board.get_possible_moves(curr_player):
        # Get the next state by playing the move
        next_state = play_move(board, curr_player, move)

        # Get the minimax value of the next state for the MIN player
        _, value = alphabeta_min_basic(next_state, get_opponent(curr_player), alpha, beta, heuristic_func)

        # Update best move and best value if a better value is found
        if value > best_value:
            best_move = move
            best_value = value

        # Update alpha
        alpha = max(alpha, best_value)

        # Prune if alpha >= beta
        if alpha >= beta:
            break

    return best_move, best_value


def alphabeta_min_basic(board, curr_player, alpha, beta, heuristic_func):
    """
    Perform Alpha-Beta Search for MIN player.
    Return the best move and the estimated minimax value.

    If the board is a terminal state,
    return None as the best move and the heuristic value of the board as the best value.

    :param board: the current board
    :param curr_player: the current player
    :param alpha: current alpha value
    :param beta: current beta value
    :param heuristic_func: the heuristic function
    :return the best move and its minimax value.
    """
    # Check if the current board state is a terminal state
    if not board.get_possible_moves(curr_player):
        return None, heuristic_func(board, get_opponent(curr_player))

    # Initialize best move and best value for MIN player
    best_move = None
    best_value = float('inf')

    # Iterate over all possible moves for the MIN player
    for move in board.get_possible_moves(curr_player):
        # Get the next state by playing the move
        next_state = play_move(board, curr_player, move)

        # Get the minimax value of the next state for the MAX player
        _, value = alphabeta_max_basic(next_state, get_opponent(curr_player), alpha, beta, heuristic_func)

        # Update best move and best value if a better value is found
        if value < best_value:
            best_move = move
            best_value = value

        # Update beta
        beta = min(beta, best_value)

        # Prune if alpha >= beta
        if alpha >= beta:
            break

    return best_move, best_value


def alphabeta_max_limit(board, curr_player, alpha, beta, heuristic_func, depth_limit):
    """
    Perform Alpha-Beta Search for MAX player up to the given depth limit.
    Return the best move and the estimated minimax value.

    If the board is a terminal state,
    return None as the best move and the heuristic value of the board as the best value.

    :param board: the current board
    :param curr_player: the current player
    :param alpha: current alpha value
    :param beta: current beta value
    :param heuristic_func: the heuristic function
    :param depth_limit: the depth limit
    :return the best move and its estimated minimax value.
    """
    # Check if the current board state is a terminal state
    if not board.get_possible_moves(curr_player) or depth_limit == 0:
        return None, heuristic_func(board, curr_player)

    # Initialize best move and best value for MAX player
    best_move = None
    best_value = float('-inf')

    # Iterate over all possible moves for the MAX player
    for move in board.get_possible_moves(curr_player):
        # Get the next state by playing the move
        next_state = play_move(board, curr_player, move)

        # Get the minimax value of the next state for the MIN player
        _, value = alphabeta_min_limit(next_state, get_opponent(curr_player), alpha, beta, heuristic_func, depth_limit - 1)

        # Update best move and best value if a better value is found
        if value > best_value:
            best_move = move
            best_value = value

        # Update alpha
        alpha = max(alpha, best_value)

        # Prune if alpha >= beta
        if alpha >= beta:
            break

    return best_move, best_value


def alphabeta_min_limit(board, curr_player, alpha, beta, heuristic_func, depth_limit):
    """
    Perform Alpha-Beta Search for MIN player up to the given depth limit.
    Return the best move and the estimated minimax value.

    If the board is a terminal state,
    return None as the best move and the heuristic value of the board as the best value.

    :param board: the current board
    :param curr_player: the current player
    :param alpha: current alpha value
    :param beta: current beta value
    :param heuristic_func: the heuristic function
    :param depth_limit: the depth limit
    :return the best move and its estimated minimax value.
    """
    # Check if the current board state is a terminal state
    if not board.get_possible_moves(curr_player) or depth_limit == 0:
        return None, heuristic_func(board, get_opponent(curr_player))

    # Initialize best move and best value for MIN player
    best_move = None
    best_value = float('inf')

    # Iterate over all possible moves for the MIN player
    for move in board.get_possible_moves(curr_player):
        # Get the next state by playing the move
        next_state = play_move(board, curr_player, move)

        # Get the minimax value of the next state for the MAX player
        _, value = alphabeta_max_limit(next_state, get_opponent(curr_player), alpha, beta, heuristic_func, depth_limit - 1)

        # Update best move and best value if a better value is found
        if value < best_value:
            best_move = move
            best_value = value

        # Update beta
        beta = min(beta, best_value)

        # Prune if alpha >= beta
        if alpha >= beta:
            break

    return best_move, best_value


def alphabeta_max_limit_opt(board, curr_player, alpha, beta, heuristic_func, depth_limit, optimizations):
    """
    Perform Alpha-Beta Search for MAX player 
    up to the given depth limit and with additional optimizations.
    Return the best move and the estimated minimax value.

    If the board is a terminal state,
    return None as the best move and the heuristic value of the board as the best value.

    :param board: the current board
    :param curr_player: the current player
    :param alpha: current alpha value
    :param beta: current beta value
    :param heuristic_func: the heuristic function
    :param depth_limit: the depth limit
    :param optimizations: a dictionary to contain any data structures for optimizations.
        You can use a dictionary called "cache" to implement caching.
    :return the best move and its estimated minimax value.
    """
    state_key = (hash(board), depth_limit)

    # check if current board state is cached and the depth limit is acceptable to use
    if state_key in optimizations["cache"]:
        cached_move, cached_value, cached_depth = optimizations["cache"][state_key]
        if cached_depth >= depth_limit:
            return cached_move, cached_value

    # check if current board state is a terminal state or depth limit was reached
    if not board.get_possible_moves(curr_player) or depth_limit == 0:
        value = heuristic_func(board, curr_player)
        optimizations["cache"][state_key] = (None, value, depth_limit)
        return None, value

    best_move = None
    best_value = float('-inf')

    for move in board.get_possible_moves(curr_player):
        next_state = play_move(board, curr_player, move)
        _, value = alphabeta_min_limit_opt(next_state, get_opponent(curr_player), alpha, beta, heuristic_func, depth_limit - 1, optimizations)

        if value > best_value:
            best_move = move
            best_value = value

        # alpha-beta pruning
        alpha = max(alpha, best_value)
        if alpha >= beta:
            break

    # Cache result
    optimizations["cache"][state_key] = (best_move, best_value, depth_limit)
    return best_move, best_value


def alphabeta_min_limit_opt(board, curr_player, alpha, beta, heuristic_func, depth_limit, optimizations):
    """
    Perform Alpha-Beta Pruning for MIN player 
    up to the given depth limit and with additional optimizations.
    Return the best move and the estimated minimax value.

    If the board is a terminal state,
    return None as the best move and the heuristic value of the board as the best value.

    :param board: the current board
    :param curr_player: the current player
    :param alpha: current alpha value
    :param beta: current beta value
    :param heuristic_func: the heuristic function
    :param depth_limit: the depth limit
    :param optimizations: a dictionary to contain any data structures for optimizations.
        You can use a dictionary called "cache" to implement caching.
    :return the best move and its estimated minimax value.
    """
    state_key = (hash(board), depth_limit)

    # check if current board state is cached and the depth limit is acceptable to use
    if state_key in optimizations["cache"]:
        cached_move, cached_value, cached_depth = optimizations["cache"][state_key]
        if cached_depth >= depth_limit:
            return cached_move, cached_value

    # check if current board state is a terminal state or depth limit was reached
    if not board.get_possible_moves(curr_player) or depth_limit == 0:
        value = heuristic_func(board, get_opponent(curr_player))
        optimizations["cache"][state_key] = (None, value, depth_limit)
        return None, value

    best_move = None
    best_value = float('inf')

    for move in board.get_possible_moves(curr_player):
        next_state = play_move(board, curr_player, move)
        _, value = alphabeta_max_limit_opt(next_state, get_opponent(curr_player), alpha, beta, heuristic_func, depth_limit - 1, optimizations)

        if value < best_value:
            best_move = move
            best_value = value

        # Alpha-beta pruning
        beta = min(beta, best_value)
        if alpha >= beta:
            break

    # Cache result
    optimizations["cache"][state_key] = (best_move, best_value, depth_limit)
    return best_move, best_value


###############################################################################
## DO NOT MODIFY THE CODE BELOW.
###############################################################################

@timeout(TIMEOUT, timeout_exception=AiTimeoutError)
def run_alphabeta(curr_board, player, limit, optimizations, hfunc):
    if optimizations is not None:
        opt = True
    else:
        opt = False

    alpha = float("-Inf")
    beta = float("Inf")
    if opt:
        move, value = alphabeta_max_limit_opt(curr_board, player, alpha, beta, hfunc, limit, optimizations)
    elif limit >= 0:
        move, value = alphabeta_max_limit(curr_board, player, alpha, beta, hfunc, limit)
    else:
        move, value = alphabeta_max_basic(curr_board, player, alpha, beta, hfunc)
    
    return move, value

