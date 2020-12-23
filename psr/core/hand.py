from enum import Enum


class Hand(Enum):
    _ignore_ = ['_WIN']

    PAPER = 'P'
    SCISSOR = 'S'
    ROCK = 'R'

    _WIN = {}

    def __gt__(self, other) -> bool:
        if isinstance(other, Hand):
            if self._WIN[self] == other:
                return True
            return False
        raise NotImplementedError(f'Unable to compare {type(other)} with Hand')

    def __lt__(self, other) -> bool:
        if isinstance(other, Hand):
            if self._WIN[other] == self:
                return True
            return False
        raise NotImplementedError(f'Unable to compare {type(other)} with Hand')

    def __str__(self):
        return self.name.capitalize()


Hand._WIN = {
    Hand.PAPER: Hand.ROCK,
    Hand.SCISSOR: Hand.PAPER,
    Hand.ROCK: Hand.SCISSOR
}
