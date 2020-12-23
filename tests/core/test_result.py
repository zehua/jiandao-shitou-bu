from unittest import TestCase

from psr.core.result import Result


class TestResult(TestCase):
    def test_opposite(self):
        self.assertEqual(Result.WON, Result.LOST.opposite())
        self.assertEqual(Result.LOST, Result.WON.opposite())
        self.assertEqual(Result.DRAW, Result.DRAW.opposite())
