from abc import ABC, abstractmethod

from psr.core.hand import Hand


class Strategy(ABC):
    """
    A strategy for playing hands, optionally based on historical data.
    """

    @abstractmethod
    def next(self) -> Hand:
        """
        Decides what to return in the next play.
        """
        pass

    @abstractmethod
    def record(self, mine: Hand, opponent: Hand):
        """
        Records what was played by the strategy and the opponent.
        The recorded info could be used to determine what's to be played next.
        """
        pass

