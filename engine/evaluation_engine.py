
from __future__ import annotations

from battle.battle_state import BattleState


class EvaluationEngine:
    """
    盤面評価エンジン

    + が有利
    - が不利
    """

    HP_WEIGHT = 100.0
    POKEMON_WEIGHT = 250.0
    STATUS_WEIGHT = 35.0
    BOOST_WEIGHT = 18.0
    HAZARD_WEIGHT = 20.0

    STATUS_SCORE = {
        None: 0,
        "brn": -25,
        "par": -20,
        "psn": -20,
        "tox": -35,
        "slp": -30,
        "frz": -40,
    }

    @classmethod
    def hp_score(cls, state: BattleState):

        player = sum(p.hp_ratio for p in state.player_team)
        opponent = sum(p.hp_ratio for p in state.opponent_team)

        return (player - opponent) * cls.HP_WEIGHT

    @classmethod
    def remaining_score(cls, state: BattleState):

        player = sum(not p.fainted for p in state.player_team)
        opponent = sum(not p.fainted for p in state.opponent_team)

        return (player - opponent) * cls.POKEMON_WEIGHT

    @classmethod
    def status_score(cls, state: BattleState):

        score = 0

        for p in state.player_team:
            score -= cls.STATUS_SCORE.get(p.status, 0)

        for p in state.opponent_team:
            score += cls.STATUS_SCORE.get(p.status, 0)

        return score

    @classmethod
    def boost_score(cls, state: BattleState):

        score = 0

        player = state.get_active_player()
        opponent = state.get_active_opponent()

        for value in player.boosts.values():
            score += value * cls.BOOST_WEIGHT

        for value in opponent.boosts.values():
            score -= value * cls.BOOST_WEIGHT

        return score

    @classmethod
    def hazard_score(cls, state: BattleState):

        score = 0

        ps = state.player_side
        os = state.opponent_side

        score -= ps.spikes * cls.HAZARD_WEIGHT
        score += os.spikes * cls.HAZARD_WEIGHT

        if ps.stealth_rock:
            score -= cls.HAZARD_WEIGHT

        if os.stealth_rock:
            score += cls.HAZARD_WEIGHT

        return score

    @classmethod
    def evaluate(cls, state: BattleState):

        total = 0.0

        total += cls.hp_score(state)
        total += cls.remaining_score(state)
        total += cls.status_score(state)
        total += cls.boost_score(state)
        total += cls.hazard_score(state)

        if state.winner == "player":
            total += 100000

        elif state.winner == "opponent":
            total -= 100000

        return float(total)

    @classmethod
    def summary(cls, state: BattleState):

        return {
            "hp": cls.hp_score(state),
            "remaining": cls.remaining_score(state),
            "status": cls.status_score(state),
            "boost": cls.boost_score(state),
            "hazard": cls.hazard_score(state),
            "total": cls.evaluate(state),
        }


print("✅ evaluation_engine.py Ready")
