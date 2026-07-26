
from dataclasses import dataclass


@dataclass
class StatusData:
    name: str
    category: str
    description: str = ""


STATUS_DB = {

    "burn": StatusData(
        "burn",
        "major",
        "Physical Attack ×0.5, damage each turn",
    ),

    "poison": StatusData(
        "poison",
        "major",
        "Damage every turn",
    ),

    "toxic": StatusData(
        "toxic",
        "major",
        "Increasing poison damage",
    ),

    "paralysis": StatusData(
        "paralysis",
        "major",
        "Speed ×0.5, may be unable to move",
    ),

    "sleep": StatusData(
        "sleep",
        "major",
        "Cannot move while asleep",
    ),

    "freeze": StatusData(
        "freeze",
        "major",
        "Cannot move until thawed",
    ),
}


def get_status(name: str):
    if not name:
        return None
    return STATUS_DB.get(name.lower())


print("✅ status_database.py Ready")
