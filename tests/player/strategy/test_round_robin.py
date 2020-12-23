from unittest import TestCase
from unittest.mock import Mock

from psr.core.hand import Hand
from psr.player.strategy.constant import ConstantStrategy
from psr.player.strategy.round_robin import RoundRobinStrategy


class TestRoundRobinStrategy(TestCase):
    def test_zero_delegates(self):
        try:
            RoundRobinStrategy()
            self.fail()
        except AssertionError:
            pass

    def test_one_delegate(self):
        delegate = Mock()
        delegate.next.side_effect = [Hand.ROCK, Hand.PAPER, Hand.SCISSOR, Hand.SCISSOR]
        strategy = RoundRobinStrategy(delegate)
        self.assertEqual(Hand.ROCK, strategy.next())
        self.assertEqual(Hand.PAPER, strategy.next())
        self.assertEqual(Hand.SCISSOR, strategy.next())
        self.assertEqual(Hand.SCISSOR, strategy.next())

        strategy.record(Hand.ROCK, Hand.SCISSOR)
        delegate.record.assert_called_with(Hand.ROCK, Hand.SCISSOR)
        strategy.record(Hand.SCISSOR, Hand.PAPER)
        delegate.record.assert_called_with(Hand.SCISSOR, Hand.PAPER)

    def test_multiple_delegates(self):
        delegate1 = Mock()
        delegate1.next.side_effect = [Hand.ROCK, Hand.PAPER]
        delegate2 = Mock()
        delegate2.next.side_effect = [Hand.SCISSOR, Hand.ROCK]
        delegate3 = Mock()
        delegate3.next.side_effect = [Hand.PAPER, Hand.SCISSOR]
        strategy = RoundRobinStrategy(delegate1, delegate2, delegate3)

        self.assertEqual(Hand.ROCK, strategy.next())  # from 1
        strategy.record(Hand.ROCK, Hand.SCISSOR)
        delegate1.record.assert_called_with(Hand.ROCK, Hand.SCISSOR)

        self.assertEqual(Hand.SCISSOR, strategy.next())  # from 2
        strategy.record(Hand.SCISSOR, Hand.PAPER)
        delegate2.record.assert_called_with(Hand.SCISSOR, Hand.PAPER)

        self.assertEqual(Hand.PAPER, strategy.next())  # from 3
        strategy.record(Hand.PAPER, Hand.ROCK)
        delegate3.record.assert_called_with(Hand.PAPER, Hand.ROCK)

        self.assertEqual(Hand.PAPER, strategy.next())  # from 1
        strategy.record(Hand.SCISSOR, Hand.SCISSOR)
        delegate1.record.assert_called_with(Hand.SCISSOR, Hand.SCISSOR)

        self.assertEqual(Hand.ROCK, strategy.next())  # from 2
        strategy.record(Hand.PAPER, Hand.SCISSOR)
        delegate2.record.assert_called_with(Hand.PAPER, Hand.SCISSOR)

        self.assertEqual(Hand.SCISSOR, strategy.next())  # from 3
        strategy.record(Hand.SCISSOR, Hand.ROCK)
        delegate3.record.assert_called_with(Hand.SCISSOR, Hand.ROCK)

    def test_record_called_first(self):
        try:
            strategy = RoundRobinStrategy(ConstantStrategy(Hand.SCISSOR))
            strategy.record(Hand.SCISSOR, Hand.ROCK)
            self.fail("Calling record() without next() first should fail.")
        except AssertionError:
            pass
