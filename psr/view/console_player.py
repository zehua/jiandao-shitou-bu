import sys
from typing import List, IO

from psr.core.hand import Hand
from psr.core.result import Result
from psr.view.base import PlayerView


class IOPlayerView(PlayerView):
    def __init__(self, out_handle: IO[str]):
        self.out_handle = out_handle

    def game_began(self, number_of_rounds: int):
        self._output(1, f'Game begins (number of rounds: {number_of_rounds})')

    def game_ended(self, results: List[Result]):
        num_rounds = len(results)
        won = len([r for r in results if r == Result.WON])
        lost = len([r for r in results if r == Result.LOST])
        final_result = Result.WON if won > lost else Result.LOST if won < lost else Result.DRAW
        self._output(1, f'Final result after {num_rounds} rounds: {self._get_result_message(final_result)}')
        self._output(1, f'Final score: You ({won}) : Opponent ({lost})')

    def round_began(self, round_number: int):
        self._output(2, f'Round {round_number} begins')

    def round_ended(self, round_number: int, result: Result):
        self._output(2, f'Round {round_number} ends: You {result}')

    def hand_began(self, round_number: int, hand_number: int):
        self._output(3, 'Get ready to start...')

    def hand_ended(self, round_number: int, hand_number: int, mine: Hand, opponent: Hand, result: Result):
        self._output(3, f'You played {mine}')
        self._output(3, f'Opponent played {opponent}')
        self._output(3, self._get_result_message(result))
        if hand_number == 5:
            self._output(3, 'This game is getting intensive.')
        elif hand_number == 10:
            self._output(3, 'Come on! You can do it!')

    @staticmethod
    def _get_result_message(result):
        return f"You {result.value}!" if result != Result.DRAW else "It's a draw."

    @staticmethod
    def _decorate(level: int, message: str) -> str:
        level_indicator = '=' * (level + 2)
        return f'{level_indicator} {message} {level_indicator}'

    def _output(self, level: int, message: str):
        self.out_handle.write(self._decorate(level, message))
        self.out_handle.write('\n')
        self.out_handle.flush()


class ConsolePlayerView(IOPlayerView):
    def __init__(self):
        super().__init__(sys.stdout)
