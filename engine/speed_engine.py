
from __future__ import annotations

from typing import Optional

from battle.battle_state import BattleState
from battle.pokemon import Pokemon


BOOST_TABLE = {
    -6: 2 / 8,
    -5: 2 / 7,
    -4: 2 / 6,
    -3: 2 / 5,
    -2: 2 / 4,
    -1: 2 / 3,
     0: 1.0,
     1: 3 / 2,
     2: 4 / 2,
     3: 5 / 2,
     4: 6 / 2,
     5: 7 / 2,
     6: 8 / 2,
}


class SpeedEngine:

    @staticmethod
    def boost_multiplier(stage: int) -> float:
        stage = max(-6, min(6, int(stage)))
        return BOOST_TABLE[stage]

    @classmethod
    def effective_speed(cls, pokemon: Pokemon) -> int:

        speed = getattr(pokemon, "speed", 100)

        stage = 0
        if hasattr(pokemon, "boosts"):
            stage = pokemon.boosts.get("spe", 0)

        speed *= cls.boost_multiplier(stage)

        item = getattr(pokemon, "item", None)
        if item == "choice scarf":
            speed *= 1.5
        elif item == "iron ball":
            speed *= 0.5

        status = getattr(pokemon, "status", None)
        ability = getattr(pokemon, "ability", None)

        if status == "par" and ability != "quick feet":
            speed *= 0.5

        return int(speed)

    @classmethod
    def move_order(
        cls,
        state: BattleState,
    ):

        p1 = state.get_active_player()
        p2 = state.get_active_opponent()

        s1 = cls.effective_speed(p1)
        s2 = cls.effective_speed(p2)

        trick_room = state.field.trick_room

        if trick_room:
            if s1 < s2:
                return "player", "opponent"
            elif s2 < s1:
                return "opponent", "player"
        else:
            if s1 > s2:
                return "player", "opponent"
            elif s2 > s1:
                return "opponent", "player"

        return "speed_tie"

    @classmethod
    def summary(
        cls,
        state: BattleState,
    ):

        p = state.get_active_player()
        o = state.get_active_opponent()

        return {
            "player_speed": cls.effective_speed(p),
            "opponent_speed": cls.effective_speed(o),
            "order": cls.move_order(state),
            "trick_room": state.field.trick_room,
        }


print("✅ speed_engine.py Ready")
