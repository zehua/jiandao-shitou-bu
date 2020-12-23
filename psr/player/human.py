import sys
from io import StringIO
from typing import IO

from psr.core.hand import Hand
from psr.core.result import Result
from psr.player.player import Player


class NoopIO(StringIO):
    """
    Convenient class to avoid boilerplate of `if not None` checks
    """

    def write(self, __text: str) -> int:
        pass

    def flush(self) -> None:
        pass


class IOPlayer(Player):
    """
    A player that takes input from and sends output to io
    """

    def __init__(self, in_handle: IO[str], out_handle: IO[str] = None):
        self.in_handle = in_handle
        self.out_handle = out_handle if out_handle else NoopIO()

    def play(self) -> Hand:
        for i in range(3, 0, -1):
            self._output('Please enter your hand (Valid choices: P, S, R): ')
            hand = self.in_handle.readline().strip()
            try:
                return Hand(hand)
            except ValueError as e:
                extra_message = ' Try again.' if i > 1 else ''
                self._output(f'"{hand}" is not a valid hand.{extra_message}\n')

        self.out_handle.flush()
        raise Exception('Too many failed attempts to enter a hand!')

    def announce(self, opponent: Hand, result: Result) -> None:
        pass

    def _output(self, message):
        self.out_handle.write(message)
        self.out_handle.flush()


class ConsolePlayer(IOPlayer):
    """
    A player that uses std io.
    """

    def __init__(self):
        super().__init__(sys.stdin, sys.stdout)
