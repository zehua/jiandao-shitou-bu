import itertools
from unittest import TestCase
from unittest.mock import Mock

from psr.core.hand import Hand
from psr.core.result import Result
from psr.player.computer import ComputerPlayer


class TestComputerPlayer(TestCase):
    def test_play(self):
        for hand in Hand:
            strategy = Mock()
            strategy.next.return_value = hand

            player = ComputerPlayer(strategy)

            self.assertEqual(hand, player.play())
            strategy.next.assert_called()

    def test_announce(self):
        for mine, opponent in itertools.product(Hand, Hand):
            strategy = Mock()
            strategy.next.return_value = mine

            player = ComputerPlayer(strategy)
            player.play()
            player.announce(opponent, Result.WON)

            strategy.record.assert_called_with(mine, opponent)
