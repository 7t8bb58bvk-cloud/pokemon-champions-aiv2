
from battle.action import ACTION_MOVE, ACTION_SWITCH

from engine.damage_engine import DamageEngine
from engine.effect_engine import EffectEngine


class TurnEngine:

    @staticmethod
    def get_priority(action):

        if action.action_type == ACTION_SWITCH:
            return 6

        if action.action_type == ACTION_MOVE:
            return action.priority

        return 0

    @staticmethod
    def decide_order(player_action, opponent_action, player_speed, opponent_speed):

        p_prio = TurnEngine.get_priority(player_action)
        o_prio = TurnEngine.get_priority(opponent_action)

        if p_prio > o_prio:
            return ["player", "opponent"]

        if o_prio > p_prio:
            return ["opponent", "player"]

        if player_speed > opponent_speed:
            return ["player", "opponent"]

        if opponent_speed > player_speed:
            return ["opponent", "player"]

        return ["player", "opponent"]

    @staticmethod
    def execute_switch(side, action):

        ok = side.switch(action.target)

        return {
            "action": "switch",
            "success": ok,
            "active": side.active.name,
        }

    @staticmethod
    def execute_move(attacker, defender, action):

        if attacker.current_hp <= 0:
            return {
                "user": attacker.name,
                "result": "fainted",
            }

        damage = DamageEngine.calculate(
            attacker,
            defender,
            action.move,
        )

        defender.current_hp = max(
            0,
            defender.current_hp - damage,
        )

        effect = EffectEngine.apply(
            attacker,
            defender,
            action.move,
        )

        return {
            "action": "move",
            "user": attacker.name,
            "target": defender.name,
            "move": action.move,
            "damage": damage,
            "effect": effect,
            "remaining_hp": defender.current_hp,
        }

    @staticmethod
    def execute_action(
        side,
        opponent_side,
        action,
    ):

        if action.action_type == ACTION_SWITCH:

            return TurnEngine.execute_switch(
                side,
                action,
            )

        return TurnEngine.execute_move(
            side.active,
            opponent_side.active,
            action,
        )


print("✅ turn_engine.py V7 Ready")
