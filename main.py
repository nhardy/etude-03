#!/usr/bin/env python3

"""
Author(s): Nathan Hardy
"""

import re
import sys

_SUITES = {
    'Clubs': {
        'string': 'C',
        'weight': 1,
    },
    'Diamonds': {
        'string': 'D',
        'weight': 2,
    },
    'Hearts': {
        'string': 'H',
        'weight': 3,
    },
    'Spades': {
        'string': 'S',
        'weight': 4,
    },
}

_SUITE_MAP = {
    shortcut: suite_name for shortcut, suite_name in [
        *map(lambda s: (s[0].lower(), s), _SUITES.keys()),
        *map(lambda s: (s[0], s), _SUITES.keys()),
    ]
}

class Suite:
    """
    Suite class used for abstraction
    """
    def __init__(self, raw: str):
        self.name = _SUITE_MAP[raw]

    @property
    def weight(self) -> int:
        """
        Relative integer weight for current suite
        """

        return _SUITES[self.name]['weight']

    def __str__(self) -> str:
        return _SUITES[self.name]['string']

    def __eq__(self, other) -> bool:
        return self.weight == other.weight

    def __lt__(self, other) -> bool:
        return self.weight < other.weight

    def __le__(self, other) -> bool:
        return self.weight <= other.weight

    def __gt__(self, other) -> bool:
        return self.weight > other.weight

    def __ge__(self, other) -> bool:
        return self.weight >= other.weight

_CARD_NAMES = {
    1: 'A',
    11: 'J',
    12: 'Q',
    13: 'K',
}

_CARD_NAME_MAP = {
    shortcut: card_value for shortcut, card_value in [
        ('t', 10),
        ('T', 10),
        *map(lambda c: (c[1], c[0]), _CARD_NAMES.items()),
        *map(lambda c: (c[1].lower(), c[0]), _CARD_NAMES.items()),
        *map(lambda n: (str(n), n), range(1, 14))
    ]
}

_CARD_REGEX = re.compile(r'^([1-9]|1[0-3]|[tjqka])([cdhs])$', re.I)

class Card:
    """
    Card class used for abstraction
    """

    def __init__(self, value: int, suite: str):
        self._value = value
        self.suite = Suite(suite)

    @classmethod
    def from_raw(cls, raw: str):
        """
        Will attempt to create an instance of a Card from a given input.
        Returns None if input is invalid
        """

        match = _CARD_REGEX.match(raw)

        if not match:
            return None

        name = match.group(1)
        value = _CARD_NAME_MAP[name]
        suite = match.group(2)

        return cls(value, suite)

    @property
    def _name(self) -> str:
        return str(self._value) if self._value not in _CARD_NAMES else _CARD_NAMES[self._value]

    @property
    def weight(self) -> int:
        """
        Relative integer weight for card number
        """

        return 14 if self._value == 1 else self._value

    def __str__(self) -> str:
        return '{}{}'.format(self._name, self.suite)

    def __eq__(self, other) -> bool:
        return self.weight == other.weight and self.suite == other.suite

    def __lt__(self, other) -> bool:
        return self.weight < other.weight or (
            self.weight == other.weight and self.suite < other.suite
        )

    def __le__(self, other) -> bool:
        return self.weight <= other.weight

    def __gt__(self, other) -> bool:
        return self.weight > other.weight or (
            self.weight == other.weight and self.suite > other.suite
        )

    def __ge__(self, other) -> bool:
        return self.weight >= other.weight

_DELIMITER = re.compile(r'[ /-]')

def contains_duplicates(collection: list):
    """
    Returns whether or not the collection contains duplicates
    """

    current = collection[:]
    while len(current) > 1:
        item, current = current[0], current[1:]
        if any(map(lambda i: i == item, current)):
            return True
    return False

def is_valid_hand(hand: list) -> bool:
    """
    Returns whether or not hand is a valid poker hand
    """

    # If we don't have 5 cards, the hand is invalid
    if len(hand) != 5:
        return False

    # If any of the tokens did not map to a valid card, the hand is invalid
    if any(map(lambda c: c is None, hand)):
        return False

    # If there are duplicate cards, the hand is invalid
    if contains_duplicates(hand):
        return False

    # Otherwise, the hand is valid
    return True

def main():
    """
    Main program method
    """

    for unstripped_line in sys.stdin.readlines():
        line = unstripped_line.strip()
        unique_delimiters = set(_DELIMITER.findall(line))
        raw_cards = _DELIMITER.split(line)
        cards = list(map(Card.from_raw, raw_cards))

        if is_valid_hand(cards) and len(unique_delimiters) == 1:
            print(' '.join(map(str, sorted(cards))))
        else:
            print('Invalid:', line)

if __name__ == '__main__':
    main()
