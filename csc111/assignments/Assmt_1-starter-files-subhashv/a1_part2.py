"""CSC111 Assignment 1: Linked Lists and Blockchain

Instructions (READ THIS FIRST!)
===============================

This Python module contains the code for Part 2 of this assignment. Please consult
the assignment handout for instructions and details.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2023 David Liu, Mario Badr
"""
from __future__ import annotations
from dataclasses import dataclass
import hashlib
from typing import Optional

from python_ta.contracts import check_contracts

###################################################################################################
# Constants used for Part 2(c)
###################################################################################################
# You may change these for testing, but should restore their original values (10 and 3, respectively)
# before your final submission. We will also test your code by providing alternate values for these
# constants, so please make sure to actually use them in your code in Part 2(c)!
MINING_AMOUNT = 10
DIFFICULTY_RATING = 3


###################################################################################################
# _Transaction and Ledger class definitions
###################################################################################################
@check_contracts
@dataclass
class _Transaction:
    """A transaction in our Titancoin (TC) cryptocurrency system.

    Instance Attributes:
        - sender:
            For a transfer transaction, this is the name of the person sending the money.
            For a mining transaction, this is an empty string.
        - recipient:
            For a transfer transaction, this is the name of the person receiving the money.
            For a mining transaction, this is the name of the person who does the mining
            (and therefore gets the money).
        - amount:
            The number =of Titancoins being transferred/mined.
        - next:
            The next transaction in the ledger, or None if this is the most recent
            transaction.
        - prev_digest:
            The digest of the previous transaction in the ledger, or 0 if there was no previous transaction.
        - nonce:
            An integer that may be used when computing the transaction digest.

    Representation Invariants:
        - self.recipient != ''
        - self.amount > 0
        - ((self.next is None) or (self.next.prev_digest == 0) or (self.next.nonce != 0)) and\
         (self.next.prev_digest == digest_from_hash(self)
    """
    sender: str
    recipient: str
    amount: int
    next: Optional[_Transaction] = None
    prev_digest: int = 0  # Default value of 0
    nonce: int = 0  # Default value of 0


@check_contracts
class Ledger:
    """A Titancoin cryptocurrency ledger, storing a sequence of transactions in a linked list.

    Instance Attributes:
        - first: the first transaction in the ledger, or None if there are no transactions
        - last: the last transaction in the ledger, or None if there are no transactions
        - _balance: a mapping from person name to their current balance (i.e., amount of money).
                    This mapping contains a key for every person who has ever been involved with
                    a transaction in this ledger, even if their current balance is 0.

    Representation Invariants:
        - all({self._balance[x] >= 0 for x in self._balance})
        - all({name != '' for all name in self._balance})
        - (self.first is None) and (self._balance == {})
        - (self.first is None) and (self.last is None)
    """
    first: Optional[_Transaction]
    last: Optional[_Transaction]
    _balance: dict[str, int]

    def is_balance_equal(self, balance: dict) -> bool:
        """ Function to check if two balance dictionaries are equal since _balance is only accessible from self.
        """
        return self._balance == balance

    def __init__(self) -> None:
        """Initialize a new ledger.

        The ledger is created with no transactions and with no people's balances recorded.
        """
        self.first = None
        self.last = None
        self._balance = {}

    ###############################################################################################
    # Part 2(a)
    ###############################################################################################
    def record_transfer(self, sender: str, recipient: str, amount: int) -> None:
        """Record a new transfer transaction with the given sender, recipient, and amount.

        Raise a ValueError if the sender's current balance is less than the given amount,
        or if the sender does not have a balance recorded.

        Preconditions:
        - sender != ''
        - recipient != ''
        - amount > 0

        IMPLEMENTATION NOTES:
        - Use self.last to quickly access the last node in the linked list (much faster than
          iterating through the entire linked list!)
        - Remember to update self.last and self._balance (possibly in addition to self.first)
        """

        if sender not in self._balance:
            raise ValueError
        if self._balance[sender] < amount:
            raise ValueError

        transaction = _Transaction(sender, recipient, amount)

        if self.first is None:
            self.first = transaction
            self.last = transaction
        else:
            self.last.next = transaction
            self.last = transaction

        self._balance[sender] = self._balance[sender] - amount
        if recipient not in self._balance:
            self._balance[recipient] = amount
        else:
            self._balance[recipient] = self._balance[recipient] + amount

    def record_mining(self, miner: str, amount: int) -> None:
        """Record a new mining transaction with the given miner (i.e., person who is mining) and amount.

        Preconditions:
        - miner != ''
        - amount > 0

        IMPLEMENTATION NOTES:
        - Use self.last to quickly access the last node in the linked list (much faster than
          iterating through the entire linked list!)
        - Remember to update self.last and self._balance (possibly in addition to self.first)
        """
        transaction = _Transaction('', miner, amount)

        if self.first is None:
            self.first = transaction
            self.last = transaction
        else:
            self.last.next = transaction
            self.last = transaction

        if miner not in self._balance:
            self._balance[miner] = amount
        else:
            self._balance[miner] = self._balance[miner] + amount

    def get_balance(self, person: str) -> int:
        """Return the current balance for the given person.

        Raise ValueError if the given person does not have a balance recorded by this ledger.

        Precondtions:
        - person != ''
        """

        if person not in self._balance:
            raise ValueError

        return self._balance[person]

    def verify_balance(self) -> bool:
        """Return whether this ledger's stored balance is consistent with its transactions.

        This function iterates across all transactions in the ledger and accumulates a
        "balance so far" after each transaction.

        - Return False if you encounter a transaction that is invalid. This occurs when
          a transfer involves a sender who doesn't have a current balance, or whose
          current balance is less than the amount being transferred.
        - Return False if the final balance accumulate does not equal self._balance.
        - Otherwise, return True.
        """

        ledger_temp = Ledger()

        curr = self.first

        while curr is not None:
            sender = curr.sender
            recipient = curr.recipient
            amount = curr.amount
            if sender == '':
                ledger_temp.record_mining(recipient, amount)
            else:
                ledger_temp.record_transfer(sender, recipient, amount)
            curr = curr.next

        return ledger_temp.is_balance_equal(self._balance)

    ###############################################################################################
    # Part 2(b)
    ###############################################################################################
    def record_transfer_digest(self, sender: str, recipient: str, amount: int) -> None:
        """Record a new transfer transaction with the given sender, recipient, and amount.

        (NEW) When the transaction is created, it stores the digest of the previous transaction,
        using the digest_from_hash function provided near the bottom of this file. If there are
        no previous transactions, 0 (the default value) is stored instead.

        Raise a ValueError if the sender's current balance is less than the given amount,
        or if the sender does not have a balance recorded.

        Preconditions:
        - sender != ''
        - recipient != ''
        - amount > 0

        IMPLEMENTATION NOTES (NEW):
        - This method should be implemented in a very similar way to Part 2(a).
        """
        if self._balance[sender] < amount:
            raise ValueError
        if sender not in self._balance:
            raise ValueError

        if self.first is None:
            transaction = _Transaction(sender, recipient, amount, None, 0)
            self.first = transaction
            self.last = transaction
        else:
            digest = digest_from_hash(self.last)
            transaction = _Transaction(sender, recipient, amount, None, digest)
            self.last.next = transaction
            self.last = transaction

        self._balance[sender] = self._balance[sender] - amount
        if recipient not in self._balance:
            self._balance[recipient] = amount
        else:
            self._balance[recipient] = self._balance[recipient] + amount

    def record_mining_digest(self, miner: str, amount: int) -> None:
        """Record a new mining transaction with the given miner (i.e., person who is mining) and amount.

        (NEW) When the transaction is created, it stores the digest of the previous transaction,
        using the digest_from_hash function provided near the bottom of this file. If there are
        no previous transactions, 0 (the default value) is stored instead.

        Preconditions:
        - miner != ''
        - amount > 0

        IMPLEMENTATION NOTES (NEW):
        - This method should be implemented in a very similar way to Part 2(a).
        """

        if self.first is None:
            transaction = _Transaction('', miner, amount, None, 0)
            self.first = transaction
            self.last = transaction
        else:
            digest = digest_from_hash(self.last)
            transaction = _Transaction('', miner, amount, None, digest)
            self.last.next = transaction
            self.last = transaction

        if miner not in self._balance:
            self._balance[miner] = amount
        else:
            self._balance[miner] = self._balance[miner] + amount

    def verify_digests(self) -> bool:
        """Return whether all of this ledger's transactions have the correct prev_digest attribute values.

        Do NOT check balances in this method, just the prev_digest values. That is, it is possible
        for self.verify_digests() to return True and self.verify_balance() to return False.

        IMPLEMENTATION NOTES:
        - As above, digests should be computed using digest_from_hash.
        - Assume that digest_from_hash never returns 0. So if a transaction after the first transaction
          has a prev_digest attribute value of 0, this method should return False.
        - Remember the vacuous truth case for universal quantifiers: if there are no transactions,
          this method should return True.
        """

        curr = self.first
        digest = 0

        while curr is not None:
            if curr.prev_digest != digest:
                return False
            digest = digest_from_hash(curr)
            curr = curr.next
        return True

    ###################################################################################################
    # Part 2(c) - Limiting mining and "proof of work"
    ###################################################################################################
    def record_mining_digest_and_nonce(self, miner: str, nonce: int) -> None:
        """Record a new mining transaction with the given miner (i.e., person who is mining) and nonce.

        Use the given nonce to construct the new transaction node.
        Use the two constants MINING_AMOUNT and DIFFICULTY_RATING defined at the top of this file:

            - MINING_AMOUNT determines the number of Titancoins to provide the miner
            - DIFFICULTY_RATING determines the minimum number of zeros the new transaction's digest
              must end with. The digest is computed by digest_from_hash_with_nonce.

        Note: if the provided nonce value does not generate a transaction node with the required number
        of zeros at the end, do NOT add the transaction and instead raise a ValueError.

        Preconditions:
        - miner != ''

        IMPLEMENTATION NOTES (NEW):
        - This method is very similar to the past functions.
        - Make sure to use the two constants MINING_AMOUNT and DIFFICULTY_RATING, and digest
          function digest_from_hash_with_nonce, in your implementation.
        """

        if self.first is None:
            transaction = _Transaction('', miner, MINING_AMOUNT, None, 0, nonce)
            self.first = transaction
            self.last = transaction
        else:
            digest = digest_from_hash_with_nonce(self.last)
            if digest % (10 ** DIFFICULTY_RATING) != 0:
                raise ValueError
            transaction = _Transaction('', miner, MINING_AMOUNT, None, digest, nonce)
            self.last.next = transaction
            self.last = transaction

        if miner not in self._balance:
            self._balance[miner] = MINING_AMOUNT
        else:
            self._balance[miner] = self._balance[miner] + MINING_AMOUNT


###################################################################################################
# Part 2(c) - Limiting mining and "proof of work"
###################################################################################################
def generate_nonce(ledger: Ledger, miner: str) -> int:
    """Return a nonce value for the given miner that will allow the miner to add a new mining transaction.

    There may be more than one valid nonce value to return; just return the first one you find to avoid
    doing extra computation.

    Use the two constants MINING_AMOUNT and DIFFICULTY_RATING defined at the top of this file:

        - MINING_AMOUNT determines the number of Titancoins to provide the miner
        - DIFFICULTY_RATING determines the minimum number of zeros the new transaction's digest
          must end with. The digest is computed by digest_from_hash_with_nonce.

    Hint: You may access ledger.last in this function.

    Preconditions:
    - miner != ''
    """

    zeros = 10 ** DIFFICULTY_RATING
    nonce = 0
    digest = 0 if ledger.last is None else digest_from_hash_with_nonce(ledger.last)
    while True:
        transaction = _Transaction('', miner, MINING_AMOUNT, None, digest, nonce)
        new_digest = digest_from_hash_with_nonce(transaction)
        if new_digest % zeros == 0:
            return nonce
        nonce += 1


###################################################################################################
# Transaction digest functions (don't change this code!)
###################################################################################################
def digest_from_hash(node: _Transaction) -> int:
    """Return a digest for the given node.

    This function has been provided for you, and you should not change it.
    If you're curious, we're using a built-in Python function called hash to
    compute a digest for the node's contents. You'll learn about hash functions
    in CSC263/265.

    You may assume that this function never returns 0.
    """
    data = (node.sender, node.recipient, node.amount, node.prev_digest)
    bytestring = hashlib.sha256(str(data).encode('utf-8')).digest()
    return int.from_bytes(bytestring, byteorder='big')


def digest_from_hash_with_nonce(node: _Transaction) -> int:
    """Return a digest for the given node.

    This function has been provided for you, and you should not change it.
    If you're curious, we're using a built-in Python function called hash to
    compute a digest for the node's contents. You'll learn about hash functions
    in CSC263/265.

    You may assume that this function never returns 0.
    """
    data = (node.sender, node.recipient, node.amount, node.prev_digest, node.nonce)
    bytestring = hashlib.sha256(str(data).encode('utf-8')).digest()
    return int.from_bytes(bytestring, byteorder='big')


###################################################################################################
# Main block
###################################################################################################
if __name__ == '__main__':
    # We have provided the following code to run any doctest examples that you add.
    # (We have not provided any doctest examples in the starter code, but encourage you
    # to add your own.)
    import doctest

    doctest.testmod(verbose=True)

    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (In PyCharm, select the lines below and press Ctrl/Cmd + / to toggle comments.)
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 120,
        'extra-imports': ['hashlib']
    })
