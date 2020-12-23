import itertools
import sys
from io import StringIO
from unittest import TestCase
from unittest.mock import patch, Mock, MagicMock

from psr.core.hand import Hand
from psr.core.result import Result
from psr.player.human import IOPlayer, ConsolePlayer


def _strings(*args: str, separator: str = ''):
    return separator.join(args)


def _lines(*args: str):
    return _strings(*args, separator='\n')


class TestIOPlayer(TestCase):

    def test_play_good_hand(self):
        for hand in Hand:
            outputs = StringIO()
            player = IOPlayer(StringIO(hand.value), outputs)
            self.assertEqual(hand, player.play())
            self.assertEqual('Please enter your hand (Valid choices: P, S, R): ', outputs.getvalue())

    def test_play_bad_hand(self):
        inputs = _lines('p', 'S')
        player = IOPlayer(StringIO(inputs))
        self.assertEqual(Hand.SCISSOR, player.play())

        inputs = _lines('', 'S')
        player = IOPlayer(StringIO(inputs))
        self.assertEqual(Hand.SCISSOR, player.play())

        inputs = _lines('ABCDEFG', 'S')
        player = IOPlayer(StringIO(inputs))
        self.assertEqual(Hand.SCISSOR, player.play())

        inputs = _lines('p', 's', 'S')
        player = IOPlayer(StringIO(inputs))
        self.assertEqual(Hand.SCISSOR, player.play())

        # too many failed attempts
        inputs = _lines('p', 's', 'r', 'S')
        player = IOPlayer(StringIO(inputs))
        try:
            player.play()
        except Exception as e:
            self.assertEqual(('Too many failed attempts to enter a hand!',), e.args)

    def test_play_bad_hand_with_output(self):
        inputs = _lines('p', 'S')
        outputs = StringIO()
        player = IOPlayer(StringIO(inputs), outputs)
        self.assertEqual(Hand.SCISSOR, player.play())
        expected_output = _strings(
            'Please enter your hand (Valid choices: P, S, R): ',
            '"p" is not a valid hand. Try again.\n',
            'Please enter your hand (Valid choices: P, S, R): '
        )
        self.assertEqual(expected_output, outputs.getvalue())

        inputs = _lines('p', 's', 'S')
        outputs = StringIO()
        player = IOPlayer(StringIO(inputs), outputs)
        self.assertEqual(Hand.SCISSOR, player.play())
        expected_output = _strings(
            'Please enter your hand (Valid choices: P, S, R): ',
            '"p" is not a valid hand. Try again.\n',
            'Please enter your hand (Valid choices: P, S, R): ',
            '"s" is not a valid hand. Try again.\n',
            'Please enter your hand (Valid choices: P, S, R): '
        )
        self.assertEqual(expected_output, outputs.getvalue())

        # too many failed attempts
        inputs = _lines('p', 's', 'r', 'S')
        outputs = StringIO()
        player = IOPlayer(StringIO(inputs), outputs)
        try:
            player.play()
        except Exception as e:
            self.assertEqual(('Too many failed attempts to enter a hand!',), e.args)
        expected_output = _strings(
            'Please enter your hand (Valid choices: P, S, R): ',
            '"p" is not a valid hand. Try again.\n',
            'Please enter your hand (Valid choices: P, S, R): ',
            '"s" is not a valid hand. Try again.\n',
            'Please enter your hand (Valid choices: P, S, R): ',
            '"r" is not a valid hand.\n'
        )
        self.assertEqual(expected_output, outputs.getvalue())


class TestConsolePlayer(TestCase):
    @patch.object(sys, "stdout", create=True)
    @patch.object(sys, "stdin", create=True)
    def test_play(self, stdin: Mock, stdout: MagicMock):
        player = ConsolePlayer()
        stdin.readline.return_value = 'S'
        self.assertEqual(Hand.SCISSOR, player.play())
        stdout.write.assert_called_with('Please enter your hand (Valid choices: P, S, R): ')
