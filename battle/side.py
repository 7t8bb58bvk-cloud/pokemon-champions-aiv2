
class Side:

    def __init__(self, team):

        self.team = team
        self.active_index = 0

    @property
    def active(self):

        return self.team[self.active_index]

    def switch(self, index):

        if index == self.active_index:
            return False

        if index < 0 or index >= len(self.team):
            return False

        if self.team[index].current_hp <= 0:
            return False

        self.active_index = index

        return True


print("✅ side.py V2.1 Ready")
