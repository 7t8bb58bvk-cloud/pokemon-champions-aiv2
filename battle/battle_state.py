
from __future__ import annotations

from typing import Any, Dict, List, Optional, Sequence, Union
import copy

from battle.pokemon import Pokemon
from battle.field import Field
from battle.side import Side
from battle.action import Action, ACTION_MOVE, ACTION_SWITCH, ACTION_TERA, ACTION_STRUGGLE, ACTION_PASS


PokemonLike = Union[Pokemon, Dict[str, Any], str]


def _normalize_name(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    value = str(value).strip().lower()
    return value or None


class BattleState:
    """
    シングル優先の試合状態。
    Pokemon / Field / Side / Action をまとめて管理する。
    """

    def __init__(
        self,
        player_team: Sequence[PokemonLike],
        opponent_team: Sequence[PokemonLike],
        player_active_index: int = 0,
        opponent_active_index: int = 0,
        field: Optional[Field] = None,
        player_side: Optional[Side] = None,
        opponent_side: Optional[Side] = None,
        turn: int = 1,
        pokemon_lookup: Optional[Dict[str, Any]] = None,
        battle_log: Optional[List[Dict[str, Any]]] = None,
    ):
        self.pokemon_lookup = pokemon_lookup or {}

        self.player_team: List[Pokemon] = [self._coerce_pokemon(p) for p in player_team]
        self.opponent_team: List[Pokemon] = [self._coerce_pokemon(p) for p in opponent_team]

        if not self.player_team:
            raise ValueError("player_team must not be empty")
        if not self.opponent_team:
            raise ValueError("opponent_team must not be empty")

        self.player_active_index = self._validate_active_index(
            player_active_index, self.player_team, "player_active_index"
        )
        self.opponent_active_index = self._validate_active_index(
            opponent_active_index, self.opponent_team, "opponent_active_index"
        )

        self.field = field.clone() if field else Field()
        self.player_side = player_side.clone() if player_side else Side()
        self.opponent_side = opponent_side.clone() if opponent_side else Side()

        self.turn = int(turn)
        self.battle_log: List[Dict[str, Any]] = battle_log[:] if battle_log else []
        self.winner: Optional[str] = None  # "player" / "opponent" / None

        self._update_winner_if_needed()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _validate_active_index(self, index: int, team: List[Pokemon], label: str) -> int:
        index = int(index)
        if index < 0 or index >= len(team):
            raise IndexError(f"{label} out of range")
        return index

    def _coerce_pokemon(self, spec: PokemonLike) -> Pokemon:
        if isinstance(spec, Pokemon):
            return spec.clone()

        if isinstance(spec, dict):
            data = dict(spec)

            name = _normalize_name(data.get("name") or data.get("species") or "")
            if not name:
                raise ValueError("Pokemon dict must have a name")

            types = list(data.get("types", []))
            ability = _normalize_name(data.get("ability"))
            item = _normalize_name(data.get("item"))
            tera_type = _normalize_name(data.get("tera_type"))
            terastallized = bool(data.get("terastallized", False))
            status = _normalize_name(data.get("status"))
            moves = list(data.get("moves", []))
            pp = dict(data.get("pp", {}))
            boosts = dict(data.get("boosts", {}))
            volatile_status = dict(data.get("volatile_status", {}))

            max_hp = data.get("max_hp")
            current_hp = data.get("current_hp", data.get("hp"))

            if max_hp is None or current_hp is None:
                base_stats = data.get("base_stats") or {}
                base_hp = base_stats.get("hp")
                if max_hp is None and base_hp is not None:
                    max_hp = int(base_hp)
                if current_hp is None and base_hp is not None:
                    current_hp = int(base_hp)

            if max_hp is None:
                max_hp = 1
            if current_hp is None:
                current_hp = max_hp

            return Pokemon(
                name=name,
                level=int(data.get("level", 50)),
                max_hp=int(max_hp),
                current_hp=int(current_hp),
                types=types,
                ability=ability,
                item=item,
                tera_type=tera_type,
                terastallized=terastallized,
                status=status,
                moves=moves,
                pp=pp,
                boosts=boosts if boosts else None,
                volatile_status=volatile_status,
            )

        if isinstance(spec, str):
            key = _normalize_name(spec) or spec
            lookup = self.pokemon_lookup.get(key)

            if isinstance(lookup, Pokemon):
                return lookup.clone()

            if isinstance(lookup, dict):
                data = dict(lookup)
                data.setdefault("name", key)
                return self._coerce_pokemon(data)

            return Pokemon(
                name=key,
                level=50,
                max_hp=1,
                current_hp=1,
            )

        raise TypeError(f"Unsupported pokemon spec: {type(spec)}")

    def _get_team(self, side: str) -> List[Pokemon]:
        side = _normalize_name(side) or side
        if side == "player":
            return self.player_team
        if side == "opponent":
            return self.opponent_team
        raise ValueError("side must be 'player' or 'opponent'")

    def _get_active_index(self, side: str) -> int:
        side = _normalize_name(side) or side
        if side == "player":
            return self.player_active_index
        if side == "opponent":
            return self.opponent_active_index
        raise ValueError("side must be 'player' or 'opponent'")

    def _set_active_index(self, side: str, index: int):
        team = self._get_team(side)
        index = self._validate_active_index(index, team, f"{side}_active_index")
        if team[index].fainted:
            raise ValueError("Cannot switch to a fainted Pokémon")

        if side == "player":
            self.player_active_index = index
        else:
            self.opponent_active_index = index

    def _active_slot(self, side: str) -> Pokemon:
        team = self._get_team(side)
        idx = self._get_active_index(side)
        return team[idx]

    def _update_winner_if_needed(self):
        player_alive = any(not p.fainted for p in self.player_team)
        opponent_alive = any(not p.fainted for p in self.opponent_team)

        if player_alive and opponent_alive:
            self.winner = None
        elif player_alive and not opponent_alive:
            self.winner = "player"
        elif opponent_alive and not player_alive:
            self.winner = "opponent"
        else:
            self.winner = None

    def _record(self, event: Dict[str, Any]):
        item = dict(event)
        item.setdefault("turn", self.turn)
        self.battle_log.append(item)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def clone(self) -> "BattleState":
        return BattleState(
            player_team=[p.clone() for p in self.player_team],
            opponent_team=[p.clone() for p in self.opponent_team],
            player_active_index=self.player_active_index,
            opponent_active_index=self.opponent_active_index,
            field=self.field.clone(),
            player_side=self.player_side.clone(),
            opponent_side=self.opponent_side.clone(),
            turn=self.turn,
            pokemon_lookup=copy.deepcopy(self.pokemon_lookup),
            battle_log=copy.deepcopy(self.battle_log),
        )

    def get_active_player(self) -> Pokemon:
        return self.player_team[self.player_active_index]

    def get_active_opponent(self) -> Pokemon:
        return self.opponent_team[self.opponent_active_index]

    def get_active_pair(self):
        return self.get_active_player(), self.get_active_opponent()

    def set_active_player(self, index: int):
        self._set_active_index("player", index)
        self._record({
            "event": "switch",
            "side": "player",
            "index": index,
            "pokemon": self.get_active_player().name,
        })

    def set_active_opponent(self, index: int):
        self._set_active_index("opponent", index)
        self._record({
            "event": "switch",
            "side": "opponent",
            "index": index,
            "pokemon": self.get_active_opponent().name,
        })

    def available_switches(self, side: str) -> List[int]:
        team = self._get_team(side)
        active_index = self._get_active_index(side)
        return [i for i, p in enumerate(team) if i != active_index and not p.fainted]

    def fainted_count(self, side: str) -> int:
        return sum(1 for p in self._get_team(side) if p.fainted)

    def all_fainted(self, side: str) -> bool:
        return all(p.fainted for p in self._get_team(side))

    def is_over(self) -> bool:
        self._update_winner_if_needed()
        return self.winner is not None

    def apply_damage(self, side: str, damage: int) -> int:
        damage = max(0, int(damage))
        target = self._active_slot(side)
        before = target.current_hp
        target.damage(damage)
        self._update_winner_if_needed()

        self._record({
            "event": "damage",
            "side": side,
            "pokemon": target.name,
            "damage": damage,
            "before": before,
            "after": target.current_hp,
        })
        return damage

    def heal(self, side: str, amount: int) -> int:
        amount = max(0, int(amount))
        target = self._active_slot(side)
        before = target.current_hp
        target.heal(amount)
        self._update_winner_if_needed()

        self._record({
            "event": "heal",
            "side": side,
            "pokemon": target.name,
            "amount": amount,
            "before": before,
            "after": target.current_hp,
        })
        return target.current_hp - before

    def set_status(self, side: str, status: Optional[str]):
        target = self._active_slot(side)
        target.set_status(status)
        self._record({
            "event": "status",
            "side": side,
            "pokemon": target.name,
            "status": target.status,
        })

    def cure_status(self, side: str):
        target = self._active_slot(side)
        target.cure_status()
        self._record({
            "event": "cure_status",
            "side": side,
            "pokemon": target.name,
        })

    def next_turn(self):
        self.turn += 1
        self.field.next_turn()
        self.player_side.next_turn()
        self.opponent_side.next_turn()
        self._record({"event": "next_turn"})
        self._update_winner_if_needed()

    def apply_action(self, side: str, action: Action):
        """
        実際の技ダメージは engine/simulation_engine.py 側で処理する。
        ここは状態更新とログの土台だけ扱う。
        """
        if action is None:
            self._record({"event": "pass", "side": side})
            return

        if action.action_type == ACTION_SWITCH:
            if action.switch_slot is None:
                raise ValueError("switch_slot is required for switch action")
            if side == "player":
                self.set_active_player(action.switch_slot)
            else:
                self.set_active_opponent(action.switch_slot)
            return

        if action.action_type == ACTION_PASS:
            self._record({"event": "pass", "side": side})
            return

        if action.action_type == ACTION_TERA:
            target = self._active_slot(side)
            target.terastallized = True
            self._record({
                "event": "tera",
                "side": side,
                "pokemon": target.name,
                "tera_type": target.tera_type,
            })
            return

        if action.action_type == ACTION_MOVE:
            if action.tera:
                target = self._active_slot(side)
                target.terastallized = True

            self._record({
                "event": "move",
                "side": side,
                "move": action.move,
                "tera": action.tera,
            })
            return

        if action.action_type == ACTION_STRUGGLE:
            self._record({"event": "struggle", "side": side})
            return

        self._record({
            "event": "unknown_action",
            "side": side,
            "action": action.summary(),
        })

    def summary(self) -> Dict[str, Any]:
        self._update_winner_if_needed()

        return {
            "turn": self.turn,
            "winner": self.winner,
            "is_over": self.is_over(),
            "player": {
                "active_index": self.player_active_index,
                "active": self.get_active_player().summary(),
                "fainted_count": self.fainted_count("player"),
                "available_switches": self.available_switches("player"),
            },
            "opponent": {
                "active_index": self.opponent_active_index,
                "active": self.get_active_opponent().summary(),
                "fainted_count": self.fainted_count("opponent"),
                "available_switches": self.available_switches("opponent"),
            },
            "field": self.field.summary(),
            "player_side": self.player_side.summary(),
            "opponent_side": self.opponent_side.summary(),
            "log_size": len(self.battle_log),
        }

    @property
    def player_side_conditions(self) -> Dict[str, Any]:
        return self.player_side.summary()

    @player_side_conditions.setter
    def player_side_conditions(self, value: Dict[str, Any]):
        if not isinstance(value, dict):
            raise TypeError("player_side_conditions must be a dict")
        if "stealth_rock" in value:
            self.player_side.stealth_rock = bool(value["stealth_rock"])
        if "spikes" in value:
            self.player_side.spikes = int(value["spikes"])
        if "toxic_spikes" in value:
            self.player_side.toxic_spikes = int(value["toxic_spikes"])
        if "sticky_web" in value:
            self.player_side.sticky_web = bool(value["sticky_web"])
        if "reflect" in value:
            self.player_side.reflect = int(value["reflect"])
        if "light_screen" in value:
            self.player_side.light_screen = int(value["light_screen"])
        if "aurora_veil" in value:
            self.player_side.aurora_veil = int(value["aurora_veil"])
        if "tailwind" in value:
            self.player_side.tailwind = int(value["tailwind"])
        if "lucky_chant" in value:
            self.player_side.lucky_chant = int(value["lucky_chant"])

    @property
    def opponent_side_conditions(self) -> Dict[str, Any]:
        return self.opponent_side.summary()

    @opponent_side_conditions.setter
    def opponent_side_conditions(self, value: Dict[str, Any]):
        if not isinstance(value, dict):
            raise TypeError("opponent_side_conditions must be a dict")
        if "stealth_rock" in value:
            self.opponent_side.stealth_rock = bool(value["stealth_rock"])
        if "spikes" in value:
            self.opponent_side.spikes = int(value["spikes"])
        if "toxic_spikes" in value:
            self.opponent_side.toxic_spikes = int(value["toxic_spikes"])
        if "sticky_web" in value:
            self.opponent_side.sticky_web = bool(value["sticky_web"])
        if "reflect" in value:
            self.opponent_side.reflect = int(value["reflect"])
        if "light_screen" in value:
            self.opponent_side.light_screen = int(value["light_screen"])
        if "aurora_veil" in value:
            self.opponent_side.aurora_veil = int(value["aurora_veil"])
        if "tailwind" in value:
            self.opponent_side.tailwind = int(value["tailwind"])
        if "lucky_chant" in value:
            self.opponent_side.lucky_chant = int(value["lucky_chant"])

    @property
    def field_state(self) -> Dict[str, Any]:
        return self.field.summary()

    @field_state.setter
    def field_state(self, value: Dict[str, Any]):
        if not isinstance(value, dict):
            raise TypeError("field_state must be a dict")
        if "weather" in value:
            self.field.weather = value["weather"]
        if "weather_turns" in value:
            self.field.weather_turns = int(value["weather_turns"])
        if "terrain" in value:
            self.field.terrain = value["terrain"]
        if "terrain_turns" in value:
            self.field.terrain_turns = int(value["terrain_turns"])
        if "trick_room" in value:
            self.field.trick_room = bool(value["trick_room"])
        if "trick_room_turns" in value:
            self.field.trick_room_turns = int(value["trick_room_turns"])
        if "gravity" in value:
            self.field.gravity = bool(value["gravity"])
        if "gravity_turns" in value:
            self.field.gravity_turns = int(value["gravity_turns"])

    def __repr__(self):
        return f"BattleState(turn={self.turn}, winner={self.winner!r})"


print("✅ battle_state.py Ready")
