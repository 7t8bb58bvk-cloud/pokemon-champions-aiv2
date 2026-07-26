
from __future__ import annotations

from dataclasses import dataclass
import copy


@dataclass
class Side:

    stealth_rock: bool = False

    spikes: int = 0

    toxic_spikes: int = 0

    sticky_web: bool = False

    reflect: int = 0

    light_screen: int = 0

    aurora_veil: int = 0

    tailwind: int = 0

    lucky_chant: int = 0

    def clone(self):
        return copy.deepcopy(self)

    # --------------------------
    # Entry Hazards
    # --------------------------

    def set_stealth_rock(self):
        self.stealth_rock = True

    def clear_stealth_rock(self):
        self.stealth_rock = False

    def add_spikes(self):
        self.spikes = min(3, self.spikes + 1)

    def clear_spikes(self):
        self.spikes = 0

    def add_toxic_spikes(self):
        self.toxic_spikes = min(2, self.toxic_spikes + 1)

    def clear_toxic_spikes(self):
        self.toxic_spikes = 0

    def set_sticky_web(self):
        self.sticky_web = True

    def clear_sticky_web(self):
        self.sticky_web = False

    # --------------------------
    # Screens
    # --------------------------

    def start_reflect(self, turns=5):
        self.reflect = turns

    def start_light_screen(self, turns=5):
        self.light_screen = turns

    def start_aurora_veil(self, turns=5):
        self.aurora_veil = turns

    def start_tailwind(self, turns=4):
        self.tailwind = turns

    def start_lucky_chant(self, turns=5):
        self.lucky_chant = turns

    # --------------------------
    # Turn
    # --------------------------

    def next_turn(self):

        if self.reflect > 0:
            self.reflect -= 1

        if self.light_screen > 0:
            self.light_screen -= 1

        if self.aurora_veil > 0:
            self.aurora_veil -= 1

        if self.tailwind > 0:
            self.tailwind -= 1

        if self.lucky_chant > 0:
            self.lucky_chant -= 1

    # --------------------------
    # Summary
    # --------------------------

    def summary(self):

        return {
            "stealth_rock": self.stealth_rock,
            "spikes": self.spikes,
            "toxic_spikes": self.toxic_spikes,
            "sticky_web": self.sticky_web,
            "reflect": self.reflect,
            "light_screen": self.light_screen,
            "aurora_veil": self.aurora_veil,
            "tailwind": self.tailwind,
            "lucky_chant": self.lucky_chant,
        }


print("✅ side.py Ready")
