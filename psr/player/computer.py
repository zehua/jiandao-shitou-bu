from psr.core.hand import Hand
from psr.core.result import Result
from psr.player.player import Player
from psr.player.strategy.base import Strategy


class ComputerPlayer(Player):
    def __init__(self, strategy: Strategy):
        self.strategy = strategy
        self.last_hand: Hand = None

    def play(self) -> Hand:
        self.last_hand = self.strategy.next()
        return self.last_hand

    def announce(self, opponent: Hand, result: Result) -> None:
        self.strategy.record(self.last_hand, opponent)
