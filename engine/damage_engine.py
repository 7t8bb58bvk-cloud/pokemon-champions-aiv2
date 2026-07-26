
from __future__ import annotations

from data.type_chart import type_multiplier
from data.move_database import get_move
from data.item_database import get_item
from data.ability_database import get_ability
from data.status_database import get_status
from engine.stat_engine import StatEngine


class DamageEngine:

    STAB = 1.5

    @staticmethod
    def calculate(attacker, defender, move_name):

        move = get_move(move_name)

        if move is None:
            raise ValueError(f"Unknown move: {move_name}")

        if move.category == "status":
            return 0

        special = move.category == "special"

        # -------------------------
        # Ability immunity
        # -------------------------
        defender_ability = get_ability(defender.ability)

        if (
            defender_ability
            and defender_ability.name == "levitate"
            and move.type == "ground"
        ):
            return 0

        atk = StatEngine.get_attack(attacker, special)
        defense = StatEngine.get_defense(defender, special)

        # -------------------------
        # Huge Power / Pure Power
        # -------------------------
        attacker_ability = get_ability(attacker.ability)

        if (
            attacker_ability
            and not special
            and attacker_ability.name in (
                "huge-power",
                "pure-power",
            )
        ):
            atk *= 2

        # -------------------------
        # Burn
        # -------------------------
        status = get_status(attacker.status)

        if (
            status
            and status.name == "burn"
            and not special
        ):
            atk *= 0.5

        # -------------------------
        # Base damage
        # -------------------------
        base = (((22 * move.power * atk) / max(1, defense)) / 50) + 2

        # -------------------------
        # STAB
        # -------------------------
        stab = (
            DamageEngine.STAB
            if move.type.lower() in [t.lower() for t in attacker.types]
            else 1.0
        )

        # -------------------------
        # Type effectiveness
        # -------------------------
        effectiveness = type_multiplier(
            move.type,
            defender.types,
        )

        # -------------------------
        # Item modifier
        # -------------------------
        item_multiplier = 1.0

        item = get_item(attacker.item)

        if item is not None:

            if (
                item.name == "choice-band"
                and move.category == "physical"
            ):
                item_multiplier = item.power_multiplier

            elif (
                item.name == "choice-specs"
                and move.category == "special"
            ):
                item_multiplier = item.power_multiplier

            elif item.name == "life-orb":
                item_multiplier = item.power_multiplier

        # -------------------------
        # Multiscale
        # -------------------------
        if (
            defender_ability
            and defender_ability.name == "multiscale"
            and defender.current_hp == defender.max_hp
        ):
            base *= 0.5

        damage = int(
            base
            * stab
            * effectiveness
            * item_multiplier
        )

        if effectiveness == 0:
            return 0

        return max(1, damage)


print("✅ damage_engine.py V8 Ready")
