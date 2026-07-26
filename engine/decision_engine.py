
from __future__ import annotations

from typing import Any, Dict, Optional

from engine.search_engine import SearchEngine


class DecisionEngine:
    """
    SearchEngine の結果から最終行動を決定する。
    """

    def __init__(self, search_engine: SearchEngine):
        self.search_engine = search_engine

    def choose_action(
        self,
        battle_state,
        depth: int = 2,
        **kwargs,
    ) -> Dict[str, Any]:

        report = self.search_engine.search(
            state=battle_state,
            depth=depth,
            **kwargs,
        )

        return {
            "action": report["best_action"],
            "score": report["best_score"],
            "ranking": report["ranking"],
        }

    def explain(
        self,
        battle_state,
        depth: int = 2,
        **kwargs,
    ) -> Dict[str, Any]:

        decision = self.choose_action(
            battle_state,
            depth=depth,
            **kwargs,
        )

        return {
            "chosen_action": decision["action"],
            "evaluation": decision["score"],
            "top_candidates": decision["ranking"][:5],
        }


print("✅ decision_engine.py Ready")
