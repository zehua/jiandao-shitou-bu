from unittest import TestCase

from psr.core.hand import Hand


class TestHand(TestCase):
    def test_comparison_greater(self):
        self.assertGreater(Hand.SCISSOR, Hand.PAPER)
        self.assertGreater(Hand.PAPER, Hand.ROCK)
        self.assertGreater(Hand.ROCK, Hand.SCISSOR)

        self.assertFalse(Hand.SCISSOR > Hand.SCISSOR)
        self.assertFalse(Hand.SCISSOR > Hand.ROCK)
        self.assertFalse(Hand.PAPER > Hand.PAPER)
        self.assertFalse(Hand.PAPER > Hand.SCISSOR)
        self.assertFalse(Hand.ROCK > Hand.ROCK)
        self.assertFalse(Hand.ROCK > Hand.PAPER)

    def test_comparison_less(self):
        self.assertLess(Hand.PAPER, Hand.SCISSOR)
        self.assertLess(Hand.ROCK, Hand.PAPER)
        self.assertLess(Hand.SCISSOR, Hand.ROCK)

        self.assertFalse(Hand.SCISSOR < Hand.SCISSOR)
        self.assertFalse(Hand.SCISSOR < Hand.PAPER)
        self.assertFalse(Hand.PAPER < Hand.PAPER)
        self.assertFalse(Hand.PAPER < Hand.ROCK)
        self.assertFalse(Hand.ROCK < Hand.ROCK)
        self.assertFalse(Hand.ROCK < Hand.SCISSOR)

    def test_comparison_equal(self):
        self.assertEqual(Hand.PAPER, Hand.PAPER)
        self.assertEqual(Hand.ROCK, Hand.ROCK)
        self.assertEqual(Hand.SCISSOR, Hand.SCISSOR)
