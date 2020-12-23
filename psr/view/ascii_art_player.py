import sys
from typing import List

from psr.core.hand import Hand
from psr.core.result import Result
from psr.view.console_player import IOPlayerView

SCISSOR_STR = """
  *     *
   *   *
    * *
 ***   **
*        *
 **      *
   *****
"""

PAPER_STR = """
        *
   *    *   *
*    *  *  *   *
   *   * *   *
     **   **
    *       *
    ** *** *
"""

ROCK_STR = """

    * * * *
  ** * * * *
 *          *
 ***       *
    ******

"""

WON_STR = """


          *
 *      *
  *   *
    *

"""

LOST_STR = """

   *     *
    *  *
     *
   *  *
 *     *

"""

DRAW_STR = """


 ======

 ======


"""

TWO_SPACES_STR = """
  






"""


class AsciiArt(object):
    """
    A class representing a simple fixed-height ascii art.
    """

    def __init__(self, data: List[str]):
        assert len(data) > 0
        # right pad with space to fixed length for all rows
        max_length = max([len(line) for line in data])
        self.data = [line + (' ' * (max_length - len(line))) for line in data]

    @staticmethod
    def from_str(data: str):
        split_data = data.split('\n')
        assert len(split_data) > 1
        # strip off first line which is empty due to """
        return AsciiArt(split_data[1:])

    def __add__(self, other):
        if isinstance(other, AsciiArt):
            self_size = len(self.data)
            other_size = len(other.data)
            if self_size == other_size:
                # concat row by row
                return AsciiArt([l + r for (l, r) in zip(self.data, other.data)])
            else:
                raise NotImplementedError(f'Unable to add AsciiArt of size {self_size} with that of size {other_size}')
        raise NotImplementedError(f'Unable to add {type(other)} with AsciiArt')

    def __str__(self):
        return '\n'.join(self.data)


HAND_TO_ASCII_ART = {
    Hand.ROCK: AsciiArt.from_str(ROCK_STR),
    Hand.PAPER: AsciiArt.from_str(PAPER_STR),
    Hand.SCISSOR: AsciiArt.from_str(SCISSOR_STR),
}

RESULT_TO_ASCII_ART = {
    Result.WON: AsciiArt.from_str(WON_STR),
    Result.LOST: AsciiArt.from_str(LOST_STR),
    Result.DRAW: AsciiArt.from_str(DRAW_STR),
}

TWO_SPACES = AsciiArt.from_str(TWO_SPACES_STR)


class AsciiArtIOPlayerView(IOPlayerView):
    """
    A player view that uses ascii art for rendering the hands played and result
    """

    def hand_ended(self, round_number: int, hand_number: int, mine: Hand, opponent: Hand, result: Result):
        ascii_art = HAND_TO_ASCII_ART[mine] + TWO_SPACES + \
                    RESULT_TO_ASCII_ART[result] + TWO_SPACES + \
                    HAND_TO_ASCII_ART[opponent]
        self._output(5, f'Result for round {round_number} hand {hand_number}:')
        self.out_handle.write(f'\n{ascii_art}\n')
        self.out_handle.flush()


class AsciiArtPlayerView(AsciiArtIOPlayerView):
    def __init__(self):
        super().__init__(sys.stdout)
