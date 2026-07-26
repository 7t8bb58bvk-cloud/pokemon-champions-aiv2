
ACTION_MOVE = "move"
ACTION_SWITCH = "switch"


class Action:

    def __init__(
        self,
        action_type,
        move=None,
        target=None,
        priority=0,
        switch_index=None,
    ):
        self.action_type = action_type
        self.move = move
        self.priority = priority

        if target is None and switch_index is not None:
            target = switch_index

        self.target = target

    @property
    def switch_index(self):
        return self.target

    def __repr__(self):
        if self.action_type == ACTION_MOVE:
            return f"Action(move={self.move!r})"
        return f"Action(switch={self.target!r})"


print("✅ action.py Fixed")
