"""File with all the designed heuristics. For the final heuristics, refer to
    2391_p2_02_mohedano_sopeña.py

Authors:
    Daniel Mohedano <daniel.mohedano@estudiante.uam.es>
    Silvia Sopeña   <silvia.sopenna@estudiante.uam.es>
"""

from game import TwoPlayerGameState
from typing import Sequence
import numpy as np
from tournament import StudentHeuristic


class MaximizePieces(StudentHeuristic):
    def get_name(self) -> str:
        return "MaximizePieces"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        state_value = 0
        if state.end_of_game:
            scores = state.scores
            # Evaluation of the state from the point of view of MAX

            assert isinstance(scores, (Sequence, np.ndarray))
            score_difference = scores[0] - scores[1]

            if state.is_player_max(state.player1):
                state_value = score_difference
            elif state.is_player_max(state.player2):
                state_value = - score_difference
            else:
                raise ValueError('Player MAX not defined')
        else:
            # Count the number of pieces
            player1_count = 0
            player2_count = 0
            for x in state.board.values():
                if x == state.player1.label:
                    player1_count += 1
                else:
                    player2_count += 1

            # Calculate difference
            piece_difference = player1_count - player2_count
            if state.is_player_max(state.player1):
                state_value = piece_difference
            elif state.is_player_max(state.player2):
                state_value = - piece_difference

        return state_value


class MinimizePieces(StudentHeuristic):
    def get_name(self) -> str:
        return "MinimizePieces"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        state_value = 0
        if state.end_of_game:
            scores = state.scores
            # Evaluation of the state from the point of view of MAX

            assert isinstance(scores, (Sequence, np.ndarray))
            score_difference = scores[0] - scores[1]

            if state.is_player_max(state.player1):
                state_value = score_difference
            elif state.is_player_max(state.player2):
                state_value = - score_difference
            else:
                raise ValueError('Player MAX not defined')
        else:
            # Count the number of pieces
            player1_count = 0
            player2_count = 0
            for x in state.board.values():
                if x == state.player1.label:
                    player1_count += 1
                else:
                    player2_count += 1

            # Calculate difference
            piece_difference = player1_count - player2_count
            if state.is_player_max(state.player1):
                state_value = - piece_difference
            elif state.is_player_max(state.player2):
                state_value = piece_difference

        return state_value


class DifferenceInOptions(StudentHeuristic):
    def get_name(self) -> str:
        return "DifferenceInOptions"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        state_value = 0
        if state.end_of_game:
            scores = state.scores
            # Evaluation of the state from the point of view of MAX

            assert isinstance(scores, (Sequence, np.ndarray))
            score_difference = scores[0] - scores[1]

            if state.is_player_max(state.player1):
                state_value = score_difference
            elif state.is_player_max(state.player2):
                state_value = - score_difference
            else:
                raise ValueError('Player MAX not defined')
        else:
            n_successors = len(state.game.generate_successors(state))

            # Depending on depth, max your options or min your opponent's
            # options
            if state.is_player_max(state.player1):
                if state.next_player == state.player1:
                    state_value = n_successors
                else:
                    state_value = -n_successors
            elif state.is_player_max(state.player2):
                if state.next_player == state.player2:
                    state_value = n_successors
                else:
                    state_value = -n_successors

        return state_value


class Solution4(StudentHeuristic):
    """ Coin parity """

    def get_name(self) -> str:
        return "2391_02_04"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
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
            # Count the number of pieces
            player1_count = 0
            player2_count = 0
            for x in state.board.values():
                if x == state.player1.label:
                    player1_count += 1
                else:
                    player2_count += 1

            # Calculate difference
            piece_difference = 100 * (player1_count - player2_count) / \
                (player1_count + player2_count)
            if state.is_player_max(state.player1):
                state_value = piece_difference
            elif state.is_player_max(state.player2):
                state_value = - piece_difference

        return state_value


class Solution5(StudentHeuristic):
    """ Mobility """

    def get_name(self) -> str:
        return "2391_02_05"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
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
            # Count the number of pieces
            mobility_value = state.game._choice_diff(state.board)

            if state.is_player_max(state.player1):
                state_value = mobility_value
            elif state.is_player_max(state.player2):
                state_value = - mobility_value

        return state_value


class Solution6(StudentHeuristic):
    """ Corners """

    def get_name(self) -> str:
        return "2391_02_06"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
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
            # Count the number of pieces
            corner_value = state.game._corner_diff(state.board)

            if state.is_player_max(state.player1):
                state_value = corner_value
            elif state.is_player_max(state.player2):
                state_value = - corner_value

        return state_value


class Solution7(StudentHeuristic):
    """ Corners and parity """
    CORNER_WEIGHT = 100
    PARITY_WEIGHT = 10

    def get_name(self) -> str:
        return "2391_02_07"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        state_value = 0
        if state.end_of_game:
            scores = state.scores
            # Evaluation of the state from the point of view of MAX

            assert isinstance(scores, (Sequence, np.ndarray))
            score_difference = scores[0] - scores[1]

            if score_difference > 0:
                score_difference += 110
            elif score_difference < 0:
                score_difference -= 110

            if state.is_player_max(state.player1):
                state_value = score_difference
            elif state.is_player_max(state.player2):
                state_value = - score_difference
            else:
                raise ValueError('Player MAX not defined')
        else:
            value = self.CORNER_WEIGHT * self.corners(state) + \
                    self.PARITY_WEIGHT * self.parity(state)

            state_value = value if state.is_player_max(state.player1) \
                else -value

        return state_value

    def parity(self, state: TwoPlayerGameState) -> float:
        """Calculates the coin parity in the state"""
        # Count the number of pieces
        player1_count = 0
        player2_count = 0
        for x in state.board.values():
            if x == state.player1.label:
                player1_count += 1
            else:
                player2_count += 1

        # Calculate difference
        return (player1_count - player2_count) / \
               (player1_count + player2_count)

    def corners(self, state: TwoPlayerGameState) -> float:
        """Calculates the corners taken by each player"""
        corners = [state.board.get((1, 1)),
                   state.board.get((1, state.game.height)),
                   state.board.get((state.game.width, 1)),
                   state.board.get((state.game.width, state.game.height))]

        p1 = corners.count(state.player1.label)
        p2 = corners.count(state.player2.label)

        return (p1 - p2) / (p1 + p2) if (p1 + p2) != 0 else 0


class Solution8(StudentHeuristic):
    """ Corners, edges and parity """
    CORNER_WEIGHT = 1000
    EDGE_WEIGHT = 100
    PARITY_WEIGHT = 10

    def get_name(self) -> str:
        return "2391_02_08"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        state_value = 0
        if state.end_of_game:
            scores = state.scores
            # Evaluation of the state from the point of view of MAX

            assert isinstance(scores, (Sequence, np.ndarray))
            score_difference = scores[0] - scores[1]

            if score_difference > 0:
                score_difference += 1110
            elif score_difference < 0:
                score_difference -= 1110

            if state.is_player_max(state.player1):
                state_value = score_difference
            elif state.is_player_max(state.player2):
                state_value = - score_difference
            else:
                raise ValueError('Player MAX not defined')
        else:
            value = self.CORNER_WEIGHT * self.corners(state) + \
                    self.PARITY_WEIGHT * self.parity(state) + \
                    self.EDGE_WEIGHT * self.edges(state)

            state_value = value if state.is_player_max(state.player1) \
                else -value

        return state_value

    def parity(self, state: TwoPlayerGameState) -> float:
        """Calculates the coin parity in the state"""
        # Count the number of pieces
        player1_count = 0
        player2_count = 0
        for x in state.board.values():
            if x == state.player1.label:
                player1_count += 1
            else:
                player2_count += 1

        # Calculate difference
        return (player1_count - player2_count) / \
               (player1_count + player2_count)

    def corners(self, state: TwoPlayerGameState) -> float:
        """Calculates the corners taken by each player"""
        corners = [state.board.get((1, 1)),
                   state.board.get((1, state.game.height)),
                   state.board.get((state.game.width, 1)),
                   state.board.get((state.game.width, state.game.height))]

        p1 = corners.count(state.player1.label)
        p2 = corners.count(state.player2.label)

        return (p1 - p2) / (p1 + p2) if (p1 + p2) != 0 else 0

    def edges(self, state: TwoPlayerGameState) -> float:
        """Calculates the edges taken by each player"""
        edges = []
        height = state.game.height
        width = state.game.width
        for i in range(3, height - 1):
            edges.append(state.board.get(i, 1))
            edges.append(state.board.get(i, height))
            edges.append(state.board.get(1, i))
            edges.append(state.board.get(width, i))

        p1 = edges.count(state.player1.label)
        p2 = edges.count(state.player2.label)

        return (p1 - p2) / (p1 + p2) if (p1 + p2) != 0 else 0


class Solution9(StudentHeuristic):
    """ Static board values """
    VALUES = [[4, -3, 2, 2, 2, 2, -3, 4],
              [-3, -4, -1, -1, -1, -1, -4, -3],
              [2, -1, 1, 0, 0, 1, -1, 2],
              [2, -1, 0, 1, 1, 0, -1, 2],
              [2, -1, 0, 1, 1, 0, -1, 2],
              [2, -1, 1, 0, 0, 1, -1, 2],
              [-3, -4, -1, -1, -1, -1, -4, -3],
              [4, -3, 2, 2, 2, 2, -3, 4]]

    def get_name(self) -> str:
        return "2391_02_09"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        state_value = 0
        if state.end_of_game:
            scores = state.scores
            # Evaluation of the state from the point of view of MAX

            assert isinstance(scores, (Sequence, np.ndarray))
            score_difference = scores[0] - scores[1]

            if score_difference > 0:
                score_difference += 1110
            elif score_difference < 0:
                score_difference -= 1110

            if state.is_player_max(state.player1):
                state_value = score_difference
            elif state.is_player_max(state.player2):
                state_value = - score_difference
            else:
                raise ValueError('Player MAX not defined')
        else:
            p1 = 0
            p2 = 0
            for i in range(state.game.width):
                for ii in range(state.game.height):
                    if state.board.get((i, ii)) == state.player1.label:
                        p1 += self.VALUES[i][ii]
                    elif state.board.get((i, ii)) == state.player2.label:
                        p2 += self.VALUES[i][ii]

            value = p1 - p2
            state_value = value if state.is_player_max(state.player1) \
                else -value

        return state_value


class Solution10(StudentHeuristic):
    """ Corners and parity without normalization """
    CORNER_WEIGHT = 15
    PARITY_WEIGHT = 1

    def get_name(self) -> str:
        return "2391_02_10"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
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
            value = self.CORNER_WEIGHT * self.corners(state) + \
                    self.PARITY_WEIGHT * self.parity(state)

            state_value = value if state.is_player_max(state.player1) \
                else -value

        return state_value

    def parity(self, state: TwoPlayerGameState) -> float:
        """Calculates the coin parity in the state"""
        # Count the number of pieces
        player1_count = 0
        player2_count = 0
        for x in state.board.values():
            if x == state.player1.label:
                player1_count += 1
            else:
                player2_count += 1

        # Calculate difference
        return player1_count - player2_count

    def corners(self, state: TwoPlayerGameState) -> float:
        """Calculates the corners taken by each player"""
        corners = [state.board.get((1, 1)),
                   state.board.get((1, state.game.height)),
                   state.board.get((state.game.width, 1)),
                   state.board.get((state.game.width, state.game.height))]

        p1 = corners.count(state.player1.label)
        p2 = corners.count(state.player2.label)

        return p1 - p2


class Solution11(StudentHeuristic):
    """ Corners parity and mobility """
    CORNER_WEIGHT = 1000
    MOBILITY_WEIGHT = 100
    PARITY_WEIGHT = 1

    def get_name(self) -> str:
        return "2391_02_11"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        state_value = 0
        if state.end_of_game:
            scores = state.scores
            # Evaluation of the state from the point of view of MAX

            assert isinstance(scores, (Sequence, np.ndarray))
            score_difference = scores[0] - scores[1]

            if score_difference > 0:
                score_difference += 4000
            elif score_difference < 0:
                score_difference -= 4000

            if state.is_player_max(state.player1):
                state_value = score_difference
            elif state.is_player_max(state.player2):
                state_value = - score_difference
            else:
                raise ValueError('Player MAX not defined')
        else:
            value = self.CORNER_WEIGHT * self.corners(state) + \
                    self.PARITY_WEIGHT * self.parity(state) + \
                    self.MOBILITY_WEIGHT * self.mobility(state)

            state_value = value if state.is_player_max(state.player1) \
                else -value

        return state_value

    def parity(self, state: TwoPlayerGameState) -> float:
        """Calculates the coin parity in the state"""
        # Count the number of pieces
        player1_count = 0
        player2_count = 0
        for x in state.board.values():
            if x == state.player1.label:
                player1_count += 1
            else:
                player2_count += 1

        # Calculate difference
        return player1_count - player2_count

    def corners(self, state: TwoPlayerGameState) -> float:
        """Calculates the corners taken by each player"""
        corners = [state.board.get((1, 1)),
                   state.board.get((1, state.game.height)),
                   state.board.get((state.game.width, 1)),
                   state.board.get((state.game.width, state.game.height))]

        p1 = corners.count(state.player1.label)
        p2 = corners.count(state.player2.label)

        return p1 - p2

    def mobility(self, state: TwoPlayerGameState) -> float:
        """Calculates the difference in mobility between the players"""
        moves_p1 = len(state.game._get_valid_moves(state.board,
                                                   state.player1.label))
        moves_p2 = len(state.game._get_valid_moves(state.board,
                                                   state.player2.label))

        return moves_p1 - moves_p2


class Solution12(StudentHeuristic):
    """ Corners and mobility """
    CORNER_WEIGHT = 10
    MOBILITY_WEIGHT = 1

    def get_name(self) -> str:
        return "2391_02_12"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
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
            value = self.CORNER_WEIGHT * self.corners(state) + \
                    self.MOBILITY_WEIGHT * self.mobility(state)

            state_value = value if state.is_player_max(state.player1) \
                else -value

        return state_value

    def corners(self, state: TwoPlayerGameState) -> float:
        """Calculates the corners taken by each player"""
        corners = [state.board.get((1, 1)),
                   state.board.get((1, state.game.height)),
                   state.board.get((state.game.width, 1)),
                   state.board.get((state.game.width, state.game.height))]

        p1 = corners.count(state.player1.label)
        p2 = corners.count(state.player2.label)

        return p1 - p2

    def mobility(self, state: TwoPlayerGameState) -> float:
        """Calculates the difference in mobility between the players"""
        moves_p1 = len(state.game._get_valid_moves(state.board,
                                                   state.player1.label))
        moves_p2 = len(state.game._get_valid_moves(state.board,
                                                   state.player2.label))

        return moves_p1 - moves_p2


class Solution13(StudentHeuristic):
    """ Corners parity and mobility """
    CORNER_WEIGHT = 1000
    MOBILITY_WEIGHT = 100
    EDGE_WEIGHT = 10
    PARITY_WEIGHT = 1

    def get_name(self) -> str:
        return "2391_02_13"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        state_value = 0
        if state.end_of_game:
            scores = state.scores
            # Evaluation of the state from the point of view of MAX

            assert isinstance(scores, (Sequence, np.ndarray))
            score_difference = scores[0] - scores[1]

            if score_difference > 0:
                score_difference += 5000
            elif score_difference < 0:
                score_difference -= 5000

            if state.is_player_max(state.player1):
                state_value = score_difference
            elif state.is_player_max(state.player2):
                state_value = - score_difference
            else:
                raise ValueError('Player MAX not defined')
        else:
            value = self.CORNER_WEIGHT * self.corners(state) + \
                    self.PARITY_WEIGHT * self.parity(state) + \
                    self.MOBILITY_WEIGHT * self.mobility(state) + \
                    self.EDGE_WEIGHT * self.edges(state)

            state_value = value if state.is_player_max(state.player1) \
                else -value

        return state_value

    def parity(self, state: TwoPlayerGameState) -> float:
        """Calculates the coin parity in the state"""
        # Count the number of pieces
        player1_count = 0
        player2_count = 0
        for x in state.board.values():
            if x == state.player1.label:
                player1_count += 1
            else:
                player2_count += 1

        # Calculate difference
        return player1_count - player2_count

    def corners(self, state: TwoPlayerGameState) -> float:
        """Calculates the corners taken by each player"""
        corners = [state.board.get((1, 1)),
                   state.board.get((1, state.game.height)),
                   state.board.get((state.game.width, 1)),
                   state.board.get((state.game.width, state.game.height))]

        p1 = corners.count(state.player1.label)
        p2 = corners.count(state.player2.label)

        return p1 - p2

    def mobility(self, state: TwoPlayerGameState) -> float:
        """Calculates the difference in mobility between the players"""
        moves_p1 = len(state.game._get_valid_moves(state.board,
                                                   state.player1.label))
        moves_p2 = len(state.game._get_valid_moves(state.board,
                                                   state.player2.label))

        return moves_p1 - moves_p2

    def edges(self, state: TwoPlayerGameState) -> float:
        """Calculates the edges taken by each player"""
        edges = []
        height = state.game.height
        width = state.game.width
        for i in range(3, height - 1):
            edges.append(state.board.get(i, 1))
            edges.append(state.board.get(i, height))
            edges.append(state.board.get(1, i))
            edges.append(state.board.get(width, i))

        p1 = edges.count(state.player1.label)
        p2 = edges.count(state.player2.label)

        return p1 - p2
