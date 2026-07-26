
class BattleState:

    def __init__(
        self,
        player_side,
        opponent_side,
    ):
        self.player_side = player_side
        self.opponent_side = opponent_side

        self.turn = 1

        self.weather = None
        self.terrain = None

    def next_turn(self):
        self.turn += 1

    @property
    def player(self):
        return self.player_side.active

    @property
    def opponent(self):
        return self.opponent_side.active


print("✅ battle_state.py V2 Ready")
