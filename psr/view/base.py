from abc import ABC, abstractmethod
from typing import List

from psr.core.hand import Hand
from psr.core.result import Result


class PlayerView(ABC):
    @abstractmethod
    def game_began(self, number_of_rounds: int):
        """
        To be invoked before the game begins.
        Could be used to render any info at the beginning of the game.
        :param number_of_rounds: number of round in the game
        """
        pass

    @abstractmethod
    def game_ended(self, results: List[Result]):
        """
        To be invoked after the game ends.
        Could be used to render any info at the end of the game.
        :param results: the results of all rounds from the player's point of view.
        """
        pass

    @abstractmethod
    def round_began(self, round_number: int):
        """
        To be invoked before each round begins.
        Could be used to render any info at the beginning of each round.
        Note that each round could consist of more than one shows of hand, as there might be draws.
        :param round_number: the current round number. 1 based.
        """
        pass

    @abstractmethod
    def round_ended(self, round_number: int, result: Result):
        """
        To be invoked after each round ends.
        Could be used to render any info at the end of each round.
        :param round_number: the current round number. 1 based.
        :param result: the result of the round from the player's point of view.
        """
        pass

    @abstractmethod
    def hand_began(self, round_number: int, hand_number: int):
        """
        To be invoked before each show of hand by both players within the rounds.
        Could be used to render any info at the beginning of each show of hand.
        :param round_number: the current round number. 1 based.
        :param hand_number: the current hand number within the current round. 1 based.
        """
        pass

    @abstractmethod
    def hand_ended(self, round_number: int, hand_number: int, mine: Hand, opponent: Hand, result: Result):
        """
        To be invoked after each show of hand by both players within the rounds.
        Could be used to render any info at the end of each show of hand.
        :param round_number: the current round number. 1 based.
        :param hand_number: the current hand number within the current round. 1 based.
        :param mine: the hand played by the current player.
        :param opponent: the hand played by the opponent player.
        :param result: the result of the current show of hand, from the player's point of view.
        """
        pass
