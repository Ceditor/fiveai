from player import Player
from checkboard import CheckerBoard, Location as _


class Game:
    def __init__(self, size: tuple, win_length: int, p1_type=Player,
                 p2_type=Player):
        self.win_length = win_length
        self.checkerboard = CheckerBoard(size)
        self.p1 = p1_type(1)
        self.p2 = p2_type(-1)

    def __str__(self):
        return str(self.checkerboard)

    def play(self):
        player = self.p1
        while True:
            try:
                loc = player.next_loc(self.checkerboard)
                self.checkerboard.move(player.color, loc)
            except:
                return 0
            if self.checkerboard.judge(player.color, self.win_length):
                return player.color
            player = self._next(player)

    def _next(self, player):
        if player == self.p1:
            return self.p2
        else:
            return self.p1


def caculate_win_times(times):
    res = {1: 0, -1: 0, 0: 0}
    for i in range(times):
        g = Game((5, 5), 3)
        res[g.play()] += 1
    return res


if __name__ == "__main__":
    print(caculate_win_times(10000))
