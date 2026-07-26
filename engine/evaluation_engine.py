class EvaluationEngine:

    @staticmethod
    def evaluate(player, opponent):

        score = 0

        # HP差
        score += player.current_hp
        score -= opponent.current_hp

        # Status
        if opponent.status is not None:
            score += 30

        if player.status is not None:
            score -= 30

        # Boost
        for stat, stage in player.boosts.items():
            score += stage * 8

        for stat, stage in opponent.boosts.items():
            score -= stage * 8

        return score


print("✅ evaluation_engine.py V2 Ready")
