import random
from typing import Set
from unittest import TestCase
from unittest.mock import patch, Mock

from psr.core.hand import Hand
from psr.player.strategy.random import RandomStrategy


class TestRandomStrategy(TestCase):
    @patch.object(random, 'choice')
    def test_next_patched(self, mocked_choice: Mock):
        strategy = RandomStrategy()
        for hand in Hand:
            mocked_choice.return_value = hand
            self.assertEqual(hand, strategy.next())

    def test_next_random(self):
        strategy = RandomStrategy()
        valid_hands = set(Hand)
        for _ in range(10):
            self._assertSetContains(valid_hands, strategy.next())

    def _assertSetContains(self, expected_set: Set[Hand], actual_item: Hand):
        self.assertTrue(actual_item in expected_set, f'{actual_item} NOT in expected set {expected_set}')
