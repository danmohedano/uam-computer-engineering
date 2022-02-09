""""
Script to test timings between pruning and no pruning.
Should be used with a modification in strategy.py to print the times or
function calls
"""
from __future__ import annotations

from game import Player, TwoPlayerGameState, TwoPlayerMatch
from heuristic import Heuristic
from reversi import Reversi
from strategy import MinimaxAlphaBetaStrategy, MinimaxStrategy
import datetime
from typing import Sequence
import numpy as np


# Deterministic heuristic
def evaluation_function(state: TwoPlayerGameState) -> float:
    return 127


# Our heuristic
# We copy all this code here because StudentHeuristic is not a compatible
# class with Heuristic and therefore we have to recreate the heuristic here
CORNER_WEIGHT = 10
MOBILITY_WEIGHT = 1


def evaluation_function2(state: TwoPlayerGameState) -> float:
    state_value = 0
    if state.end_of_game:
        scores = state.scores
        # Evaluation of the state from the point of view of MAX

        assert isinstance(scores, (Sequence, np.ndarray))
        score_difference = scores[0] - scores[1]

        if score_difference > 0:
            score_difference += 100
        elif score_difference < 0:
            score_difference -= 100

        if state.is_player_max(state.player1):
            state_value = score_difference
        elif state.is_player_max(state.player2):
            state_value = - score_difference
        else:
            raise ValueError('Player MAX not defined')
    else:
        value = CORNER_WEIGHT * corners(state) + \
                MOBILITY_WEIGHT * mobility(state)

        state_value = value if state.is_player_max(state.player1) else -value

    return state_value


def corners(state: TwoPlayerGameState) -> float:
    """Calculates the corners taken by each player"""
    corners = [state.board.get((1, 1)),
               state.board.get((1, state.game.height)),
               state.board.get((state.game.width, 1)),
               state.board.get((state.game.width, state.game.height))]

    p1 = corners.count(state.player1.label)
    p2 = corners.count(state.player2.label)

    return p1 - p2


def mobility(state: TwoPlayerGameState) -> float:
    """Calculates the difference in mobility between the players"""
    moves_p1 = len(state.game._get_valid_moves(state.board,
                                               state.player1.label))
    moves_p2 = len(state.game._get_valid_moves(state.board,
                                               state.player2.label))

    return moves_p1 - moves_p2


heuristic = Heuristic(name="heuristic",
                      evaluation_function=evaluation_function)

DEPTH = 4
player_minmax1 = Player(name="player1",
                        strategy=MinimaxStrategy(
                            heuristic=heuristic,
                            max_depth_minimax=DEPTH,
                            verbose=0))
player_minmax2 = Player(name="player2",
                        strategy=MinimaxStrategy(
                            heuristic=heuristic,
                            max_depth_minimax=DEPTH,
                            verbose=0))
player_pruning1 = Player(name="player1",
                         strategy=MinimaxAlphaBetaStrategy(
                             heuristic=heuristic,
                             max_depth_minimax=DEPTH,
                             verbose=0))
player_pruning2 = Player(name="player2",
                         strategy=MinimaxAlphaBetaStrategy(
                             heuristic=heuristic,
                             max_depth_minimax=DEPTH,
                             verbose=0))

# Play match with no pruning
print("Match with NO pruning")
player_a, player_b = player_minmax1, player_minmax2

game = Reversi(player1=player_a, player2=player_b, height=8, width=8)
game_state = TwoPlayerGameState(game=game, board=None, initial_player=player_a)
match = TwoPlayerMatch(game_state, max_sec_per_move=1000, gui=False)

start_time = datetime.datetime.now()
match.play_match()
end_time = datetime.datetime.now()
print("FINAL: ", end_time - start_time)

# Play match with pruning
print()
print("Match with pruning")
player_a, player_b = player_pruning1, player_pruning2

game = Reversi(player1=player_a, player2=player_b, height=8, width=8)
game_state = TwoPlayerGameState(game=game, board=None, initial_player=player_a)
match = TwoPlayerMatch(game_state, max_sec_per_move=1000, gui=False)

start_time = datetime.datetime.now()
match.play_match()
end_time = datetime.datetime.now()
print("FINAL: ", end_time - start_time)
