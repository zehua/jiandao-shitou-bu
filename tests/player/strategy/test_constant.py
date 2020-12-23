from unittest import TestCase

from psr.core.hand import Hand
from psr.player.strategy.constant import ConstantStrategy


class TestConstantStrategy(TestCase):
    def test_next(self):
        for hand in Hand:
            for _ in range(10):
                strategy = ConstantStrategy(hand)
                self.assertEqual(hand, strategy.next())
