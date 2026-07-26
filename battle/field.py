
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional
import copy


WEATHERS = {
    None,
    "sun",
    "rain",
    "sand",
    "snow",
}

TERRAINS = {
    None,
    "electric",
    "grassy",
    "misty",
    "psychic",
}


@dataclass
class Field:

    weather: Optional[str] = None
    weather_turns: int = 0

    terrain: Optional[str] = None
    terrain_turns: int = 0

    trick_room: bool = False
    trick_room_turns: int = 0

    gravity: bool = False
    gravity_turns: int = 0

    def clone(self):
        return copy.deepcopy(self)

    # ---------- Weather ----------

    def set_weather(self, weather: Optional[str], turns: int = 5):

        if weather not in WEATHERS:
            raise ValueError(f"Unknown weather: {weather}")

        self.weather = weather
        self.weather_turns = 0 if weather is None else turns

    def clear_weather(self):

        self.weather = None
        self.weather_turns = 0

    # ---------- Terrain ----------

    def set_terrain(self, terrain: Optional[str], turns: int = 5):

        if terrain not in TERRAINS:
            raise ValueError(f"Unknown terrain: {terrain}")

        self.terrain = terrain
        self.terrain_turns = 0 if terrain is None else turns

    def clear_terrain(self):

        self.terrain = None
        self.terrain_turns = 0

    # ---------- Trick Room ----------

    def start_trick_room(self, turns: int = 5):

        self.trick_room = True
        self.trick_room_turns = turns

    def end_trick_room(self):

        self.trick_room = False
        self.trick_room_turns = 0

    # ---------- Gravity ----------

    def start_gravity(self, turns: int = 5):

        self.gravity = True
        self.gravity_turns = turns

    def end_gravity(self):

        self.gravity = False
        self.gravity_turns = 0

    # ---------- Turn ----------

    def next_turn(self):

        if self.weather_turns > 0:
            self.weather_turns -= 1
            if self.weather_turns == 0:
                self.clear_weather()

        if self.terrain_turns > 0:
            self.terrain_turns -= 1
            if self.terrain_turns == 0:
                self.clear_terrain()

        if self.trick_room_turns > 0:
            self.trick_room_turns -= 1
            if self.trick_room_turns == 0:
                self.end_trick_room()

        if self.gravity_turns > 0:
            self.gravity_turns -= 1
            if self.gravity_turns == 0:
                self.end_gravity()

    def summary(self):

        return {
            "weather": self.weather,
            "weather_turns": self.weather_turns,
            "terrain": self.terrain,
            "terrain_turns": self.terrain_turns,
            "trick_room": self.trick_room,
            "trick_room_turns": self.trick_room_turns,
            "gravity": self.gravity,
            "gravity_turns": self.gravity_turns,
        }


print("✅ field.py Ready")
