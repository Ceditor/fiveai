import numpy as np
from checkerboard import CheckerBoard


class BoardState:
    def __init__(self, state):
        self.state = state


class MCTSNode(CheckerBoard):
    def __init__(self, parent, state, next_player):
        super().__init__(parent.size)
        self.state = state
        self.parent = parent
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
        return self.results[self.parent.next_player] + self.results[0] - \
               self.results[-self.parent.next_player]

    def selection(self, c_param=1.4):
        return max(self.children,
                   key=lambda child: (child.q / (
                           child.n + 1)) + c_param * np.sqrt(
                       (np.log(self.n) / (child.n + 1))))

    def expansion(self):
        loc = self.legal_locations.pop()
        state = self.state
        self.move(self.next_player, loc)
        next_node = MCTSNode(self, self.state, -self.next_player)
        self.children.append(next_node)
        self.state = state
        return next_node
