
from dataclasses import dataclass


@dataclass
class ItemData:
    name: str
    category: str
    power_multiplier: float = 1.0
    recoil: float = 0.0
    description: str = ""


ITEM_DB = {

    "choice-band": ItemData(
        name="choice-band",
        category="power",
        power_multiplier=1.5,
        description="Physical Attack ×1.5",
    ),

    "choice-specs": ItemData(
        name="choice-specs",
        category="power",
        power_multiplier=1.5,
        description="Special Attack ×1.5",
    ),

    "life-orb": ItemData(
        name="life-orb",
        category="power",
        power_multiplier=1.3,
        recoil=0.1,
        description="Power ×1.3 / 10% recoil",
    ),

    "expert-belt": ItemData(
        name="expert-belt",
        category="power",
        power_multiplier=1.2,
        description="Super effective ×1.2",
    ),

    "focus-sash": ItemData(
        name="focus-sash",
        category="survival",
        description="Survive at 1 HP from full",
    ),

    "leftovers": ItemData(
        name="leftovers",
        category="recovery",
        description="Recover HP every turn",
    ),
}


def get_item(name: str):
    if not name:
        return None
    return ITEM_DB.get(name.lower())


print("✅ item_database.py Ready")
