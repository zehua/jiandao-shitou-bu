from psr.core.result import Result
from psr.player.player import Player
from psr.view.base import PlayerView


class Game(object):
    def __init__(self, rounds: int, player1: Player, player2: Player, player_view1: PlayerView,
                 player_view2: PlayerView):
        assert rounds > 0
        self.rounds = rounds
        self.player1 = player1
        self.player2 = player2
        self.player_view1 = player_view1
        self.player_view2 = player_view2

    def play(self):
        """
        Play the game with the number of rounds specified in self.rounds.
        """
        results = []
        self.player_view1.game_began(self.rounds)
        self.player_view2.game_began(self.rounds)
        for round_number in range(1, self.rounds + 1):
            result = self.play_one_round(round_number)
            results.append(result)
        self.player_view1.game_ended(results)
        self.player_view2.game_ended([r.opposite() for r in results])

    def play_one_round(self, round_number: int) -> Result:
        """
        Play one or more rounds until getting a non draw result.
        """
        self.player_view1.round_began(round_number)
        self.player_view2.round_began(round_number)
        hand_number = 0
        while True:
            hand_number += 1
            result = self.play_one_hand(round_number, hand_number)
            if result != Result.DRAW:
                self.player_view1.round_ended(round_number, result)
                self.player_view2.round_ended(round_number, result.opposite())
                return result

    def play_one_hand(self, round_number: int, hand_number: int) -> Result:
        """
        Play a round and return the result for player1 against player2.
        :return:
        """
        self.player_view1.hand_began(round_number, hand_number)
        self.player_view2.hand_began(round_number, hand_number)

        hand1 = self.player1.play()
        hand2 = self.player2.play()

        result = self.get_result(hand1, hand2)

        self.player1.announce(hand2, result)
        self.player2.announce(hand1, result.opposite())

        self.player_view1.hand_ended(round_number, hand_number, hand1, hand2, result)
        self.player_view2.hand_ended(round_number, hand_number, hand2, hand1, result.opposite())

        return result

    @staticmethod
    def get_result(hand1, hand2) -> Result:
        if hand1 == hand2:
            return Result.DRAW
        elif hand1 > hand2:
            return Result.WON
        else:
            return Result.LOST
