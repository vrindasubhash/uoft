"""CSC110 Fall 2022 Assignment 4, Part 3: Number Theory, Cryptography, and Algorithm Running Time Analysis

Instructions (READ THIS FIRST!)
===============================

This Python module contains the functions you should complete for Part 3 of this assignment.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC110 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC110 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2022 David Liu and Tom Fairgrieve
"""
# You may uncomment this statement to import the math module in this file
import math

from python_ta.contracts import check_contracts


###############################################################################
# Part (a): From strings to numbers
###############################################################################
@check_contracts
def base128_to_int(digits: list[int]) -> int:
    """Return the integer represented by the given base-128 representation.

    The input list has the units (128 ** 0) digit at the LAST index.

    Preconditions:
        - digits != []
        - all({0 <= d < 128 for d in digits})

    >>> base128_to_int([1])
    1
    >>> base128_to_int([3, 2, 4])  # 3 * (128 ** 2) + 2 * (128 ** 1) + 4 * (128 ** 0)
    49412
    >>> base128_to_int([72, 101, 108, 108, 111])
    19540948591

    NOTE: this function can be implemented by either a for loop or a comprehension.
    For practice, we strongly recommend trying both implementations.
    """
    new_digits = []
    position = len(digits) - 1

    for i in range(0, len(digits)):
        new_digits.append(digits[i] * (128 ** (position - i)))

    return sum(new_digits)


@check_contracts
def int_to_base128(n: int) -> list[int]:
    """Return the base-128 representation of the given number.

    The returned list has the units (128 ** 0) digit at the LAST index.
    The returned list should not have any leading zeros (i.e., the first element should be > 0).

    Preconditions:
    - n >= 1

    >>> int_to_base128(1)
    [1]
    >>> int_to_base128(49412)
    [3, 2, 4]

    HINTS: Here are two possible (ideas for) algorithms to solve this problem.
    You may use a different approach, as long as you use only programming elements and techniques
    allowed for this assignment. In particular, "recursion" is not permitted.

    APPROACH 1 ("big to small"):
        Start by computing the largest power of 128 that's less than n, and then compute the
        quotient (n // (128 ** ___)); that gives you the first element of the list.
        Update n in some way, and then repeat. You will find the math.log function useful.

    APPROACH 2 ("small to big"):
        Compute the remainder n % 128. That gives you the units digit (last element of the list).
        Update n in some way, and then repeat.
    """

    digits = []

    digits.append(n % 128)
    shift = n // 128

    while shift != 0:
        digits.append(shift % 128)
        shift = shift // 128

    digits.reverse()

    return digits


###############################################################################
# Part (b): Encrypting and decrypting blocks
###############################################################################
@check_contracts
def rsa_encrypt_block(public_key: tuple[int, int], plaintext: str) -> list[int]:
    """Encrypt the given plaintext using the recipient's public key.

    Preconditions:
        - public_key is a valid RSA public key (n, e)
        - public_key[0] >= 128
        - all({ord(c) < 128 for c in plaintext})
        - plaintext != ''
        - len(plaintext) is divisibile by the block length

    NOTES:

    1. Use the math.pow function to compute a modular exponentiation, not ** and %.
       math.pow is much more efficient for larger numbers!
    2. You may find it useful to use range with THREE arguments, e.g. range(0, 10, 2).
       Experiment with this in the Python console!
    """

    n, e = public_key
    encrypted_ints = []

    block_length = math.floor(math.log(n, 128))
    word_blocks = []

    for i in range(0, len(plaintext), block_length):
        word_blocks.append(plaintext[i: i + block_length])

    block_int_vals = []

    for block in word_blocks:
        digits = []
        for char in block:
            digits.append(ord(char))
        block_int_vals.append(base128_to_int(digits))

    for block_int in block_int_vals:
        encrypted_ints.append(int(pow(block_int, e, n)))

    return encrypted_ints


@check_contracts
def rsa_decrypt_block(private_key: tuple[int, int, int], ciphertext: list[int]) -> str:
    """Decrypt the given ciphertext using the recipient's private key.

    Preconditions:
        - private_key is a valid RSA private key (p, q, d)
        - private_key[0] * private_key[1] >= 128
        - ciphertext != []
        - all({0 <= num < private_key[0] * private_key[1] for num in ciphertext})
    """

    p, q, d = private_key
    n = p * q

    word_blocks = []
    decrypted_ints = []

    for num in ciphertext:
        decrypted_ints.append(pow(num, d, n))

    for val in decrypted_ints:
        char_ints = int_to_base128(val)
        for char in char_ints:
            word_blocks.append(chr(char))

    decrypted_text = ''.join(word_blocks)
    return decrypted_text


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)

    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (In PyCharm, select the lines below and press Ctrl/Cmd + / to toggle comments.)
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['use-a-generator'],
        'extra-imports': ['math']
    })
