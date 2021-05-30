#!/usr/bin/env python3
"""
module string
"""

__author__ = "Joost Langeveld"
__license__ = "MIT"

MINOR_SUITS = ['C', 'D']
MAJOR_SUITS = ['H', 'S']
NT_SUIT = 'N'
SUIT_ORDER = [*MINOR_SUITS, *MAJOR_SUITS, NT_SUIT]

DOUBLED_STATUS_ORDER = ['', 'x', 'xx']


class SimpleContract:
    _suit: str
    _level: int
    _doubled_status: str

    def __init__(self, suit: str, level: int, doubled_status: str):
        self._suit = suit.upper()
        self._level = level
        self._doubled_status = doubled_status

    def __str__(self):
        result = f'SimpleContract(suit={self._suit},level={self._level}'
        if self._doubled_status:
            result += f'doubled_status={self._doubled_status}'
        result += ')'
        return result

    def __repr__(self):
        return self.__str__()

    @property
    def suit(self) -> str:
        return self._suit

    @property
    def level(self) -> int:
        return self._level

    @property
    def doubled_status(self) -> str:
        return self._doubled_status

    def __eq__(self, other):
        if not isinstance(other, SimpleContract):
            return False
        return self.suit == other.suit and self.level == other.level and self.doubled_status == other.doubled_status

    def __lt__(self, other):
        if not isinstance(other, SimpleContract):
            raise ValueError('other is wrong type:' + other)
        if not self.level == other.level:
            return self.level < other.level
        if not self.suit == other.suit:
            return SUIT_ORDER.index(self.suit) < SUIT_ORDER.index(other.suit)
        return DOUBLED_STATUS_ORDER.index(self.doubled_status) < DOUBLED_STATUS_ORDER.index(other.doubled_status)

    def is_part_score(self) -> bool:
        if self.suit in MINOR_SUITS:
            return self.level <= 4
        elif self.suit in MAJOR_SUITS:
            return self.level <= 3
        elif self.suit == NT_SUIT:
            return self.level <= 2

    def is_game(self) -> bool:
        if self.suit in ('C', 'D'):
            return self.level == 5
        elif self.suit in ('H', 'S'):
            return self.level in (4, 5)
        elif self.suit == 'N':
            return self.level in (3, 4, 5)

    def is_slam(self) -> bool:
        return self.level == 6

    def is_grand_slam(self) -> bool:
        return self.level == 7

    def level_type(self) -> str:
        if self.is_grand_slam():
            return 'grand_slam'
        elif self.is_slam():
            return 'slam'
        elif self.is_game():
            return 'game'
        elif self.is_part_score():
            return 'part_score'
        else:
            return 'all_passed_???'

    def is_minor_suit(self) -> bool:
        return self.suit in ('C', 'D')

    def is_major_suit(self) -> bool:
        return self.suit in ('H', 'S')

    def is_no_trump_suit(self) -> bool:
        return self.suit == 'N'

    def suit_type(self) -> str:
        if self.is_no_trump_suit():
            return 'no_trump'
        elif self.is_major_suit():
            return 'major'
        elif self.is_major_suit():
            return 'minor'
        else:
            return 'all_passed_???'

    def is_equivalent(self, other_contract: object) -> bool:
        """2 clubs is equivalent to 3 clubs if made and same number of tricks"""
        if not isinstance(other_contract, SimpleContract):
            raise ValueError('is_equivalent: other_contract of wrong type: ' + other_contract)
        if self.level_type() != other_contract.level_type():
            return False
        return self.suit == other_contract.suit

    def is_equivalent_scoring(self, other_contract: object) -> bool:
        """2 clubs scores equivalently to 3 diamonds if made and same number of tricks"""
        if not isinstance(other_contract, SimpleContract):
            raise ValueError('is_equivalent: other_contract of wrong type: ' + other_contract)
        if self.level_type() != other_contract.level_type():
            return False
        return self.suit_type() == other_contract.suit_type()


class ContractWithDeclarer(SimpleContract):
    _declarer: str

    def __init__(self, suit: str, level: int, doubled_status: str, declarer: str):
        super().__init__(suit, level, doubled_status)
        self._declarer = declarer

    def __str__(self):
        result = f'ContractWithDeclarer(declarer={self._declarer}, suit={self._suit}, level={self._level}'
        if self._doubled_status:
            result += f', doubled_status={self._doubled_status}'
        result += f')'
        return result

    def __repr__(self):
        return self.__str__()


class ContractFactory:
    @staticmethod
    def parse_simple_contract_string(contract_string: str) -> list:
        parse_contract_string = contract_string
        if parse_contract_string[-2:] == DOUBLED_STATUS_ORDER[2]:
            doubled_status = DOUBLED_STATUS_ORDER[2]
        elif parse_contract_string[-1:] == DOUBLED_STATUS_ORDER[1]:
            doubled_status = DOUBLED_STATUS_ORDER[1]
        else:
            doubled_status = DOUBLED_STATUS_ORDER[0]
        parse_contract_string = parse_contract_string.replace(doubled_status, '')

        suit = parse_contract_string[-1]
        parse_contract_string = parse_contract_string[:-1]

        return [SimpleContract(suit, int(a_level_string), doubled_status)
                for a_level_string in parse_contract_string]

    @staticmethod
    def convert_declarer_and_simple_contract(declarer: str, simple_contract: SimpleContract) -> ContractWithDeclarer:
        return ContractWithDeclarer(suit=simple_contract.suit,
                                    level=simple_contract.level,
                                    doubled_status=simple_contract.doubled_status,
                                    declarer=declarer)

    @staticmethod
    def convert_contract_string(contract_string: str) -> list:
        """"returns list of ContractWithDeclarer"""
        result = []
        for singular_contract_string in contract_string.split(','):
            declarers = singular_contract_string.split(' ')[0]
            simple_contract_string = singular_contract_string.split(' ')[1]
            simple_contracts = ContractFactory.parse_simple_contract_string(simple_contract_string)
            result += [ContractFactory.convert_declarer_and_simple_contract(declarer=declarer,
                                                                            simple_contract=simple_contract)
                       for simple_contract in simple_contracts
                       for declarer in declarers]
        return result
