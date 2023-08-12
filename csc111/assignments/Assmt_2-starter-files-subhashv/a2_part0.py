"""CSC111 Winter 2023 Assignment 2: Trees, Wordle, and Artificial Intelligence (Part 0)

Module Description
===============================

This Python module contains a sample GameTree that matches an example from the assignment
handout. Please feel free to modify this file to experiment with the code found in
a2_game_tree.py and a2_adversarial_wordle.py. You won't be submitting this file for grading
(nor will this file affect other parts of this assignment).

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2023 Mario Badr, David Liu, and Isaac Waller.
"""
from a2_game_tree import GameTree, GAME_START_MOVE
from a2_adversarial_wordle import CORRECT, WRONG_POSITION, INCORRECT


def build_sample_game_tree() -> GameTree:
    """Create an example game tree."""
    game_tree = GameTree(GAME_START_MOVE)

    game_tree.add_subtree(GameTree('sepal'))
    game_tree.add_subtree(GameTree('tiger'))
    game_tree.add_subtree(GameTree('hello'))

    sub1 = GameTree('reach')
    sub2 = GameTree((WRONG_POSITION, INCORRECT, CORRECT, INCORRECT, WRONG_POSITION))
    sub2.add_subtree(GameTree('brawl'))
    sub2.add_subtree(GameTree('quart'))
    sub1.add_subtree(sub2)
    game_tree.add_subtree(sub1)

    game_tree.add_subtree(GameTree('allow'))
    game_tree.add_subtree(GameTree('music'))

    return game_tree
