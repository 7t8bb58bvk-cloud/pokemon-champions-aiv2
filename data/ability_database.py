
from dataclasses import dataclass


@dataclass
class AbilityData:
    name: str
    category: str
    description: str = ""


ABILITY_DB = {

    "intimidate": AbilityData(
        "intimidate",
        "entry",
        "Lower opponent Attack by one stage",
    ),

    "multiscale": AbilityData(
        "multiscale",
        "defense",
        "Half damage at full HP",
    ),

    "flash-fire": AbilityData(
        "flash-fire",
        "immunity",
        "Immune to Fire moves",
    ),

    "levitate": AbilityData(
        "levitate",
        "immunity",
        "Immune to Ground moves",
    ),

    "huge-power": AbilityData(
        "huge-power",
        "attack",
        "Double physical Attack",
    ),

    "pure-power": AbilityData(
        "pure-power",
        "attack",
        "Double physical Attack",
    ),
}


def get_ability(name: str):
    if not name:
        return None
    return ABILITY_DB.get(name.lower())


print("✅ ability_database.py Ready")
