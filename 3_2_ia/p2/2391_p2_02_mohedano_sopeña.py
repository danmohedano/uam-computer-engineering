from typing import Sequence
import numpy as np
from game import (
    TwoPlayerGameState,
)
from tournament import (
    StudentHeuristic,
)


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
