
from copy import deepcopy

from battle.action import Action
from battle.action import ACTION_MOVE
from battle.action import ACTION_SWITCH

from engine.turn_engine import TurnEngine
from engine.evaluation_engine import EvaluationEngine


class SearchEngine:

    @staticmethod
    def generate_actions(side):

        actions = []

        # 技
        for move in side.active.moves:
            actions.append(
                Action(
                    action_type=ACTION_MOVE,
                    move=move,
                )
            )

        # 交代
        for i, pokemon in enumerate(side.team):

            if pokemon is side.active:
                continue

            if pokemon.current_hp <= 0:
                continue

            actions.append(
                Action(
                    action_type=ACTION_SWITCH,
                    switch_index=i,
                )
            )

        return actions

    @staticmethod
    def choose_best_action(player_side, opponent_side):

        best_action = None
        best_score = -999999

        actions = SearchEngine.generate_actions(player_side)

        for action in actions:

            sim_player = deepcopy(player_side)
            sim_opponent = deepcopy(opponent_side)

            if action.action_type == ACTION_SWITCH:

                sim_player.switch(
                    action.switch_index,
                )

            else:

                TurnEngine.execute_move(
                    sim_player.active,
                    sim_opponent.active,
                    action,
                )

            score = EvaluationEngine.evaluate(
                sim_player.active,
                sim_opponent.active,
            )

            if score > best_score:
                best_score = score
                best_action = action

        return {
            "action": best_action,
            "score": best_score,
        }


print("✅ search_engine.py V9 Ready")
