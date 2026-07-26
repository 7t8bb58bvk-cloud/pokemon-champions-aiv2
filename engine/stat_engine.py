
from __future__ import annotations


class StatEngine:

    @staticmethod
    def stage_multiplier(stage: int) -> float:
        stage = max(-6, min(6, int(stage)))

        if stage >= 0:
            return (2 + stage) / 2

        return 2 / (2 - stage)

    @staticmethod
    def apply_stage(base: int, stage: int) -> int:
        return max(
            1,
            int(base * StatEngine.stage_multiplier(stage))
        )

    @staticmethod
    def get_attack(pokemon, special=False):

        if special:
            base = pokemon.spa
            stage = pokemon.boosts["spa"]
        else:
            base = pokemon.atk
            stage = pokemon.boosts["atk"]

        return StatEngine.apply_stage(base, stage)

    @staticmethod
    def get_defense(pokemon, special=False):

        if special:
            base = pokemon.spd
            stage = pokemon.boosts["spd"]
        else:
            base = pokemon.def_
            stage = pokemon.boosts["def"]

        return StatEngine.apply_stage(base, stage)


print("✅ stat_engine.py V2 Ready")
