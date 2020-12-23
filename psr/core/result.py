from enum import Enum


class Result(Enum):
    WON = 'won'
    LOST = 'lost'
    DRAW = 'draw'

    _ignore_ = ['_OPPOSITES']
    _OPPOSITES = {}

    def __str__(self):
        return self.value

    def opposite(self):
        return self._OPPOSITES[self]


Result._OPPOSITES = {
    Result.DRAW: Result.DRAW,
    Result.WON: Result.LOST,
    Result.LOST: Result.WON
}
