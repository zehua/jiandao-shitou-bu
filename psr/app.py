import argparse
import sys

from psr.controller.game import Game
from psr.core.hand import Hand
from psr.player.computer import ComputerPlayer
from psr.player.human import ConsolePlayer
from psr.player.strategy.constant import ConstantStrategy
from psr.player.strategy.random import RandomStrategy
from psr.player.strategy.round_robin import RoundRobinStrategy
from psr.view.ascii_art_player import AsciiArtPlayerView
from psr.view.console_player import ConsolePlayerView
from psr.view.noop_player import NoopPlayerView


def main(*args):
    parser = argparse.ArgumentParser(description='Short sample app')
    parser.add_argument('num_of_rounds', type=int)

    parsed = parser.parse_args(*args)

    # player1 = ComputerPlayer(ConstantStrategy(Hand.ROCK))
    player1 = ConsolePlayer()
    player2 = ComputerPlayer(RoundRobinStrategy(
        RandomStrategy(),
        ConstantStrategy(Hand.PAPER),
        ConstantStrategy(Hand.SCISSOR),
        ConstantStrategy(Hand.ROCK),
    ))
    # player_view1 = ConsolePlayerView()
    player_view1 = AsciiArtPlayerView()
    player_view2 = NoopPlayerView()
    game = Game(parsed.num_of_rounds, player1, player2, player_view1, player_view2)
    game.play()


if __name__ == "__main__":
    main(sys.argv[1:])
