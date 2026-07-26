
from data.move_effect_database import MOVE_EFFECTS


class EffectEngine:

    @staticmethod
    def apply(attacker, defender, move_name, force=False):

        if move_name == "protect":
            attacker.volatile_status["protect"] = True

            return {
                "effect": "protect",
            }

        effect = MOVE_EFFECTS.get(move_name)

        if effect is None:
            return None

        if effect.effect == "stat_drop":

            defender.boosts[effect.stat] += effect.stages

            return {
                "effect": effect.effect,
                "stat": effect.stat,
                "stages": effect.stages,
            }

        if effect.effect == "burn":

            defender.status = "burn"

            return {
                "effect": "burn",
            }

        return None


print("✅ effect_engine.py V2 Ready")
