#!/usr/bin/env python3

import re
import sys

_SUITES = {
    'Clubs': {
        'repr': 'C',
        'weight': 1,
    },
    'Diamonds': {
        'repr': 'D',
        'weight': 2,
    },
    'Hearts': {
        'repr': 'H',
        'weight': 3,
    },
    'Spades': {
        'repr': 'S',
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
    def __init__(self, raw: str):
        self.name = _SUITE_MAP[raw]

    @property
    def weight(self) -> int:
        return _SUITES[self.name]['weight']

    def __str__(self) -> str:
        return _SUITES[self.name]['repr']

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

_CARD_REGEX = re.compile(r'^([1-9]|1[0-3]|t|j|q|k|a)(c|d|h|s)$', re.I)

class Card:
    def __init__(self, value: int, suite: str):
        self._value = value
        self.suite = Suite(suite)

    @classmethod
    def from_raw(cls, raw: str):
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
        return 14 if self._value == 1 else self._value

    def __str__(self) -> str:
        return '{}{}'.format(self._name, self.suite)

    def __eq__(self, other) -> bool:
        return self.weight == other.weight and self.suite == other.suite

    def __lt__(self, other) -> bool:
        return self.weight < other.weight or (self.weight == other.weight and self.suite < other.suite)

    def __le__(self, other) -> bool:
        return self.weight <= other.weight

    def __gt__(self, other) -> bool:
        return self.weight > other.weight or (self.weight == other.weight and self.suite > other.suite)

    def __ge__(self, other) -> bool:
        return self.weight >= other.weight

_DELIMITER = re.compile(r'[ /-]')

def is_valid_hand(hand: list) -> bool:
    if len(hand) != 5:
        return False

    if any(map(lambda c: c is None, hand)):
        return False

    # TODO: More Validation checks?

    return True

def main():
    for unstripped_line in sys.stdin.readlines():
        line = unstripped_line.strip()
        raw_cards = _DELIMITER.split(line)
        cards = list(map(Card.from_raw, raw_cards))
        if is_valid_hand(cards):
            print(' '.join(map(str, sorted(cards))))
        else:
            print('Invalid:', line)

if __name__ == '__main__':
    main()
