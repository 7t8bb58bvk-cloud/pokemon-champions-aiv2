
from __future__ import annotations

from battle.battle_state import BattleState
from battle.action import ACTION_MOVE
from engine.speed_engine import SpeedEngine
from engine.damage_engine import DamageEngine


class SimulationEngine:

    @staticmethod
    def execute_turn(
        state: BattleState,
        player_action,
        opponent_action,
    ):

        order = SpeedEngine.move_order(state)

        if order == "speed_tie":
            order = ("player", "opponent")

        for side in order:

            if state.is_over():
                break

            if side == "player":
                action = player_action
                attacker = state.get_active_player()
                defender = state.get_active_opponent()
            else:
                action = opponent_action
                attacker = state.get_active_opponent()
                defender = state.get_active_player()

            if action.action_type != ACTION_MOVE:
                continue

            if action.move is None:
                continue

            damage = DamageEngine.apply_damage(
                attacker,
                defender,
                action.move,
            )

            state._record({
                "event": "damage",
                "side": side,
                "move": action.move.name,
                "damage": damage,
                "target_hp": defender.current_hp,
            })

        state.next_turn()

        return state

    @staticmethod
    def simulate(
        state,
        player_action,
        opponent_action,
    ):

        copied = state.clone()

        SimulationEngine.execute_turn(
            copied,
            player_action,
            opponent_action,
        )

        return copied


print("✅ simulation_engine.py Ready")
