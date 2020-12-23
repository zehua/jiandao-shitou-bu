from io import StringIO
from unittest import TestCase

from psr.core.result import Result
from psr.view.console_player import IOPlayerView


class TestIOPlayerView(TestCase):
    def test_get_result_message(self):
        self.assertEqual("You won!", IOPlayerView._get_result_message(Result.WON))
        self.assertEqual("You lost!", IOPlayerView._get_result_message(Result.LOST))
        self.assertEqual("It's a draw.", IOPlayerView._get_result_message(Result.DRAW))

    def test_game_ended(self):
        data = [
            ([Result.WON, Result.WON, Result.WON], "You won!", 3, 0),
            ([Result.WON, Result.WON, Result.LOST], "You won!", 2, 1),
            ([Result.LOST, Result.WON, Result.LOST], "You lost!", 1, 2),
            ([Result.LOST, Result.LOST, Result.LOST], "You lost!", 0, 3),
            ([Result.WON, Result.LOST], "It's a draw.", 1, 1),
            ([Result.WON, Result.LOST, Result.DRAW], "It's a draw.", 1, 1),
            ([Result.WON], "You won!", 1, 0),
            ([Result.LOST], "You lost!", 0, 1),
        ]

        for results, message, won, lost in data:
            out_handle = StringIO()
            view = IOPlayerView(out_handle)
            view.game_ended(results)

            num_rounds = len(results)
            expected = f'=== Final result after {num_rounds} rounds: {message} ===\n' + \
                       f'=== Final score: You ({won}) : Opponent ({lost}) ===\n'
            self.assertEqual(expected, out_handle.getvalue())
