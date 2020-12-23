from psr.core.hand import Hand
from psr.player.strategy.base import Strategy


class RoundRobinStrategy(Strategy):
    def __init__(self, *delegates: Strategy):
        assert len(delegates) > 0
        self.delegates = delegates
        self.cur_delegate = -1

    def next(self) -> Hand:
        self.cur_delegate = (self.cur_delegate + 1) % len(self.delegates)
        return self.delegates[self.cur_delegate].next()

    def record(self, mine: Hand, opponent: Hand):
        assert self.cur_delegate != -1
        self.delegates[self.cur_delegate].record(mine, opponent)