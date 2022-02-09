"""Illustration of tournament.

Authors:
    Alejandro Bellogin <alejandro.bellogin@uam.es>

"""

from __future__ import annotations  # For Python 3.7

import datetime

from game import Player, TwoPlayerGameState, TwoPlayerMatch
from heuristic import complex_evaluation_function
from reversi import Reversi
from tournament import StudentHeuristic, Tournament

import designed_heuristics

myheuristics = __import__("2391_p2_02_mohedano_sopeña")


class Heuristic1(StudentHeuristic):

    def get_name(self) -> str:
        return "dummy"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        # Use an auxiliary function.
        return self.dummy(123)

    def dummy(self, n: int) -> int:
        return n + 4


class BaseHeuristic(StudentHeuristic):

    def get_name(self) -> str:
        return "base"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        return complex_evaluation_function(state)


def create_match(player1: Player, player2: Player) -> TwoPlayerMatch:
    initial_board = None
    initial_player = player1

    game = Reversi(
        player1=player1,
        player2=player2,
        height=8,
        width=8
    )

    game_state = TwoPlayerGameState(
        game=game,
        board=initial_board,
        initial_player=initial_player,
    )

    return TwoPlayerMatch(game_state, max_sec_per_move=1000, gui=False)


tour = Tournament(max_depth=3, init_match=create_match)
strats = {'base': [BaseHeuristic], 'maxpieces': [designed_heuristics.MaximizePieces],
          'sol4': [designed_heuristics.Solution4],
          'sol5': [designed_heuristics.Solution5],
          'sol6': [designed_heuristics.Solution6]}

n = 1
start_time = datetime.datetime.now()
scores, totals, names = tour.run(
    student_strategies=strats,
    increasing_depth=False,
    n_pairs=n,
    allow_selfmatch=False,
)
end_time = datetime.datetime.now()

print('Time of execution: ', end_time-start_time)

print(
    'Results for tournament where each game is repeated '
    + '%d=%dx2 times, alternating colors for each player' % (2 * n, n),
)

# print(totals)
# print(scores)

print('\ttotal:', end='')
for name1 in names:
    print('\t%s' % (name1), end='')
print()
for name1 in names:
    print('%s\t%d:' % (name1, totals[name1]), end='')
    for name2 in names:
        if name1 == name2:
            print('\t---', end='')
        else:
            print('\t%d' % (scores[name1][name2]), end='')
    print()
