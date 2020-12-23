from psr.core.hand import Hand
from psr.player.strategy.base import Strategy


class ConstantStrategy(Strategy):
    """
    A strategy that always returns the same hand.
    """

    def __init__(self, hand: Hand):
        self.hand = hand

    def next(self) -> Hand:
        return self.hand

    def record(self, mine: Hand, opponent: Hand):
        pass
