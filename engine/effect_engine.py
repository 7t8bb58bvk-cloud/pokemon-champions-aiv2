
from __future__ import annotations

import random

from data.move_effect_database import get_move_effect


class EffectEngine:

    @staticmethod
    def apply(attacker, defender, move_name, force=False):

        effect = get_move_effect(move_name)

        if effect is None:
            return None

        triggered = force or (random.random() < effect.chance)

        if not triggered:
            return None

        # 能力ダウン
        if effect.effect == "stat_drop":

            defender.add_boost(
                effect.stat,
                effect.stages,
            )

            return {
                "effect": "stat_drop",
                "stat": effect.stat,
                "stages": effect.stages,
            }

        # やけど
        if effect.effect == "burn":

            if defender.status is None:
                defender.status = "burn"

            return {
                "effect": "burn",
            }

        # まひ
        if effect.effect == "paralysis":

            if defender.status is None:
                defender.status = "paralysis"

            return {
                "effect": "paralysis",
            }

        # こおり
        if effect.effect == "freeze":

            if defender.status is None:
                defender.status = "freeze"

            return {
                "effect": "freeze",
            }

        # ひるみ
        if effect.effect == "flinch":

            defender.volatile_status["flinch"] = True

            return {
                "effect": "flinch",
            }

        return None


print("✅ effect_engine.py Ready")
