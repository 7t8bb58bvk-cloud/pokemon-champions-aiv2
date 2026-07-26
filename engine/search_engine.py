
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Tuple

from battle.action import Action, ACTION_MOVE, ACTION_SWITCH, ACTION_PASS
from battle.battle_state import BattleState
from engine.evaluation_engine import EvaluationEngine
from engine.simulation_engine import SimulationEngine


MoveProvider = Callable[[str], Any]


@dataclass
class SearchResult:
    action: Optional[Action]
    score: float
    detail: Dict[str, Any]


class SearchEngine:
    """
    いまの SimulationEngine (simulate) に合わせた探索エンジン。
    """

    def __init__(
        self,
        simulation_engine: Any,
        evaluation_engine: Any,
        move_catalog: Optional[Dict[str, Any]] = None,
        move_provider: Optional[MoveProvider] = None,
    ):
        self.simulation_engine = simulation_engine
        self.evaluation_engine = evaluation_engine
        self.move_catalog = move_catalog or {}
        self.move_provider = move_provider
        self._cache: Dict[Tuple[Any, ...], float] = {}

    def _resolve_move(self, move_name: str, move_provider: Optional[MoveProvider] = None):
        name = str(move_name).strip().lower()

        if name in self.move_catalog:
            return self.move_catalog[name]

        provider = move_provider or self.move_provider
        if provider is not None:
            move = provider(name)
            if move is not None:
                return move

        return None

    def _active_moves(self, state: BattleState, side: str) -> List[str]:
        if side == "player":
            return list(getattr(state.get_active_player(), "moves", []) or [])
        if side == "opponent":
            return list(getattr(state.get_active_opponent(), "moves", []) or [])
        raise ValueError("side must be 'player' or 'opponent'")

    def generate_actions(
        self,
        state: BattleState,
        side: str,
        move_names: Optional[List[str]] = None,
        move_provider: Optional[MoveProvider] = None,
        allow_switch: bool = True,
        allow_pass: bool = True,
    ) -> List[Action]:

        if move_names is None:
            move_names = self._active_moves(state, side)

        actions: List[Action] = []

        for move_name in move_names:
            move_obj = self._resolve_move(move_name, move_provider=move_provider)
            if move_obj is None:
                continue

            actions.append(
                Action(
                    action_type=ACTION_MOVE,
                    move=move_obj,
                )
            )

        if allow_switch:
            for idx in state.available_switches(side):
                actions.append(
                    Action(
                        action_type=ACTION_SWITCH,
                        switch_slot=idx,
                    )
                )

        if allow_pass:
            actions.append(
                Action(
                    action_type=ACTION_PASS,
                )
            )

        unique: List[Action] = []
        seen = set()
        for act in actions:
            key = (
                act.action_type,
                getattr(act.move, "name", act.move),
                act.switch_slot,
                act.tera,
            )
            if key in seen:
                continue
            seen.add(key)
            unique.append(act)

        return unique

    def _state_key(
        self,
        state: BattleState,
        depth: int,
        side: str,
        player_move_names: Optional[List[str]],
        opponent_move_names: Optional[List[str]],
    ) -> Tuple[Any, ...]:

        player = state.get_active_player()
        opponent = state.get_active_opponent()

        return (
            depth,
            side,
            state.turn,
            state.winner,
            player.name,
            player.current_hp,
            player.status,
            tuple(sorted(player.boosts.items())),
            opponent.name,
            opponent.current_hp,
            opponent.status,
            tuple(sorted(opponent.boosts.items())),
            tuple(player_move_names or []),
            tuple(opponent_move_names or []),
            state.field.weather,
            state.field.terrain,
            state.field.trick_room,
            state.player_side.stealth_rock,
            state.player_side.spikes,
            state.opponent_side.stealth_rock,
            state.opponent_side.spikes,
        )

    def _evaluate_state(self, state: BattleState) -> float:
        return float(self.evaluation_engine.evaluate(state))

    def _simulate_joint_turn(
        self,
        state: BattleState,
        player_action: Optional[Action],
        opponent_action: Optional[Action],
    ) -> BattleState:

        simulator = self.simulation_engine

        if hasattr(simulator, "simulate"):
            return simulator.simulate(
                state=state,
                player_action=player_action,
                opponent_action=opponent_action,
            )

        raise AttributeError("simulation_engine must provide simulate()")

    def _minimax(
        self,
        state: BattleState,
        depth: int,
        player_move_names: Optional[List[str]] = None,
        opponent_move_names: Optional[List[str]] = None,
        player_move_provider: Optional[MoveProvider] = None,
        opponent_move_provider: Optional[MoveProvider] = None,
    ) -> float:

        if depth <= 0 or state.is_over():
            return self._evaluate_state(state)

        key = self._state_key(
            state=state,
            depth=depth,
            side="player",
            player_move_names=player_move_names,
            opponent_move_names=opponent_move_names,
        )
        if key in self._cache:
            return self._cache[key]

        player_actions = self.generate_actions(
            state=state,
            side="player",
            move_names=player_move_names,
            move_provider=player_move_provider,
        )

        opponent_actions = self.generate_actions(
            state=state,
            side="opponent",
            move_names=opponent_move_names,
            move_provider=opponent_move_provider,
        )

        if not player_actions:
            player_actions = [Action(action_type=ACTION_PASS)]
        if not opponent_actions:
            opponent_actions = [Action(action_type=ACTION_PASS)]

        best_score = float("-inf")

        for p_action in player_actions:
            worst_reply = float("inf")

            for o_action in opponent_actions:
                next_state = self._simulate_joint_turn(
                    state=state,
                    player_action=p_action,
                    opponent_action=o_action,
                )

                score = self._minimax(
                    state=next_state,
                    depth=depth - 1,
                    player_move_names=player_move_names,
                    opponent_move_names=opponent_move_names,
                    player_move_provider=player_move_provider,
                    opponent_move_provider=opponent_move_provider,
                )

                if score < worst_reply:
                    worst_reply = score

            if worst_reply > best_score:
                best_score = worst_reply

        self._cache[key] = best_score
        return best_score

    def search(
        self,
        state: BattleState,
        depth: int = 2,
        player_move_names: Optional[List[str]] = None,
        opponent_move_names: Optional[List[str]] = None,
        player_move_provider: Optional[MoveProvider] = None,
        opponent_move_provider: Optional[MoveProvider] = None,
    ) -> Dict[str, Any]:

        self._cache.clear()

        player_actions = self.generate_actions(
            state=state,
            side="player",
            move_names=player_move_names,
            move_provider=player_move_provider,
        )

        if not player_actions:
            player_actions = [Action(action_type=ACTION_PASS)]

        ranking = []

        for action in player_actions:
            worst_score = float("inf")
            worst_reply_action = None

            opponent_actions = self.generate_actions(
                state=state,
                side="opponent",
                move_names=opponent_move_names,
                move_provider=opponent_move_provider,
            )
            if not opponent_actions:
                opponent_actions = [Action(action_type=ACTION_PASS)]

            for o_action in opponent_actions:
                next_state = self._simulate_joint_turn(
                    state=state,
                    player_action=action,
                    opponent_action=o_action,
                )

                score = self._minimax(
                    state=next_state,
                    depth=max(0, depth - 1),
                    player_move_names=player_move_names,
                    opponent_move_names=opponent_move_names,
                    player_move_provider=player_move_provider,
                    opponent_move_provider=opponent_move_provider,
                )

                if score < worst_score:
                    worst_score = score
                    worst_reply_action = o_action

            ranking.append(
                {
                    "action": {
                        "type": action.action_type,
                        "move": getattr(action.move, "name", None),
                        "switch_slot": action.switch_slot,
                        "tera": action.tera,
                    },
                    "score": round(worst_score, 2),
                    "worst_reply": {
                        "type": getattr(worst_reply_action, "action_type", None),
                        "move": getattr(getattr(worst_reply_action, "move", None), "name", None),
                        "switch_slot": getattr(worst_reply_action, "switch_slot", None),
                        "tera": getattr(worst_reply_action, "tera", None),
                    } if worst_reply_action is not None else None,
                }
            )

        ranking.sort(key=lambda x: x["score"], reverse=True)

        best = ranking[0] if ranking else None

        return {
            "best_action": best["action"] if best else None,
            "best_score": best["score"] if best else None,
            "ranking": ranking,
        }

    def explain(
        self,
        state: BattleState,
        depth: int = 2,
        player_move_names: Optional[List[str]] = None,
        opponent_move_names: Optional[List[str]] = None,
        player_move_provider: Optional[MoveProvider] = None,
        opponent_move_provider: Optional[MoveProvider] = None,
    ) -> Dict[str, Any]:

        report = self.search(
            state=state,
            depth=depth,
            player_move_names=player_move_names,
            opponent_move_names=opponent_move_names,
            player_move_provider=player_move_provider,
            opponent_move_provider=opponent_move_provider,
        )

        return {
            "best_action": report["best_action"],
            "best_score": report["best_score"],
            "ranking": report["ranking"],
        }


print("✅ search_engine.py Ready")
