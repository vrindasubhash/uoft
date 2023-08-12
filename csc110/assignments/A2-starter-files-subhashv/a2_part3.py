"""CSC110 Fall 2022 Assignment 2, Part 3: Wordle!

Module Description
==================
This Python file contains the starter code for Part 3 of this assignment.
For more information, please see the assignment handout.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC110 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC110 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2022 David Liu, Tom Fairgrieve, and Angela Zavaleta Bernuy.
"""
from python_ta.contracts import check_contracts

from a2_wordle_helpers import ALL_STATUSES, INCORRECT, CORRECT, WRONG_POSITION, cartesian_product_general
import a2_visualizer


###################################################################################################
# Part 3(a)
###################################################################################################
@check_contracts
def is_correct_char(answer: str, guess: str, i: int) -> bool:
    """Return whether the character status of guess[i] with respect to answer is CORRECT.

    Preconditions:
    - len(answer) == len(guess)
    - 0 <= i < len(answer)

    >>> is_correct_char('teach', 'adieu', 3)
    False
    >>> is_correct_char('teaching', 'reacting', 1)
    True
    """
    return guess[i] == answer[i]


@check_contracts
def is_wrong_position_char(answer: str, guess: str, i: int) -> bool:
    """Return whether the character status of guess[i] with respect to answer is WRONG_POSITION.

    Preconditions:
    - len(answer) == len(guess)
    - 0 <= i < len(answer)

    >>> is_wrong_position_char('teach', 'adieu', 3)
    True
    >>> is_wrong_position_char('teaching', 'reacting', 1)
    False
    >>> # Cases with duplicate characters!
    >>> is_wrong_position_char('hello', 'hoops', 1)
    True
    >>> is_wrong_position_char('hello', 'hoops', 2)
    True
    >>> is_wrong_position_char('aabbcc', 'abbbef', 1)
    False
    """

    c = guess[i]
    list_of_index_matches = [j for j, item in enumerate(answer) if item == c]
    valid_list = [j for j in list_of_index_matches if guess[j] != c]

    return c != answer[i] and valid_list != []


@check_contracts
def is_incorrect_char(answer: str, guess: str, i: int) -> bool:
    """Return whether the character status of guess[i] with respect to answer is INCORRECT.

    Preconditions:
    - len(answer) == len(guess)
    - 0 <= i < len(answer)

    >>> is_incorrect_char('teach', 'adieu', 1)
    True
    >>> is_incorrect_char('teaching', 'reacting', 1)
    False
    >>> is_incorrect_char('hello', 'keeps', 2)
    True

    HINT: you can use the previous two status functions to implement this one.
    """
    return not (is_correct_char(answer, guess, i) or is_wrong_position_char(answer, guess, i))


@check_contracts
def get_character_status(answer: str, guess: str, i: int) -> str:
    """Return the character status of guess[i] with respect to answer.

    The return value is one of the three values {INCORRECT, WRONG_POSITION, CORRECT}.
    (These values are imported from the a2_helpers.py module for you already.)

    Preconditions:
    - len(answer) == len(guess)
    - 0 <= i < len(answer)

    >>> get_character_status('teach', 'adieu', 1) == INCORRECT
    True
    >>> get_character_status('teaching', 'reacting', 1) == CORRECT
    True
    """
    possible_outputs = [INCORRECT, WRONG_POSITION, CORRECT]
    wrong_position = is_wrong_position_char(answer, guess, i)
    correct = is_correct_char(answer, guess, i)

    return possible_outputs[wrong_position + 2 * correct]


@check_contracts
def get_guess_status(answer: str, guess: str) -> list[str]:
    """Return the guess status of the given guess with respect to answer.

    The return value is a list with the same length as guess, whose
    elements are all in the set {INCORRECT, WRONG_POSITION, CORRECT}.

    Preconditions:
    - answer != ''
    - len(answer) == len(guess)

    >>> example_status = get_guess_status('teach', 'adieu')
    >>> example_status == [WRONG_POSITION, INCORRECT, INCORRECT, WRONG_POSITION, INCORRECT]
    True
    """
    return [get_character_status(answer, guess, i) for i in range(0, len(answer))]


@check_contracts
def get_guesses_statuses(answer: str, guesses: list[str]) -> list[list[str]]:
    """Return the guess statuses of each given guess with respect to answer.

    The return value is a list with the same length as guesses, where each status has
    elements that are all in the set {INCORRECT, WRONG_POSITION, CORRECT}.

    Preconditions:
    - answer != ''
    - all({len(answer) == len(guess) for guess in guesses})

    >>> example_statuses = get_guesses_statuses('teach', ['adieu'])
    >>> example_statuses == [[WRONG_POSITION, INCORRECT, INCORRECT, WRONG_POSITION, INCORRECT]]
    True
    """
    return [get_guess_status(answer, guess) for guess in guesses]


@check_contracts
def part3a_example(answer: str, guesses: list[str]) -> None:
    """Visualize the Wordle game for the given answer and guesses.

    Complete this function in two steps:

    1. First, use your get_guesses_statuses function to compute the statuses of each given guess.
    2. Then, call a2_visualizer.draw_wordle to display the result! (You will need to read
       the docstring of that function, in a2_visualizer.py, to understand how to use it.)

    NOTE: You do *NOT* need a return statement in this function. The return type annotation
    is "None", which is a special annotation meaning this function doesn't return anything.
    When you call this function in the Python console, you should see a Pygame window appear,
    like in some of the examples in Assignment 1. But after you close the Pygame window, nothing
    should display in the Python console, since this function doesn't return anything.
    """
    result_of_guesses = get_guesses_statuses(answer, guesses)
    a2_visualizer.draw_wordle(answer, guesses, result_of_guesses)


###################################################################################################
# Part 3(b)
###################################################################################################
@check_contracts
def is_correct_single(word: str, guess: str, status: list[str]) -> bool:
    """Return whether the given word is a correct answer for the given guess and status.

    Preconditions:
    - len(word) == len(guess) == len(status)
    - _is_valid_status(status)
    - word != ''

    Note: the second precondition makes uses of a helper function at the bottom of this file,
    which checks that a guess status consists only of the elements {INCORRECT, WRONG_POSITION, CORRECT}.

    >>> is_correct_single('later', 'tower', [WRONG_POSITION, INCORRECT, INCORRECT, CORRECT, CORRECT])
    True
    >>> is_correct_single('later', 'tower', [INCORRECT] * 5)
    False
    """
    word_status = get_guess_status(word, guess)
    return word_status == status


@check_contracts
def is_correct_multiple(word: str, guesses: list[str], statuses: list[list[str]]) -> bool:
    """Return whether the given word is a correct answer for the given guesses and statuses.

    Preconditions:
    - len(guesses) == len(statuses)
    - all({len(word) == len(guess) for guess in guesses})
    - all({len(word) == len(status) for status in statuses})
    - all({_is_valid_status(status) for status in statuses})
    - word != ''

    >>> example_guesses = ['tower', 'lower', 'power', 'round']
    >>> example_statuses = [
    ...     [WRONG_POSITION, INCORRECT, INCORRECT, CORRECT, CORRECT],
    ...     [CORRECT, INCORRECT, INCORRECT, CORRECT, CORRECT],
    ...     [INCORRECT, INCORRECT, INCORRECT, CORRECT, CORRECT],
    ...     [WRONG_POSITION, INCORRECT, INCORRECT, INCORRECT, INCORRECT]
    ... ]
    >>> is_correct_multiple('later', example_guesses, example_statuses)
    True
    """
    word_statuses = get_guesses_statuses(word, guesses)
    return word_statuses == statuses


@check_contracts
def find_correct_answers(word_set: set[str],
                         guesses: list[str], statuses: list[list[str]]) -> list[str]:
    """Return the list of words (from word_set) that are correct answer for the given guesses and statuses.

    The returned list should be in alphabetical order---use the built-in `sorted` function to achieve this.

    Preconditions:
    - all words in word_set have the same non-zero length
    - all({guess in word_set for guess in guesses})
    - len(guesses) == len(statuses)
    - all({len(guesses[i]) == len(statuses[i]) for i in range(0, len(guesses))})
    - all({_is_valid_status(status) for status in statuses})

    >>> example_word_set = {'later', 'liter', 'tower', 'lower', 'power', 'round', 'tiger'}
    >>> example_guesses = ['tower', 'lower', 'power', 'round']
    >>> example_statuses = [
    ...     [WRONG_POSITION, INCORRECT, INCORRECT, CORRECT, CORRECT],
    ...     [CORRECT, INCORRECT, INCORRECT, CORRECT, CORRECT],
    ...     [INCORRECT, INCORRECT, INCORRECT, CORRECT, CORRECT],
    ...     [WRONG_POSITION, INCORRECT, INCORRECT, INCORRECT, INCORRECT]
    ... ]
    >>> find_correct_answers(example_word_set, example_guesses, example_statuses)
    ['later', 'liter']
    """

    def handle_correct(words: list[str], guess: str, i: int) -> list[bool]:
        """Find if ith character matches between guess and word in words.
        Each item represents a match or no match for each word in words.
        """
        return [is_correct_char(word, guess, i) for word in words]

    def handle_incorrect(words: list[str], guess: str, i: int) -> list[bool]:
        """Find if ith character is incorrect between guess and word in words.
        Each item represents an incorrect position for each word in words.
        """
        return [is_incorrect_char(word, guess, i) for word in words]

    def handle_wrong_position(words: list[str], guess: str, i: int) -> list[bool]:
        """Find if ith character is in the wrong position between guess and word in words.
        Each item represents a wrong position for each word in words.
        """
        return [is_wrong_position_char(word, guess, i) for word in words]

    def reduce_bool(table: list[list[bool]], n: int) -> list[bool]:
        """Given a list of a list of bools, do a column-wise and to create a new list.

        Steps:
            flatten the list in column order
            create a new table by column order
            sum each row (original column) (make it one list)
            check if the sum == original number of rows to decide if it is True or False
        """
        nrow = len(table)
        ncol = n
        flattened = [table[j][i] for i in range(ncol) for j in range(nrow)]
        column_order_table = [flattened[i * nrow: i * nrow + nrow] for i in range(ncol)]
        sum_of_trues = [sum(row) for row in column_order_table]
        return [s == nrow for s in sum_of_trues]

    def handle_guess(words: list[str], guess: str, status: list[str]) -> list[bool]:
        """Given a list of words, find words that matches a guess and its corresponding status.
        Returns a boolean list with True values for correct words from the word list.
        """
        n = len(words)

        # correct, incorrect, wrong_position are tables of boolean.
        # the rows correspond to a character in guess.
        # the columns correspond to a word in the word list.

        correct = [handle_correct(words, guess, i) for i in range(len(guess)) if status[i] == CORRECT]
        # only consider rows where the guess status is correct.

        incorrect = [handle_incorrect(words, guess, i) for i in range(len(guess)) if status[i] == INCORRECT]
        # only consider rows where the guess status is incorrect.

        wrong_position = [handle_wrong_position(words, guess, i) for i in range(len(guess))
                          if status[i] == WRONG_POSITION]
        # only consider rows where the guess status is in the wrong position.

        # find rows (words from word list) with all Trues (status is same as guess status)
        correct = reduce_bool(correct, n)
        incorrect = reduce_bool(incorrect, n)
        wrong_position = reduce_bool(wrong_position, n)

        # now combine rows (words from word list) with all Trues (corresponding to CORRECT, INCORRECT, WRONG_POSITION)
        return reduce_bool([correct, incorrect, wrong_position], n)

    word_list = list(word_set)

    x = [handle_guess(word_list, guesses[i], statuses[i]) for i in range(0, len(guesses))]
    y = reduce_bool(x, len(word_list))
    z = [word_list[j] for j in range(len(word_list)) if y[j]]

    return sorted(z)


@check_contracts
def part3b_example(word_set_file: str, guesses: list[str], statuses: list[list[str]]) -> None:
    """Visualize the Wordle game (with correct answers!) for the given guesses and statuses.

    Complete this function in two steps:

    1. Compute the correct answers for the given guesses and statuses, using the word set
        that's read in from word_set_file. (We've provided the code for reading in the
        words from the file for this function.)
    2. Then, call a2_visualizer.draw_wordle_answers to display the result!
       Note that this visualization is a bit more sophisticated than the one you used in
       part3a_example, as this one lets the user flip through the possible correct answers
       using the left/right arrow keys.

    Preconditions:
        - all words in the word_set_file have the same non-zero length
        - all guesses appear in the word_set_file
        - guesses and statuses satisfy all preconditions of find_correct_answers

    NOTE: Like part3a_example, this function shouldn't have a return statement.
    """
    with open(word_set_file) as f:
        # word_set is assigned to a set[str] containing the words in the file
        word_set = {str.strip(w) for w in f.readlines()}

    # Complete this function by deleting the ... and following the instructions in the docstring
    answers = find_correct_answers(word_set, guesses, statuses)
    a2_visualizer.draw_wordle_answers(answers, guesses, statuses)


###################################################################################################
# Part 3(c)
###################################################################################################
@check_contracts
def find_correct_guesses_single(word_set: set[str], answer: str, status: list[str]) -> list[str]:
    """Return the list of guesses from word_set that are consistent with the answer and status.

    The returned list should be in alphabetical order---as you did above, use the `sorted` function to
    achieve this.

    Preconditions:
    - answer != ''
    - answer in word_set
    - all words in word_set have the same non-zero length
    - len(answer) == len(status)
    - _is_valid_status(status)

    >>> example_word_set = {'later', 'liter', 'tower', 'lower', 'power', 'round', 'tiger'}
    >>> example_status = [WRONG_POSITION, INCORRECT, INCORRECT, CORRECT, CORRECT]
    >>> find_correct_guesses_single(example_word_set, 'later', example_status)
    ['tiger', 'tower']
    """
    word_list = list(word_set)
    list_of_guess_statuses = [get_guess_status(answer, word) for word in word_list]
    answers = [word_list[j] for j in range(len(list_of_guess_statuses)) if list_of_guess_statuses[j] == status]
    return sorted(answers)


@check_contracts
def find_correct_guesses_multiple(word_set: set[str],
                                  answer: str, statuses: list[list[str]]) -> list[list[str]]:
    """Return the possible guess words from word_set that are consistent with the answer and statuses.

    The returned value is a list of lists, where each of the inner lists is a sequence of words that yields
    the given statuses with respect to the given answer.

    IMPORTANT: Call the sorted function on the list of lists before returning it. This will ensure
    that the inner lists are sorted alphabetically by their first words, breaking ties by comparing
    their second words, etc.

    Preconditions:
    - answer != ''
    - answer in word_set
    - all words in word_set have the same non-zero length
    - all({len(answer) == len(status) for status in statuses})
    - all({_is_valid_status(status) for status in statuses})

    >>> example_word_set = {'later', 'liter', 'tower', 'lower', 'power', 'round', 'tiger'}
    >>> example_statuses = [
    ...     [WRONG_POSITION, INCORRECT, INCORRECT, CORRECT, CORRECT],
    ...     [CORRECT, INCORRECT, INCORRECT, CORRECT, CORRECT]
    ... ]
    >>> find_correct_guesses_multiple(example_word_set, 'later', example_statuses)
    [['tiger', 'lower'], ['tower', 'lower']]

    Note that ['tiger', 'lower'] comes before ['tower', 'lower'] because 'tiger' comes before
    'tower' alphabetically.
    """

    list_of_guesses = [find_correct_guesses_single(word_set, answer, status) for status in statuses]
    return cartesian_product_general(list_of_guesses)


@check_contracts
def part3c_example(word_set_file: str, answer: str, statuses: list[list[str]]) -> None:
    """Visualize the Wordle game (with reverse-engineered guesses!) for the given answer and statuses.

    Complete this function in three steps (similar to part3b_example):

    1. First, *read in the words in word_set_file*. You can reuse the same code from
       part3b_example for this step.
    2. Then, compute the possible guesses for the given answer and statuses.
    3. Then, call a2_visualizer.draw_wordle_guesses to display the result!

    Preconditions:
        - answer appears in the word_set_file
        - all words in the word_set_file have the same non-zero length
        - answer and statuses satisfy the preconditions of find_correct_guesses_multiple
    """

    with open(word_set_file) as f:
        # word_set is assigned to a set[str] containing the words in the file
        word_set = {str.strip(w) for w in f.readlines()}

    correct_possible_guesses = find_correct_guesses_multiple(word_set, answer, statuses)
    a2_visualizer.draw_wordle_guesses(answer, correct_possible_guesses, statuses)


###################################################################################################
# Part 3(d)
###################################################################################################
@check_contracts
def information_score(answer: str, guess: str) -> float:
    """Return the information score of guess with respect to answer.

    See assignment handout for the formula for information score.

    Preconditions:
    - len(answer) == len(guess)
    - answer != ''
    """

    status = get_guess_status(answer, guess)
    return status.count(CORRECT) + 0.5 * status.count(WRONG_POSITION)


@check_contracts
def find_correct_answers_and_scores(word_set: set[str],
                                    guesses: list[str], statuses: list[list[str]]) -> dict[str, float]:
    """Return a mapping from possible correct answers to their average information score (see handout for details).

    You MUST call find_correct_answers in this function. We strongly encourage you to also define at least
    one new helper function to break down this computation.

    Preconditions:
    - all words in word_set have the same non-zero length
    - all({guess in word_set for guess in guesses})
    - len(guesses) == len(statuses)
    - all({len(guesses[i]) == len(statuses[i]) for i in range(0, len(guesses))})
    - all({_is_valid_status(status) for status in statuses})
    - (NEW!) there is at least one possible correct answer

    NOTE: we haven't provided "example" code for testing this function. You may choose to do your testing
    in the Python console, by writing doctests, and/or by writing test cases or an "example" function
    similar to part3b_example/part3c_example. For the latter two testing options, please write them
    in a separate file (that will not be submitted) rather than including them in this file.
    """

    def compute_score(k: str, candidates: list[str]) -> float:
        """Compute average of information score for one candidate with respect to others.
        """
        score = [information_score(k, v) for v in candidates]
        s = sum(score)
        return s / len(candidates)

    possible_answers = find_correct_answers(word_set, guesses, statuses)

    # for each possible answers, combine its score with all other possible answer
    cartesian = {key: possible_answers for key in possible_answers}
    result_map = {key: compute_score(key, val) for key, val in cartesian}
    return result_map


###################################################################################################
# Additional helper function (for some preconditions)
###################################################################################################
@check_contracts
def _is_valid_status(status: list[str]) -> bool:
    """Return whether s is a valid status.

    A valid status is a list that contains only the three statuses in ALL_STATUSES.
    This function is used in some of the precondition expressions in this file.
    You should not change this function.
    """
    return all({char_status in ALL_STATUSES for char_status in status})


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)

    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (In PyCharm, select the lines below and press Ctrl/Cmd + / to toggle comments.)
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 120,
        'extra-imports': ['a2_wordle_helpers', 'a2_visualizer'],
        'disable': ['use-a-generator'],
        'allowed-io': ['part3b_example', 'part3c_example']
    })
