
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional
import copy


ACTION_MOVE = "move"
ACTION_SWITCH = "switch"
ACTION_TERA = "tera"
ACTION_STRUGGLE = "struggle"
ACTION_PASS = "pass"


@dataclass
class Action:

    action_type: str

    move: Optional[str] = None

    target: Optional[int] = None

    switch_slot: Optional[int] = None

    tera: bool = False

    priority: int = 0

    def clone(self):

        return copy.deepcopy(self)

    @classmethod
    def move_action(
        cls,
        move: str,
        target: int = 0,
        tera: bool = False,
    ):

        return cls(
            action_type=ACTION_MOVE,
            move=move,
            target=target,
            tera=tera,
        )

    @classmethod
    def switch_action(
        cls,
        slot: int,
    ):

        return cls(
            action_type=ACTION_SWITCH,
            switch_slot=slot,
        )

    @classmethod
    def struggle_action(cls):

        return cls(
            action_type=ACTION_STRUGGLE,
        )

    @classmethod
    def pass_action(cls):

        return cls(
            action_type=ACTION_PASS,
        )

    def is_move(self):

        return self.action_type == ACTION_MOVE

    def is_switch(self):

        return self.action_type == ACTION_SWITCH

    def is_struggle(self):

        return self.action_type == ACTION_STRUGGLE

    def is_pass(self):

        return self.action_type == ACTION_PASS

    def summary(self):

        return {
            "type": self.action_type,
            "move": self.move,
            "target": self.target,
            "switch_slot": self.switch_slot,
            "tera": self.tera,
            "priority": self.priority,
        }


print("✅ action.py Ready")
