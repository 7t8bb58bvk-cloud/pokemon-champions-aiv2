
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional
import copy


BOOST_NAMES = (
    "atk",
    "def",
    "spa",
    "spd",
    "spe",
    "accuracy",
    "evasion",
)


@dataclass
class Pokemon:

    name: str
    level: int = 50

    max_hp: int = 1
    current_hp: int = 1

    # ===== 能力値 =====
    atk: int = 100
    def_: int = 100
    spa: int = 100
    spd: int = 100
    spe: int = 100

    types: List[str] = field(default_factory=list)

    ability: Optional[str] = None
    item: Optional[str] = None

    tera_type: Optional[str] = None
    terastallized: bool = False

    status: Optional[str] = None

    moves: List[str] = field(default_factory=list)
    pp: Dict[str, int] = field(default_factory=dict)

    boosts: Dict[str, int] = field(
        default_factory=lambda: {k: 0 for k in BOOST_NAMES}
    )

    volatile_status: Dict[str, bool] = field(default_factory=dict)

    def clone(self):
        return copy.deepcopy(self)

    @property
    def fainted(self):
        return self.current_hp <= 0

    @property
    def hp_ratio(self):
        if self.max_hp == 0:
            return 0
        return self.current_hp / self.max_hp

    def damage(self, value: int):
        self.current_hp = max(0, self.current_hp - int(value))

    def heal(self, value: int):
        self.current_hp = min(self.max_hp, self.current_hp + int(value))

    def add_boost(self, stat: str, amount: int):
        if stat not in self.boosts:
            return
        self.boosts[stat] = max(-6, min(6, self.boosts[stat] + amount))

    def summary(self):
        return {
            "name": self.name,
            "hp": self.current_hp,
            "max_hp": self.max_hp,
            "atk": self.atk,
            "def": self.def_,
            "spa": self.spa,
            "spd": self.spd,
            "spe": self.spe,
            "status": self.status,
            "boosts": self.boosts.copy(),
        }


print("✅ pokemon.py V2 Ready")
