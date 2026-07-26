
class BattleEngine:

    @staticmethod
    def check_winner(player, opponent):

        if player.hp <= 0 and opponent.hp <= 0:
            return "draw"

        if player.hp <= 0:
            return "opponent"

        if opponent.hp <= 0:
            return "player"

        return None

    @staticmethod
    def battle_finished(player, opponent):

        return BattleEngine.check_winner(
            player,
            opponent,
        ) is not None


print("✅ battle_engine.py Ready")
