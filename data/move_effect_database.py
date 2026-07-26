
from dataclasses import dataclass
from typing import Optional


@dataclass
class MoveEffect:

    move: str

    effect: Optional[str] = None

    chance: float = 0.0

    stat: Optional[str] = None

    stages: int = 0


MOVE_EFFECTS = {

    "moonblast": MoveEffect(
        move="moonblast",
        effect="stat_drop",
        chance=0.30,
        stat="spa",
        stages=-1,
    ),

    "shadow-ball": MoveEffect(
        move="shadow-ball",
        effect="stat_drop",
        chance=0.20,
        stat="spd",
        stages=-1,
    ),

    "air-slash": MoveEffect(
        move="air-slash",
        effect="flinch",
        chance=0.30,
    ),

    "heat-wave": MoveEffect(
        move="heat-wave",
        effect="burn",
        chance=0.10,
    ),

    "ice-beam": MoveEffect(
        move="ice-beam",
        effect="freeze",
        chance=0.10,
    ),

    "thunderbolt": MoveEffect(
        move="thunderbolt",
        effect="paralysis",
        chance=0.10,
    ),

}


def get_move_effect(move_name):

    if not move_name:
        return None

    return MOVE_EFFECTS.get(move_name.lower())


print("✅ move_effect_database.py Ready")
