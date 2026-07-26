
from battle.action import ACTION_MOVE
from battle.action import ACTION_SWITCH


class TurnEngine:

    @staticmethod
    def execute(state, player_action, opponent_action):

        log = []

        # -------------------------
        # Player
        # -------------------------

        if player_action.action_type == ACTION_SWITCH:

            state.player_side.switch(
                player_action.switch_index,
            )

            log.append(
                {
                    "side": "player",
                    "action": "switch",
                    "active": state.player.name,
                }
            )

        # -------------------------
        # Opponent
        # -------------------------

        if opponent_action.action_type == ACTION_SWITCH:

            state.opponent_side.switch(
                opponent_action.switch_index,
            )

            log.append(
                {
                    "side": "opponent",
                    "action": "switch",
                    "active": state.opponent.name,
                }
            )

        state.next_turn()

        return log


print("✅ turn_engine.py BattleState Ready")
