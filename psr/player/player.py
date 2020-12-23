from abc import ABC, abstractmethod

from psr.core.hand import Hand
from psr.core.result import Result


class Player(ABC):
    """
    A player for playing the game.
    """

    @abstractmethod
    def play(self) -> Hand:
        """
        Returns the next hand to play.
        """
        pass

    @abstractmethod
    def announce(self, opponent: Hand, result: Result) -> None:
        """
        Receives announcement of the result from the past show of hand.
        :param opponent: what the opponent just played
        :param result: the result of the show of hand with respect to the player. i.e., WON means the player won.
        """
        pass
