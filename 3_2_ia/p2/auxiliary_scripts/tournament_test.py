"""Tournament modification to test multiple heuristics with multiple states.

    To use: just add heuristics to the 'strats' dictionary and select in MAX_STATES
    the amount of different initial states that should be used. For a cleaner representation,
    heuristic's names should be 4 characters long.

Authors:
    Daniel Mohedano <daniel.mohedano@estudiante.uam.es>
    Silvia Sopeña   <silvia.sopenna@estudiante.uam.es>
"""

from __future__ import annotations  # For Python 3.7
from game import Player, TwoPlayerGameState, TwoPlayerMatch
from heuristic import complex_evaluation_function
from reversi import Reversi, from_array_to_dictionary_board
from tournament import StudentHeuristic, Tournament

import designed_heuristics


class BaseHeuristic(StudentHeuristic):

    def get_name(self) -> str:
        return "base"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        return complex_evaluation_function(state)


# All randomly generated states to test heuristics
STATES = [['........', '........', '........', '...WB...', '...BW...', '........', '........', '........'],
          ['....W...', '..WBWB..', '...BW...', '...BW...', '.BBBW...', '..B.....', '........', '........'],
          ['.BW.W...', '..WWWB..', '.BWWW...', 'BBWWW...', 'WBWWW...', '..B.WB..', '........', '........'],
          ['WWW.WW..', '..WWWWWW', '.BBBBB..', 'BBBBBB..', 'WBWBW.B.', '..B.WW.B', '....WB..', '........'],
          ['WWW.WWB.', '..WWWWBW', 'WWWWBBW.', 'WWWWWWWW', 'WBWWWBW.', '.WBBWW.B', '....WWB.', '......W.'],
          ['WWW.WWB.', '.BWWWWWW', 'WBBWBBWW', 'WBWBBBWW', 'WBBWBBW.', '.BWBWB.B', 'B..WWWWW', '..BBBBWW'],
          ['........', '.....B..', '.WB.B...', '.WWBW...', '..WWB...', '.B.W.B..', '........', '........'],
          ['....B.W.', 'B...BW..', '.BB.BW..', 'BBBBW...', '..BWB...', '.WWB.B..', 'WW.B....', '........'],
          ['....B.W.', 'B.WBBBW.', '.BB.BBW.', 'BBWBW.W.', '.BBBB.W.', '.WWWWWW.', 'WW.W....', '....W...'],
          ['W..BB.W.', 'WWBBBBW.', 'WBW.BBBB', 'BWWWW.B.', 'BWWBW.WB', '.WWWWWW.', 'WWWW....', 'BW..W...'],
          ['W.WBB.WB', 'WWWWWWWW', 'WBWBBBBB', 'WWWWB.B.', 'WWWBWBBB', 'WWWWBBBB', 'WWWWW.W.', 'BW..WW..'],
          ['........', '.BBBB...', '..BWB...', '...WWW..', '..WBB...', '.....B..', '........', '........'],
          ['..W.....', '.BBWB...', '.BWWW.B.', 'WWBWWB..', '..WWB...', '.BWWBB..', '........', '........'],
          ['WWW.....', 'WWBBBB..', 'WBWWB.B.', 'WBBWWB..', '.WBWWW..', '.WWBWWW.', '.WB.....', '........'],
          ['WWW.....', 'WWBBBB.W', 'WBWWB.W.', 'WWBWBW..', '.BWWWBB.', 'BBBWBWBB', '.WW.WB..', '..W..WWW'],
          ['WWWW.W..', 'WWWBWW.W', 'WWWWBWB.', 'WWBBBW.B', '.WWBWWB.', 'BBWBBWWB', 'BWBBBW.W', 'WBBB.WWW'],
          ['........', '....B...', '....B...', '.WWWBB..', 'WWWWB...', '...W....', '...W....', '........'],
          ['........', '...WB...', '..W.BB..', '.WWBBBBB', 'WWWWWW..', '..WWW...', '..WB....', '...B....'],
          ['...WB...', '...BW.W.', 'WWB.BWWW', 'BWWBWBWB', 'BBWWBW..', 'B.BBW...', '..BB....', '.B.B....'],
          ['...WWW..', '..BWWBBB', 'WWWWBBBB', 'BWWWWBWB', 'BBWWWWBB', 'B.WWW..B', '.WWWW...', '.B.B....'],
          ['.BBWWWW.', '.BBBWWWB', 'WBWBWBWB', 'BBWWBBWB', 'BBBBWBWB', 'BWWBW.BB', '.BWWW..B', 'BB.BWB..'],
          ['........', '........', '..BW....', '..BBW...', '..WBBW..', '.WB..BW.', '.....B..', '........'],
          ['........', '.BW.B...', '.WBWWW..', '..WBW...', '.BBWBB..', '.BW..BB.', 'BW...B.B', '........'],
          ['.B..W...', '.BB.W...', '.WBBWWW.', 'W.WBBWB.', 'BBWBWB..', '.BWW.BB.', 'BBW..B.B', '.B......'],
          ['.B..WB..', 'BBB.B...', 'WWWWWWW.', 'W.BBBWW.', 'WWWBBWW.', 'WBWBBBB.', 'WBBB.B.B', 'WBB.W...'],
          ['BBWWWB..', 'BBBWW..B', 'WWWBBWBB', 'WWWWWBB.', 'WWWBWBWW', 'WBWWWWWB', 'WWWWWW.B', 'WBB.W...']]

# Heuristics to be tested
strats = {'C___': [designed_heuristics.Solution6],
          'CMP_': [designed_heuristics.Solution11],
          'CM__': [designed_heuristics.Solution12],
          'CMEP': [designed_heuristics.Solution13],
          }

# User defined constants
HEURISTICS = len(strats)
MAX_STATES = 21
DEPTH = 3

# System defined variables & constants
MATCH = 0
MAX = HEURISTICS * (HEURISTICS - 1)


def create_match(player1: Player, player2: Player) -> TwoPlayerMatch:
    global MATCH
    initial_player = player1

    game = Reversi(
        player1=player1,
        player2=player2,
        height=8,
        width=8
    )

    game_state = TwoPlayerGameState(
        game=game,
        board=from_array_to_dictionary_board(STATES[MATCH // MAX]),
        initial_player=initial_player,
    )

    MATCH += 1

    return TwoPlayerMatch(game_state, max_sec_per_move=1000, gui=False)


tour = Tournament(max_depth=DEPTH, init_match=create_match)

n = 1

FINAL_RESULTS = {}
SCORES = {}

for heur in strats:
    FINAL_RESULTS[heur] = 0
    SCORES[heur] = {}
    for h2 in strats:
        SCORES[heur][h2] = 0

for i in range(MAX_STATES):
    scores, totals, names = tour.run(
        student_strategies=strats,
        increasing_depth=False,
        n_pairs=n,
        allow_selfmatch=False,
    )

    print('Results for tournament')
    print('State: ', STATES[(MATCH // MAX) - 1])

    print('\ttotal:', end='')
    for name1 in names:
        print('\t%s' % (name1[:4]), end='')
    print()
    for name1 in names:
        print('%s\t%d:' % (name1[:4], totals[name1]), end='')
        FINAL_RESULTS[name1[:4]] += totals[name1]
        for name2 in names:
            if name1 == name2:
                print('\t---', end='')
            else:
                print('\t%d' % (scores[name1][name2]), end='')
                SCORES[name1[:4]][name2[:4]] += scores[name1][name2]
        print()

print("---------------------------------------------------------")
print("Final results of tournament. DEPTH=", DEPTH, ", HEURISTICS=", HEURISTICS, ", STATES=", MAX_STATES)
print('\ttotal:', end='')
for name1 in strats:
    print('\t%s' % (name1[:4]), end='')
print()
for name1 in strats:
    print('%s\t%d:' % (name1, FINAL_RESULTS[name1]), end='')
    for name2 in strats:
        if name1 == name2:
            print('\t---', end='')
        else:
            print('\t%d' % (SCORES[name1][name2]), end='')
    print()
