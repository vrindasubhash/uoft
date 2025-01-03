###############################################################################
# This file contains helper functions and the heuristic functions
# for our AI agents to play the Mancala game.
#
# CSC 384 Assignment 2 Starter Code
# version 2.0
###############################################################################

import sys

###############################################################################
### DO NOT MODIFY THE CODE BELOW

### Global Constants ###
TOP = 0
BOTTOM = 1
TIMEOUT = 60

### Errors ###
class InvalidMoveError(RuntimeError):
    pass

class AiTimeoutError(RuntimeError):
    pass

### Functions ###
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def get_opponent(player):
    if player == BOTTOM:
        return TOP
    return BOTTOM

### DO NOT MODIFY THE CODE ABOVE
###############################################################################


def heuristic_basic(board, player):
    """
    Compute the heuristic value of the current board for the current player 
    based on the basic heuristic function.

    :param board: the current board.
    :param player: the current player.
    :return: an estimated utility of the current board for the current player.
    """
    top_score, bottom_score = board.mancalas[TOP], board.mancalas[BOTTOM]

    if player == TOP:
       player_score = top_score
       opponent_score = bottom_score
    else:
       player_score = bottom_score
       opponent_score = top_score

    return player_score - opponent_score


def heuristic_advanced(board, player): 
    """
    Compute the heuristic value of the current board for the current player
    based on the advanced heuristic function.

    :param board: the current board object.
    :param player: the current player.
    :return: an estimated heuristic value of the current board for the current player.
    """
    # use heuristic basic as base score difference
    basic_value = heuristic_basic(board, player)

    # calculate number of empty pockets for the player and the opponent
    player_empty_pockets = sum(1 for stones in board.pockets[player] if stones == 0)
    opponent_empty_pockets = sum(1 for stones in board.pockets[get_opponent(player)] if stones == 0)

    # calculate difference between the opponents and players empty pockets
    empty_pockets_diff = opponent_empty_pockets - player_empty_pockets
 
    heuristic_value = basic_value + 0.3 * empty_pockets_diff

    return heuristic_value
 
