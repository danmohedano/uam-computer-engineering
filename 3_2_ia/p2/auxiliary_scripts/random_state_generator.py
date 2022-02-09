"""Small script to generate random states of a game. Should be used
    with a modification in strategy.py that prints the state after each move

Authors:
    Daniel Mohedano <daniel.mohedano@estudiante.uam.es>
    Silvia Sopeña   <silvia.sopenna@estudiante.uam.es>
"""
from __future__ import annotations

from game import Player, TwoPlayerGameState, TwoPlayerMatch
from heuristic import Heuristic
from reversi import Reversi
from strategy import MinimaxAlphaBetaStrategy
from random import randrange


def evaluation_function(state: TwoPlayerGameState) -> float:
    return randrange(-100, 100.0)


heuristic = Heuristic(name="heuristic",
                      evaluation_function=evaluation_function)

player1 = Player(name="player1",
                 strategy=MinimaxAlphaBetaStrategy(heuristic=heuristic,
                                                   max_depth_minimax=0,
                                                   verbose=0))
player2 = Player(name="player2",
                 strategy=MinimaxAlphaBetaStrategy(heuristic=heuristic,
                                                   max_depth_minimax=0,
                                                   verbose=0))

game = Reversi(player1=player1, player2=player2, height=8, width=8)
game_state = TwoPlayerGameState(game=game, board=None, initial_player=player1)
match = TwoPlayerMatch(game_state, max_sec_per_move=1000, gui=False)

match.play_match()

