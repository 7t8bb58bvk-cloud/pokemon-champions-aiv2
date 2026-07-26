
from copy import deepcopy

from engine.turn_engine import TurnEngine
from engine.evaluation_engine import EvaluationEngine


class DummyAction:
    action_type = "move"
    priority = 0

    def __init__(self, move):
        self.move = move


class SearchEngine:

    @staticmethod
    def _terminal_score(player, opponent):
        if player.current_hp <= 0 and opponent.current_hp <= 0:
            return 0

        if opponent.current_hp <= 0:
            return 10**6

        if player.current_hp <= 0:
            return -10**6

        return EvaluationEngine.evaluate(player, opponent)

    @staticmethod
    def minimax(player, opponent, depth, maximizing, alpha=-10**9, beta=10**9):

        if depth == 0 or player.current_hp <= 0 or opponent.current_hp <= 0:
            return SearchEngine._terminal_score(player, opponent)

        if maximizing:
            value = -10**9
            moves = player.moves or []

            if not moves:
                return SearchEngine._terminal_score(player, opponent)

            for move in moves:
                sim_player = deepcopy(player)
                sim_opponent = deepcopy(opponent)

                TurnEngine.execute_move(
                    sim_player,
                    sim_opponent,
                    DummyAction(move),
                )

                score = SearchEngine.minimax(
                    sim_player,
                    sim_opponent,
                    depth - 1,
                    False,
                    alpha,
                    beta,
                )

                value = max(value, score)
                alpha = max(alpha, value)

                if beta <= alpha:
                    break

            return value

        value = 10**9
        moves = opponent.moves or []

        if not moves:
            return SearchEngine._terminal_score(player, opponent)

        for move in moves:
            sim_player = deepcopy(player)
            sim_opponent = deepcopy(opponent)

            TurnEngine.execute_move(
                sim_opponent,
                sim_player,
                DummyAction(move),
            )

            score = SearchEngine.minimax(
                sim_player,
                sim_opponent,
                depth - 1,
                True,
                alpha,
                beta,
            )

            value = min(value, score)
            beta = min(beta, value)

            if beta <= alpha:
                break

        return value

    @staticmethod
    def choose_best_move(player, opponent, depth=2):

        best_move = None
        best_score = -10**9

        moves = player.moves or []

        for move in moves:
            sim_player = deepcopy(player)
            sim_opponent = deepcopy(opponent)

            TurnEngine.execute_move(
                sim_player,
                sim_opponent,
                DummyAction(move),
            )

            score = SearchEngine.minimax(
                sim_player,
                sim_opponent,
                depth - 1,
                False,
            )

            if score > best_score:
                best_score = score
                best_move = move

        return {
            "move": best_move,
            "score": best_score,
        }


print("✅ search_engine.py V7 Ready")
