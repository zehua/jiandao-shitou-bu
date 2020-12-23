from typing import List

from psr.core.hand import Hand
from psr.core.result import Result
from psr.view.base import PlayerView


class NoopPlayerView(PlayerView):
    def game_began(self, number_of_rounds: int):
        pass

    def game_ended(self, results: List[Result]):
        pass

    def round_began(self, round_number: int):
        pass

    def round_ended(self, round_number: int, result: Result):
        pass

    def hand_began(self, round_number: int, hand_number: int):
        pass

    def hand_ended(self, round_number: int, hand_number: int, mine: Hand, opponent: Hand, result: Result):
        pass