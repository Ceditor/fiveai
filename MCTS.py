import numpy as np
from checkerboard import CheckerBoard


class BoardState:
    def __init__(self, state):
        self.state = state


class MCTSNode(CheckerBoard):
    def __init__(self, parent, state, next_player):
        super().__init__(parent.size)
        self.from_numpy(state)
        self.parent = parent
        self.state = state
        self.children = []
        self.visits = 0
        self.results = {1: 0, 0: 0, -1: 0}
        self.next_player = next_player
        self.legal_locations = set(self.empty_locations)

    def back_update(self, result):
        self.results[result] += 1
        self.visits += 1
        if hasattr(self.parent, "back_update"):
            self.parent.back_update(result)

    @property
    def n(self):
        return self.visits

    @property
    def q(self):
        return self.results[self.next_player] - self.results[-self.next_player]

    def best_child(self, c_param=1.4):
        return max(self.children,
                   key=lambda child: (child.q / (child.n + 1)) + c_param * np.sqrt(
                       (2 * np.log(self.n) / (child.n + 1))))
