import random

from psr.core.hand import Hand
from psr.player.strategy.base import Strategy


class RandomStrategy(Strategy):
    """
    A strategy that randomly returns a hand.
    """

    def next(self) -> Hand:
        return random.choice(list(Hand))

    def record(self, mine: Hand, opponent: Hand):
        pass
