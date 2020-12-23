from unittest import TestCase
from unittest.mock import Mock, call

from psr.controller.game import Game
from psr.core.hand import Hand
from psr.core.result import Result
from psr.player.player import Player
from psr.view.base import PlayerView


class TestGame(TestCase):
    def test_get_result(self):
        self.assertEqual(Result.DRAW, Game.get_result(Hand.PAPER, Hand.PAPER))
        self.assertEqual(Result.DRAW, Game.get_result(Hand.ROCK, Hand.ROCK))
        self.assertEqual(Result.DRAW, Game.get_result(Hand.SCISSOR, Hand.SCISSOR))

        self.assertEqual(Result.WON, Game.get_result(Hand.PAPER, Hand.ROCK))
        self.assertEqual(Result.WON, Game.get_result(Hand.ROCK, Hand.SCISSOR))
        self.assertEqual(Result.WON, Game.get_result(Hand.SCISSOR, Hand.PAPER))

        self.assertEqual(Result.LOST, Game.get_result(Hand.PAPER, Hand.SCISSOR))
        self.assertEqual(Result.LOST, Game.get_result(Hand.ROCK, Hand.PAPER))
        self.assertEqual(Result.LOST, Game.get_result(Hand.SCISSOR, Hand.ROCK))

    def test_play_one_hand(self):
        player1 = Mock(Player)
        player2 = Mock(Player)
        player_view1 = Mock(PlayerView)
        player_view2 = Mock(PlayerView)

        # player1 win
        player1.play.return_value = Hand.ROCK
        player2.play.return_value = Hand.SCISSOR

        game = Game(3, player1, player2, player_view1, player_view2)
        game.play_one_hand(1, 2)

        player1.announce.assert_called_with(Hand.SCISSOR, Result.WON)
        player2.announce.assert_called_with(Hand.ROCK, Result.LOST)
        player_view1.hand_began.assert_called_with(1, 2)
        player_view2.hand_began.assert_called_with(1, 2)
        player_view1.hand_ended.assert_called_with(1, 2, Hand.ROCK, Hand.SCISSOR, Result.WON)
        player_view2.hand_ended.assert_called_with(1, 2, Hand.SCISSOR, Hand.ROCK, Result.LOST)

    def test_play_one_round_with_one_hand(self):
        player1 = Mock(Player)
        player2 = Mock(Player)
        player_view1 = Mock(PlayerView)
        player_view2 = Mock(PlayerView)

        game = Game(3, player1, player2, player_view1, player_view2)

        # player1 win
        game.play_one_hand = Mock(return_value=Result.WON)

        game.play_one_round(2)

        game.play_one_hand.assert_called_with(2, 1)
        player_view1.round_began.assert_called_with(2)
        player_view2.round_began.assert_called_with(2)
        player_view1.round_ended.assert_called_with(2, Result.WON)
        player_view2.round_ended.assert_called_with(2, Result.LOST)

    def test_play_one_round_with_multiple_hands(self):
        player1 = Mock(Player)
        player2 = Mock(Player)
        player_view1 = Mock(PlayerView)
        player_view2 = Mock(PlayerView)

        game = Game(3, player1, player2, player_view1, player_view2)

        # draw twice and then player1 lost
        game.play_one_hand = Mock(side_effect=[Result.DRAW, Result.DRAW, Result.LOST])

        game.play_one_round(2)

        expected_calls = [call(2, 1), call(2, 2), call(2, 3)]
        game.play_one_hand.assert_has_calls(expected_calls)
        player_view1.round_began.assert_called_with(2)
        player_view2.round_began.assert_called_with(2)
        player_view1.round_ended.assert_called_with(2, Result.LOST)
        player_view2.round_ended.assert_called_with(2, Result.WON)

    def test_play_game_fail_zero_round(self):
        player1 = Mock(Player)
        player2 = Mock(Player)
        player_view1 = Mock(PlayerView)
        player_view2 = Mock(PlayerView)

        try:
            Game(0, player1, player2, player_view1, player_view2)
            self.fail("expect AssertionError when rounds == 0")
        except AssertionError:
            pass

    def test_play_game_one_round(self):
        player1 = Mock(Player)
        player2 = Mock(Player)
        player_view1 = Mock(PlayerView)
        player_view2 = Mock(PlayerView)

        game = Game(1, player1, player2, player_view1, player_view2)

        game.play_one_round = Mock(return_value=Result.WON)

        game.play()

        game.play_one_round.assert_called_with(1)
        player_view1.game_began.assert_called_with(1)
        player_view2.game_began.assert_called_with(1)
        player_view1.game_ended.assert_called_with([Result.WON])
        player_view2.game_ended.assert_called_with([Result.LOST])

    def test_play_game_multiple_rounds(self):
        player1 = Mock(Player)
        player2 = Mock(Player)
        player_view1 = Mock(PlayerView)
        player_view2 = Mock(PlayerView)

        game = Game(3, player1, player2, player_view1, player_view2)

        game.play_one_round = Mock(side_effect=[Result.WON, Result.LOST, Result.DRAW])

        game.play()

        expected_calls = [call(1), call(2), call(3)]
        game.play_one_round.assert_has_calls(expected_calls)
        player_view1.game_began.assert_called_with(3)
        player_view2.game_began.assert_called_with(3)
        player_view1.game_ended.assert_called_with([Result.WON, Result.LOST, Result.DRAW])
        player_view2.game_ended.assert_called_with([Result.LOST, Result.WON, Result.DRAW])


class TestGameEndToEnd(TestCase):
    def test_play_real_quick(self):
        player1 = Mock(Player)
        player2 = Mock(Player)
        player_view1 = Mock(PlayerView)
        player_view2 = Mock(PlayerView)

        # one round, player1 immediately win
        player1.play.return_value = Hand.ROCK
        player2.play.return_value = Hand.SCISSOR

        game = Game(1, player1, player2, player_view1, player_view2)
        game.play()

        player1.announce.assert_called_with(Hand.SCISSOR, Result.WON)
        player2.announce.assert_called_with(Hand.ROCK, Result.LOST)
        player_view1.game_began.assert_called_with(1)
        player_view2.game_began.assert_called_with(1)
        player_view1.round_began.assert_called_with(1)
        player_view2.round_began.assert_called_with(1)
        player_view1.hand_began.assert_called_with(1, 1)
        player_view2.hand_began.assert_called_with(1, 1)
        player_view1.hand_ended.assert_called_with(1, 1, Hand.ROCK, Hand.SCISSOR, Result.WON)
        player_view2.hand_ended.assert_called_with(1, 1, Hand.SCISSOR, Hand.ROCK, Result.LOST)
        player_view1.round_ended.assert_called_with(1, Result.WON)
        player_view2.round_ended.assert_called_with(1, Result.LOST)
        player_view1.game_ended.assert_called_with([Result.WON])
        player_view2.game_ended.assert_called_with([Result.LOST])

    def test_play_three_rounds_with_some_draws(self):
        player1 = Mock(Player)
        player2 = Mock(Player)
        player_view1 = Mock(PlayerView)
        player_view2 = Mock(PlayerView)

        # three rounds, 7 hands
        hands = [
            (1, 1, Hand.ROCK, Hand.SCISSOR, Result.WON),
            (2, 1, Hand.ROCK, Hand.ROCK, Result.DRAW),
            (2, 2, Hand.SCISSOR, Hand.SCISSOR, Result.DRAW),
            (2, 3, Hand.PAPER, Hand.PAPER, Result.DRAW),
            (2, 4, Hand.PAPER, Hand.SCISSOR, Result.LOST),
            (3, 1, Hand.SCISSOR, Hand.SCISSOR, Result.DRAW),
            (3, 2, Hand.ROCK, Hand.PAPER, Result.LOST),
        ]
        player1.play.side_effect = [h1 for (_, _, h1, _, _) in hands]
        player2.play.side_effect = [h2 for (_, _, _, h2, _) in hands]

        game = Game(3, player1, player2, player_view1, player_view2)
        game.play()

        expected_calls = [call(h2, r) for (_, _, _, h2, r) in hands]
        player1.announce.assert_has_calls(expected_calls)
        expected_calls = [call(h1, r.opposite()) for (_, _, h1, _, r) in hands]
        player2.announce.assert_has_calls(expected_calls)
        player_view1.game_began.assert_called_with(3)
        player_view2.game_began.assert_called_with(3)
        expected_calls = [call(i) for i in range(1, 4)]
        player_view1.round_began.assert_has_calls(expected_calls)
        player_view2.round_began.assert_has_calls(expected_calls)
        expected_calls = [call(rn, hn) for (rn, hn, _, _, _) in hands]
        player_view1.hand_began.assert_has_calls(expected_calls)
        player_view2.hand_began.assert_has_calls(expected_calls)
        expected_calls = [call(rn, hn, h1, h2, r) for (rn, hn, h1, h2, r) in hands]
        player_view1.hand_ended.assert_has_calls(expected_calls)
        expected_calls = [call(rn, hn, h2, h1, r.opposite()) for (rn, hn, h1, h2, r) in hands]
        player_view2.hand_ended.assert_has_calls(expected_calls)
        last_hands_in_rounds = [hands[0], hands[4], hands[6]]
        expected_calls = [call(rn, r) for (rn, _, _, _, r) in last_hands_in_rounds]
        player_view1.round_ended.assert_has_calls(expected_calls)
        expected_calls = [call(rn, r.opposite()) for (rn, _, _, _, r) in last_hands_in_rounds]
        player_view2.round_ended.assert_has_calls(expected_calls)
        expected_results = [r for (_, _, _, _, r) in last_hands_in_rounds]
        player_view1.game_ended.assert_called_with(expected_results)
        expected_results = [r.opposite() for (_, _, _, _, r) in last_hands_in_rounds]
        player_view2.game_ended.assert_called_with(expected_results)
