
from dataclasses import dataclass


@dataclass
class MoveData:
    name: str
    type: str
    category: str      # physical / special / status
    power: int
    accuracy: int
    pp: int
    priority: int = 0
    contact: bool = False


MOVE_DB = {

    "earthquake": MoveData(
        "earthquake",
        "ground",
        "physical",
        100,
        100,
        10,
    ),

    "dragon-claw": MoveData(
        "dragon-claw",
        "dragon",
        "physical",
        80,
        100,
        15,
        contact=True,
    ),

    "stone-edge": MoveData(
        "stone-edge",
        "rock",
        "physical",
        100,
        80,
        5,
    ),

    "moonblast": MoveData(
        "moonblast",
        "fairy",
        "special",
        95,
        100,
        15,
    ),

    "protect": MoveData(
        "protect",
        "normal",
        "status",
        0,
        100,
        10,
    ),

    "swords-dance": MoveData(
        "swords-dance",
        "normal",
        "status",
        0,
        100,
        20,
    ),

    "dragon-dance": MoveData(
        "dragon-dance",
        "dragon",
        "status",
        0,
        100,
        20,
    ),

    "extreme-speed": MoveData(
        "extreme-speed",
        "normal",
        "physical",
        80,
        100,
        5,
        priority=2,
        contact=True,
    ),
}


def get_move(name: str):
    return MOVE_DB.get(name.lower())


print("✅ move_database.py Ready")
